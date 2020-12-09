# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 09:53:35 2020

@author: cwiens
"""


"""
filt_butter
    butterworth filter
    
Inputs
    data_in: ARRAY signal to be filtered
    samp: INT sampling rate of signal (Hz)
    N: INT order of filter
    fc: INT cut-off frequency of filter
    filt_pass: STRING low, high, or band pass filter (default: low)
    
Outputs
    data_filt: ARRAY filtered signal
"""
def filt_butter(data_in, samp, N, fc, filt_pass='low'):
    from scipy import signal
    # normalize the frequency
    w = fc / (samp / 2)
    # calculate coefficients
    b, a = signal.butter(N, w, filt_pass)
    # filter signal
    data_filt = signal.filtfilt(b, a, data_in)
    
    return data_filt


"""
calc_rss
    Calculate residual sum of squares

Input:
    data_orig: SERIES unfiltered data to be compared to filtered (data_filt) data
    data_filt: SERIES filtered data to be compared to unfiltered (data_orig) data

Output:
    rss: FLOAT residual sum of squares of unfiltered/filtered data comparison

Dependencies:
    numpy
"""
def calc_rss(data_orig, data_filt):
    import numpy as np

    """ calculate residual sum of squares """
    # sqrt( 1/N sum( ( x_i - x_hat_i )^2 ) )
    rss = np.sqrt(np.mean(np.sum(np.square(data_orig - data_filt))))

    return rss


"""
residual_analysis
    Perform residual analysis of multiple cutoff frequencys using Winter's method and a Butterworth filter

Input:
    data_in: DATAFRAME unfiltered data to be compared to filtered
    fo: FLOAT initial cutoff frequency for residual analysis
    ff: FLOAT final cutoff frequency for residual analysis
    N: INT order of Butterworth filter
    samp: INT sampling rate of signal (Hz)
    fi: FLOAT interval to increase cutoff frequency for residual analysis
    filt_pass: STRING low, high, or band pass filter (default: low)

Output:
    data_rss: DATAFRAME the residual sum of squares for each cutoff frequency

Dependencies:
    pandas
    numpy
"""
def residual_analysis(data_in, fo, ff, N, samp, fi=0.1, filt_pass='low'):
    import pandas as pd
    import numpy as np

    """ initialize variables """
    data_rss = pd.DataFrame(columns=['cf', 'rss'])

    for cf in np.arange(fo, ff+fi, fi):
        # filter data
        data_filt = filt_butter(data_in, samp, N, cf, filt_pass=filt_pass)
        # calculate residual sum of squares
        rss = calc_rss(data_in, data_filt)
        # store data
        data_rss = data_rss.append({'cf': cf,
                                    'rss': rss},
                                    ignore_index=True)

    return data_rss


"""
best_fit_slope_and_intercept
    Calculate the slope and y-intercept for the best fit line
    
Input:
    xs: SERIES x-axis data
    ys: SERIES y-axis data

Output:
    data_rss: DATAFRAME the residual sum of squares for each cutoff frequency

Dependencies:
    statistics
"""
def best_fit_slope_and_intercept(xs, ys):
    from statistics import mean

    """ calculate slope """
    m = (((mean(xs) * mean(ys)) - mean(xs * ys)) /
         ((mean(xs) * mean(xs)) - mean(xs * xs)))

    """ calculate y-intercept """
    b = mean(ys) - m * mean(xs)

    return m, b


"""
est_optimal_cutoff_freq
    Estimate the optimal cutoff frequency using Winter's method (1990)

Input:
    data_in: DATAFRAME unfiltered data to be compared to filtered
    fo: FLOAT initial cutoff frequency for residual analysis
    ff: FLOAT final cutoff frequency for residual analysis
    N: INT order of Butterworth filter
    samp: INT sampling rate of signal (Hz)
    fi: FLOAT interval to increase cutoff frequency for residual analysis
    filt_pass: STRING low, high, or band pass filter (default: low)

Output:
    f_c: FLOAT estimated optimal cutoff frequency

Dependencies:
    none
"""
def est_optimal_cutoff_freq(data_in, fo, ff, N, samp, fi=0.1, filt_pass='low'):

    """ perform residual analysis """
    data_rss = residual_analysis(data_in, fo, ff, N, samp, fi=0.1, filt_pass='low')

    """ calculate slope and y-intercept with trimmed data """
    m, b = best_fit_slope_and_intercept(data_rss['cf'].iloc[-150:, ], data_rss['rss'].iloc[-150:, ])

    """ calculate the rms value of the noise (Winter, 2009) """
    a = abs(data_rss['rss'] - b).idxmin()

    """ calculate the optimal cutoff frequency (Winter, 2009) """
    f_c = data_rss['cf'].loc[a]

    return f_c


"""
filt_butter_winter
    Filter a dataframe using Winter's method (1990) and a Buttworth filter

Input:
    data_orig: DATAFRAME unfiltered data to be compared to filtered
    fo: FLOAT initial cutoff frequency for residual analysis
    ff: FLOAT final cutoff frequency for residual analysis
    N: INT order of Butterworth filter
    samp: INT sampling rate of signal (Hz)
    fi: FLOAT interval to increase cutoff frequency for residual analysis
    filt_pass: STRING low, high, or band pass filter (default: low)

Output:
    data_out: DATAFRAME filtered version of data_orig
    data_fc: DATAFRAME each signal (i.e., column) and the estimated cutoff frequency

Dependencies:
    pandas
    numpy
"""
def filt_butter_winter(data_orig, fo, ff, N, samp, fi=0.1, filt_pass='low'):
    import pandas as pd
    import numpy as np

    if isinstance(data_orig, pd.DataFrame):

        """ initialize variables """
        data_fc = pd.DataFrame(columns=['signal', 'fc'])
        data_out = pd.DataFrame(np.nan, index = data_orig.index, columns=data_orig.columns)

        """ filter data """
        for col in data_orig.columns:
            if col.lower() == 'frame' or col.lower() == 'time' or col.lower() == 't':
                # set estimate cutoff frequency as nan
                f_c = np.nan
                # keep original column
                data_temp = data_orig[col].copy()
            else:
                # estimate cutoff frequency
                f_c = est_optimal_cutoff_freq(data_orig[col], fo, ff, 2, 240, fi=0.1, filt_pass='low')
                # filter data
                data_temp = filt_butter(data_orig[col], samp, N, f_c, filt_pass=filt_pass)
            # store data
            data_out[col] = data_temp
            data_fc = data_fc.append({'signal': col,
                                      'fc': f_c},
                                     ignore_index=True)

    return data_out, data_fc