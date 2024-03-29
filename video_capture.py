#necessary imports
import cv2
import os
import time
import numpy as np
import uuid
import shutil
import signal
import platform
import threading
import base64
import subprocess
import video_capture as vc
import convenientfunctions as cnv #imports con
import image_save as save #imports image_save.py
import imagehash
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
capture_mode = 1

#capture_Frames funciton to read frames from specified source
#used to send all image frames to the interface
def capture_Frames():
    '''
    This function capture an image stream from the specified camera, encode
    the images to jpg files, and converts them to bytes, then yield them to
    a format able to be read by the browser


    input: None
    output: byte frames
    '''
    camera = cv2.VideoCapture(0) #capture images from the specified camera
    while True: #while loop, runs while in template_1
        success, frame = camera.read()  # read the camera frame
        if not success: #if no image is read, breaks the while loop
            break
        else: #if there is an frame captured
            ret, buffer = cv2.imencode('.jpg', frame) #encodes the image to .jpg
            frame = buffer.tobytes() #converts the frame to bites
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') #yeld the image to a format able to be read by the browser

#first iteration of detection frozen images
def freeze_image_detection(imgpath): #takes argument that specifies the start of the image save path
    '''
    This function capture an image stream from the specified camera, checks if
    the image stream is frozen and saves the image to a specified path,
    then returns the path of which the image was saved.


    input: directory path
    output: image path
    '''
    cap = cv2.VideoCapture(capture_mode) #captures video stream
    count = 1 #counter that indicates which image is getting captured
    success, frame = cap.read() #reads the first frame
    prevdiff = 0 #setting previous difference for still frozen funtion
    img = uuid.uuid4().int #unique int for image save path
    path = imgpath+os.sep+str(img)+'.jpg' #specified path for image save
    while True: #while loop running until frozen image has been detected
        prev = frame.copy() #copies the first image read
        success, frame = cap.read() #reads next image
        diff = np.sum(np.abs(prev-frame)) #calculate difference between previous and new frame
        print(success,count,np.sum(np.abs(prev-frame))) #prints, if the image was captured, count, and difference
        if not still_frozen(prevdiff, diff): #checks if the image is still frozen
            if (diff == 0): #checks if difference is 0 and the image is frozen
                cv2.imwrite(path, frame) #saves the image to specified path
                count+=1 #updates counter
                return path #returns path
            prevdiff = diff #updates the difference when the image has stopped to be frozen
        time.sleep(0.25) #sleep timer at half of nyquist limit

    cap.release() #releases the VideoCapture

#first iteration of background capture of images
def background_capture(fps, bufferPath): #takes argument of frequency and path to directory of bufferimages
    '''
    This function capture an image stream from the specified camera at a specified frequency
    and saves them to a specific directory.


    input: frequency, directory path
    output: image
    '''
    cap = cv2.VideoCapture(capture_mode) #captures images from specified camera
    count = 1 #counter for image name
    success, frame = cap.read() #capture the first frame
    while success: #checks if image stream is active
        save_path = bufferPath+os.sep+str(count)+'.jpg' #path for image save
        success, frame = cap.read() #reads the frame
        cv2.imwrite(save_path, frame) #saves the image at specified path
        count+=1 #update counter
        time.sleep(1/int(fps)) #sleeptimer


            #path = vc.freeze_image_detection(imgpath)
#still_frozen checks if image is still frozen since last frozen image captured
def still_frozen(prevdiff, currdiff): #takes differences as argument
    '''
    This function checks if image is still frozen in the image stream.


    input: previous difference, current difference
    output: boolean (True or False)
    '''
    if (np.sum(np.abs(prevdiff-currdiff)==0)): #if their difference is equal to 0 the image is still frozen
        return True #returns True
    else: #if the image is frozen no more
        return False #return false and a new image can be captured

def singleprocess(frame,path,count,fullPath):
    img_index,lab_index,res_index,desc_index = cnv.getOutputIndecies()
    fps, resolution,device_name,image_format = cnv.getImgCapCon()

    fnc = cnv.get_function()
    
    resList = fnc(fullPath)

    #print('this is the resultlist index 0: ',resList[img_index])
    #cv2.imwrite(path+os.sep+'frame-'+str(count)+'.jpg',resList[0])
    #resList[img_index] = cv2.resize(resList[img_index],(640,480))
    #fig, ax = plt.subplots()
    plt.imshow(resList[img_index],cmap='gray')
    #plt.margins(x=0)
    #ax.imshow(resList[img_index])
    plt.axis('off')
    #plt.set_frame_on(False)
    output_file = path+os.sep+'frame-'+str(count)+'.'+image_format
    plt.savefig(output_file,format=image_format,bbox_inches='tight',pad_inches = 0)
    #cv2.imwrite(output_file,cv2.cvtColor(resList[img_index],cv2.COLOR_BGR2RGB))
    resList = list(resList)
    retval, buffer = cv2.imencode('.jpg', resList[img_index])
    #jpg_as_text = base64.b64encode(buffer).decode()
    with open(path+os.sep+'frame-'+str(count)+'.txt','a') as w:
        for i in resList[1:]:
            w.writelines("%s\n" % i)
    with open(output_file,'rb') as r:
        jpg_as_text = base64.b64encode(r.read()).decode()
    #retval, buffer = cv2.imencode('.jpg', resList[0])
    #im_byte= buffer.tobytes()
    #jpg_as_text = base64.b64encode(im_byte).decode()
    resList[img_index] = jpg_as_text
    return resList


#Function for "processing" the image
def process_image(frame,path):#takes a frame as an argument
    '''
    This function calculates the mean of a frames pixelvalues and return true or
    false depending on the mean


    input: image frame
    output: boolean (True or False)
    '''
    mean = int(frame.mean()) #calculate the mean of the image pixel values
    print("consumed frame") #prints
    print("The result is:")
    if mean > 115: #checks if the mean is above 115
        return True, mean, path
        cv2.imwrite(path,frame)

    else: #if the mean is below 115
        return False, mean, path

#python class extending threading.Thread() class
class freezeDetection(threading.Thread):
    #initialization of variables
    '''
    This class is extending threading.Thread and works as a background process.
    This class is used to check if an image stream is frozen, saves the
    frozen image to a directory and emits an image to an interface using a WebSocket.
    The __init__ function takes the input arguments and initializes them.
    The run() function reads from the image stream and checks if the image stream
    is frozen by looking at the current and previous image. The function also checks
    whether the image is still frozen or the image has changed to avoid duplicates.
    The function then saves the frozen images and saves them to at a specified path
    and emits the image to the interface. The funtion will continue to check for
    frozen images until _stop_event is set.
    The stop() function sets _stop_event and stops the while loop

    Input: socketio, VideoCapture
    Output: frozen image
    '''
    def __init__(self,socketio,cap):

        super().__init__()
        self._stop_event = threading.Event() #initialize thread.Event as flag to stop while loop in run()
        self.socketio = socketio #initialize WebSocket to send image to interface
        self.cap = cap #initialize the OpenCV VideoCapture() to read image stream
    #run() to start the threads functionallity. reading image stream and detect if the image is frozen
    def run(self):
        #getting the necesary paths needed for the to save the images
        stamp,dataPath,absfolder,bufferPath,bufferProcessed,capImgPath,clientProcessed = cnv.getMetadata()
        fps, resolution,device_name,image_format = cnv.getImgCapCon()

        count = 1 #initialize counter to make image save path
        success, frame = self.cap.read() #reads first the frame captured
        prevdiff = 0; #initialize previous difference for still_frozen function
        while not self._stop_event.is_set(): #while loop continuoing untill stopevent is set in stop() function
            prev = frame.copy() #sets previous frame captured
            success, frame = self.cap.read() #captures new frame

            diff = np.sum(np.abs(prev[50:-100,:-100]-frame[50:-100,:-100])) #calculate difference between previous and current frame
            #print(diff,prevdiff)
            #print(success,count,np.sum(np.abs(prev-frame))) # prints output
            if not (still_frozen(prevdiff, diff)): #checks if the image is still froxen
                if (diff == 0): # checks if the different is 0 and the image is frozen
                    path = capImgPath+os.sep+str(count)+'.'+image_format #initialize the path for image to be saved
                    cv2.imwrite(path, frame) #saves the frozen image to the specified path
                    retval, buffer = cv2.imencode('.jpg', frame)
                    jpg_as_text = base64.b64encode(buffer).decode()
                    #print('this is the captured frame',frame)
                    #print('sending works!!!') #print sending works
                    self.socketio.emit('nextimg',{'value':jpg_as_text}) #WebSocket emits the frame to the interface
                    #print('sending works!!!') #print sending works
                    #self.socketio.emit('nextimg',{'value':path}) 
                    proFrame = frame.copy()
                    print(proFrame.shape[:2])
                    resList = singleprocess(proFrame,clientProcessed,count,path)
                    self.socketio.emit('output',{'res':resList[:]})

                    #imgPro.join()
                    #print('this is the prev diff '+str(prevdiff))
                    #print('stopped')
                    count+=1 # count is updated
                    self.socketio.sleep(0.5) #socket sleep timer
                    #print('blah')
                            #return path
                prevdiff = diff #sets previous difference to new difference
            time.sleep(0.25) #half of nyquist limit
        self.cap.release() #release OpenCV VideoCapture
    #stop() function sets the threading event to set and stops the while loop
    def stop(self):
        self._stop_event.set() #set the threading event

#python class extending threading.Thread() class
#Captures images in the background at a specified frequency, saves the images and puts them into a que
class BackgroundCapture(threading.Thread):
    '''
    This class is extending threading.Thread and works as a background process.
    This class reads the images from a image stream, saves them and puts them
    into a que the for later process.

    The __init__ function takes the input arguments and initializes them.

    The run() function reads from the image stream saves the images at a
    specified path, and fill up a que with the framedata for later analysis
    The funtion will continue until _stop_event is set.

    The stop() function sets _stop_event and stops the while loop

    Input: frequency(fps), VideoCapture, Queue()
    Output: images, Queue()
    '''
    def __init__(self,fps,cap,que):
        super().__init__()
        self._stop_event = threading.Event() #initialize threading.Event as a flag to stop while loop in run()
        self.fps = int(fps) #initialize the frequency of which the function should capture the images
        self.que = que #initialize the que
        self.cap = cap #initialize the OpenCV VideoCapture to read image stream
    #run() start the threads funtionallity. reads images and saves the in a que and a specified folder
    def run(self):
        #getting the necesary paths needed for the to save the images
        stamp,dataPath,absfolder,bufferPath,bufferProcessed,capImgPath,clientProcessed = cnv.getMetadata()
        fps, resolution,device_name,image_format = cnv.getImgCapCon()

        count = 1 #initialize counter to make image save path
        sleeptime = 1/self.fps #initialize sleep timer
        while not self._stop_event.is_set(): #while loop running until _stop_event is set
            success, frame = self.cap.read() #reads the frame captured
            if success: #checks if frame was captured
                #process_image(frame)
                self.que.put(frame) #puts frame into que
                print("produced frame") #prints that a frame was "produced in the command prompt"
                path = bufferPath+os.sep+str(count)+'.'+image_format #specifies the image path to save image
                cv2.imwrite(path, frame) #saves the image at the specified path
                #result = process_image(self.que.get())
                #if result:
                #    print('High enought mean is above 115')
                #else:
                #    print('Not high enough, mean is below 115')
                count+=1 #updates the counter
            time.sleep(sleeptime) #sleep timer
        self.cap.release() #release the VideoCapture
    #stop function setting the _stop_event and thereby stopping the while loop
    def stop(self):
        self._stop_event.set() #sets _stop_event to set

class BCAnalysis(threading.Thread):
    def __init__(self):
        super().__init__()
    def run(self):
        stamp,dataPath,absfolder,bufferPath,bufferProcessed,capImgPath,clientProcessed = cnv.getMetadata()
        fps, resolution,device_name,image_format = cnv.getImgCapCon()
        input_stream = 'video="DVI2USB 3.0 D2S342374"'
        os_name = platform.system()
        #print('operation system: '+os_name)
        #command = [ffmpeg_path,'-i',input_stream,'-f','image2', f'{bufferPath}/frame-%d.jpg']
        newCommand = 'ffmpeg -f dshow -video_size '+str(resolution[0])+'x'+str(resolution[1])+' -i video="'+device_name+'" -r '+str(fps)+' -vf scale='+str(resolution[0])+':'+str(resolution[1])+' -f image2 '+bufferPath+'/frame-%d.'+image_format

        #print(command)
        global process

        if os_name == 'Windows':
            newCommand = 'ffmpeg -f dshow -i video="'+device_name+'" -r '+str(fps)+' -vf scale='+str(resolution[0])+':'+str(resolution[1])+' -f image2 '+bufferPath+'/frame-%d.'+image_format
            process = subprocess.Popen(newCommand,stdin=subprocess.PIPE, shell=True,creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
        if os_name == 'Linux':
            newCommand = 'ffmpeg -f v4l2 -video_size '+str(resolution[0])+'x'+str(resolution[1])+' -i '+device_name+' -video_size -r '+str(fps)+' -f image2 '+bufferPath+'/frame-%d.'+image_format
            process = subprocess.Popen(newCommand,stdin=subprocess.PIPE, shell=True,preexec_fn=os.setsid)

        #framecount = 1
        #time.sleep(2)

        #while True:

        #    filename = f'{bufferPath}/frame-{framecount}.ima'
        #    if not os.path.exists(filename):
        #        break
        #    frame = cv2.imread(filename)
        #    resList = singleprocess(frame,bufferProcessed,framecount)
            #print('list of results'+str(resList))
        #    framecount +=1
        #    time.sleep(1/fps)
    def stop(self):
        global process
        if platform.system() == 'Windows':
            process.send_signal(signal.CTRL_BREAK_EVENT)
        if platform.system() == 'Linux':
            os.killpg(os.getpgid(process.pid),signal.SIGTERM)
        process.kill()
class background_image_analysis(threading.Thread):
    def __init__(self):
        super().__init__()
        self._stop_event = threading.Event()
    def run(self):
        stamp,dataPath,absfolder,bufferPath,bufferProcessed,capImgPath,clientProcessed = cnv.getMetadata()
        fps, resolution,device_name,image_format = cnv.getImgCapCon()
        count = 1
        buffer_image_path = bufferPath+os.sep+'frame-'+str(count)+'.'+image_format

        while True:
            print('hi')
            
            frame = cv2.imread(buffer_image_path)
            copy_frame = frame.copy()
            reslist = singleprocess(copy_frame,bufferProcessed,count,buffer_image_path)
            count += 1    
            buffer_image_path = bufferPath+os.sep+'frame-'+str(count)+'.'+image_format
            time.sleep(1/fps)


    def stop(self):
        self._stop_event.set()            
class ffmpeg_freezeDetection(threading.Thread):
    def __init__(self, socketio):
        super().__init__()
        self.socketio = socketio
        self._stop_event = threading.Event()
        self.total_time = 0
    def run(self):
        stamp,dataPath,absfolder,bufferPath,bufferProcessed,capImgPath,clientProcessed = cnv.getMetadata()
        fps, resolution,device_name,image_format = cnv.getImgCapCon()

        os_name = platform.system()
        print('operation system: '+os_name)
        test_list= os.listdir('static/placeholder_images/test_jpg')
        global process

        if os_name == 'Windows':
            newCommand = 'ffmpeg -f dshow -i video="'+device_name+'" -r '+str(fps)+' -vf scale='+str(resolution[0])+':'+str(resolution[1])+' -f image2 '+bufferPath+'/frame-%d.'+image_format
            process = subprocess.Popen(newCommand,stdin=subprocess.PIPE, shell=True,creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
        if os_name == 'Linux':
            newCommand = 'ffmpeg -f v4l2 -video_size '+str(resolution[0])+'x'+str(resolution[1])+' -i '+device_name+' -r '+str(fps)+' -vf scale='+str(resolution[0])+':'+str(resolution[1])+' -f image2 '+bufferPath+'/frame-%d.'+image_format
            process = subprocess.Popen(newCommand,stdin=subprocess.PIPE, shell=True,preexec_fn=os.setsid)

        count = 1
        framecount = 1
        time.sleep(4)
        print('hello')
        filename = f'{bufferPath}/frame-{framecount}.'+image_format
        frame = cv2.imread(filename)
        errorframe = cv2.imread('static/placeholder_images/unsupported_frame.jpg')
        prevdiff = 0

        gray1 = cv2.cvtColor(errorframe, cv2.COLOR_BGR2GRAY)

        hash1 = imagehash.dhash(Image.fromarray(gray1))

        while not self._stop_event.is_set():
            #print('hi')
            dir = os.listdir(bufferPath)
            #print(len(dir))
            filename = dir[-1]
            framepath = f'{bufferPath}/frame-'+str(len(dir)-1)+'.'+image_format
            #print(framepath)
            prev = frame.copy()
            frame = cv2.imread(framepath)
            #print('still error image'+str(np.sum(np.abs(errorframe[50:,:]-frame[50:,:]))))
            gray2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            hash2 = imagehash.dhash(Image.fromarray(gray2))
            #print(hash1 - hash2)

            while (hash1 - hash2) == 0:
                print('still error image '+str(np.sum(np.abs(errorframe[50:,:]-frame[50:,:]))))
                dir = os.listdir(bufferPath)
                filename = dir[-1]
                framepath = f'{bufferPath}/frame-'+str(len(dir)-1)+'.jpg'
                frame = cv2.imread(framepath)
                gray2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                hash2 = imagehash.dhash(Image.fromarray(gray2))


            diff = np.sum(np.abs(prev[50:-100,0:-100]-frame[50:-100,0:-100])) #calculate difference between previous and current frame
            #diff = hash3-hash2
            #print('the difference is ',diff)
            #print(success,count,np.sum(np.abs(prev-frame))) # prints output
            if not (still_frozen(prevdiff, diff)): #checks if the image is still froxen
                if (diff == 0): # checks if the different is 0 and the image is frozen
                    start_time = time.time()
                    path = capImgPath+os.sep+str(count)+'.'+image_format #initialize the path for image to be saved
                    cv2.imwrite(path, frame) #saves the frozen image to the specified path
                    retval, buffer = cv2.imencode('.jpg', frame)
                    jpg_as_text = base64.b64encode(buffer).decode()
                    #print('this is the captured frame',frame)
                    #print('sending works!!!') #print sending works
                    self.socketio.emit('nextimg',{'value':jpg_as_text}) #WebSocket emits the frame to the interface
                    proFrame = frame.copy()
                    testPath = 'static/placeholder_images/test_jpg'+os.sep+test_list[count]
                    resList = singleprocess(proFrame,clientProcessed,count,path)
                    #for i in resList:
                        #print('type',type(i))
                    self.socketio.emit('output',{'res':resList[:]})
                    end_time = time.time()
                    self.total_time += end_time-start_time
                    #imgPro.join()
                    #print('this is the prev diff '+str(prevdiff))
                    #print('stopped')
                    count+=1 # count is updated
                    self.socketio.sleep(0.5) #socket sleep timer
                    #print('blah')
                            #return path
                prevdiff = diff #sets previous difference to new difference
            time.sleep(0.25) #half of nyquist limit
    def stop(self):
        self._stop_event.set()
        print('total_time = ',self.total_time)
        global process
        if platform.system() == 'Windows':
       		process.send_signal(signal.CTRL_BREAK_EVENT)
       	if platform.system() == 'Linux':
       		os.killpg(os.getpgid(process.pid),signal.SIGTERM)
        process.kill()

#background_threat reads from the que
def analyze_que(que):

    '''
    This function reads from the que every second and uses the process_image(Queue().get())
    to get a return value then prints the result, untill the queue is empty.

    input: Queue()
    output: print boolean (True or False)
    '''
    stamp,dataPath,absfolder,bufferPath,bufferProcessed,capImgPath,clientProcessed = cnv.getMetadata()
    fps = cnv.getConfig()
    blah = []
    count = 1
    while que.empty():
        print('waiting for que to start')
        time.sleep(0.5)
        que = que
    while True:
        if not que.empty(): #checks if the que is not empty
            path = bufferProcessed+os.sep+str(count)+'.jpg'
            blah.append(list(process_image(que.get(),path))) #prints the result of the process_image function
            print(blah[-1])
            count+=1
            time.sleep(1) #sleep timer

        else: #if the que is empty, the while loop breaks
            break
    print(blah)
    print("finished que") #prints in the command prompt when the que is empty
