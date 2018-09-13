import os
import glob
import pandas as pd
import argparse
import xml.etree.ElementTree as ET
from os import listdir

def xml_to_csv(path):
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):

            value = (root.find('filename').text,
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     member[0].text,
                     int(member.find('bndbox').find('xmin').text),
                     int(member.find('bndbox').find('ymin').text),
                     int(member.find('bndbox').find('xmax').text),
                     int(member.find('bndbox').find('ymax').text)
                     )
            xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df

def run(path, imagesPath):

    messages = []
    listImages = listdir(imagesPath)
    listFileNames = []

    folders = {}
    folders['root'] = {}
    folders['root']['classes'] = {}
    folders['root']['total images'] = 0
    folders['root']['total objects'] = 0
    
    for folder in listdir(path):

        listDir = glob.glob(os.path.join(path,folder) + '/*.xml') #os.listdir(os.path.join(path,folder))

        folders['root']['total images'] += len(listDir)

        folders[folder] = {}
        folders[folder]['classes'] = {}
        folders[folder]['total images'] = len(listDir)
        folders[folder]['total objects'] = 0

        for xml_file in listDir:
            if xml_file.endswith(".xml"):
                tree = ET.parse(xml_file)
                root = tree.getroot()

                if not root.find('filename').text in (listImages):
                    messages.append('File '+root.find('filename').text+' not found') 

                if root.find('filename').text in (listFileNames):
                    messages.append('File '+root.find('filename').text+' used in two folders') 
                listFileNames.append(root.find('filename').text)

                for member in root.findall('object'):

                    folders['root']['total objects'] += 1
                    folders[folder]['total objects'] += 1

                    if not member[0].text in folders['root']['classes'].keys(): 
                        folders['root']['classes'][member[0].text] = 0
                    folders['root']['classes'][member[0].text] += 1

                    if not member[0].text in folders[folder]['classes'].keys():
                        folders[folder]['classes'][member[0].text] = 0
                    folders[folder]['classes'][member[0].text] += 1
    
    for i, v in enumerate(folders):
        if not v=='root':
            print('--------------------------------------------')
            print('folder name:',v)
            print('total images:','\t', folders[v]['total images'], '\t', folders[v]['total images']/folders['root']['total images'])
            print('total objects:','\t', folders[v]['total objects'], '\t', folders[v]['total objects']/folders['root']['total objects'])
            for j, c in enumerate(folders[v]['classes']):
                print('class => ',c,'\t', folders[v]['classes'][c], '\t', folders[v]['classes'][c]/folders['root']['classes'][c] )
        
    print()
    print('============================================')
    print('TOTAL')
    print('total images:','\t', folders['root']['total images'])
    print('total objects:','\t', folders['root']['total objects'])
    for j, c in enumerate(folders['root']['classes']):
        print('class => ',c,'\t', folders['root']['classes'][c] )

    print()
    print('Messages:')
    for msg in messages:
        print(msg)
        


#=============================================================================
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--path", required=True, help="root annotations path")
ap.add_argument("-i", "--images", required=True, help="images path")

args = vars(ap.parse_args())

run(args["path"], args["images"])