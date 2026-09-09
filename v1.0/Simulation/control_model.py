"""Provisional specification model, NOT ATtiny firmware or motor simulation."""
import math

def resistance(celsius, r25=10000., beta=3435.):
    return r25 * math.exp(beta * (1 / (celsius + 273.15) - 1 / 298.15))

def adc_code(celsius):
    r = resistance(celsius)
    return round(1023 * r / (10000 + r))

def temperature(code):
    # Provisional near-rail fault thresholds; not diagnostics for every failure.
    if not 5 < code < 1018:
        return None
    r = 10000 * code / (1023 - code)
    return 1 / (1 / 298.15 + math.log(r / 10000) / 3435) - 273.15

class Controller:
    """2F/2TH: each sensor controls its matching fan independently.

    1F/2TH provisionally uses the hotter sensor. Off<=33, start>=35 C.

    20% minimum running duty, linear to 100% at 65 C, one-second boost.
    Fault output is 100% plus alarm. No latching/retry/tach watchdog yet.
    """
    def __init__(self, sensors=2, fans=2):
        if (sensors, fans) not in ((1, 1), (2, 1), (2, 2)):
            raise ValueError('Supported variants: 1F/1TH, 1F/2TH, 2F/2TH')
        self.sensors, self.fans = sensors, fans
        self.running = [False] * fans
        self.boost_until = [-1.] * fans

    def update(self, now, codes):
        if len(codes) != self.sensors:
            raise ValueError('Incorrect sensor count')
        values = [temperature(c) for c in codes]
        if None in values:
            return {'duty': [1.] * self.fans, 'alarm': True, 'reason': 'sensor fault'}
        targets = values if self.fans == 2 else [max(values)]
        duties = []
        for channel, t in enumerate(targets):
            if not self.running[channel] and t >= 35:
                self.running[channel] = True
                self.boost_until[channel] = now + 1
            elif self.running[channel] and t <= 33:
                self.running[channel] = False
            duty = 0.
            if self.running[channel]:
                duty = 1. if now < self.boost_until[channel] else min(1., max(.2, .2 + .8 * (t - 35) / 30))
            duties.append(duty)
        return {'duty': duties, 'alarm': False, 'reason': 'normal'}
