import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET
import argparse
import numpy as np

def run(path, output):
    #xml_df = xml_to_csv(path)
    #xml_df.to_csv(output, index=None)

    # for filename in os.listdir(path):
    #     base_file, ext = os.path.splitext(filename)
    #     print(base_file, ext)

    for xml_file in glob.glob(path + '/*.xml'):

        tree = ET.parse(xml_file)
        root = tree.getroot()

        base_file, ext = os.path.splitext(root.find('filename').text)
        txtFileName = os.path.join(output, base_file+".txt")

        l = []
        for member in root.findall('object'):

            #================ CLASS NAMES =======================
            if member[0].text == 'opened_door':
                iclass = 0
            elif member[0].text == 'closed_door':
                iclass = 1
            elif member[0].text == 'elevator_door':
                iclass = 2
            elif member[0].text == 'ascending_stair':
                iclass = 3
            elif member[0].text == 'descending_stair':
                iclass = 4
            elif member[0].text == 'door':
                iclass = 1
            
            #class_number x1 y1 width height image_width image_height
            l.append([iclass, 
                      int(member.find('bndbox').find('xmin').text), 
                      int(member.find('bndbox').find('ymin').text), 
                      int(member.find('bndbox').find('xmax').text)-int(member.find('bndbox').find('xmin').text), 
                      int(member.find('bndbox').find('ymax').text)-int(member.find('bndbox').find('ymin').text), 
                      int(root.find('size')[0].text), 
                      int(root.find('size')[1].text) ])

            np.savetxt(txtFileName, np.asarray(l),fmt='%d', delimiter =' ',newline='\n')  

    print('Successfully converted xml to txt.')

#=============================================================================
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--path", required=True, help="annotations path")
ap.add_argument("-o", "--output", required=True, help="txt output path")

args = vars(ap.parse_args())


print()
print()
print()
print('==========================================================================')
print('                      ATENTION                                            ')
print()
print('                      ATENTION                                            ')
print()
print()
print('Hi body - dont forget update CLASS NAMES')
print()
print('==========================================================================')
print()
print()
print()

run(args["path"], args["output"])

