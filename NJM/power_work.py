# -*- coding: utf-8 -*-
"""
power_work
    Modules to calculate joint power and joint work.
    
Modules
    __init__: initializes variables
    power: calculates power
    work: calculates work (and calculates power as by-product)
    main: calculates power and work
    
Dependencies

    
Created on Wed May 27 07:07:17 2020

@author: cwiens
"""


#%%    
"""
Inputs
    njm: DATAFRAME net joint moment data (Nm)
    omega: DATAFRAME joint angular velocity data (rad/s)
    samp: INT sampling rate of data (Hz)
    
Outputs
    data_power: DATAFRAME joint power data
    data_work: DATAFRAME joint work data
"""

class powerwork:
    
    def __init__(self, njm, omega, samp=1200):
        # initialize variables
        self.njm = njm
        self.omega = omega
        self.samp = samp
    
    #%% calculate power
    def power(self):
        # njm * angular_velocity
        self.data_power = self.njm * self.omega
    
    #%% calculate work
    def work(self):
        # run power function
        powerwork.power(self)
        # sum(power) / sampling_rate
        self.data_work = self.data_power.sum()/self.samp
    
    #%% run all functions
    def main(self):
        powerwork.power(self)
        powerwork.work(self)