import time
import os
import sys
from os.path import exists
import shutil
import threading
from binascii import a2b_base64
import base64
from array import *
#from statistics import mean
from PIL import Image
from threading import Lock
import cv2
import numpy as np
import video_capture as vc
import convenientfunctions as cnv
import image_save as save
from flask import Flask, render_template,Response, request,redirect, send_from_directory, jsonify
from flask_socketio import SocketIO

app = Flask(__name__)

socketio = SocketIO(app, cors_allowed_origins='*')
myp = os.path.realpath(os.path.dirname(__file__))


@app.route('/', methods=['GET','POST'])
def index():


    return render_template('index.html')

@app.route('/template_1', methods=['GET','POST'])
def template_1():
    path = ''

    buttonMode,freezeMode,backgroundMode = cnv.getConfig()
    fps, resolution,device_name,image_format = cnv.getImgCapCon()

    save.make_dirs(myp)
    return render_template('template_1.html', path = path, fps = fps)


@app.route('/template_2', methods=['GET','POST'])
def template_2():
    cap = cv2.VideoCapture(1)
    global f
    f = vc.freezeDetection(socketio,cap)
    f.start()
    return render_template('template_2.html')

@app.route('/template_3', methods=['GET','POST'])
def template_3():

    buttonMode,freezeMode,backgroundMode = cnv.getConfig()
    fps, resolution, device_name,image_format = cnv.getImgCapCon()

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
    fps, resolution,device_name,image_format = cnv.getImgCapCon()
    img_index,lab_index,res_index,desc_index = cnv.getOutputIndecies()
    cap_img,an_img,res_plc,desc_plc,plane_plc,btn_plc = cnv.getConfigInterface()
    image_bool,desc_bool,res_bool,lab_bool = cnv.getConfigReturns()
    save.make_dirs(myp)
    cap = cv2.VideoCapture(1)

    print(res_index)
    if backgroundMode:
        global b
            #b = vc.BackgroundCapture(fps,cap,que)
        b = vc.BCAnalysis()
        b.start()
    if freezeMode:
        global f
        f = vc.freezeDetection(socketio,cap)
        f.start()



    return render_template('template_4.html', btnMode=buttonMode, fMode=freezeMode,img_bool = image_bool,desc_bool = desc_bool,res_bool = res_bool, res_index = res_index,img_plc = cap_img,an_plc=an_img,res_plc=res_plc,desc_plc=desc_plc,plane_plc=plane_plc)

@app.route('/template_5', methods=['GET', 'POST'])
def template_5():
    save.make_dirs(myp) #creates necesarry libraries
    buttonMode,freezeMode,backgroundMode = cnv.getConfig()
    fps, resolution, device_name, image_format = cnv.getImgCapCon()
    image_bool,desc_bool,res_bool,lab_bool = cnv.getConfigReturns()
    cap_img,an_img,res_plc,desc_plc,plane_plc,btn_plc = cnv.getConfigInterface()
    img_index,lab_index,res_index,desc_index = cnv.getOutputIndecies()
    global f
    if freezeMode and backgroundMode:
        f = vc.ffmpeg_freezeDetection(socketio)
        f.start()
    if freezeMode and not backgroundMode:
        cap = cv2.VideoCapture(0)
        f = vc.freezeDetection(socketio,cap)
        f.start()
    global b
    if buttonMode and backgroundMode:
        b = vc.BCAnalysis()
        b.start()
    if buttonMode and not backgroundMode:
        global capture
        capture = cv2.VideoCapture(0)

    global clickCount
    clickCount = 0
    return render_template('template_5.html',btnMode=buttonMode, fMode=freezeMode,backgroundMode = backgroundMode,img_bool = image_bool,img_index = img_index,desc_bool = desc_bool,desc_index = desc_index,res_bool = res_bool,lab_bool= lab_bool,lab_index = lab_index, res_index = res_index,img_plc = cap_img,an_plc=an_img,res_plc=res_plc,desc_plc=desc_plc,plane_plc=plane_plc,btn_plc = btn_plc)

@app.route('/buffer_page', methods=['GET','POST'])
def buffer_page():
    stamp,dataPath,absfolder,bufferPath,bufferProcessed,capImgPath,clientProcessed = cnv.getMetadata()
    buffer = os.listdir(bufferProcessed)
    bufferlist=[]
    for i in buffer:
        bufferlist.append(bufferProcessed+os.sep+i)
    return render_template('buffer_page.html', bufferlist = bufferlist)



@socketio.on('disconnect')
def disconnect():
    #connect = False
    #vc.freeze_with_socket(socketio,connect)
    buttonMode,freezeMode,backgroundMode = cnv.getConfig()
    if(freezeMode):
        f.stop()
        f.join()
    global b
    if(buttonMode and backgroundMode):
        b.stop()
    #    b.join()
    global capture
    if buttonMode and not backgroundMode:
        capture.release()
@socketio.on('stop')
def stop():
    f.stop()
    f.join()

@socketio.on('Capimg')
def btnCap():
    stamp,dataPath,absfolder,bufferPath,bufferProcessed,capImgPath,clientProcessed = cnv.getMetadata()
    fps, resolution,device_name,image_format = cnv.getImgCapCon()
    global clickCount
    clickCount +=1
    imgList = os.listdir(bufferPath)
    length = len(imgList)-1
    emit_path = f'{bufferPath}/frame-'+str(len(imgList)-1)+'.'+image_format
    img = cv2.imread(emit_path)
    retval, buffer = cv2.imencode('.jpg', img)
    jpg_as_text = base64.b64encode(buffer).decode()
    print('click number',clickCount)
    socketio.emit('nextimg',{'value':jpg_as_text})
    frame = cv2.imread(bufferPath+os.sep+imgList[length])
    count=1
    save_path = capImgPath+os.sep+str(count)+'.'+image_format
    while os.path.exists(save_path):
        count+=1
        save_path = capImgPath+os.sep+str(count)+'.'+image_format
    cv2.imwrite(save_path,frame)
    resList = vc.singleprocess(frame,clientProcessed,count,emit_path)
    socketio.emit('output',{'res':resList[:]})


@socketio.on('clientImage')
def clientImg(clientImage):
    stamp,dataPath,absfolder,bufferPath,bufferProcessed,capImgPath,clientProcessed = cnv.getMetadata()
    pa =save.save_from_dataUrl(clientImage,capImgPath)

@socketio.on('capImage')
def capImg():
    stamp,dataPath,absfolder,bufferPath,bufferProcessed,capImgPath,clientProcessed = cnv.getMetadata()
    fps, resolution, device_name, image_format = cnv.getImgCapCon()

    #cap = cv2.VideoCapture(0)
    ret,img = capture.read()
    count=1
    save_path = capImgPath+os.sep+str(count)+'.'+image_format
    while os.path.exists(save_path):
        count+=1
        save_path = capImgPath+os.sep+str(count)+'.'+image_format
    cv2.imwrite(save_path,img)
    retval, buffer = cv2.imencode('.jpg', img)
    jpg_as_text = base64.b64encode(buffer).decode()
    socketio.emit('nextimg',{'value':jpg_as_text})
    resList = vc.singleprocess(img,clientProcessed,count,save_path)
    socketio.emit('output',{'res':resList[:]})


@socketio.on('buffer_image')
def recieve_image(buffer_image):
    stamp,dataPath,absfolder,bufferPath,bufferProcessed,capImgPath,clientProcessed = cnv.getMetadata()
    save.save_from_dataUrl(buffer_image,bufferPath)

    #cv2.imwrite('/tryimage.jpg',image)

@app.route('/video_feed')
def video_feed():
    return Response(vc.capture_Frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":

    app.run(debug=False,host='0.0.0.0',port=5000)
