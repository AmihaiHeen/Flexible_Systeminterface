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
import random
import string
from array import *
#from statistics import mean
from threading import Lock
import cv2
import numpy as np
import video_capture as vc
import convenientfunctions as cnv
import image_save as save



def modelOut(image):
    image = cv2.imread(image)
    labellist = ['label','conf','diff']
    resultlist = [random.randint(0,10),random.randint(0,10),random.randint(0,10)]
    # Center coordinates
    center_coordinates = (120*random.randint(1,5), 50*random.randint(1,5))
    # Radius of circle
    radius = 20*random.randint(1,5)
    # Blue color in BGR
    color = (255, 0, 0)
    # Line thickness of 2 px
    thickness = 2
    # Using cv2.circle() method
    # Draw a circle with blue line borders of thickness of 2 px
    image = cv2.circle(image, center_coordinates, radius, color, thickness)
    letters = string.ascii_lowercase
    describingtext = ''.join(random.choice(letters) for i in range(100))

    return labellist,describingtext,image,resultlist
