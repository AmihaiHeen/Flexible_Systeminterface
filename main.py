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
    cnv.getConfigReturns()
    print()
    return render_template('index.html')

@app.route('/template_1', methods=['GET','POST'])
def template_1():
    path = ''

    buttonMode,freezeMode,backgroundMode = cnv.getConfig()
    fps, resolution = cnv.getImgCapCon()

    save.make_dirs(myp)
    return render_template('template_1.html', path = path, fps = fps)


@app.route('/template_2', methods=['GET','POST'])
def template_2():
    cap = cv2.VideoCapture(0)
    global f
    f = vc.freezeDetection(socketio,cap)
    f.start()
    return render_template('template_2.html')

@app.route('/template_3', methods=['GET','POST'])
def template_3():

    buttonMode,freezeMode,backgroundMode = cnv.getConfig()
    fps, resolution = cnv.getImgCapCon()

    '''
    save.make_dirs(myp)
    cap = cv2.VideoCapture(0)

    global f
    f = vc.freezeDetection(socketio,cap)
    global b
    b = vc.BackgroundCapture(fps,cap,que)
    f.start()
    b.start()
    '''
    return render_template('template_3.html',fps=fps)


@app.route('/template_4', methods=['GET', 'POST'])
def template_4():
    buttonMode,freezeMode,backgroundMode = cnv.getConfig()
    fps, resolution = cnv.getImgCapCon()
    save.make_dirs(myp)
    cap = cv2.VideoCapture(1)
    image_bool,image_index,desc_bool,desc_index,res_bool,res_amount,res_index= cnv.getConfigReturns()
    cap_img,an_img,res_plc,desc_plc,plane_plc = cnv.getConfigInterface()
    print(res_index)
    if freezeMode:
        global f
        f = vc.freezeDetection(socketio,cap)
        f.start()

    if backgroundMode:
        global b
        #b = vc.BackgroundCapture(fps,cap,que)
        b = vc.BCAnalysis()
        b.start()

    return render_template('template_4.html', btnMode=buttonMode, fMode=freezeMode,img_bool = image_bool,desc_bool = desc_bool,res_bool = res_bool, res_index = res_index,img_plc = cap_img,an_plc=an_img,res_plc=res_plc,desc_plc=desc_plc,plane_plc=plane_plc)

@app.route('/template_5', methods=['GET', 'POST'])
def template_5():
    buttonMode,freezeMode,backgroundMode = cnv.getConfig()
    fps, resolution = cnv.getImgCapCon()
    save.make_dirs(myp)
    cap = cv2.VideoCapture(1)
    image_bool,image_index,desc_bool,desc_index,res_bool,res_amount,res_index= cnv.getConfigReturns()
    cap_img,an_img,res_plc,desc_plc,plane_plc = cnv.getConfigInterface()
    print(res_index)
    if freezeMode:
        global f
        f = vc.freezeDetection(socketio,cap)
        f.start()

    if backgroundMode:
        global b
        #b = vc.BackgroundCapture(fps,cap,que)
        b = vc.BCAnalysis()
        b.start()

    return render_template('template_5.html', btnMode=buttonMode, fMode=freezeMode,img_bool = image_bool,desc_bool = desc_bool,res_bool = res_bool, res_index = res_index,img_plc = cap_img,an_plc=an_img,res_plc=res_plc,desc_plc=desc_plc,plane_plc=plane_plc)

@app.route('/buffer_page', methods=['GET','POST'])
def buffer_page():
    stamp,dataPath,absfolder,bufferPath,bufferProcessed,capImgPath,clientProcessed = cnv.getMetadata()
    buffer = os.listdir(bufferProcessed)
    bufferlist=[]
    for i in buffer:
        bufferlist.append(bufferProcessed+os.sep+i)
    return render_template('buffer_page.html', bufferlist = bufferlist)


@socketio.on('freez')
def handlemessage():
        global thread
        thread = None
        with thread_lock:
            if thread is None:
                thread = socketio.start_background_task(vc.analyze_que,que)


@socketio.on('disconnect')
def disconnect():
    #connect = False
    #vc.freeze_with_socket(socketio,connect)
    buttonMode,freezeMode,backgroundMode = cnv.getConfig()

    if(freezeMode):
        f.stop()
        f.join()
    if(backgroundMode):
        b.stop()
        b.join()


@socketio.on('stop')
def stop():
    f.stop()
    f.join()
@socketio.on('clientImage')
def clientImg(clientImage):
    stamp,dataPath,absfolder,bufferPath,bufferProcessed,capImgPath,clientProcessed = cnv.getMetadata()
    pa =save.save_from_dataUrl(clientImage,capImgPath)

    #img = cv2.imread(pa)
    #fnc = cnv.get_function()
    #returnList = fnc(img)
    #print(returnList[0])
    #returnList = list(returnList)
    #print(type(returnList[0]))
    #retval, buffer = cv2.imencode('.jpg', returnList[0])
    #im_byte= buffer.tobytes()
    #jpg_as_text = base64.b64encode(im_byte).decode()
    #print(jpg_as_text)
    #returnList[0] = jpg_as_text

    #socketio.emit('output',{'res':returnList[:]})



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
