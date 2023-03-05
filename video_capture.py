import cv2
import os
import time
import serial
import numpy as np
import uuid
import shutil



def capture_Frames():
    camera = cv2.VideoCapture(0)

    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
def freeze_image_detection(imgpath):
    cap = cv2.VideoCapture(1)
    count = 1
    success, frame = cap.read()
    prevdiff = 0;
    img = uuid.uuid4().int
    path = imgpath+os.sep+str(img)+'.jpg'
    while True:
        prev = frame.copy()
        success, frame = cap.read()
        diff = np.sum(np.abs(prev-frame))
        print(success,count,np.sum(np.abs(prev-frame)))
        if (still_frozen(prevdiff, diff)==False):
            if (diff == 0):
                cv2.imwrite(path, frame)
                count+=1
                return path
            prevdiff = diff
        time.sleep(0.25) #half of nyquist limit

    cap.release()


def freeze_with_socket(socketio,connect,imgpath):


    cap = cv2.VideoCapture(1)
    count = 1
    success, frame = cap.read()
    prevdiff = 0;
    img = uuid.uuid4().int
    path = imgpath+os.sep+str(img)+'.jpg'
    while connect:
        prev = frame.copy()
        success, frame = cap.read()
        diff = np.sum(np.abs(prev-frame))
        print(success,count,np.sum(np.abs(prev-frame)))
        if (still_frozen(prevdiff, diff)==False):
            if (diff == 0):
                cv2.imwrite(path, frame)
                count+=1
                break
                        #return path
            prevdiff = diff
        time.sleep(0.25) #half of nyquist limit
    cap.release()
            #path = vc.freeze_image_detection(imgpath)
    if connect:

        print('sending works!!!')
        socketio.emit('nextimg',{'value':path})
        socketio.sleep(0.5)
        print('blah')
        shutil.move(path,'static\processed')

def still_frozen(prevdiff, currdiff):
    if (np.sum(np.abs(prevdiff-currdiff)==0)):
        return True
    else:
        return False
