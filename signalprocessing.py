"""
Script: signalprocessing
    Signal processing for biomechanics.

Modules
    butter_filtfilt: Butterworth filter, Note use of filtfilt which doubles order*
    calc_rss: Calculate residual sum of squares
    residual_analysis: Perform residual analysis of multiple cutoff frequencys using Winter's method and a Butterworth filter
    module_4: module description here

Author:
    Casey Wiens
    cwiens32@gmail.com
"""


def butter_filtfilt(data_in, fs, N, fc, filt_pass='low'):
    """
    Function::: butter_filtfilt
    	Description: butterworth filter for signals
    	Details: * the function filtfilt is a dualpass so it doubles the order (e.g. resulting order = 2*order)

    Inputs
        data_in: ARRAY signal to be filtered
        fs: INT sampling rate of signal (Hz)
        N: INT order of filter (this will effectively be doubled since using filtfilt)
        fc: INT cut-off frequency of filter
        filt_pass: STRING low, high, or band pass filter (default: low)

    Outputs
        data_filt: ARRAY filtered signal

    Dependencies
        scipy
        numpy
    """

    # Dependencies
    from scipy.signal import butter, filtfilt
    import numpy as np

    """ set parameters """
    # nyquist frequency
    fn = (fs/2)
    # number of passes (since using filtfilt it is 2)
    n_pass = 2

    """ normalize cutoff frequency using Winter's method
        correction factor - from Winter's Biomechanics and Motor Control of Human Movement (4ed) pg 68
        c = correction factor
    """
    # c = (2^(1/n_pass) - 1)^(1/(2*order))
    c = (2**(1/n_pass) - 1)**(1/(2*N))
    # normalized cutoff frequency using correction factor
    # wn = tan(pi*fc*fs) / c
    wn = (np.tan(np.pi*fc/fs)) / c
    fc_corrected = np.arctan(wn)*fs/np.pi

    """ filter data using butter and filtfilt"""
    # calculate coefficients
    b, a = butter(N, fc_corrected/fn, filt_pass)
    # filter signal
    data_filt = filtfilt(b, a, data_in)

    return data_filt


def calc_rss(data_orig, data_filt):
    """
    Function::: calc_rss
    	Description: Calculate residual sum of squares
    	Details:

    Inputs
        data_orig: SERIES unfiltered data to be compared to filtered (data_filt) data
        data_filt: SERIES filtered data to be compared to unfiltered (data_orig) data

    Outputs
        rss: FLOAT residual sum of squares of unfiltered/filtered data comparison

    Dependencies
        numpy
    """

    # Dependencies
    import numpy as np

    """ calculate residual sum of squares """
    # sqrt( 1/N sum( ( x_i - x_hat_i )^2 ) )
    rss = np.sqrt(np.mean(np.square(data_orig - data_filt)))

    return rss


def residual_analysis(data_in, fo=None, ff=None, N=None, samp=None, fi=0.1, filt_pass='low',
                      k=None, si=None, sf=None, ss=None, cf=None, w=None):
    """
    Function::: residual_analysis
    	Description: Perform residual analysis of multiple cutoff frequencys using Winter's method and a Butterworth filter
    	Details:

    Inputs
        data_in: DATAFRAME unfiltered data to be compared to filtered
        fo: FLOAT initial cutoff frequency for residual analysis
        ff: FLOAT final cutoff frequency for residual analysis
        N: INT order of Butterworth filter
        samp: INT sampling rate of signal (Hz)
        fi: FLOAT interval to increase cutoff frequency for residual analysis
        filt_pass: STRING low, high, or band pass filter (default: low)

    Outputs
        data_rss: DATAFRAME the residual sum of squares for each cutoff frequency

    Dependencies
        pandas
        numpy
        scipy
    """

    # Dependencies
    import pandas as pd
    import numpy as np
    from scipy.interpolate import UnivariateSpline

    """ initialize variables """
    data_rss = pd.DataFrame(columns=['cf', 'rss'])

    if fo is not None:
        " for butterworth filter "
        for cf in np.arange(fo, ff+fi, fi):
            # filter data
            data_filt = butter_filtfilt(data_in, samp, N, cf, filt_pass=filt_pass)
            # calculate residual sum of squares
            rss = calc_rss(data_in, data_filt)
            # store data
            data_rss = data_rss.append({'cf': cf,
                                        'rss': rss},
                                        ignore_index=True)
    else:
        " for spline fitting "
        if cf is None:
            " searching for cutoff frequency "
            for cf in np.arange(si, sf+ss, ss):
                # create x variable
                x = np.linspace(data_in.index[0], data_in.index[-1], len(data_in))
                # filter data
                spl = UnivariateSpline(x, data_in, k=k)
                # set smoothing parameter
                spl.set_smoothing_factor(cf)
                # calculate residual sum of squares
                rss = calc_rss(data_in, spl(x))
                # store data
                data_rss = data_rss.append({'cf': cf,
                                            'rss': rss},
                                            ignore_index=True)
        else:
            " searching for weighting factors "
            for i in np.arange(0.025, 1, 0.025):
                # create x variable
                x = np.linspace(data_in.index[0], data_in.index[-1], len(data_in))
                # set weights
                w[np.where(w!=1)] = i
                # filter data
                spl = UnivariateSpline(x, data_in, k=k, w=w, s=cf)
                # calculate residual sum of squares
                rss = calc_rss(data_in, spl(x))
                # store data
                data_rss = data_rss.append({'wf': i,
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
    """
    Function::: name_of_function
    	Description: brief description here (1 line)
    	Details: Full description with details here

    Inputs
        input1: DATATYPE description goes here (units)
        input2: DATATYPE description goes here (units)
        input3: DATATYPE description goes here (units)
        input4: DATATYPE description goes here (units)

    Outputs
        output1: DATATYPE description goes here (units)
        output2: DATATYPE description goes here (units)
        output3: DATATYPE description goes here (units)
        output4: DATATYPE description goes here (units)

    Dependencies
        dep1
        dep2
        dep3 from uscbrl_script.py (USCBRL repo)
    """
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
    fi: FLOAT interval to increase cutoff frequency for residual analysis (default: 0.1)
    filt_pass: STRING low, high, or band pass filter (default: low)

Output:
    f_c: FLOAT estimated optimal cutoff frequency

Dependencies:
    none
"""
def est_optimal_cutoff_freq(data_in, fo=None, ff=None, N=None, samp=None, fi=0.1, filt_pass='low',
                            k=None, si=None, sf=None, ss=None):
    """
    Function::: name_of_function
    	Description: brief description here (1 line)
    	Details: Full description with details here

    Inputs
        input1: DATATYPE description goes here (units)
        input2: DATATYPE description goes here (units)
        input3: DATATYPE description goes here (units)
        input4: DATATYPE description goes here (units)

    Outputs
        output1: DATATYPE description goes here (units)
        output2: DATATYPE description goes here (units)
        output3: DATATYPE description goes here (units)
        output4: DATATYPE description goes here (units)

    Dependencies
        dep1
        dep2
        dep3 from uscbrl_script.py (USCBRL repo)
    """

    """ perform residual analysis """
    if fo is not None:
        # for Butterworth fitler
        data_rss = residual_analysis(data_in, fo, ff, N, samp, fi=0.1, filt_pass='low')
    else:
        # for Quintic Spline
        data_rss = residual_analysis(data_in, k=k, si=si, sf=sf, ss=ss)

    """ calculate slope and y-intercept with trimmed data """
    m, b = best_fit_slope_and_intercept(data_rss['cf'].iloc[-60:, ], data_rss['rss'].iloc[-60:, ])

    """ calculate the rms value of the noise (Winter, 2009) """
    a = abs(data_rss['rss'] - b).idxmin()

    """ calculate the optimal cutoff frequency (Winter, 2009) """
    f_c = data_rss['cf'].loc[a]

    return f_c


"""
est_optimal_weights
    Estimate the optimal cutoff frequency using Winter's method (1990)

Input:
    data_in: DATAFRAME unfiltered data to be compared to filtered
    fo: FLOAT initial cutoff frequency for residual analysis
    ff: FLOAT final cutoff frequency for residual analysis
    N: INT order of Butterworth filter
    samp: INT sampling rate of signal (Hz)
    fi: FLOAT interval to increase cutoff frequency for residual analysis (default: 0.1)
    filt_pass: STRING low, high, or band pass filter (default: low)

Output:
    f_c: FLOAT estimated optimal cutoff frequency

Dependencies:
    none
"""
def est_optimal_weights(data_in, cf, w, k):
    """
    Function::: name_of_function
    	Description: brief description here (1 line)
    	Details: Full description with details here

    Inputs
        input1: DATATYPE description goes here (units)
        input2: DATATYPE description goes here (units)
        input3: DATATYPE description goes here (units)
        input4: DATATYPE description goes here (units)

    Outputs
        output1: DATATYPE description goes here (units)
        output2: DATATYPE description goes here (units)
        output3: DATATYPE description goes here (units)
        output4: DATATYPE description goes here (units)

    Dependencies
        dep1
        dep2
        dep3 from uscbrl_script.py (USCBRL repo)
    """

    """ perform residual analysis """
    data_rss = residual_analysis(data_in, cf=cf, w=w, k=k)

    """ calculate slope and y-intercept with trimmed data """
    m, b = best_fit_slope_and_intercept(data_rss['wf'].iloc[-10:, ], data_rss['rss'].iloc[-10:, ])

    """ calculate the rms value of the noise (Winter, 2009) """
    a = abs(data_rss['rss'] - b).idxmin()

    """ calculate the optimal weighting factor (Winter, 2009) """
    w_f = data_rss['wf'].loc[a]

    return w_f


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
    """
    Function::: name_of_function
    	Description: brief description here (1 line)
    	Details: Full description with details here

    Inputs
        input1: DATATYPE description goes here (units)
        input2: DATATYPE description goes here (units)
        input3: DATATYPE description goes here (units)
        input4: DATATYPE description goes here (units)

    Outputs
        output1: DATATYPE description goes here (units)
        output2: DATATYPE description goes here (units)
        output3: DATATYPE description goes here (units)
        output4: DATATYPE description goes here (units)

    Dependencies
        dep1
        dep2
        dep3 from uscbrl_script.py (USCBRL repo)
    """
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
                f_c = est_optimal_cutoff_freq(data_orig[col], fo, ff, N, samp, fi=0.1, filt_pass='low')
                # filter data
                data_temp = butter_filtfilt(data_orig[col], samp, N, f_c, filt_pass=filt_pass)
            # store data
            data_out[col] = data_temp
            data_fc = data_fc.append({'signal': col,
                                      'fc': f_c},
                                     ignore_index=True)

    return data_out, data_fc

"""
spline_winter
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

def spline_winter(data_orig, k=3, si=0, sf=1200, ss=10, samp=240, int_s=None, int_f=None, fc=None):
    """
    Function::: name_of_function
    	Description: brief description here (1 line)
    	Details: Full description with details here

    Inputs
        input1: DATATYPE description goes here (units)
        input2: DATATYPE description goes here (units)
        input3: DATATYPE description goes here (units)
        input4: DATATYPE description goes here (units)

    Outputs
        output1: DATATYPE description goes here (units)
        output2: DATATYPE description goes here (units)
        output3: DATATYPE description goes here (units)
        output4: DATATYPE description goes here (units)

    Dependencies
        dep1
        dep2
        dep3 from uscbrl_script.py (USCBRL repo)
    """
    import pandas as pd
    import numpy as np
    from scipy.interpolate import UnivariateSpline

    if isinstance(data_orig, pd.DataFrame):

        """ initialize variables """
        data_fc = pd.DataFrame(columns=['signal', 'fc', 'func'])
        data_out = pd.DataFrame(np.nan, index=data_orig.index, columns=data_orig.columns)

        """ filter data """
        for col in data_orig.columns:
            if col.lower() == 'frame' or col.lower() == 'time' or col.lower() == 't':
                # set estimate cutoff frequency as nan
                f_c = np.nan
                # keep original column
                data_temp = data_orig[col].copy()
                # set spline function as nan
                spl = np.nan
            else:
                if int_s is not None:
                    """ if main interval was provided """
                    # extract data
                    x = np.linspace(int_s, int_f, int(int_f-int_s)+1) * (1/samp)
                    y = data_orig[col].loc[int_s:int_f].copy()
                    # estimate cutoff frequency
                    f_c = est_optimal_cutoff_freq(y, k=k, si=si, sf=sf, ss=ss)

                    # initialize weighting factor array
                    w = np.zeros(len(data_orig[col]))
                    # set main interval to weighting factor of 1
                    w[int(int_s):int(int_f)+1] = 1
                    # estimate weights
                    w_fac = est_optimal_weights(y, f_c, w, k=k)

                    # filter data
                    spl = UnivariateSpline(x, y, k=k)
                    # set smoothing parameter
                    spl.set_smoothing_factor(f_c)
                    # keep original column
                    data_temp = spl(x)
                elif fc is not None:
                    # extract data
                    x = np.linspace(data_orig.index[0], data_orig.index[-1], len(data_orig)) * (1/samp)
                    y = data_orig[col].copy()
                    # take care of nans if exists
                    if np.isnan(y).any():
                        w = np.isnan(y)
                        y[w] = 0
                        # filter data
                        spl = UnivariateSpline(x, y, k=k, w=~w, s=fc)
                    else:
                        # filter data
                        spl = UnivariateSpline(x, y, k=k, s=fc)
                    # set smoothing parameter
                    f_c = fc
                    # keep original column
                    data_temp = spl(x)
                else:
                    """ if main interval was NOT provided """
                    # extract data
                    x = np.linspace(data_orig.index[0], data_orig.index[-1], len(data_orig)) * (1/samp)
                    y = data_orig[col].copy()
                    # estimate cutoff frequency
                    f_c = est_optimal_cutoff_freq(y, k=k, si=si, sf=sf, ss=ss)
                    # filter data
                    spl = UnivariateSpline(x, y, k=k)
                    # set smoothing parameter
                    spl.set_smoothing_factor(f_c)
                    # keep original column
                    data_temp = spl(x)
            # store data
            data_out[col] = data_temp
            data_fc = data_fc.append({'signal': col,
                                      'fc': f_c,
                                      'func': spl},
                                     ignore_index=True)

    return data_out, data_fc


"""

"""
def remove_switches():
    """
    Function::: name_of_function
    	Description: brief description here (1 line)
    	Details: Full description with details here

    Inputs
        input1: DATATYPE description goes here (units)
        input2: DATATYPE description goes here (units)
        input3: DATATYPE description goes here (units)
        input4: DATATYPE description goes here (units)

    Outputs
        output1: DATATYPE description goes here (units)
        output2: DATATYPE description goes here (units)
        output3: DATATYPE description goes here (units)
        output4: DATATYPE description goes here (units)

    Dependencies
        dep1
        dep2
        dep3 from uscbrl_script.py (USCBRL repo)
    """
    from scipy.signal import medfilt


    dfout = medfilt(df, 15)
    ind = abs(dfout - df) > 50
    df1 = df.copy()
    buffer = 1
    for i in range(1,len(ind)-1):
        if ind.iloc[i]:
            df1.iloc[i-1] = np.nan
            df1.iloc[i] = np.nan
            df1.iloc[i+1] = np.nan

    df2 = df1.interpolate(method='spline', order=3)





def fit_spline_csaps(x, y, thresh=0.000001, imp_f=None, pif_f=None, samp=240, set_weights=False):
    """
    Function::: name_of_function
    	Description: brief description here (1 line)
    	Details: Full description with details here

    Inputs
        input1: DATATYPE description goes here (units)
        input2: DATATYPE description goes here (units)
        input3: DATATYPE description goes here (units)
        input4: DATATYPE description goes here (units)

    Outputs
        output1: DATATYPE description goes here (units)
        output2: DATATYPE description goes here (units)
        output3: DATATYPE description goes here (units)
        output4: DATATYPE description goes here (units)

    Dependencies
        dep1
        dep2
        dep3 from uscbrl_script.py (USCBRL repo)
    """
    from csaps import csaps
    import numpy as np
    import pandas as pd


    """ calculate residuals while iterating through smoothing parameter """
    # store potential smoothing parameters
    p = []
    for ii in np.arange(1,4.1,0.1):
        p.append(1 / ( 1 + ((1/samp)**3) / (60*10**(1-ii))))

    # fit spline and calculate residuals for each smoothing parameter
    r_df = pd.DataFrame(columns={'r_fp', 'r_im', 'r_pp'})
    for ii in p:
        ys = csaps(x, y, x, smooth=ii)
        r_fp = ((ys[1:imp_f] - y[1:imp_f])**2).sum()
        r_im = ((ys[imp_f:pif_f] - y[imp_f:pif_f])**2).sum()
        r_pp = ((ys[pif_f: ] - y[pif_f: ])**2).sum()
        r_df = r_df.append({'r_fp': r_fp,
                            'r_im': r_im,
                            'r_pp': r_pp},
                           ignore_index=True)


    """ find first derivative of r_im to determine data "knee" """
    dr_im = pd.DataFrame(index=range(len(r_df)), columns={'dr_1', 'dr_2'})
    for ii in range(1, len(r_df)-1):
        dr_im['dr_1'][ii] = ( r_df['r_im'][ii+1]-r_df['r_im'][ii-1] ) / 2
    dr_im['dr_1'][0] = dr_im['dr_1'][1]
    dr_im['dr_1'].iloc[-1] = dr_im['dr_1'].iloc[-2]
    dr_im['dr_1'] = pd.to_numeric(dr_im['dr_1'])


    """ find second derivative of r_im to determine data "knee" """
    for ii in range(1, len(r_df) - 1):
        dr_im.loc[ii, 'dr_2'] = ( dr_im['dr_1'][ii+1]-dr_im['dr_1'][ii-1] ) / 2
    dr_im.loc[0, 'dr_2'] = dr_im['dr_2'][1]
    dr_im.iloc[-1, 1] = dr_im['dr_2'].iloc[-2]
    dr_im['dr_2'] = pd.to_numeric(dr_im['dr_2'])


    #""" find index for maximum value of second derivative """
    #p_im = p[dr_im['dr_2'].idxmax()]
    """ find index for value of second derivative that is above threshold """
    p_im = p[(dr_im['dr_2'] > thresh).idxmax()]


    """ determine weights for non-impact phases"""
    w_r_df = pd.DataFrame(columns={'w_r_fp', 'w_r_im', 'w_r_pp'})
    for ii in np.arange(0.01, 1, 0.01):
        # set weights
        w = np.zeros(len(x))
        w[imp_f:pif_f] = 1
        w[w == 0] = ii
        # fit spline
        ys = csaps(x, y, x, weights=w, smooth=p_im)
        # calculate residuals for each phase
        w_r_fp = ((ys[1:imp_f] - y[1:imp_f]) ** 2).sum()
        w_r_im = ((ys[imp_f:pif_f] - y[imp_f:pif_f]) ** 2).sum()
        w_r_pp = ((ys[pif_f:] - y[pif_f:]) ** 2).sum()
        w_r_df = w_r_df.append({'w_r_fp': w_r_fp,
                                'w_r_im': w_r_im,
                                'w_r_pp': w_r_pp},
                               ignore_index=True)

    # set weights
    w = np.zeros(len(x))
    w[imp_f:pif_f] = 1
    w[w==0] = 0.01


    """ fit the spline """
    if set_weights is False:
        ys = csaps(x, y, x, smooth=p_im)
    else:
        ys = csaps(x, y, x, weights=w, smooth=p_im)


    return ys


# from gcvspline import SmoothedNSpline
# import matplotlib.pyplot as plt
#
# x = np.linspace(-3, 3, 50)
# y0 = np.exp(-x**2)
# np.random.seed(1234)
#
# n = 0.1 * np.random.normal(size=50)
# w = 1.0 / (np.ones_like(n) * std(n))
# y = y0 + n
#
# xs = np.linspace(-3, 3, 1000)
#
# GCV_auto = GCVSmoothedNSpline(x, y, w=w) # gcvspline fit
#
# y_smoothed = GCV_auto(xs) # retrieving the smoothed values