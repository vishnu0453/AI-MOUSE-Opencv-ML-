
import volumeControlClass as vc
import modeDetectorClass as md
import cv2
import pyttsx3
import mediapipe as mp
import numpy as np
# import master as master
# cap=cv2.VideoCapture(0)
# Initialize the text-to-speech engine


class volume:
    def execute(self):
        print('volume control')
        engine = pyttsx3.init()


        def speak(message):
            engine.say(message)
            engine.runAndWait()
            engine.setProperty('rate', 190)
        speak("Volume control mode activated")


        mode_detector=md.mode()
        volume_controler=vc.volumeGesture()
        


        mode_decider=[]
        flag=0 

        cap=cv2.VideoCapture(0)
        while True:
            
            ret,frame=cap.read()
            # if frame is not None:
            frame_copy1=frame.copy()
            frame_copy2=frame.copy()

            mode_img=None
                    
            if mode_detector.hand_present(frame_copy1): #this checks whether hand is present in frame or not

                mode_img,x1,y1,x2,y2,prediction,predicted_character=mode_detector.modefunc(frame_copy1)

                mode_decider.append(int(prediction[0]))
                volume_img=volume_controler.volumeGesturefunc(frame_copy2)

            if(mode_decider.count(5)>22):
                # frame2=test_obj.execute(frame)
                # cv2.imshow('frame',frame2)
                flag=1 
                speak("master mode activated")
                break
                
            if (mode_img is not None):
                cv2.rectangle(volume_img, (x1, y1), (x2, y2), (0, 0, 0), 4)
                cv2.putText(volume_img, predicted_character, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3,
                                            cv2.LINE_AA)
                cv2.imshow('frame',volume_img)
            else:
                cv2.imshow('frame',frame)

        
        
        
        
            if cv2.waitKey(1) & 0xFF == 27:
                break
        
        if flag==1:
            with open('C:/Users/venkatson/OneDrive/Desktop/CV/CV  projects/AI MOUSE/master.py', 'r') as f:
                code = f.read()
                exec(code)

        cap.release()
        cv2.destroyAllWindows()
# import volumeControlClass as vc
# import modeDetectorClass as md
# import cv2
# import mediapipe as mp
# import numpy as np
# # cap=cv2.VideoCapture(0)
# class test:
#     def execute(self,frame):
#         print('test')
#         mode_detector=md.mode()
#         volume_controler=vc.volumeGesture()


        

#         # while True:
#             # ret,frame=cap.read()
#         if frame is not None:
#             frame_copy1=frame.copy()
#             frame_copy2=frame.copy()

#             mode_img=None
                    
#             if mode_detector.hand_present(frame_copy1): #this checks whether hand is present in frame or not

#                 # mode_img,x1,y1,x2,y2,prediction,predicted_character=mode_detector.modefunc(frame_copy1)
#                 x1,y1,x2,y2,prediction,predicted_character=mode_detector.modefunc(frame_copy1)
#                 volume_img=volume_controler.volumeGesturefunc(frame_copy2)

                
                
#             # if (mode_img is not None):
#             if (prediction is not None):
#                 cv2.rectangle(volume_img, (x1, y1), (x2, y2), (0, 0, 0), 4)
#                 cv2.putText(volume_img, predicted_character, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3,
#                                             cv2.LINE_AA)
#                 # cv2.imshow('frame',volume_img)
#                 return volume_img
#             else:
#                 # cv2.imshow('frame',frame)
#                 return frame

    
    
    
    
#             # if cv2.waitKey(1) & 0xFF == 27:
#             #  break

# # cap.release()
# # cv2.destroyAllWindows()








