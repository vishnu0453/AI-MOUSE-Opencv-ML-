import cv2
import numpy as np
import mediapipe as mp
import time
import handModule as hm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


class volumeGesture:

    def __init__(self):
        self.detector=hm.handDetector()
        self.devices = AudioUtilities.GetSpeakers()
        self.interface = self.devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(self.interface, POINTER(IAudioEndpointVolume))
        self.x=self.volume.GetVolumeRange()
        self.min_vol=-65.25
        self.max_vol=0
        self.vol_percent=0
        self.str_vol=''
        self.prev_time=0
        self.curr_time=0

        self.flag=0

    def volumeGesturefunc(self,frame):
        # # cap=cv2.VideoCapture(0)
        # # detector=hm.handDetector()
        # devices = AudioUtilities.GetSpeakers()
        # interface = devices.Activate(
        #     IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        # volume = cast(interface, POINTER(IAudioEndpointVolume))
        # # r=volume.GetMute()
        # # volume.GetMasterVolumeLevel()
        # x=volume.GetVolumeRange()

        # min_vol=-65.25
        # max_vol=0
        # vol_percent=0
        # str_vol=''

        # prev_time=0
        # curr_time=0

        # flag=0

        
                
        # ret,frame=cap.read()
        # frame=cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
        frame=self.detector.mark_handlms(frame)
        id_coords_list=self.detector.coordinates(frame)
        cv2.rectangle(frame,(30,100),(55,300),(0,0,255),2)
        if(len(id_coords_list)!=0):
                    
            thumb_x,thumb_y=(id_coords_list[4][1],id_coords_list[4][2])
            middle_x,middle_y=(id_coords_list[12][1],id_coords_list[12][2])
            ring_x,ring_y=(id_coords_list[16][1],id_coords_list[16][2])
            pinky_x,pinky_y=(id_coords_list[20][1],id_coords_list[20][2])
            wrist_x,wrist_y=(id_coords_list[0][1],id_coords_list[0][2])

            cv2.circle(frame,(thumb_x,thumb_y),6,(0,0,255),-1)
            cv2.circle(frame,(middle_x,middle_y),6,(0,0,255),-1)
            cv2.circle(frame,(ring_x,ring_y),6,(0,255,0),-1)
            cv2.circle(frame,(pinky_x,pinky_y),6,(0,255,0),-1)    
            cv2.circle(frame,(wrist_x,wrist_y),6,(0,255,0),-1) 
                    
                    
            dist_wrist_ring=int(math.hypot((wrist_x-ring_x),(wrist_y-ring_y)))
            # print(dist_wrist_ring)``
            dist_pinky_ring=int(math.hypot((pinky_x-ring_x),(pinky_y-ring_y)))
            if(dist_pinky_ring>60):
                self.flag=1

            if(dist_wrist_ring>=40 and dist_wrist_ring<=85):
                self.flag=0
            # print(dist_pinky_ring)
            # print(flag)
            dist=int(np.hypot((thumb_x-middle_x),(thumb_y-middle_y)))
            cv2.line(frame,(wrist_x,wrist_y),(ring_x,ring_y),(255,0,0),2,cv2.LINE_AA)
            cv2.line(frame,(pinky_x,pinky_y),(ring_x,ring_y),(0,255,0),2,cv2.LINE_AA)
            cv2.line(frame,(thumb_x,thumb_y),(middle_x,middle_y),(0,0,255),2,cv2.LINE_AA)
            # print(dist)
            min_dist=0
            max_dist=150
            if(self.flag!=1):
                interpreted_vol=np.interp(dist,(min_dist,max_dist),(self.min_vol,self.max_vol))
                # print(interpreted_vol)
                self.volume.SetMasterVolumeLevel(interpreted_vol, None)
                self.vol_percent=np.interp(interpreted_vol,(self.min_vol,self.max_vol),(295,103))
                vol_bar=np.interp(interpreted_vol,(self.min_vol,self.max_vol),(0,100))
                self.str_vol=str(int(vol_bar))+' %'
                cv2.rectangle(frame,(32,int(self.vol_percent)),(53,298),(0,250,0),-1)
                    
                        
        if(self.flag==1):     
            cv2.rectangle(frame,(32,int(self.vol_percent)),(53,298),(0,250,0),-1)   
        self.curr_time=time.time()
        fps=1/(self.curr_time-self.prev_time)
        fps=str(int(fps))
        self.prev_time=self.curr_time
        font=cv2.FONT_HERSHEY_COMPLEX
        fps='FPS: '+fps
        cv2.putText(frame,fps,(10,30),font,1,(255,255,0),2,cv2.LINE_AA)
        cv2.putText(frame,self.str_vol,(20,340),font,1,(255,0,244),2,cv2.LINE_AA)
        # cv2.imshow('window',frame)
        return frame
        # if(cv2.waitKey(1) & 0xFF==27):
        #     break