# -*- coding: utf-8 -*-
"""
CropVideo

Crop the original video to set duration

Created on Thu Oct 10 09:45:08 2019

@author: Casey Wiens, cwiens32@gmail.com
"""

#    from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
# from moviepy.video.io.VideoFileClip import VideoFileClip
import cv2
import numpy as np

def increase_brightness(img, value=30):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    
    return img


def CropVideo(file_o, file_n='croppedvideo.mp4', frame_start=1, frame_end=2, 
              camera_hz=120, exportclips=0, padB=1/8, padE=1/2,
              exportclip_name='croppedvideo.jpg', brighten=0):

    
    #%% initialzie variables
    # load video file
    cap = cv2.VideoCapture(file_o)
    # set end frame as last frame
    if frame_end == 2:
        frame_end = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        
    
    #%%
    """
    subtract padB of the camera sampling rate from the beginning (extra padding)
    add padE of the camera sampling rate to the ending (extra padding)
    """
    frame_start_pad = int(np.amax([frame_start - camera_hz * padB,
                                   1]))
    frame_end_pad = int(np.amin([frame_end + camera_hz * padE,
                                 cap.get(cv2.CAP_PROP_FRAME_COUNT)]))
    # cap.release()
    
    #%% Write video
    # vidclip = VideoFileClip(file_o)
    # fps = vidclip.fps
    # vidclip.close()
    # video = VideoFileClip(file_o).subclip(frame_start_pad/fps,frame_end_pad/fps)
    # video.write_videofile(file_n,fps=fps)
    # video.close()
    # default resolutions of the frame are obtained.The default resolutions are system dependent.
    # we convert the resolutions from float to integer.
    frame_width, frame_height = int(cap.get(3)), int(cap.get(4))
    # define the codec and create VideoWriter object
    out = cv2.VideoWriter(file_n, cv2.VideoWriter_fourcc('M','P','4','V'),
                          camera_hz/4, (frame_width,frame_height))
    
    # load in first frame
    ret, frame = cap.read()
    for cntf in range(frame_start_pad,frame_end_pad):
        # set current frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, cntf)
        ret, frame = cap.read()
        if ret == True:
            # if brightness should be changed
            if brighten > 0:
                frame = increase_brightness(frame, value=brighten)
            # write the frame into the file
            out.write(frame)
        else:
            break
    # when everything done, release the video capture and video write objects
    cap.release()
    out.release()
    # closes all the frames
    cv2.destroyAllWindows()
    
    # this is causing error with freezing frames and/or frame number misordering
    # hopefully find a resolution soon (acknowledged 2019 Nov 14)
#    ffmpeg_extract_subclip(filename = file_o,
#                           t1 = frame_start_pad/fps,
#                           t2 = frame_end_pad/fps,
#                           targetname = file_n)
    
    #%% Create image of key frames as a quality control check
    """
    export jpg of six images selected evenly spaced from start and end of new video
    """
    if exportclips > 0:
        cap = cv2.VideoCapture(file_o)
        ret, im1 = cap.read()
        img = None
        count = 1
        for x in np.linspace(frame_start_pad, frame_end_pad, 6).round():
            cap.set(cv2.CAP_PROP_POS_FRAMES, x-3)
            ret, im1 = cap.read()
            
            if img is None:     
                dim = im1.shape
                img = np.zeros([dim[0]*3,dim[1]*2,3],dtype=np.uint8)
            
            if count <= 3:
                img[ dim[0]*(count-1):dim[0]*count, :dim[1] , ] = im1
            else:
                img[ dim[0]*(count-4):dim[0]*(count-3), dim[1]:dim[1]*2 , ] = im1
                
            count += 1
            
        cap.release()
        cv2.destroyAllWindows()
        
        cv2.imwrite(exportclip_name, img)
