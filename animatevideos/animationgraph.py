"""
Script: animationgraph
    Create animations with videos and graphical data.

Modules
    linegraph: Combine a video and (line) graph into an animation graph.

Author:
    Casey Wiens
    cwiens32@gmail.com
"""


def linegraph(filename, fig, ax, t, video_file, graph_start=0, samp_factor=10):
    """
    Function::: linegraph
    	Description: Combine a video and (line) graph into an animation graph.
    	Details:

    Inputs
        filename: STRING file name of output video
        fig: FIGURE matplotlib figure object of graph
            ex.) fig, ax = plt.subplots()
        ax: AxesSubplot matplotlib axes object of the graph
            ex.) fig, ax = plt.subplots()
        xind: ARRAY indices of x-axis for line animation advancement
            ex.) this would be the time array if the x-axis was time
        video_file: STRING file name of original video
        graph_start: INT (default: 0) the frame number the graph animation should begin
        samp_factor: INT (default: 10) the factor of plot signal sampling rate to the video sampling rate
            ex.) 1200 / 120 = 10  -> samp_force / samp_video = samp_factor

    Outputs
        output1: FILE mp4 file will be created with the name of the input 'filename'

    Dependencies
        cv2
        matplotlib
        os
    """

    # Dependencies
    import cv2
    import matplotlib.animation
    import os
    
    """ create animation function """
    def animate(samp, i):
        if int(i*samp) < len(t):
            sc.set_xdata(x=t.iloc[int(i)*samp])
        else:
            sc.set_xdata(x=None)
        
    
    """ initialize graph line """
    sc = ax.axvline()
    
    
    """ create animation """
    ani = matplotlib.animation.FuncAnimation(fig, animate, fargs=(int(samp_factor), ),
                                  frames=len(t), interval=0, repeat=False) 
    ani.save('anim_temp.mp4', fps=1, extra_args=['-vcodec', 'libx264'])
    
    
    """ create video """
    # initialize video video reader
    cap = cv2.VideoCapture(video_file)
    frame_width, frame_height = int(cap.get(3)), int(cap.get(4))
    # initilaize graph video reader
    graph = cv2.VideoCapture('anim_temp.mp4')
    # create output video file
    out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc('M','P','4','V'),
                          cap.get(cv2.CAP_PROP_FPS), (frame_width,int(frame_height*2)))
    # first video frame number
    framenum_vid = 0
    # read in first frame of video and graph
    ret_v, frame_v = cap.read()
    ret_g, frame_g = graph.read()
    # resize video and graph images
    frame_v = cv2.resize(frame_v, (frame_width, frame_height))
    frame_g = cv2.resize(frame_g, (frame_width, frame_height))
    # ;oop through while video still has frames
    while(ret_v == True):
        ret_v, frame_v = cap.read()
        if ret_v == True:
            # if current frame is when the graph should start
            if framenum_vid >= int(graph_start):
                ret_g, frame_g = graph.read()
                if ret_g == True:
                    # resize video and graph images
                    frame_v = cv2.resize(frame_v, (int(frame_width), int(frame_height)))
                    frame_g = cv2.resize(frame_g, (int(frame_width), int(frame_height)))
        # safety if either graph or video has no more frames
        if ret_v == True and ret_g == True:
            both = cv2.vconcat([frame_v, frame_g])
            out.write(both)
            framenum_vid += 1
    
    # release all captures and close any windows
    cap.release()
    graph.release()
    out.release()
    cv2.destroyAllWindows()
    
    """ remove animation file """
    os.remove("anim_temp.mp4")
