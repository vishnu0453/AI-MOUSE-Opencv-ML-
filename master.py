import volume_control as vc
import cv2
import pyttsx3
import mediapipe as mp
import numpy as np
import modeDetectorClass as md
import mouse as mouse
import mose_safe as ms

count0 = 0
count1 = 0
count2 = 0
count3 = 0

count4 = 0
count5 = 0
max_count0 = 0
max_count1 = 0
max_count2 = 0
max_count3 = 0
max_count4 = 0
max_count5 = 0

cap= cv2.VideoCapture(0)

mode_detector=md.mode()
volume_obj=vc.volume()
mouse_obj=ms.mouse_control()
flag=0

mode_decider=[]

# engine = pyttsx3.init()

# def speak(message):
#         engine.say(message)
#         engine.runAndWait()
#         engine.setProperty('rate', 165)
# speak("Master mode activated")

while True:
    ret,frame=cap.read()

    # frame_copy1=frame
    # frame_copy2=frame

    for num in mode_decider:
        if num == 0:
            count0 += 1
        else:
            count0=0
        if count0==31 :    
            max_count0 = max(max_count0, count0)
        
        if num == 1:
            count1 += 1
        else:
            count1=0
        if count1==21:    
            max_count1 = max(max_count1, count1)
        if num == 2:
            count2 += 1
        else:
            count2=0
        if count2==21:    
            max_count2 = max(max_count2, count2)
        if num == 3:
            count3 += 1
        else:
            count3=0
        if count3==31:    
            max_count3 = max(max_count3, count3)
        if num == 4:
            count4 += 1
        else:
            count4=0
        if count0==31:    
            max_count4 = max(max_count4, count4)

        if num == 5:
            count5 += 1
        else:
            count5=0
        if count5==31:    
            max_count5 = max(max_count5, count5)
            # count = 0

    if mode_detector.hand_present(frame):
    # if mode_detector.hand_present(frame_copy1) and max_count<=30:
    # if mode_detector.hand_present(frame_copy1) and mode_decider.count(1)<=40:
        # frame_copy1,x1,y1,x2,y2,prediction,predicted_character=mode_detector.modefunc(frame_copy1)
        mode_img,x1,y1,x2,y2,prediction,predicted_character=mode_detector.modefunc(frame)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
        cv2.putText(frame, predicted_character, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3,
                                            cv2.LINE_AA)
        cv2.imshow('frame',frame)
        mode_decider.append(int(prediction[0]))
    else:
    # elif(max_count<=30):
    # elif(mode_decider.count(1)<=40):
        cv2.imshow('frame',frame)

    
    # print(count)
    # print(count1)
    print(f'c1 {count1}')
    if(max_count1>20):
    
        flag=1
        break
        # test_obj.execute()

    print(f'c2 {count2}')
    if (max_count2>20):
        break

    
    if cv2.waitKey(1) & 0xFF==27:
        break
if flag==1:
    volume_obj.execute()

if max_count2>20:

    mouse_obj.execute()
    
   

cap.release()
cv2.destroyAllWindows()








