"""
Script: fbd_display
    Create a visual displaying free body diagram at an instance along with
    the NJM curves of the segments. CURRENTLY ONLY FOR LOWER BODY.

Modules
    __init__: Initialize class to create free body diagram visual.
    fig_init: Initializes the figure with an empty subplot for the free body diagram
    fbd_update: Refreshes and displays the free body diagram at the instant of choice.
    fbd_animate: Create an animated video of FBD at every instant in contact phase.
    fbd_overlay: Main function to create FBD animation

Author:
    Casey Wiens
    cwiens@gmail.com
"""


class fbd_vis():
    
    #%%
    def __init__(self, data_force, data_digi, data_cm, data_njm, side,
                 cnt=None, ylim=[-600,600], colorlegend='flexext', rf_scale=0.0002):
        """
        Function::: __init__
        	Description: Initialize class to create free body diagram visual.
        	Details:

        Inputs
            data_force : DATAFRAME
                force data (fx, fy, ax, ay) (N, N, m, m).
            data_digi : DATAFRAME
                digitized data (m).
            data_cm : DATAFRAME
                center of mass data for segments and body (m).
                format mathces that of NJM.dig2jointkinetics.dig2jk.main().
            data_njm : DATAFRAME
                contains calculated variables for segment's joint kinetics.
            side : STRING
                which side of the body.
                (ex: 'left')
            cnt : INT, optional
                counter - index of data to be visualized.
                The default is None, but will be reset to the first index of data
            ylim : LIST, optional (default: [-600, 600])
                limits for y-axis of the graph
            colorlegend : STRING, optional (default: 'flexext')
                What do positive/negative values represent?
                Possible inputs:
                    'flexext': positive = extensor moment; negative = flexor moment
                    'posneg': positive = positive moment w/r reference frame; negative = negative moment w/r reference frame
            rf_scale : INT, optional (default: 0.0002)
                It scales the force and moments ONLY IN THE VISUAL.

        Outputs
            output1: None

        Dependencies

        """

        self.data_force = data_force
        self.data_digi = data_digi
        self.data_cm = data_cm
        self.data_njm = data_njm
        self.side = side
        if cnt == None:
            self.cnt = data_njm.first_valid_index()
        else:
            self.cnt = cnt
        self.ylim = ylim
        self.colorlegend = colorlegend
        self.rf_scale = rf_scale
        fbd_vis.fig_init(self)
        
    #%%
    def fig_init(self):
        """
        Function::: fig_init
        	Description: Initializes the figure with an empty subplot for the free body diagram.
        	Details:  foot, shank and thigh joint kinetic variables plotted.

        Inputs
            self: 

        Outputs
            output1: None

        Dependencies
            matplotlib

        """
        # Dependencies
        import matplotlib.pyplot as plt
        
        """ initialize figure """
        # create subplots of figure
        self.fig = plt.figure(constrained_layout=True)
        # manually set window size
        self.fig.set_size_inches(1920/self.fig.dpi, 960/self.fig.dpi)
        # create 3x2 with second column double the width
        gs = self.fig.add_gridspec(3,2, width_ratios=[1,2])
        self.f_ax1 = self.fig.add_subplot(gs[0:, 0])
        self.f_ax1.xaxis.set_visible(False)
        self.f_ax1.yaxis.set_visible(False)
        self.f_ax2 = self.fig.add_subplot(gs[0,-1])
        self.f_ax3 = self.fig.add_subplot(gs[1,-1])
        self.f_ax4 = self.fig.add_subplot(gs[-1,-1])
        
        """ plot moment time curves and move time tracer along x-axis """
        ### foot
        self.f_ax4.plot(self.data_njm['time'], self.data_njm['foot_md'],
                        '#BEBCC5', label='Distal NJF Moment')
        self.f_ax4.plot(self.data_njm['time'], self.data_njm['foot_mp'],
                        '#F4D4D4', label='Proximal NJF Moment')
        self.f_ax4.plot(self.data_njm['time'], self.data_njm['foot_njmd'],
                        '#DCB69F', label='Distal NJM Moment')
        self.f_ax4.plot(self.data_njm['time'], self.data_njm['foot_njmp'],
                        '#342A1F', label='Proximal NJM Moment')
        self.f_ax4.plot(self.data_njm['time'], self.data_njm['foot_icm']*self.data_njm['foot_alpha'],
                        '#342A1F', linestyle='--', label='Icm * alpha')
        self.f_ax4.hlines(0, xmin=self.data_njm['time'].iloc[0],
                          xmax=self.data_njm['time'].iloc[-1], color='k')
        self.f_ax4.set_ylim(self.ylim[0], self.ylim[1])
        self.f_ax4.set_title('Foot')
        self.f_ax4.set_ylabel('Moment (Nm)')
        self.f_ax4.set_xlabel('Time (s)')
        ### shank
        self.f_ax3.plot(self.data_njm['time'], self.data_njm['shank_md'],
                        '#BEBCC5', label='Distal NJF Moment')
        self.f_ax3.plot(self.data_njm['time'], self.data_njm['shank_mp'],
                        '#F4D4D4', label='Proximal NJF Moment')
        self.f_ax3.plot(self.data_njm['time'], self.data_njm['shank_njmd'],
                        '#DCB69F', label='Distal NJM Moment')
        self.f_ax3.plot(self.data_njm['time'], self.data_njm['shank_njmp'],
                        '#342A1F', label='Proximal NJM Moment')
        self.f_ax3.plot(self.data_njm['time'], self.data_njm['shank_icm']*self.data_njm['shank_alpha'],
                        '#342A1F', linestyle='--', label='Icm * alpha')
        self.f_ax3.hlines(0, xmin=self.data_njm['time'].iloc[0],
                          xmax=self.data_njm['time'].iloc[-1], color='k')
        self.f_ax3.set_ylim(self.ylim[0], self.ylim[1])
        self.f_ax3.set_title('Shank')
        self.f_ax3.set_ylabel('Moment (Nm)')
        ### thigh
        self.f_ax2.plot(self.data_njm['time'], self.data_njm['thigh_md'],
                        '#BEBCC5', label='Distal NJF Moment')
        self.f_ax2.plot(self.data_njm['time'], self.data_njm['thigh_mp'],
                        '#F4D4D4', label='Proximal NJF Moment')
        self.f_ax2.plot(self.data_njm['time'], self.data_njm['thigh_njmd'],
                        '#DCB69F', label='Distal NJM Moment')
        self.f_ax2.plot(self.data_njm['time'], self.data_njm['thigh_njmp'],
                        '#342A1F', label='Proximal NJM Moment')
        self.f_ax2.plot(self.data_njm['time'], self.data_njm['thigh_icm']*self.data_njm['thigh_alpha'],
                        '#342A1F', linestyle='--', label='Icm * alpha')
        self.f_ax2.hlines(0, xmin=self.data_njm['time'].iloc[0],
                          xmax=self.data_njm['time'].iloc[-1], color='k')
        self.f_ax2.set_ylim(self.ylim[0], self.ylim[1])
        self.f_ax2.set_title('Thigh')
        self.f_ax2.set_ylabel('Moment (Nm)')
        # add legends
        self.f_ax4.legend()
        self.f_ax3.legend()
        self.f_ax2.legend()
        
    #%%
    def fbd_update(self):
        """
        Function::: fbdupdate
            Description: Refreshes and displays the free body diagram at the instant of choice.
            Details:

        Inputs
            input: self

        Outputs
            output: None

        Dependencies
            matplotlib
            numpy
        """

        # Dependencies
        import matplotlib.pyplot as plt
        import matplotlib.patheffects as pe
        import numpy as np
        
        """ add vertical time line """
        if hasattr(self, 'line4'):
            #var_exists = True
            (self.line4).remove()
            (self.line3).remove()
            (self.line2).remove()
        self.line4 = self.f_ax4.vlines(self.data_njm['time'][self.cnt],
                                       ymin=self.ylim[0], ymax=self.ylim[1], color='k')
        self.line3 = self.f_ax3.vlines(self.data_njm['time'][self.cnt],
                                       ymin=self.ylim[0], ymax=self.ylim[1], color='k')
        self.line2 = self.f_ax2.vlines(self.data_njm['time'][self.cnt],
                                       ymin=self.ylim[0], ymax=self.ylim[1], color='k')
        
        """ identify labels for segments """
        toe_x = [col for col in self.data_digi.columns if ('toe' in col and self.side in col and '_x' in col)][0]
        toe_y = [col for col in self.data_digi.columns if ('toe' in col and self.side in col and '_y' in col)][0]
        heel_x = [col for col in self.data_digi.columns if ('heel' in col and self.side in col and '_x' in col)][0]
        heel_y = [col for col in self.data_digi.columns if ('heel' in col and self.side in col and '_y' in col)][0]
        foot_x = [col for col in self.data_cm.columns if ('foot' in col and self.side in col and '_x' in col)][0]
        foot_y = [col for col in self.data_cm.columns if ('foot' in col and self.side in col and '_y' in col)][0]
        ank_x = [col for col in self.data_digi.columns if ('ankle' in col and self.side in col and '_x' in col)][0]
        ank_y = [col for col in self.data_digi.columns if ('ankle' in col and self.side in col and '_y' in col)][0]
        shank_x = [col for col in self.data_cm.columns if ('shank' in col and self.side in col and '_x' in col)][0]
        shank_y = [col for col in self.data_cm.columns if ('shank' in col and self.side in col and '_y' in col)][0]
        knee_x = [col for col in self.data_digi.columns if ('knee' in col and self.side in col and '_x' in col)][0]
        knee_y = [col for col in self.data_digi.columns if ('knee' in col and self.side in col and '_y' in col)][0]
        thigh_x = [col for col in self.data_cm.columns if ('thigh' in col and self.side in col and '_x' in col)][0]
        thigh_y = [col for col in self.data_cm.columns if ('thigh' in col and self.side in col and '_y' in col)][0]
        hip_x = [col for col in self.data_digi.columns if ('hip' in col and self.side in col and '_x' in col)][0]
        hip_y = [col for col in self.data_digi.columns if ('hip' in col and self.side in col and '_y' in col)][0]
        
        # refresh subplot and set FBD axis limits
        self.f_ax1.clear()
        self.f_ax1.set_xlim(-0.75,0.75)
        self.f_ax1.set_ylim(-0.5,2.5)
        self.f_ax1.set_aspect(1)
        
        # display title
        self.f_ax1.set_title('Time (s): ' + str(round(self.data_njm['time'][self.cnt], 4)))
        
        # set offsets
        offset_x = np.mean(self.data_force['ax'])
        offset_y = np.mean(self.data_force['ay'])
        offset_shank_x = 0
        offset_thigh_x = offset_shank_x + 0
        offset_shank_y = 0.3
        offset_thigh_y = offset_shank_y + 0.3
        
        #### create legend for positive/negative moments
        circ_pos = plt.Circle((-99, -99), 0.1, color='tab:orange')
        self.f_ax1.add_artist(circ_pos)
        circ_neg = plt.Circle((-99, -99), 0.1, color='tab:purple')
        self.f_ax1.add_artist(circ_neg)
        if self.colorlegend is 'posneg':
            self.f_ax1.legend([circ_pos, circ_neg], ['Positive', 'Negative'])
        elif self.colorlegend is 'flexext':
            self.f_ax1.legend([circ_pos, circ_neg], ['Extension', 'Flexion'])


        #### ground
        self.f_ax1.hlines(0,xmin=-2, xmax=2, color=(0, 0, 0, 0.75))

        
        #### foot
        # plot line from ankle to toe
        self.f_ax1.plot((self.data_digi[ank_x][self.cnt]-offset_x, self.data_digi[toe_x][self.cnt]-offset_x),
                        (self.data_digi[ank_y][self.cnt]-offset_y, self.data_digi[toe_y][self.cnt]-offset_y),
                        'k-', zorder=0)
        # plot line from ankle to heel
        self.f_ax1.plot((self.data_digi[ank_x][self.cnt]-offset_x, self.data_digi[heel_x][self.cnt]-offset_x),
                        (self.data_digi[ank_y][self.cnt]-offset_y, self.data_digi[heel_y][self.cnt]-offset_y),
                        'k-', zorder=0)
        # plot line from toe to heel
        self.f_ax1.plot((self.data_digi[toe_x][self.cnt]-offset_x, self.data_digi[heel_x][self.cnt]-offset_x),
                        (self.data_digi[toe_y][self.cnt]-offset_y, self.data_digi[heel_y][self.cnt]-offset_y),
                        'k-', zorder=0)
        # plot center of mass
        self.f_ax1.plot(self.data_cm[foot_x][self.cnt]-offset_x, self.data_cm[foot_y][self.cnt]-offset_y,
                        'y*', zorder=0)
        
        # plot reaction force
        self.f_ax1.arrow(self.data_force['ax'][self.cnt]-offset_x, self.data_force['ay'][self.cnt]-offset_y,
                         self.data_njm['foot_rxd'][self.cnt]*self.rf_scale, self.data_njm['foot_ryd'][self.cnt]*self.rf_scale,
                         ec='tab:blue', zorder=15)
        # plot NJF at ankle
        self.f_ax1.arrow(self.data_digi[ank_x][self.cnt]-offset_x, self.data_digi[ank_y][self.cnt]-offset_y,
                         self.data_njm['foot_rxp'][self.cnt]*self.rf_scale, self.data_njm['foot_ryp'][self.cnt]*self.rf_scale,
                         ec='tab:blue', zorder=15)
        
        # plot moment
        # if positive, plot green...if negative, plot red
        if self.data_njm['foot_njmp'][self.cnt] >= 0:
            moment_color = 'tab:orange'
        else:
            moment_color = 'tab:purple'
        circ = plt.Circle((self.data_digi[ank_x][self.cnt]-offset_x, self.data_digi[ank_y][self.cnt]-offset_y),
                          abs(self.data_njm['foot_njmp'][self.cnt])*self.rf_scale,
                          color=moment_color, zorder=10)
        self.f_ax1.add_artist(circ)
        
        
        #### shank
        # plot line for "right" side of shank
        self.f_ax1.plot((self.data_digi[knee_x][self.cnt]-offset_x+offset_shank_x, self.data_digi[ank_x][self.cnt]-offset_x+offset_shank_x),
                        (self.data_digi[knee_y][self.cnt]-offset_y+offset_shank_y, self.data_digi[ank_y][self.cnt]-offset_y+offset_shank_y),
                        'w-', path_effects=[pe.Stroke(linewidth=8, foreground='k'), pe.Normal()], zorder=0)
            
        # plot center of mass
        self.f_ax1.plot(self.data_cm[shank_x][self.cnt]-offset_x+offset_shank_x, self.data_cm[shank_y][self.cnt]-offset_y+offset_shank_y,
                        'y*', zorder=5)
        
        # plot NJF at knee
        self.f_ax1.arrow(self.data_digi[ank_x][self.cnt]-offset_x+offset_shank_x, self.data_digi[ank_y][self.cnt]-offset_y+offset_shank_y,
                         self.data_njm['shank_rxd'][self.cnt]*self.rf_scale, self.data_njm['shank_ryd'][self.cnt]*self.rf_scale,
                         ec='tab:blue', zorder=15)
        # plot NJF at ankle
        self.f_ax1.arrow(self.data_digi[knee_x][self.cnt]-offset_x+offset_shank_x, self.data_digi[knee_y][self.cnt]-offset_y+offset_shank_y,
                         self.data_njm['shank_rxp'][self.cnt]*self.rf_scale, self.data_njm['shank_ryp'][self.cnt]*self.rf_scale,
                         ec='tab:blue', zorder=15)
        
        # plot proximal moment
        # if positive, plot green...if negative, plot red
        if self.data_njm['shank_njmp'][self.cnt] >= 0:
            moment_color_p = 'tab:orange'
        else:
            moment_color_p = 'tab:purple'
        circ_p = plt.Circle((self.data_digi[knee_x][self.cnt]-offset_x+offset_shank_x, self.data_digi[knee_y][self.cnt]-offset_y+offset_shank_y),
                            abs(self.data_njm['shank_njmp'][self.cnt])*self.rf_scale, color=moment_color_p)
        self.f_ax1.add_artist(circ_p)
        # plot distal moment
        # if positive, plot green...if negative, plot red
        if self.data_njm['shank_njmd'][self.cnt] >= 0:
            moment_color_d = 'tab:orange'
        else:
            moment_color_d = 'tab:purple'
        circ_d = plt.Circle((self.data_digi[ank_x][self.cnt]-offset_x+offset_shank_x, self.data_digi[ank_y][self.cnt]-offset_y+offset_shank_y),
                            abs(self.data_njm['shank_njmd'][self.cnt])*self.rf_scale, color=moment_color_d)
        self.f_ax1.add_artist(circ_d)
        
        
        #### thigh
        # plot line for "right" side of thigh
        self.f_ax1.plot((self.data_digi[hip_x][self.cnt]-offset_x+offset_thigh_x, self.data_digi[knee_x][self.cnt]-offset_x+offset_thigh_x),
                        (self.data_digi[hip_y][self.cnt]-offset_y+offset_thigh_y, self.data_digi[knee_y][self.cnt]-offset_y+offset_thigh_y),
                        'w-', path_effects=[pe.Stroke(linewidth=8, foreground='k'), pe.Normal()], zorder=0)
        
        # plot center of mass
        self.f_ax1.plot(self.data_cm[thigh_x][self.cnt]-offset_x+offset_thigh_x,
                        self.data_cm[thigh_y][self.cnt]-offset_y+offset_thigh_y,
                        'y*', zorder=5)
        
        # plot NJF at hip
        self.f_ax1.arrow(self.data_digi[knee_x][self.cnt]-offset_x+offset_thigh_x, self.data_digi[knee_y][self.cnt]-offset_y+offset_thigh_y,
                         self.data_njm['thigh_rxd'][self.cnt]*self.rf_scale, self.data_njm['thigh_ryd'][self.cnt]*self.rf_scale,
                         ec='tab:blue', zorder=15)
        # plot NJF at knee
        self.f_ax1.arrow(self.data_digi[hip_x][self.cnt]-offset_x+offset_thigh_x, self.data_digi[hip_y][self.cnt]-offset_y+offset_thigh_y,
                         self.data_njm['thigh_rxp'][self.cnt]*self.rf_scale, self.data_njm['thigh_ryp'][self.cnt]*self.rf_scale,
                         ec='tab:blue', zorder=15)
        
        # plot proximal moment
        # if positive, plot green...if negative, plot red
        if self.data_njm['thigh_njmp'][self.cnt] >= 0:
            moment_color_p = 'tab:orange'
        else:
            moment_color_p = 'tab:purple'
        circ_p = plt.Circle((self.data_digi[hip_x][self.cnt]-offset_x+offset_thigh_x, self.data_digi[hip_y][self.cnt]-offset_y+offset_thigh_y),
                            abs(self.data_njm['thigh_njmp'][self.cnt])*self.rf_scale,
                            color=moment_color_p, zorder=10)
        self.f_ax1.add_artist(circ_p)
        # plot distal moment
        # if positive, plot green...if negative, plot red
        if self.data_njm['thigh_njmd'][self.cnt] >= 0:
            moment_color_d = 'tab:orange'
        else:
            moment_color_d = 'tab:purple'
        circ_d = plt.Circle((self.data_digi[knee_x][self.cnt]-offset_x+offset_thigh_x, self.data_digi[knee_y][self.cnt]-offset_y+offset_thigh_y),
                            abs(self.data_njm['thigh_njmd'][self.cnt])*self.rf_scale,
                            color=moment_color_d, zorder=10)
        self.f_ax1.add_artist(circ_d)


    def fbd_animate(self, filename='fbd_animate.mp4', ):
        """
        Function::: fbd_animate
            Description: Create an animated video of the free body diagram.
            Details:  At every instant in contact phase.

        Inputs
            self:
            filename: STR Name of the animation file

        Outputs
            output1: None

        Dependencies
            matplotlib

        """

        # Dependencies
        import matplotlib.animation
        
        """ initialize lines """
        sc_ax4 = self.f_ax4.axvline()
        sc_ax3 = self.f_ax3.axvline()
        sc_ax2 = self.f_ax2.axvline()
        
        """ create animation function """
        def animate(i):
            # update counter
            self.cnt = i + self.data_njm.first_valid_index()
            # update free body diagram
            fbd_vis.fbd_update(self)
            # update line counter
            sc_ax4.set_xdata(x=self.data_njm['time'][self.cnt])
            sc_ax3.set_xdata(x=self.data_njm['time'][self.cnt])
            sc_ax2.set_xdata(x=self.data_njm['time'][self.cnt])
        
        
        """ create animation """
        ani = matplotlib.animation.FuncAnimation(self.fig, animate, fargs=( ),
                                                 frames=len(self.data_njm), interval=1, repeat=False)
        dpi = int(self.fig.dpi)
        writer = matplotlib.animation.writers['ffmpeg'](fps=30)
        ani.save(filename, writer=writer, dpi=dpi)




def fbd_overlay(file_vid, data_force, data_digi, data_cm, data_njm, side, frame_start,
                samp_vid=240, samp_force=1200, colorlegend="flexext", body_mass=None, rf_scale=0.1, imout=False,
                flipy="yes", innercirc_mag=5, legend_loc="topleft", file_vid_n="fbd_overlay.mp4"):
    """
    Function::: fbd_overlay
            Description: Run functions to create animation of FBD
            Details:

    Inputs
    file_vid : STR full path file name of the video to overlay the free body diagram visual
    data_force : DATAFRAME force data (fx, fy, ax, ay) (N, N, m, m).
    data_digi : DATAFRAME digitized data (m).
    data_cm : DATAFRAME center of mass data for segments and body (m).
        format matches that of NJM.dig2jointkinetics.dig2jk.main().
    data_njm : DATAFRAME contains calculated variables for segment's joint kinetics.
    side : STRING which side of the body (ex- 'left')
    frame_start : INT frame number when the net joint moment calculations begin (i.e., contact frame)
        this is zero-based
    samp_vid : INT, optional (default: 240) sampling rate of the video
    samp_force : INT, optional (default: 1200) sampling rate of the force data
    colorlegend : STRING, optional (default: 'flexext')
        What do positive/negative values represent?
        Possible inputs:
            'flexext': positive = extensor moment; negative = flexor moment
            'posneg': positive = positive moment w/r reference frame; negative = negative moment w/r reference frame
    body_mass : FLOAT, optinal (default: None)
        body mass of individual. this will be used to scale the circles
    rf_scale : INT, optional (default: 0.1) It scales the force and moments ONLY IN THE VISUAL.
    imout : BOOLEAN, optional (default: False) export still frame images for the entire video
    flipy : STR, optional (default: "yes")
        yes/no to flip the digitized data to match video reference system
    innercirc_mag : INT, optional (default: 5)
        magnitude (units: Nm/kg) of the inner circles displayed on video
    legend_loc : STR, optional (default: "yes")
        description of location for the legend (currently only topleft or northwest are possible)
    file_vid_n : STR (default: "fbd_overlay.mp4)
        the name of the new video output

    Outputs
        output1: None

    Dependencies
        cv2
        pandas
        numpy
    """

    # Dependencies
    import cv2
    import pandas as pd
    import numpy as np

    """ convert njm data to match digitized data """
    # find sampling factor
    samp_fact = int(samp_force / samp_vid)
    # keep every other samp_fact row
    data_njm_crop = data_njm.copy().iloc[::samp_fact, :]
    # set index to match digitized data
    data_njm_crop = data_njm_crop.set_index(pd.Index(range(frame_start, len(data_njm.iloc[::samp_fact, :])+frame_start)))

    """ filter digitized endpoints and center of mass to only side that njm was calculated """
    data_digi_side = data_digi.copy().filter(regex = side)
    data_cm_side = data_cm.copy().filter(regex = side)

    """ set body mass for normalization """
    if body_mass is None:
        # make one to not alter calculations
        body_mass = 1

    """ sync net joint moment data with the video """
    samp_fact = samp_force / samp_vid

    """ set up location for new images """
    if imout is True:
        # if just file name was given
        if os.path.dirname(file_vid) == '':
            savefolder = 'FBD_OL'
        else:
            savefolder = os.path.join(os.path.dirname(file_vid), 'FBD_OL')
        # if folder does not exist
        if not os.path.exists(savefolder):
            os.makedirs(savefolder)

    """ load video file and initialize new video """
    # load current video
    cap = cv2.VideoCapture(file_vid)
    # default resolutions of the frame are obtained.The default resolutions are system dependent.
    # we convert the resolutions from float to integer.
    frame_width, frame_height = int(cap.get(3)), int(cap.get(4))
    # define the codec and create VideoWriter object
    vid_out = cv2.VideoWriter(file_vid_n, cv2.VideoWriter_fourcc('M', 'P', '4', 'V'),
                              samp_vid / 4, (frame_width, frame_height))

    """ flip y axis of digitized data to match video reference system """
    if flipy == 'yes':
        # digitized data
        data_digi_side.loc[:, data_digi_side.columns.str.contains('_y')] = frame_height - data_digi_side.loc[:, data_digi_side.columns.str.contains('_y')]
        # center of mass data
        data_cm_side.loc[:, data_cm_side.columns.str.contains('_y')] = frame_height - data_cm_side.loc[:, data_cm_side.columns.str.contains('_y')]

    """ create video """
    # find all frame numbers
    frame_num_list = data_digi['frame']
    # create frame counter
    frame_cnt = 0
    # create njm counter
    njm_cnt = 0

    while (True):
        ret, frame = cap.read()
        if ret == True:

            """ add legend """
            # calculate location of box and text
            if legend_loc in ["northwest", "topleft"]:
                rec_1 = (int(frame_width*0.023), int(frame_height*0.014))
                rec_2 = (int(frame_width*0.438), int(frame_height*0.236))
                ext_loc = (int(frame_width*0.031), int(frame_height*0.083))
                fle_loc = (int(frame_width*0.031), int(frame_height*0.167))
                inc_loc = (int(frame_width*0.031), int(frame_height*0.222))
            # add to image
            frame = cv2.rectangle(frame, rec_1, rec_2, (255, 255, 255), -1)
            frame = cv2.putText(frame, "Extension NJM", ext_loc, cv2.FONT_HERSHEY_COMPLEX, 0.825, (80, 127, 255), 2)
            frame = cv2.putText(frame, "Flexion NJM", fle_loc, cv2.FONT_HERSHEY_COMPLEX, 0.825, (211,85,186), 2)
            frame = cv2.putText(frame, "Inner Circle Mag = " + str(innercirc_mag) + " Nm/kg",
                                inc_loc, cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,0), 1)

            """ apply skeleton on each image """
            # if current frame is in data
            if any(data_njm_crop.index.isin([frame_cnt])):

                # find what index current frame is
                frameloc = np.where(frame_num_list == frame_cnt)[0][0]

                """ hip """
                # create njm tuple location
                njm_loc = tuple(data_digi_side.filter(regex='hip').loc[frameloc, :].astype(int))
                # create njm magnitude
                njm_mag = abs(int(round(data_njm_crop["thigh_njmp"][frame_cnt] / body_mass)))
                # if positive, plot "coral"...if negative, plot "mediumorchid"
                if data_njm_crop['thigh_njmp'][frame_cnt] >= 0:
                    moment_color_p = (80, 127, 255)
                else:
                    moment_color_p = (211, 85, 186)
                # display net joint moment
                frame = cv2.circle(frame, njm_loc, njm_mag, moment_color_p, 2)
                # display inner circles
                for in_mag in range(int(round(njm_mag/innercirc_mag))):
                    # display net joint moment
                    frame = cv2.circle(frame, njm_loc, (in_mag+1)*innercirc_mag, moment_color_p, 1)

                """ knee """
                # create njm tuple location
                njm_loc = tuple(data_digi_side.filter(regex='knee').loc[frameloc, :].astype(int))
                # create njm magnitude
                njm_mag = abs(int(round(data_njm_crop["shank_njmp"][frame_cnt] / body_mass)))
                # if positive, plot "coral"...if negative, plot "mediumorchid"
                if data_njm_crop['shank_njmp'][frame_cnt] >= 0:
                    moment_color_p = (80, 127, 255)
                else:
                    moment_color_p = (211, 85, 186)
                # display net joint moment
                frame = cv2.circle(frame, njm_loc, njm_mag, moment_color_p, 2)
                # display inner circles
                for in_mag in range(int(round(njm_mag/innercirc_mag))):
                    # display net joint moment
                    frame = cv2.circle(frame, njm_loc, (in_mag+1)*innercirc_mag, moment_color_p, 1)

                """ ankle """
                # create njm tuple location
                njm_loc = tuple(data_digi_side.filter(regex='ankle').loc[frameloc, :].astype(int))
                # create njm magnitude
                njm_mag = abs(int(round(data_njm_crop["foot_njmp"][frame_cnt] / body_mass)))
                # if positive, plot "coral"...if negative, plot "mediumorchid"
                if data_njm_crop['foot_njmp'][frame_cnt] >= 0:
                    moment_color_p = (80,127,255)
                else:
                    moment_color_p = (211,85,186)
                # display net joint moment
                frame = cv2.circle(frame, njm_loc, njm_mag, moment_color_p, 2)
                # display inner circles
                for in_mag in range(int(round(njm_mag/innercirc_mag))):
                    # display net joint moment
                    frame = cv2.circle(frame, njm_loc, (in_mag+1)*innercirc_mag, moment_color_p, 1)

                """ iterate counter """
                njm_cnt += 1

            """ save frame and add to video """
            if imout is True:
                # create frame name
                framename = os.path.join(savefolder,
                                         os.path.basename(file_vid)[:-4] + '_' + str(frame_cnt) + '.png')
                cv2.imwrite(framename, frame)

            # write the frame into the file
            vid_out.write(frame)
            # iterate frame number
            frame_cnt += 1
        else:
            break

    """ when everything done, release the video capture and video write objects """
    cap.release()
    vid_out.release()
    # closes all the frames
    cv2.destroyAllWindows()