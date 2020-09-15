# -*- coding: utf-8 -*-
"""
fbd_vis
    Create a visual displaying free body diagram at an instance along with
    the NJM curves of the segments. CURRENTLY ONLY FOR LOWER BODY.
        
Created on Mon Sep 14 17:03:38 2020

@author: cwiens
"""

class fbd_vis():
    
    #%%
    def __init__(self, data_force, data_digi, data_cm, data_njm, side, cnt=None):
        """
        Initialize class to create free body diagram visual.

        Parameters
        ----------
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
            (ex: 'left').
        cnt : INT, optional
            counter - index of data to be visualized.
            The default is None, but will be reset to the first index of data

        Returns
        -------
        None.

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
        fbd_vis.fig_init(self)
        
    #%%
    def fig_init(self):
        """
        Initializes the figure with an empty subplot for the free body diagram,
        and the foot, shank and thigh joint kinetic variables plotted.

        Returns
        -------
        None.

        """
        
        import matplotlib.pyplot as plt
        
        """ initialize figure """
        # create subplots of figure
        self.fig = plt.figure(constrained_layout=True)
        # maximize figure
        manager = plt.get_current_fig_manager()
        manager.window.showMaximized()
        # create 3x2 with second column double the width
        gs = self.fig.add_gridspec(3,2, width_ratios=[1,2])
        self.f_ax1 = self.fig.add_subplot(gs[0:, 0])
        self.f_ax2 = self.fig.add_subplot(gs[0,-1])
        self.f_ax3 = self.fig.add_subplot(gs[1,-1])
        self.f_ax4 = self.fig.add_subplot(gs[-1,-1])
        
        """ plot moment time curves and move time tracer along x-axis """
        ### foot
        self.f_ax4.plot(self.data_njm['time'], self.data_njm['foot_md'], '#BEBCC5', label='Distal NJF Moment')
        self.f_ax4.plot(self.data_njm['time'], self.data_njm['foot_mp'], '#F4D4D4', label='Proximal NJF Moment')
        self.f_ax4.plot(self.data_njm['time'], self.data_njm['foot_njmd'], '#DCB69F', label='Distal NJM Moment')
        self.f_ax4.plot(self.data_njm['time'], self.data_njm['foot_njmp'], '#342A1F', label='Proximal NJM Moment')
        self.f_ax4.set_ylim(-600, 600)
        self.f_ax4.set_title('Foot')
        ### shank
        self.f_ax3.plot(self.data_njm['time'], self.data_njm['shank_md'], '#BEBCC5', label='Distal NJF Moment')
        self.f_ax3.plot(self.data_njm['time'], self.data_njm['shank_mp'], '#F4D4D4', label='Proximal NJF Moment')
        self.f_ax3.plot(self.data_njm['time'], self.data_njm['shank_njmd'], '#DCB69F', label='Distal NJM Moment')
        self.f_ax3.plot(self.data_njm['time'], self.data_njm['shank_njmp'], '#342A1F', label='Proximal NJM Moment')
        self.f_ax3.set_ylim(-600, 600)
        self.f_ax3.set_title('Shank')
        ### thigh
        self.f_ax2.plot(self.data_njm['time'], self.data_njm['thigh_md'], '#BEBCC5', label='Distal NJF Moment')
        self.f_ax2.plot(self.data_njm['time'], self.data_njm['thigh_mp'], '#F4D4D4', label='Proximal NJF Moment')
        self.f_ax2.plot(self.data_njm['time'], self.data_njm['thigh_njmd'], '#DCB69F', label='Distal NJM Moment')
        self.f_ax2.plot(self.data_njm['time'], self.data_njm['thigh_njmp'], '#342A1F', label='Proximal NJM Moment')
        self.f_ax2.set_ylim(-600, 600)
        self.f_ax2.set_title('Thigh')
        # add legends
        self.f_ax4.legend()
        self.f_ax3.legend()
        self.f_ax2.legend()
        
    #%%
    def fbd_update(self, rf_scale=0.0002):
        """
        Refreshes and displays the free body diagram at the instant of choice.
        
        Parameters
        ----------
        rf_scale : FLOAT, optional
            Scaling of the reaction force vector. The default is 0.0002.

        Returns
        -------
        None.

        """
        
        import matplotlib.pyplot as plt
        import matplotlib.patheffects as pe
        
        """ identify labels for segments """
        toe_x = 'toe_' + self.side + '_x'
        toe_y = 'toe_' + self.side + '_y'
        heel_x = 'heel_' + self.side + '_x'
        heel_y = 'heel_' + self.side + '_y'
        foot_x = 'foot_' + self.side + '_x'
        foot_y = 'foot_' + self.side + '_y'
        ank_x = 'ankle_' + self.side + '_x'
        ank_y = 'ankle_' + self.side + '_y'
        shank_x = 'shank_' + self.side + '_x'
        shank_y = 'shank_' + self.side + '_y'
        knee_x = 'knee_' + self.side + '_x'
        knee_y = 'knee_' + self.side + '_y'
        thigh_x = 'thigh_' + self.side + '_x'
        thigh_y = 'thigh_' + self.side + '_y'
        hip_x = 'hip_' + self.side + '_x'
        hip_y = 'hip_' + self.side + '_y'
        
        # refresh subplot and set FBD axis limits
        self.f_ax1.clear()
        self.f_ax1.set_xlim(-0.75,0.75)
        self.f_ax1.set_ylim(-0.5,2.5)
        self.f_ax1.set_aspect(1)
        
        # display title
        self.f_ax1.set_title('Time (s): ' + str(round(self.data_njm['time'][self.cnt], 4)))
        
        # set offsets
        offset_x = self.data_cm[foot_x][self.cnt]
        offset_y = self.data_cm[foot_y][self.cnt]
        offset_shank_x = 0
        offset_thigh_x = offset_shank_x + 0
        offset_shank_y = 0.3
        offset_thigh_y = offset_shank_y + 0.3
        
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
                         self.data_njm['foot_rxd'][self.cnt]*rf_scale, self.data_njm['foot_ryd'][self.cnt]*rf_scale,
                         ec='tab:blue', zorder=15)
        # plot NJF at ankle
        self.f_ax1.arrow(self.data_digi[ank_x][self.cnt]-offset_x, self.data_digi[ank_y][self.cnt]-offset_y,
                         self.data_njm['foot_rxp'][self.cnt]*rf_scale, self.data_njm['foot_ryp'][self.cnt]*rf_scale,
                         ec='tab:blue', zorder=15)
        
        # plot moment
        # if positive, plot green...if negative, plot red
        if self.data_njm['foot_njmp'][self.cnt] >= 0:
            moment_color = 'tab:orange'
        else:
            moment_color = 'tab:purple'
        circ = plt.Circle((self.data_digi[ank_x][self.cnt]-offset_x, self.data_digi[ank_y][self.cnt]-offset_y),
                          abs(self.data_njm['foot_njmp'][self.cnt])*rf_scale,
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
                         self.data_njm['shank_rxd'][self.cnt]*rf_scale, self.data_njm['shank_ryd'][self.cnt]*rf_scale,
                         ec='tab:blue', zorder=15)
        # plot NJF at ankle
        self.f_ax1.arrow(self.data_digi[knee_x][self.cnt]-offset_x+offset_shank_x, self.data_digi[knee_y][self.cnt]-offset_y+offset_shank_y,
                         self.data_njm['shank_rxp'][self.cnt]*rf_scale, self.data_njm['shank_ryp'][self.cnt]*rf_scale,
                         ec='tab:blue', zorder=15)
        
        # plot proximal moment
        # if positive, plot green...if negative, plot red
        if self.data_njm['shank_njmp'][self.cnt] >= 0:
            moment_color_p = 'tab:orange'
        else:
            moment_color_p = 'tab:purple'
        circ_p = plt.Circle((self.data_digi[knee_x][self.cnt]-offset_x+offset_shank_x, self.data_digi[knee_y][self.cnt]-offset_y+offset_shank_y),
                            abs(self.data_njm['shank_njmp'][self.cnt])*rf_scale, color=moment_color_p)
        self.f_ax1.add_artist(circ_p)
        # plot distal moment
        # if positive, plot green...if negative, plot red
        if self.data_njm['shank_njmd'][self.cnt] >= 0:
            moment_color_d = 'tab:orange'
        else:
            moment_color_d = 'tab:purple'
        circ_d = plt.Circle((self.data_digi[ank_x][self.cnt]-offset_x+offset_shank_x, self.data_digi[ank_y][self.cnt]-offset_y+offset_shank_y),
                            abs(self.data_njm['shank_njmd'][self.cnt])*rf_scale, color=moment_color_d)
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
                         self.data_njm['thigh_rxd'][self.cnt]*rf_scale, self.data_njm['thigh_ryd'][self.cnt]*rf_scale,
                         ec='tab:blue', zorder=15)
        # plot NJF at knee
        self.f_ax1.arrow(self.data_digi[hip_x][self.cnt]-offset_x+offset_thigh_x, self.data_digi[hip_y][self.cnt]-offset_y+offset_thigh_y,
                         self.data_njm['thigh_rxp'][self.cnt]*rf_scale, self.data_njm['thigh_ryp'][self.cnt]*rf_scale,
                         ec='tab:blue', zorder=15)
        
        # plot proximal moment
        # if positive, plot green...if negative, plot red
        if self.data_njm['thigh_njmp'][self.cnt] >= 0:
            moment_color_p = 'tab:orange'
        else:
            moment_color_p = 'tab:purple'
        circ_p = plt.Circle((self.data_digi[hip_x][self.cnt]-offset_x+offset_thigh_x, self.data_digi[hip_y][self.cnt]-offset_y+offset_thigh_y),
                            abs(self.data_njm['thigh_njmp'][self.cnt])*rf_scale,
                            color=moment_color_p, zorder=10)
        self.f_ax1.add_artist(circ_p)
        # plot distal moment
        # if positive, plot green...if negative, plot red
        if self.data_njm['thigh_njmd'][self.cnt] >= 0:
            moment_color_d = 'tab:orange'
        else:
            moment_color_d = 'tab:purple'
        circ_d = plt.Circle((self.data_digi[knee_x][self.cnt]-offset_x+offset_thigh_x, self.data_digi[knee_y][self.cnt]-offset_y+offset_thigh_y),
                            abs(self.data_njm['thigh_njmd'][self.cnt])*rf_scale,
                            color=moment_color_p, zorder=10)
        self.f_ax1.add_artist(circ_d)
    
    #%%
    def fbd_animate(self, filename='fbd_animate.mp4'):
        """
        Create an animated video of the free body diagram at every instant in
        contact phase.

        Parameters
        ----------
        filename : STRING, optional
            Filename for the created animated video.
            The default is 'fbd_animate.mp4'.

        Returns
        -------
        None.

        """
        
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
                                                 frames=len(self.data_njm), interval=0, repeat=False) 
        ani.save(filename, fps=1, extra_args=['-vcodec', 'libx264'])
            