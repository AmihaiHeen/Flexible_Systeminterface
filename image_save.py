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

def make_dirs(myp):
    '''
    This function create the directories that the different data is getting saved
    into.

    Input: project directory path
    output: matadata.txt

    '''
    timer = int(time.time())
    stamp = str(time.asctime( time.localtime(timer)))
    stamp = stamp.replace(' ', '_').replace(':','_')

    dataPath = 'static'+os.sep+'Data'+os.sep+stamp
    absfolder = myp+dataPath
    bufferPath = dataPath+os.sep+'buffer'
    bufferProcessed = dataPath+os.sep+'Processed_buffer'
    capImgPath = dataPath+os.sep+'Client_Image_Captured'
    clientProcessed = dataPath+os.sep+'Client_Image_Processed'
    os.mkdir(dataPath)
    os.mkdir(bufferPath)
    os.mkdir(bufferProcessed)
    os.mkdir(capImgPath)
    os.mkdir(clientProcessed)
    with open(myp +os.sep+ "metadata.txt","w") as metaf:
        metaf.write("%s;%s;%s;%s;%s;%s;%s;\n" % (stamp,dataPath,absfolder,bufferPath,bufferProcessed,capImgPath,clientProcessed))



def save_from_dataUrl(data,path):
    '''
    This functions saves an image based on the dataUrl emitted from the interface
    by converting it to base64 binary data and use the file writer.

    Input: dataUrl, directory path
    output: Image to specified directory

    '''
    data = data.split(',')[1]
    print('client image captured')
    count = 0
    currImg = path+os.sep+str(count)+'.jpg'
    binary_data = a2b_base64(data)
    while os.path.exists(currImg):
        count+=1
        currImg = path+os.sep+str(count)+'.jpg'
    with open(currImg, 'w+b') as fd:
        fd.write(binary_data)
