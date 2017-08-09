# Teste Capturing image ROI with Python and OpenCV
# 25/01/2017 - Marcelo Cabral 

# import the necessary packages
import argparse
import cv2
import os
import numpy as np
from libROI import imageRegionOfInterest

def run(path, isFirstEmpty = False):

    valid_images = [".jpg",".gif",".png",".tga"]

    fileNames = []
    firstEmpty = -1 
    qtd = 0 
    for filename in os.listdir(path):
        ext = os.path.splitext(filename)[1]
        if ext.lower() not in valid_images:
            continue
        fileNames.append(filename)
        if (firstEmpty==-1 and not os.path.exists(os.path.join(path,filename+".txt"))):
            firstEmpty = qtd
        qtd += 1

    obj = imageRegionOfInterest(path)
    obj.isSavePoints = True
    obj.pathToSave = path

    print ("Total", qtd)
    print ("Marked", firstEmpty)

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

            # next image
            elif key == ord("n"):
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
                return
        
#=============================================================================
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--path", required=True, help="images path")
ap.add_argument("-v", "--version", required=False, help="label version", choices=["YOLO", "SIMPLE"], default="YOLO")
ap.add_argument("-f", "--first", required=False, dest='firstEmpty', action='store_const', const=False, default=True,
                      help='starts on the first image (default: Jump to first image without label)')

args = vars(ap.parse_args())

run(args["path"], args["firstEmpty"])