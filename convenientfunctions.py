import os
import sys


#Path to script
myp = os.path.realpath(os.path.dirname(__file__))


def getMetadata():
    firstline = ""
    with open(myp +os.sep+ "metadata.txt","r") as metaf:
        firstline = metaf.readlines()[0]



    stamp,dataPath,absfolder,bufferPath,bufferProcessed,capImgPath,clientProcessed,_ = firstline.split(";")
    return stamp,dataPath,absfolder,bufferPath,bufferProcessed,capImgPath,clientProcessed

def getConfig():
    with open('config.txt', 'r') as con:
        data = con.readlines()[0]

    fps,_ = data.split(';')
    return fps
