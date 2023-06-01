import os
import sys
import toml
import importlib.util

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

    return buttonMode, freezeMode, backgroundMode

def getImgCapCon():
    config = toml.load('config.toml')

    fps = config['capture_settings']['background_capture_fps']
    resolution = config['capture_settings']['resolution']
    device_name = config['capture_settings']['device_name']
    image_format = config['capture_settings']['image_format']

    return fps,resolution,device_name,image_format

def getConfigInterface():
    config = toml.load('config.toml')
    interface = config['interface']
    #results = config['interface']['results']
    #planes = config['interface']['standardplanes']
    cap_img = interface['captured_image_placement']
    an_img = interface['analyzed_image_placement']
    res_plc = interface['result_list_placement']
    desc_plc = interface['description_placement']
    plane_plc = interface['standardplanes_placement']
    button_plc = interface['button_placement']


    return cap_img,an_img,res_plc,desc_plc,plane_plc,button_plc

def getConfigReturns():
    config = toml.load('config.toml')
    image_bool = config['output']['booleans']['image_bool']
    desc_bool = config['output']['booleans']['description_bool']
    res_bool = config['output']['booleans']['result_bool']
    lab_bool = config['output']['booleans']['labels_bool']

    return image_bool,desc_bool,res_bool,lab_bool

def get_function():
    config = toml.load('config.toml')
    module_name = config['model']['module']
    funtion_name = config['model']['function']
    module_spec = importlib.util.spec_from_file_location(module_name,module_name+'.py')
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    #module = importlib.import_module(module_name)
    function = getattr(module,funtion_name)
    print('getting model')

    return function

def getOutputIndecies():
    config = toml.load('config.toml')
    img_index = config['output']['indecies']['image_index']
    labels_index = config['output']['indecies']['labels_index']
    result_index = config['output']['indecies']['result_index']
    desc_index = config['output']['indecies']['description_index']

    return img_index,labels_index,result_index,desc_index
