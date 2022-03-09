"""
Script: power_work
    Modules to calculate joint power and joint work.

Modules
    __init__: initializes variables
    power: calculates power
    work: calculates work (and calculates power as by-product)
    main: calculates power and work

Author:
    Casey Wiens
    cwiens32@gmail.com
"""


class powerwork:

    def __init__(self, njm, omega, samp=1200):
        """
        Function::: __init__
        	Description: Initialize variables for class powerwork
        	Details:

        Inputs
            njm: DATAFRAME net joint moment data (Nm)
            omega: DATAFRAME joint angular velocity data (rad/s)
            samp: INT sampling rate of data (Hz)

        Outputs
            None

        Dependencies
            None
        """

        # initialize variables
        self.njm = njm
        self.omega = omega
        self.samp = samp
    

    def power(self):
        """
        Function::: power
        	Description: Calculate power
        	Details:

        Inputs
            self: Takes variables initialized in class "powerwork": (njm, omega, samp)

        Outputs
            data_power: DATAFRAME joint power data


        Dependencies
            None
        """
        # njm * angular_velocity
        self.data_power = self.njm * self.omega
    

    def work(self):
        """
        Function::: work
        	Description: Calculate work
        	Details:

        Inputs
            self: Takes variables initialized in class "powerwork": (njm, omega, samp)

        Outputs
            data_work: DATAFRAME joint work data

        Dependencies
            None
        """
        # run power function
        powerwork.power(self)
        # sum(power) / sampling_rate
        self.data_work = self.data_power.sum()/self.samp
    

    def main(self):
        """
        Function::: main
        	Description: Run all functions in powerwork
        	Details: Calculates power and work

        Inputs
            self: Takes variables initialized in class "powerwork": (njm, omega, samp)

        Outputs
            data_work: DATAFRAME joint work data
            data_power: DATAFRAME joint power data

        Dependencies
            None
        """
        powerwork.power(self)
        powerwork.work(self)