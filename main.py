import os
import sys
from os.path import exists
import time
import json
import uuid
import shutil
import threading
from binascii import a2b_base64
import base64
from multiprocess import Process, Queue, Lock
from array import *
#from statistics import mean
from threading import Lock
import cv2
import numpy as np
import video_capture as vc
import convenientfunctions as cnv
import image_save as save
from flask import Flask, render_template,Response, request,redirect, send_from_directory, jsonify
from flask_socketio import SocketIO

app = Flask(__name__)
thread_lock = Lock()
socketio = SocketIO(app, cors_allowed_origins='*')
myp = os.path.realpath(os.path.dirname(__file__))
que = Queue()


@app.route('/', methods=['GET','POST'])
def beginning():
    #freezeThread = threading.Thread(target=vc.freeze_image_detection)
    #freezeThread.start()
    return render_template('index.html')

@app.route('/template_1', methods=['GET','POST'])
def template_1():
    path = ''

    fps = cnv.getConfig()
    save.make_dirs(myp)
    return render_template('template_1.html', path = path, fps = fps)


@app.route('/template_2', methods=['GET','POST'])
def template_2():
    imgpath = 'static/newimage.jpg'
    vc.freeze_image_detection(imgpath)
    return render_template('template_2.html', imgpath = imgpath)

@app.route('/template_3', methods=['GET','POST'])
def template_3():
    fps = cnv.getConfig()
    save.make_dirs(myp)
    cap = cv2.VideoCapture(1)

    global f
    f = vc.frozenThread(socketio,cap)
    global b
    b = vc.BackgroundCapture(fps,cap,que)
    f.start()
    b.start()
    return render_template('template_3.html',fps=fps)

@socketio.on('freeze')
def handlemessage():
        global thread
        thread = None
        with thread_lock:
            if thread is None:
                thread = socketio.start_background_task(vc.background_thread,que)


@socketio.on('disconnect')
def disconnect():
    #connect = False
    #vc.freeze_with_socket(socketio,connect)
    f.stop()
    b.stop()
    b.join()

    f.join()


@socketio.on('clientImage')
def clientImg(clientImage):
    stamp,dataPath,absfolder,bufferPath,bufferProcessed,capImgPath,clientProcessed = cnv.getMetadata()
    save.save_from_dataUrl(clientImage,capImgPath)

@socketio.on('buffer_image')
def recieve_image(buffer_image):
    stamp,dataPath,absfolder,bufferPath,bufferProcessed,capImgPath,clientProcessed = cnv.getMetadata()
    save.save_from_dataUrl(buffer_image,bufferPath)

    #cv2.imwrite('/tryimage.jpg',image)

@app.route('/video_feed')
def video_feed():
    return Response(vc.capture_Frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":

    app.run(debug =True, host ='0.0.0.0' )
