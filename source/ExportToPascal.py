import argparse
import os
import glob
import pandas as pd
from libraryTools import imageRegionOfInterest
from lxml import etree, objectify

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

def run(image_path, ann_path, classNameList = ["someclass"]):

    obj = imageRegionOfInterest(image_path)
    valid_images = [".jpg",".gif",".png",".tga",".jpeg"]

    #print(image_path)

    xml_list = []
    for filename in os.listdir(image_path):
        name, ext = os.path.splitext(filename)
        if ext.lower() not in valid_images:
            continue

        xmlFileName = os.path.join(ann_path,name+".xml")

        obj.setFileImage(filename)
        obj.loadFromFile()            
        points = obj.loadBoxFromTxt()     

        #print(image_path, filename, int(obj.image.shape[1]), int(obj.image.shape[0]))

        annotation = root(image_path, filename, int(obj.image.shape[1]), int(obj.image.shape[0]))

        if len(points)>0:
            for point in points:
                annotation.append(instance_to_xml(point, classNameList))


        #print(etree.tostring(annotation, pretty_print=True))
        print(xmlFileName)
        etree.ElementTree(annotation).write(xmlFileName)

    print('Successfully converted to xml PASCAL.')
    return 


#=============================================================================
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--path", required=True, help="images path")
ap.add_argument("-a", "--annpath", required=True, help="annotation path")
ap.add_argument('-className', nargs='*', help='class name list (0..9 positions, max 10), e.g. -classes dog cat')

args = vars(ap.parse_args())

run(args["path"], args["annpath"], args["className"])