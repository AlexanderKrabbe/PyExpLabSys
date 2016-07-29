# -*- coding: utf-8 -*-

"""Steps for voltage_current_programs"""

from time import time
from yaml import load


class ConstantStepBase(object):
    """A base step with time keeping a probe interval"""

    def __init__(self, duration, voltage, max_current, probe_interval):
        self.duration = duration
        self.probe_interval = probe_interval
        # For interbal bookkeeping of the time
        self._start = None
        self._elapsed = 0.0
        
        # Overwrite in baseclasses
        self._voltage = voltage
        self._max_current = max_current

    def start(self):
        """Start this step"""
        self._start = time()

    def stop(self):
        """Stop the step"""
        self._elapsed = time() - self._start
        self._start = None

    def elapsed(self):
        """Return the elapsed time"""
        if self._start is None:
            return self._elapsed
        else:
            return time() - self._start

    def remaining(self):
        """Return remaining time"""
        return self.duration - self.elapsed()

    def __str__(self):
        """Return the str representation"""
        return '{}(duration={}, voltage={}, max_current={}, probe_interval={})'.format(
            self.__class__.__name__, self.duration, self._voltage, self._max_current, 
            self.probe_interval,
        )

    def values(self):
        """Return voltage and max_current"""
        return self._voltage, self._max_current


class ConstantVoltageStep(ConstantStepBase):
    """A constant voltage step"""


class ConstantCurrentStep(ConstantStepBase):
    """A constant voltage step"""


def parse_ramp(file_):
    """Parse the ramp file"""
    # Eveything in the steps file is config, except the step list
    # which is extracted below
    config = load(file_)

    # Load steps
    steps = []
    step_definitions = config.pop('steps')
    for step_definition in step_definitions:
        type_  = step_definition.pop('type')
        if type_ == 'ConstantVoltageStep':
            steps.append(ConstantVoltageStep(**step_definition))
        if type_ == 'ConstantCurrentStep':
            steps.append(ConstantCurrentStep(**step_definition))

    return config, steps