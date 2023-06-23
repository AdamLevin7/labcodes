# -*- coding: utf-8 -*-
"""
FindContactIntervals

Find the beginning and end of contact intervals when provided a single column
vertical force data.

Input
    data: single column of vertical force data
    thresh: force threshold to identify when contact occurs (default=50)
    
Output
    CI: two column data frame. "Start" identifies beginning of contact
        interval, while "End" identifies the end of interval. The number
        of rows signifies the number of contact intervals
        
Dependencies
    pandas
    scipy

Created on Thu Nov  7 15:12:26 2019

@author: cwiens, Casey Wiens, cwiens32@gmail.com
"""

    
def FindContactIntervals(data, samp=1200, thresh=50):

    # Dependencies
    import pandas as pd
    from scipy import stats
    
    #%% buffer time
    # set amount of time after event to search for next
    # useful for when data fluctuates around threshold
    buff = int(samp*0.1)
    
    #%% find start and end of contact intervals
    # find start of first contact
    if (stats.trim_mean(data.iloc[0:100], 0.2) > thresh):
        ciStart = pd.Series(1);
    else:
        ciStart = pd.Series((data >= thresh).idxmax())
    
    #%% find remaining contact intervals
    # if contact occured throughout the entire data
    if all(data>=thresh):
        # set end of contact as end of data
        ciEnd = pd.Series(len(data))
    else:
        # find end of first contact interval
        cntCI = 0
        ciEnd = pd.Series((data.iloc[ciStart.iloc[cntCI]+buff: ] < thresh).idxmax())
        # continue through rest of the code finding start and end of contacts
        while (data.iloc[ciEnd.iloc[cntCI]: ] >= thresh).idxmax() != ciEnd.iloc[cntCI]:
            # iterate counter
            cntCI += 1
            # set start of next contact interval
            ciStart = ciStart.append(pd.Series([(data.iloc[ciEnd.iloc[cntCI-1]: ] >= thresh).idxmax()],
                                                index = [cntCI]))
            # set end of next contact interval
            if (data.iloc[ciStart.iloc[cntCI]+buff: ] <= thresh).idxmax() != ciStart.iloc[cntCI]:
                ciEnd = ciEnd.append(pd.Series([(data.iloc[ciStart.iloc[cntCI]+buff: ] < thresh).idxmax()],
                                                index = [cntCI]))
            else:
                ciEnd = ciEnd.append(pd.Series([len(data)], index = [cntCI]))
                break
            
    #%% store contact indices
    CI = pd.DataFrame(pd.concat([ciStart, ciEnd],
                                axis=1)).rename(columns={0: "Start", 1: "End"})
    
    
    return CI
