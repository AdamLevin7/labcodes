
"""
Script: findbw
    Find bodyweight (bw) in N in a data stream (ie. Treadmill collection) using ginput

Modules
    find_avg: Find the average value of a data stream between two points

Author:
    Harper Stewart
    harperestewart7@gmail.com
"""

"""    
Function::: find_avg
	Description: Find the average value of a data stream between two points
	Details: Use ginput to select 2 points and then take the average between those x-values

Inputs
    data: LIST Data stream
    start_ind: INT Index to start the region for the average
    end_ind: INT Index to end the region for the average

Outputs
    avg: FLOAT average between the start and end values in the data stream


Dependencies
    matplotlib.pyplot    
    statistics

"""

def find_avg(data,start_ind = '', end_ind = ''):

    # Dependencies
    import matplotlib.pyplot as plt
    from statistics import mean

    # Plot the data stream
    plt.plot(data)

    # Use the provided first and last values if they exist
    if start_ind == '' or end_ind == '':
        # Use ginput to select the points
       start_val, end_val = plt.ginput(2)

    # Take the average between those x-values
    avg = mean(data[start_ind:end_ind])

    return avg




