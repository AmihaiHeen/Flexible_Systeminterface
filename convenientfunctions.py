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

    fps = config['image_capture']['fps']
    resolution = config['image_capture']['resolution']
    device_name = config['image_capture']['device_name']
    return fps,resolution,device_name
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

    desc_bool = config['returns']['description']['description_bool']

    res_bool = config['returns']['results']['result_bool']

    lab_bool = config['returns']['labels']['labels_bool']

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
    img_index = config['returns']['output']['image_index']
    labels_index = config['returns']['output']['labels_index']
    result_index = config['returns']['output']['result_index']
    desc_index = config['returns']['output']['description_index']
    return img_index,labels_index,result_index,desc_index
