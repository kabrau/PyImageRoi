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

def cityscapeMask2Pascal(databaseName, extractedFolderAnn, outputFolderAnn, imagesFolder):

    print("extractedFolderAnn", extractedFolderAnn)
    print("outputFolderAnn", outputFolderAnn)
    print("imagesFolder", imagesFolder)

    imageSufix = ""
    if os.path.isfile(os.path.join(imagesFolder,"aachen_000000_000019_leftImg8bit.png")) or os.path.isfile(os.path.join(imagesFolder,"frankfurt_000000_000294_leftImg8bit.png")):
       imageSufix = '_leftImg8bit.png'
    elif os.path.isfile( os.path.join(imagesFolder,"aachen_000000_000019_leftImg8bit_foggy_beta_0.02.png")) or os.path.isfile( os.path.join(imagesFolder,"frankfurt_000000_000294_leftImg8bit_foggy_beta_0.02.png")):
       imageSufix = '_leftImg8bit_foggy_beta_0.02.png'
    elif os.path.isfile( os.path.join(imagesFolder,"aachen_000000_000019_leftImg8bit_foggy_beta_0.01.png")) or os.path.isfile( os.path.join(imagesFolder,"frankfurt_000000_000294_leftImg8bit_foggy_beta_0.01.png")):
       imageSufix = '_leftImg8bit_foggy_beta_0.01.png'
    elif os.path.isfile( os.path.join(imagesFolder,"aachen_000000_000019_leftImg8bit_foggy_beta_0.005.png")) or os.path.isfile( os.path.join(imagesFolder,"frankfurt_000000_000294_leftImg8bit_foggy_beta_0.005.png")):
       imageSufix = '_leftImg8bit_foggy_beta_0.005.png'

    if imageSufix=="":
        print()
        print("=== Atention ===")
        print("Do not exist files in {}, or add new sufixe".format(imagesFolder) )
        sys.exit()           

    #--------------------------------------------------------------------------
    # download files from https://www.cityscapes-dataset.com/downloads/
    # - gtFine_trainvaltest.zip (241MB) [md5]
    # - leftImg8bit_trainvaltest.zip (11GB) [md5]
    #--------------------------------------------------------------------------

    # Set Labels to Include, if empty then all
    include_labels = ["car", "bicycle", "person", "rider", "motorcycle", "bus", "truck", "train"]

    #------------------------------------------------------------------------------------------------------------
    categories = []

    jsonFiles = glob.glob('{}**/**/*.json'.format(extractedFolderAnn))

    #------------------------------------------------------------------------------------------------------------
    for fileName in jsonFiles:

        fileName = fileName.replace('\\','/')
        jsonFileName = fileName.split('/')[-1:][0]
        imageFileName = jsonFileName.replace('_gtFine_polygons.json',imageSufix)
        xmlFileName = os.path.join(outputFolderAnn, imageFileName.replace('.png','.xml')) 

        with open(fileName,'r') as fp:
            data = json.load(fp)

            E = objectify.ElementMaker(annotate=False)
            annotation = E.annotation(
                E.folder(imagesFolder),
                E.filename(imageFileName),
                E.source(
                    E.database(databaseName),
                    E.annotation(jsonFileName),
                    E.image(imageFileName),
                    ),
                E.size(
                    E.width(data['imgWidth']),
                    E.height(data['imgHeight']),
                    E.depth('3'),
                    ),
                )
            
            for obj_json in data['objects']:
                label = obj_json['label'].replace(' ','_')

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
    print(set(categories))


