import os
from ImportForce_TXT import ImportForce_TXT
from FindContactIntervals import FindContactIntervals
from findplate import findplate
from pixelratios import pix2m_fromplate, bw2pix
from dataconversion_force import convertdata
from VectorOverlay.vectoroverlay import vectoroverlay

pathOfForce = r'C:\Users\shani\OneDrive\Documents\USC Data'
pathOfVideo = r'C:\Users\shani\OneDrive\Documents\USC Data'

forceFilename = '5.5min_120Hz_SSRun_Fa19_Force.txt'
videoFilename = '5.5min_120Hz_SSRun_Fa19.mp4'
videoFileOL = videoFilename[:-4] + '_0L.mp4'

fp1 = 'Attila49'
fp2 = 'Ryan52'

videoSamplingRate = 120
contactFrame = 241-1

rawData_1, samp, bw = ImportForce_TXT(os.path.join(pathOfForce, forceFilename))

contactIntervals_1 = FindContactIntervals((rawData_1['Attila49 9286BA_Fz'] + rawData_1['Ryan52 9286BA_Fz'])
                                          , samp, thresh=16)
data_1 = {0: rawData_1.filter(regex = fp1).iloc[contactIntervals_1['Start'][0]:contactIntervals_1['End'][0],:],
          1: rawData_1.filter(regex = fp2).iloc[contactIntervals_1['Start'][0]:contactIntervals_1['End'][0],:]}

plateArea = findplate(os.path.join(pathOfForce, videoFilename), framestart = 0, label = 'Insert image here')

#def findarea(video, frame = 0, label = 'frame', method = "clickdrag"):
pixel2meter = pix2m_fromplate(plateArea, (0.6, 0.4))
magnitude2pixel = bw2pix(pixel2meter['x'], bw, bwpermeter = 2)
flip = {0: ['fy', 'ax', 'fx'],
        1: ['fy', 'ay']}

def flipdata(self):
    convertdata.selectdata(self)
    if self.flip is not None:
        for cnt in range(len(self.data)):
            if 'fx' in self.flip[cnt]:
                self.data_fp[cnt]['fx'] = self.data_fp[cnt]['fx'] * -1
            if 'fy' in self.flip[cnt]:
                self.data_fp[cnt]['fy'] = self.data_fp[cnt]['fy'] * -1
            if 'ax' in self.flip[cnt]:
                self.data_fp[cnt]['ax'] = self.data_fp[cnt]['ax'] * -1
            if 'ay' in self.flip[cnt]:
                self.data_fp[cnt]['ay'] = self.data_fp[cnt]['ay'] * -1
transform_data = convertdata(data_1, magnitude2pixel, pixel2meter, view = "fx", mode = "combine",
                             platelocs = plateArea, flip = flip)
transform_data.data2pix()

dataPixels_1 = transform_data.data_fp

vectoroverlay(os.path.join(pathOfVideo, videoFilename), videoFileOL, dataPixels_1, contactFrame, samp_force = samp,
              samp_video = videoSamplingRate, dispthresh = 60)