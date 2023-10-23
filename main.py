import time
import os
import sys
from os.path import exists
import shutil
import threading
from binascii import a2b_base64
import base64
#from array import *
#from statistics import mean
from PIL import Image
from threading import Lock
import cv2
import numpy as np
import video_capture as vc
import convenientfunctions as cnv
#import keycloak_and_db_test as kdbt
import image_save as save
from flask import Flask,flash,render_template,Response, request,redirect, send_from_directory, jsonify, session, url_for, g
from flask_socketio import SocketIO
#from flask_oidc import OpenIDConnect
#from keycloak import KeycloakOpenID
#from functools import wraps
#import jwt
#from cryptography.x509 import load_pem_x509_certificate
#from cryptography.hazmat.backends import default_backend
'''
def keycloak_protected(route_function):
    @wraps(route_function)
    def decorated(*args, **kwargs):
        # Get the access token from the session
        access_token = session.get("access_token")

        # Validate the access token with Keycloak
        if not access_token or not keycloak_openid.userinfo(access_token):
            return redirect(url_for("login"))

        # The user is authenticated, call the original route function
        return route_function(*args, **kwargs)

    return decorated
'''

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')
myp = os.path.realpath(os.path.dirname(__file__))
os.chdir('C:/Users/ami/OneDrive/Skrivebord/EngineeringProject/Flexible_Systeminterface')
'''
app.config.update({
    'SECRET_KEY': '4f0b081429d9f4f4ea7c2ab01318e6e41a9e6a84a2fbccaf01e2c41894765ee2',
    'TESTING': True,
    'DEBUG': True,
    'OIDC_CLIENT_SECRETS': 'auth.json',
    'OIDC_ID_TOKEN_COOKIE_SECURE': False,
    'OIDC_REQUIRE_VERIFIED_EMAIL': False,
    'OIDC_USER_INFO_ENABLED': True,
    'OIDC_OPENID_REALM': 'Colo',
    'OIDC_SCOPES': ['openid','email','profile','roles'],
    'OIDC_TOKEN_TYPE_HINT': 'access_token',
    'OIDC_INTROSPECTION_AUTH_METHOD': 'client_sectret_post'

    })


oidc = OpenIDConnect(app)

keycloak_openid = KeycloakOpenID(
    server_url="http://localhost:8080",
    client_id="Flask_login_app",
    realm_name="Colo",
    client_secret_key="9Y7p8dlJ7aAYXcOsn9e83oMcJT4tPR9U",
)
def require_roles(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            info = oidc.user_getinfo(['sub',])
            user_id = info.get('sub')
            if user_id in oidc.credentials_store:
                try:
                    from oauth2client.client import OAuth2Credentials
                    access_token = OAuth2Credentials.from_json(oidc.credentials_store[user_id]).access_token
                    role = jwt.decode(access_token, options={"verify_signature": False}).get("resource_access", {}).get("Flask_login_app", {}).get("roles", [])[0]
                    print(role)
                except:
                    print('ohnonono')

            if not role in roles:
                flash("You are not authorized to view this page!", category='error')                
                return redirect(url_for('index'))  # Redirect to an 'unauthorized' route
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route("/login")
def login():

    # Get the authorization URL from Keycloak and redirect the user
    return redirect(keycloak_openid.get_authorization_url())
'''

@app.route('/', methods=['GET','POST'])
#@oidc.require_login
def index():
    #info = oidc.user_getinfo(['preferred_username','email','sub','account','group_membership','resource_access',])
    #access_token = oidc.get_access_token()
    #print(access_token)
    #kdbt.get_files_for_user()
    #print(d)
    #username = info.get('realm_access').get('roles')
    #print('this is the user info',info)
    #username = info.get('preferred_username')
    #email = info.get('email')
    #user_id = info.get('sub')
    #role = info.get('new_client_role')[0]
   # print('client role:',role)



    return render_template('index.html' )
@app.route('/logout', methods=['GET','POST'])
def logout():
    refreshtoken = None
    # Check if oidc_id_token exists before getting the refresh token
    if g.get('oidc_id_token'):
        refreshtoken = oidc.get_refresh_token()

    # Log out from OIDC
    oidc.logout()

    # If we got a refresh token, log out from Keycloak
    if refreshtoken:
        keycloak_openid.logout(refreshtoken)

    # Clear the oidc_id_token
    g.oidc_id_token = None

    return redirect(url_for('index'))


@app.route('/template_1', methods=['GET','POST'])
#@oidc.require_login
#@require_roles('admin')
#@oidc.require_keycloak_role('Flask_login_app',['newadmin','user'])
def template_1():
    path = ''

    buttonMode,freezeMode,backgroundMode = cnv.getConfig()
    fps, resolution,device_name,image_format = cnv.getImgCapCon()

    save.make_dirs(myp)
    return render_template('template_1.html', path = path, fps = fps)


@app.route('/template_2', methods=['GET','POST'])
#@oidc.require_login
#@require_roles('user')
#@oidc.require_keycloak_role('Flask_login_app',['newadmin'])
def template_2():
    cap = cv2.VideoCapture(1)
    global f
    f = vc.freezeDetection(socketio,cap)
    f.start()
    return render_template('template_2.html')

@app.route('/template_3', methods=['GET','POST'])
#@oidc.require_login
#@require_roles('user','admin')
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
        cap = cv2.VideoCapture(1)
        f = vc.freezeDetection(socketio,cap)
        f.start()
    global b
    if buttonMode and backgroundMode:

        b = vc.BCAnalysis()
        b.start()

    if buttonMode and not backgroundMode:
        global capture
        capture = cv2.VideoCapture(1)

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
        d.stop()
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
    buttonMode,freezeMode,backgroundMode = cnv.getConfig()

   
    ret,img = capture.read()
  
    img = cv2.resize(img,resolution)
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
'''
@app.route("/callback")
def callback():
    # Handle the callback from Keycloak and get the access token
    code = request.args.get("code")
    token = keycloak_openid.token(code)

    # Store the access token in the session for later use
    session["access_token"] = token["access_token"]

    # Redirect to a protected resource
    return redirect(url_for("index"))
'''
@app.route('/video_feed')
def video_feed():
    return Response(vc.capture_Frames(), mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == "__main__":

    app.run(debug=True,host='0.0.0.0',port=5000)
