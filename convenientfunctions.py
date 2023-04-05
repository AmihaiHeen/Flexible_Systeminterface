import os
import sys
import toml


#Path to script
myp = os.path.realpath(os.path.dirname(__file__))


def getMetadata():
    '''
    This function reads all metadate from metadata.txt

    input: None
    output: Current in-use Paths
    '''

    firstline = ""
    with open(myp +os.sep+ "metadata.txt","r") as metaf:
        firstline = metaf.readlines()[0]



    stamp,dataPath,absfolder,bufferPath,bufferProcessed,capImgPath,clientProcessed,_ = firstline.split(";")
    return stamp,dataPath,absfolder,bufferPath,bufferProcessed,capImgPath,clientProcessed

def getConfig():
    config = toml.load('config.toml')
    buttonMode = config['image_capture']['image_capture_button']
    freezeMode = config['image_capture']['image_capture_freeze']
    backgroundMode = config['image_capture']['image_capture_background']
    fps = config['fps']['fps']

    return buttonMode, freezeMode, backgroundMode, fps

def getConfigInterface():
    config = toml.load('config.toml')
    images = config['interface']['images']
    results = config['interface']['results']
    planes = config['interface']['standardplanes']

    cap_img = images['captured_image_placement']
    an_img = images['analyzed_image_placement']
    res_plc = results['result_list_placement']
    desc_plc = results['description_placement']
    plane_plc = planes['standardplanes_placement']

    return cap_img,an_img,res_plc,desc_plc,plane_plc

def getConfigReturns():
    config = toml.load('config.toml')
    image_bool = config['returns']['image']['image_bool']
    if image_bool:
        image_index = config['returns']['image']['return_index']
    else:
        image_index = ""
    desc_bool = config['returns']['description']['description_bool']
    if desc_bool:
        desc_index = config['returns']['description']['return_index']
    else:
        desc_index = ""
    res_bool = config['returns']['results']['result_bool']
    if res_bool:
        res_amount = config['returns']['results']['return_amount']
        res_index = config['returns']['results']['result_index']
    else:
        res_amount = ""
        res_index = ""
    return image_bool,image_index,desc_bool,desc_index,res_bool,res_amount,res_index
