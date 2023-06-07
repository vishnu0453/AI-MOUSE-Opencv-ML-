
import cv2
import numpy as np
import HandTrackingModule as htm
import time
import math
import pyautogui
pyautogui.FAILSAFE = False
import handModule as hm
import pyttsx3
import modeDetectorClass as md


 
##########################
class mouse_control:
    def execute(self,frame):
        mode_detector=md.mode()
        print('mouse control')
        engine = pyttsx3.init()

        # mode_detector=md.mode()
        # mode_decider=[]
        # flag=0 

        def speak(message):
            engine.say(message)
            engine.runAndWait()
            engine.setProperty('rate', 165)
        # speak('mouse control mode activated')
        
        wCam, hCam = 640, 480
        frameR = 80 # Frame Reduction
        smoothening = 4
        #########################
        
        pTime = 0
        plocX, plocY = 0, 0
        clocX, clocY = 0, 0
        
        # cap = cv2.VideoCapture(0)
        # cap.set(3, wCam)
        # cap.set(4, hCam)
        detector = hm.handDetector()
        wScr, hScr = pyautogui.size()
        # print(wScr, hScr)
        
        
            # 1. Find hand Landmarks
        # success, img = cap.read()
        frame_copy1=frame.copy()
        frame_copy2=frame.copy()
        coords=[]

        handpresent=mode_detector.hand_present(frame_copy2)
        if handpresent:
             mouse_img=detector.mark_handlms(frame_copy1)
             coords=detector.coordinates(frame_copy1)
             

        # mode_img=None
                    
        # if mode_detector.hand_present(frame_copy1): #this checks whether hand is present in frame or not

        #     mode_img,x1,y1,x2,y2,prediction,predicted_character=mode_detector.modefunc(img)

        #     mode_decider.append(int(prediction[0]))
        #     mouse_img=detector.mark_handlms(frame_copy1)
        #     coords=detector.coordinates(frame_copy1)

        # if(mode_decider.count(5)>35):
        #     flag=1 
        #     speak("master mode activated")
        #     break


        # 2. Get the tip of the index and middle fingers
        # x1,y1,x2,y2=0,0,0,0
        if len(coords) != 0:
            thumb_tip_x, thumb_tip_y = coords[4][1:]
            index_tip_x, index_tip_y = coords[8][1:]

            # print(x1, y1, x2, y2)

            dist_thumb_index=int(math.hypot((thumb_tip_x-index_tip_x),(thumb_tip_y-index_tip_y)))
            cv2.line(frame_copy1,(thumb_tip_x,thumb_tip_y),(index_tip_x,index_tip_y),(255,0,0),2,cv2.LINE_AA)

            print(dist_thumb_index)
            
            x3 = np.interp(thumb_tip_x, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(thumb_tip_y, (frameR, hCam - frameR), (0, hScr))
                # 6. Smoothen Values
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening
                
                    # 7. Move Mouse
            if(dist_thumb_index<160):
                pyautogui.moveTo(wScr - clocX, clocY)
            # pyautogui.moveTo(wScr-x3,y3)

            if(dist_thumb_index>70 and dist_thumb_index<160):
                pyautogui.click(wScr - clocX,clocY)
                cv2.circle(frame_copy1, (thumb_tip_x, thumb_tip_y), 7, (0, 255, 0), cv2.FILLED)
                plocX, plocY = clocX, clocY

                cv2.circle(frame_copy1, (index_tip_x, index_tip_y), 7, (0, 255, 0), cv2.FILLED)
                plocX, plocY = clocX, clocY


            cv2.circle(frame_copy1, (thumb_tip_x, thumb_tip_y), 7, (255, 255, 0), cv2.FILLED)
            plocX, plocY = clocX, clocY

            cv2.circle(frame_copy1, (index_tip_x, index_tip_y), 7, (255, 255, 0), cv2.FILLED)
            plocX, plocY = clocX, clocY
                
           
            
        # 11. Frame Rate
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime



        # # if (mode_img is not None):
        # cv2.rectangle(frame_copy1, (x1, y1), (x2, y2), (0, 0, 0), 4)
        # cv2.putText(frame_copy1, predicted_character, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3,
        #                                                 cv2.LINE_AA)
        cv2.putText(frame_copy1, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 0), 3)
        # 12. Display
        cv2.rectangle(frame_copy1, (frameR, frameR), (wCam - frameR, hCam - frameR),
                        (255, 255, 0), 2)
                    
        if handpresent:
            return frame_copy1
        else:
            return frame
        # else:
        #         # cv2.rectangle(mouse_img, (frameR, frameR), (wCam - frameR, hCam - frameR),
        #         #     (255, 255, 0), 2)
        #         cv2.imshow('frame',img)


        # if cv2.waitKey(1) & 0xFF==27:
        #     break
    # if flag==1:
    #     with open('C:/Users/venkatson/OneDrive/Desktop/CV/CV  projects/AI MOUSE/master.py', 'r') as f:
    #         code = f.read()
    #         exec(code)

        # cap.release()
        # cv2.destroyAllWindows()