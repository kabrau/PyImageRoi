import argparse
import os
import glob
import pandas as pd
from libraryTools import imageRegionOfInterest

#filename,width,height,class,xmin,ymin,xmax,ymax
#20170730_132530-(F00000).jpeg,576,1024,sinaleira,221,396,246,437

def to_csv(path):

    classNameList = ["ascending_stair", "descending_stair", "door", "elevator_door"]

    obj = imageRegionOfInterest(path)
    valid_images = [".jpg",".gif",".png",".tga",".jpeg"]

    xml_list = []
    for filename in os.listdir(path):
        name, ext = os.path.splitext(filename)
        if ext.lower() not in valid_images:
            continue
        if (not os.path.exists(os.path.join(path,name+".txt"))):
            continue

        obj.setFileImage(filename)
        print(filename)
        points = obj.loadBoxFromTxt() 
        if len(points)>0:
            obj.loadFromFile()            
            for point in points:
                iclass = int(point[4])
                value = (filename,
                        int(obj.image.shape[1]),
                        int(obj.image.shape[0]),
                        classNameList[iclass], 
                        int(point[0]),
                        int(point[1]),
                        int(point[2]),
                        int(point[3])
                        )
                xml_list.append(value)

    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df


def run(image_path, cvs_file):
    xml_df = to_csv(image_path)
    xml_df.to_csv(cvs_file, index=None)
    print('Successfully converted to csv.')


#=============================================================================
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--path", required=True, help="images path")
ap.add_argument("-c", "--cvs_file", required=True, help="cvs file")

args = vars(ap.parse_args())

run(args["path"], args["cvs_file"])