import argparse
import os
from libraryTools import imageRegionOfInterest

#=============================================================================
def run(path, destPath):

    obj = imageRegionOfInterest(path)

    valid_images = [".jpg",".gif",".png",".tga",".jpeg"]

    qtd = 0
    for filename in os.listdir(path):
        name, ext = os.path.splitext(filename)
        if ext.lower() not in valid_images:
            continue
        if (not os.path.exists(os.path.join(path,name+".txt"))):
            continue

        obj.setFileImage(filename)
        points = obj.loadBoxFromTxt()     
        
        if len(points)>0:
            obj.loadFromFile()
            boxNumber = 0
            for point in points:
                name, ext = os.path.splitext(filename)
                obj.extractBox(os.path.join(destPath,point[4]),name+"-"+str(boxNumber)+ext, point)
                boxNumber += 1
        
        qtd += 1

#=============================================================================
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--path", required=True, help="images path")
ap.add_argument("-d", "--dest", required=True, help="destination images path")

args = vars(ap.parse_args())

run(args["path"], args["dest"])