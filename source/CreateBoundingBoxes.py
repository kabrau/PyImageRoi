# Teste Capturing image ROI with Python and OpenCV
# 25/01/2017 - Marcelo Cabral 

# import the necessary packages
import argparse
import cv2
import os
import numpy as np
from libraryTools import imageRegionOfInterest

def run(path, isFirstEmpty = False, classNumber = "0", classNameList = None):

    valid_images = [".jpg",".gif",".png",".tga",".jpeg"]

    fileNames = []
    firstEmpty = -1 
    qtd = 0 
    for filename in os.listdir(path):
        name, ext = os.path.splitext(filename)
        if ext.lower() not in valid_images:
            continue
        fileNames.append(filename)
        if (firstEmpty==-1 and not os.path.exists(os.path.join(path,name+".txt"))):
            firstEmpty = qtd
        qtd += 1

    obj = imageRegionOfInterest(path)

    obj.isSavePoints = True
    obj.pathToSave = path
    obj.classNumber = classNumber
    obj.classNameList = classNameList

    print("Total", qtd)
    print("Labeled", firstEmpty)

    index = 0
    if (isFirstEmpty and firstEmpty!=-1):
        index = firstEmpty

    while index < len(fileNames):

        if index < 0:
            index = 0 
        if index==len(fileNames):
            index = len(fileNames)-1

        filename = fileNames[index]

        obj.loadImage(filename)
        

        # keep looping until the 'q' key is pressed
        while True:
            key = cv2.waitKey(1) & 0xFF

            # refresh
            if key == ord("r"):
                obj.refresh()

            # save 
            elif key == ord("s"):
                obj.savePoints()

            # change Class Number
            elif key >= ord("0") and key <= ord("9"):
                obj.classNumber = chr(key)
            
            # change Class 0  (' key is left side 1 key)
            elif key == ord("'"):
                obj.classNumber = "0"

            # next image or spacebar
            elif key == ord("n") or key==32:
                obj.savePoints()
                index += 1
                break

            # previus image
            elif key == ord("p"):
                obj.savePoints()
                index -= 1
                break

            # quit
            elif key == ord("q"):
                if len(obj.points)>0:
                    obj.savePoints()
                return
        
#=============================================================================
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--path", required=True, help="images path")
ap.add_argument("-f", "--first", required=False, dest='firstEmpty', action='store_const', const=False, default=True,
                      help='starts on the first image (default: Jump to first image without label)')

ap.add_argument("-c", "--class", required=False, help="class number started (default = 0)", default="0")

ap.add_argument('-className', nargs='*', help='class name list (0..9 positions, max 10), e.g. -classes dog cat')

args = vars(ap.parse_args())

run(args["path"], args["firstEmpty"], args["class"], args["className"])