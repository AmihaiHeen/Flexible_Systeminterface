import os
import sys
from os.path import exists
import time
import json
import uuid
import shutil
import threading
from binascii import a2b_base64
from array import *
#from statistics import mean
from threading import Lock
import serial



import cv2
import numpy as np
import video_capture as vc


from flask import Flask, render_template,Response, request,redirect, send_from_directory, jsonify
from flask_socketio import SocketIO

app = Flask(__name__)
thread_lock = Lock()

socketio = SocketIO(app, cors_allowed_origins='*')

@app.route('/', methods=['GET','POST'])
def beginning():
    #freezeThread = threading.Thread(target=vc.freeze_image_detection)
    #freezeThread.start()
    return render_template('index.html')

@app.route('/template_1', methods=['GET','POST'])
def template_1():
    path = ''
    if request.method == 'POST':
        path = 'static/img2.jpeg'
        img = request.form.get('imageCap')
        data = img.split(',')[1]
        #print(data)
        binary_data = a2b_base64(data)
        with open("static/img2.jpeg", 'w+b') as fd:
            fd.write(binary_data)
        return render_template('template_1.html', path = path)

    return render_template('template_1.html', path = path)


@app.route('/template_2', methods=['GET','POST'])
def template_2():
    imgpath = 'static/newimage.jpg'
    vc.freeze_image_detection(imgpath)
    return render_template('template_2.html', imgpath = imgpath)



@app.route('/template_3', methods=['GET','POST'])
def template_3():

    return render_template('template_3.html')

@socketio.on('connect')
def handlemessage():
        global thread
        thread = None
        with thread_lock:
            if thread is None:
                thread = socketio.start_background_task(background_thread)

#background threat starts on websocket connect.
def background_thread():
    imgpath = 'static'
    global connect
    connect = True
    cap = cv2.VideoCapture(1)
    count = 1

    while connect:
        success, frame = cap.read()
        prevdiff = 0;
        img = uuid.uuid4().int
        path = imgpath+os.sep+str(img)+'.jpg'
        while connect:
            prev = frame.copy()
            success, frame = cap.read()
            diff = np.sum(np.abs(prev-frame))
            print(success,count,np.sum(np.abs(prev-frame)))
            if (vc.still_frozen(prevdiff, diff)==False):
                if (diff == 0):
                    cv2.imwrite(path, frame)
                    count+=1
                    break
                    #return path
                prevdiff = diff
            time.sleep(0.25) #half of nyquist limit

        #path = vc.freeze_image_detection(imgpath)
        if connect:

            print('sending works!!!')
            socketio.emit('nextimg',{'value':path})
            socketio.sleep(0.5)
            print('blah')
            shutil.move(path,'static\processed' )
    cap.release()

@socketio.on('disconnect')
def disconnect():
    global connect
    connect = False


@app.route('/video_feed')
def video_feed():
    return Response(vc.capture_Frames(), mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == "__main__":
    app.run(debug =True, host ='0.0.0.0' )
