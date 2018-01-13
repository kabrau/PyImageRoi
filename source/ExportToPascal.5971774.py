import argparse
from argparse import RawTextHelpFormatter
import os
import glob
import cv2
import pandas as pd
from libraryTools import imageRegionOfInterest
from lxml import etree, objectify
import csv

#filename,width,height,class,xmin,ymin,xmax,ymax
#20170730_132530-(F00000).jpeg,576,1024,sinaleira,221,396,246,437

def root(folder, filename, width, height):
    E = objectify.ElementMaker(annotate=False)
    return E.annotation(
            E.folder(folder),
            E.filename(filename),
            E.source(
                E.database('MS COCO 2014'),
                E.annotation('MS COCO 2014'),
                E.image('Flickr'),
                ),
            E.size(
                E.width(width),
                E.height(height),
                E.depth('3'),
                ),
            )

def instance_to_xml(point, classNameList):
    E = objectify.ElementMaker(annotate=False)

    className = classNameList[0]
    if (int(point[4])<=len(classNameList[0])):
        className = classNameList[int(point[4])]

    return E.object(
            E.name(className),
            E.bndbox(
                E.xmin(point[0]),
                E.ymin(point[1]),
                E.xmax(point[2]),
                E.ymax(point[3]),
                ),
            )

def run(image_path, gt_file, ann_path):

    classNameList = ["go","stop"]

    files = []
    with open(gt_file) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=' ')
        for row in readCSV:
            cols = []
            for col in row:
                cols.append( int(col) )
            files.append(cols)

    #obj = imageRegionOfInterest(image_path)
    valid_images = [".jpg",".gif",".png",".tga",".jpeg"]

    classes_qtd = []
    images_total_qtd = 0
    images_without_classes_qtd = 0

    xml_list = []
    for filename in os.listdir(image_path):
        name, ext = os.path.splitext(filename)
        if ext.lower() not in valid_images:
            continue
        
        images_total_qtd = images_total_qtd + 1

        #load image
        image = cv2.imread(os.path.join(image_path,filename))    
        annotation = root(image_path, filename, int(image.shape[1]), int(image.shape[0]))

        #found GT
        numberFile = int(name)
        points = []
        for index, item in enumerate(files):
            if item[0] == numberFile:
                points.append([item[2],item[1],item[4],item[3],0 if item[5]==2 else 1])

        if len(points)>0:
            for point in points:
                annotation.append(instance_to_xml(point, classNameList))
                iclass = int(point[4]) 
                while len(classes_qtd) < iclass+1:
                    classes_qtd.append(0)

                classes_qtd[iclass] = classes_qtd[iclass] + 1
        else:
            images_without_classes_qtd = images_without_classes_qtd + 1

        #create xml
        xmlFileName = os.path.join(ann_path,name+".xml")
        print(xmlFileName)
        etree.ElementTree(annotation).write(xmlFileName)

    print('Successfully converted to xml PASCAL.')

    print('Total Images: ', images_total_qtd)
    print('Images without classes: ', images_without_classes_qtd)
    print('Classes: ')
    for q in classes_qtd:
        print( q)



    return 


#=============================================================================
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser(description="TOOL to Create a XML files (PASCAL FORMAT).\n"+
                              "Specific converter for PedestrianLights dataset available at:\n"+
                              "http://www.uni-muenster.de/PRIA/en/forschung/index.shtml", 
                              formatter_class=RawTextHelpFormatter)

ap.add_argument("-p", "--path", required=True, help="images path")
ap.add_argument("-o", "--gtfile", required=True, help="original ground truth file")
ap.add_argument("-a", "--annpath", required=True, help="annotation path")

args = vars(ap.parse_args())

run(args["path"], args["gtfile"], args["annpath"])
#print(args["path"], args["gtfile"], args["annpath"])