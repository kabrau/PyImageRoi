import argparse
import os
import glob
import pandas as pd
from libraryTools import imageRegionOfInterest
from lxml import etree, objectify

#filename,width,height,class,xmin,ymin,xmax,ymax
#20170730_132530-(F00000).jpeg,576,1024,sinaleira,221,396,246,437

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            print("Make dir {}".format(directory))
            os.makedirs(directory)
    except OSError:
        print()
        print("=== Atention ===")
        print ('Error: Creating directory. ' +  directory)
        sys.exit()

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

valid_images = [".jpg",".gif",".png",".tga",".jpeg"]

def run(image_path, ann_path, classNameList = ["someclass"], searchSubdir = False):

    global classes_qtd
    global images_total_qtd
    global images_without_classes_qtd
    global xml_list

    classes_qtd = []
    images_total_qtd = 0
    images_without_classes_qtd = 0
    xml_list = []

    searchFolder(image_path, ann_path, classNameList, searchSubdir)

    print('Successfully converted to xml PASCAL.')

    print('Total Images: ', images_total_qtd)
    print('Images without classes: ', images_without_classes_qtd)
    print('Classes: ')
    for q in classes_qtd:
        print( q)


def searchFolder(image_path, ann_path, classNameList, searchSubdir):

    global valid_images
    global classes_qtd
    global images_total_qtd
    global images_without_classes_qtd
    global xml_list

    print("Folder", image_path)

    obj = imageRegionOfInterest(image_path)
    for filename in os.listdir(image_path):
        if searchSubdir and os.path.isdir(os.path.join(image_path, filename)):
            searchFolder(os.path.join(image_path, filename), ann_path, classNameList, searchSubdir)

        name, ext = os.path.splitext(filename)
        if ext.lower() not in valid_images:
            continue

        images_total_qtd = images_total_qtd + 1

        xmlFileName = os.path.join(ann_path,name+".xml")

        obj.setFileImage(filename)
        obj.loadFromFile()            
        points = obj.loadBoxFromTxt()     

        #print(image_path, filename, int(obj.image.shape[1]), int(obj.image.shape[0]))

        annotation = root(image_path, filename, int(obj.image.shape[1]), int(obj.image.shape[0]))

        if len(points)>0:
            for point in points:
                annotation.append(instance_to_xml(point, classNameList))
                iclass = int(point[4]) 
                while len(classes_qtd) < iclass+1:
                    classes_qtd.append(0)

                classes_qtd[iclass] = classes_qtd[iclass] + 1
        else:
            images_without_classes_qtd = images_without_classes_qtd + 1


        #print(etree.tostring(annotation, pretty_print=True))
        print(xmlFileName)
        createFolder(os.path.dirname(xmlFileName))
        etree.ElementTree(annotation).write(xmlFileName)




    return 


#=============================================================================
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--path", required=True, help="images path")
ap.add_argument("-a", "--annpath", required=True, help="annotation path")
ap.add_argument('-className', nargs='*', help='class name list (0..9 positions, max 10), e.g. -classes dog cat')
ap.add_argument('-s', '--subdir', action='store_true', help="Search sub folders")

args = vars(ap.parse_args())

run(args["path"], args["annpath"], args["className"], args["subdir"])