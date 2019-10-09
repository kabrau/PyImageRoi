import argparse
import os
import glob
import pandas as pd
from libraryTools import imageRegionOfInterest

#filename,width,height,class,xmin,ymin,xmax,ymax
#20170730_132530-(F00000).jpeg,576,1024,sinaleira,221,396,246,437

valid_images = [".jpg",".gif",".png",".tga",".jpeg"]

def run(image_path, classNameList = ["someclass"], searchSubdir = False):

    global classes_qtd
    global images_total_qtd
    global images_without_classes_qtd
    global xml_list

    classes_qtd = []
    images_total_qtd = 0
    images_without_classes_qtd = 0
    xml_list = []

    searchFolder(image_path, classNameList, searchSubdir)

    print()

    print('Total Images: ', images_total_qtd)
    print('Images without classes: ', images_without_classes_qtd)
    print('Classes: ')
    for q in classes_qtd:
        print( q)


def searchFolder(image_path, classNameList, searchSubdir):

    global valid_images
    global classes_qtd
    global images_total_qtd
    global images_without_classes_qtd
    global xml_list

    print("Folder", image_path)

    obj = imageRegionOfInterest(image_path)
    for filename in os.listdir(image_path):
        if searchSubdir and os.path.isdir(os.path.join(image_path, filename)):
            searchFolder(os.path.join(image_path, filename), classNameList, searchSubdir)

        name, ext = os.path.splitext(filename)
        if ext.lower() not in valid_images:
            continue

        print(filename)
        images_total_qtd = images_total_qtd + 1

        obj.setFileImage(filename)
        points = obj.loadBoxFromTxt()     

        if len(points)>0:
            for point in points:
                iclass = int(point[4]) 
                while len(classes_qtd) < iclass+1:
                    classes_qtd.append(0)

                classes_qtd[iclass] = classes_qtd[iclass] + 1
        else:
            images_without_classes_qtd = images_without_classes_qtd + 1

    return 


#=============================================================================
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--path", required=True, help="images path")
ap.add_argument('-className', nargs='*', help='class name list (0..9 positions, max 10), e.g. -classes dog cat')
ap.add_argument('-s', '--subdir', action='store_true', help="Search sub folders")

args = vars(ap.parse_args())

run(args["path"], args["className"], args["subdir"])