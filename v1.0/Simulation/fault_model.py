"""Provisional supervisory logic; no calibration or hardware emulation."""
import math
from control_model import Controller, temperature

class Supervisor:
    def __init__(self, sensors=2, fans=2):
        self.control=Controller(sensors,fans)
        self.last_time=None
        self.applied=[0.]*fans
        self.started=[None]*fans
        self.edge=[None]*fans
        self.tach_fault=[False]*fans
        self.tach_good_since=[None]*fans
        self.sensor_fault=False
        self.sensor_good_since=None

    def update(self, now, codes, pulses):
        """pulses: rising-edge counts since previous update, one count per fan.

        Provisional timings: 2s no-edge detection, 5s healthy recovery.
        Calls required at <=100ms intervals; no scheduler/watchdog simulated.
        Any fault overrides all fan outputs to full; this is not fan power cycling.
        """
        if not math.isfinite(now) or now<0 or (self.last_time is not None and now<=self.last_time):
            raise ValueError('Time must be finite, nonnegative and increasing')
        if self.last_time is not None and now-self.last_time>.100001:
            raise ValueError('Model requires updates at least every 100ms')
        if len(codes)!=self.control.sensors or any(type(c) is not int or not 0<=c<=1023 for c in codes):
            raise ValueError('Expected one 10-bit integer ADC value per sensor')
        if len(pulses)!=self.control.fans or any(type(p) is not int or p<0 for p in pulses):
            raise ValueError('Expected nonnegative integer edge counts per fan')
        self.last_time=now
        invalid=any(temperature(c) is None for c in codes)
        if invalid:
            self.sensor_fault=True;self.sensor_good_since=None
        elif self.sensor_fault:
            if self.sensor_good_since is None:self.sensor_good_since=now
            if now-self.sensor_good_since>=5-1e-9:self.sensor_fault=False
        normal=self.control.update(now,codes)
        for i in range(self.control.fans):
            # Monitor the command actually applied during the previous interval.
            if self.applied[i]>0:
                if pulses[i]>0:self.edge[i]=now
                origin=self.edge[i] if self.edge[i] is not None else self.started[i]
                if now-origin>=2-1e-9:self.tach_fault[i]=True
                if self.tach_fault[i]:
                    fresh=self.edge[i] is not None and now-self.edge[i]<=.2+1e-9
                    if fresh:
                        if self.tach_good_since[i] is None:self.tach_good_since[i]=now
                        if now-self.tach_good_since[i]>=5-1e-9:
                            self.tach_fault[i]=False;self.tach_good_since[i]=None
                    else:self.tach_good_since[i]=None
            else:
                self.edge[i]=None;self.started[i]=None;self.tach_good_since[i]=None
        alarm=self.sensor_fault or any(self.tach_fault)
        output=[1.]*self.control.fans if alarm else normal['duty']
        for i,duty in enumerate(output):
            if duty>0 and self.applied[i]==0:self.started[i]=now;self.edge[i]=None
            if duty==0:self.started[i]=None;self.edge[i]=None
        self.applied=output
        return {'duty':output.copy(),'alarm':alarm,'sensor_fault':self.sensor_fault,
                'tach_fault':self.tach_fault.copy()}
