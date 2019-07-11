import argparse
import json
import matplotlib.pyplot as plt
import skimage.io as io
import cv2
import numpy as np
import glob
import PIL.Image
import os,sys
from lxml import etree, objectify

#--------------------------------------------------------------------------
# download files from https://www.cityscapes-dataset.com/downloads/
# - gtFine_trainvaltest.zip (241MB) [md5]
# - leftImg8bit_trainvaltest.zip (11GB) [md5]
#--------------------------------------------------------------------------

# Set folderers
jsonfolder = 'E:/datasets/cityscape/gtFine_trainvaltest/gtFine/'
imagesfolder = 'E:/datasets/cityscape/leftImg8bit_trainvaltest/leftImg8bit/'
outputBboxfolder = 'E:/datasets/cityscape/BBoxCarclass/'

# Set Labels to Include, if empty then all
include_labels = ["car", "bicycle", "person", "rider", "motorcycle", "bus", "truck", "train"]

# Set Labels to Exclude/Ignore
exclude_labels = ['out_of_roi']
exclude_labels.append('road')
exclude_labels.append('sidewalk')
exclude_labels.append('sky')
exclude_labels.append('building')
exclude_labels.append('vegetation')
exclude_labels.append('pole')
exclude_labels.append('traffic_sign')
exclude_labels.append('static')
exclude_labels.append('license_plate')
exclude_labels.append('ego_vehicle')
exclude_labels.append('terrain')
exclude_labels.append('ground')
exclude_labels.append('traffic_light')
exclude_labels.append('dynamic')
exclude_labels.append('wall')
exclude_labels.append('cargroup')
exclude_labels.append('fence')
exclude_labels.append('bicyclegroup')
exclude_labels.append('parking')
exclude_labels.append('persongroup')
exclude_labels.append('bridge')
exclude_labels.append('trailer')
exclude_labels.append('polegroup')
exclude_labels.append('tunnel')
exclude_labels.append('caravan')
exclude_labels.append('guard_rail')
exclude_labels.append('rectification_border')
exclude_labels.append('rail_track')
exclude_labels.append('motorcyclegroup')
exclude_labels.append('ridergroup')
exclude_labels.append('truckgroup')
#exclude_labels.append('')

#------------------------------------------------------------------------------------------------------------
categories = []

jsonFiles = glob.glob('{}**/**/*.json'.format(jsonfolder))

#------------------------------------------------------------------------------------------------------------
for fileName in jsonFiles:

    fileName = fileName.replace('\\','/')
    jsonFileName = fileName.split('/')[-1:][0]
    imageFileName = jsonFileName.replace('_gtFine_polygons.json','_leftImg8bit.png')
    image_path =  fileName.replace(jsonfolder,imagesfolder).replace(jsonFileName,'')
    
    xmlFileName = fileName.replace(jsonfolder,outputBboxfolder).replace(jsonFileName,imageFileName.replace('.png','.xml'))

    with open(fileName,'r') as fp:
        data = json.load(fp)

        E = objectify.ElementMaker(annotate=False)
        annotation = E.annotation(
            E.folder(image_path),
            E.filename(imageFileName),
            E.source(
                E.database('Cityscape'),
                E.annotation('Cityscape'),
                E.image('Cityscape'),
                ),
            E.size(
                E.width(data['imgWidth']),
                E.height(data['imgHeight']),
                E.depth('3'),
                ),
            )
        
        for obj_json in data['objects']:
            label = obj_json['label'].replace(' ','_')
            if label in exclude_labels:
                continue

            if len(include_labels)>0 and label not in include_labels:
                continue

            if label not in categories:
                categories.append(label)

            points=obj_json['polygon']
            Xs = list(np.asarray( obj_json['polygon']).flatten())[::2]  #pega todos os X
            Ys = list(np.asarray( obj_json['polygon']).flatten())[1::2]  #pega todos os Y
            
            E = objectify.ElementMaker(annotate=False)
            annotation.append(E.object(
                                E.name(label),
                                E.bndbox(
                                    E.xmin(np.min(Xs)),
                                    E.ymin(np.min(Ys)),
                                    E.xmax(np.max(Xs)),
                                    E.ymax(np.max(Ys)),
                                ),
            ))

        
        if not os.path.exists(os.path.dirname(xmlFileName)):
            os.makedirs(os.path.dirname(xmlFileName))
        etree.ElementTree(annotation).write(xmlFileName)
    



print('=========== Categorias ===============')
for lbl in categories:
    print(lbl)




#------------------------------------------------------------------
def root(folder, filename, width, height):
    E = objectify.ElementMaker(annotate=False)
    return E.annotation(
            E.folder(folder),
            E.filename(filename),
            E.source(
                E.database('Cityscape'),
                E.annotation('Cityscape'),
                E.image('Cityscape'),
                ),
            E.size(
                E.width(width),
                E.height(height),
                E.depth('3'),
                ),
            )