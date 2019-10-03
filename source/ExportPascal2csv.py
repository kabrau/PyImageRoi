import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET
import argparse

def toInt(value):
    rs = 0
    try:
        rs = int(value)
    except:
        rs = int(float(value))
    return rs


def xml_to_csv(path, addPathCol):
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            if addPathCol:
                value = (root.find('folder').text,
                        root.find('filename').text,
                        int(root.find('size')[0].text),
                        int(root.find('size')[1].text),
                        member[0].text,
                        toInt(member.find('bndbox').find('xmin').text),
                        toInt(member.find('bndbox').find('ymin').text),
                        toInt(member.find('bndbox').find('xmax').text),
                        toInt(member.find('bndbox').find('ymax').text)
                        )
            else:
                value = (root.find('filename').text,
                        int(root.find('size')[0].text),
                        int(root.find('size')[1].text),
                        member[0].text,
                        toInt(member.find('bndbox').find('xmin').text),
                        toInt(member.find('bndbox').find('ymin').text),
                        toInt(member.find('bndbox').find('xmax').text),
                        toInt(member.find('bndbox').find('ymax').text)
                        )
            if (not member[0].text=="DontCare"):
                xml_list.append(value)

    if addPathCol:
        column_name = ['path','filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    else:
        column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']

    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df


def run(path, output, addPathCol ):
    xml_df = xml_to_csv(path, addPathCol)
    xml_df.to_csv(output, index=None)

    print('Successfully converted xml to csv.')

#=============================================================================
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--path", required=True, help="annotations path")
ap.add_argument("-o", "--output", required=True, help="csv output file")
ap.add_argument("-a", "--addPathCol",  action='store_true', help="add path collumn")

args = vars(ap.parse_args())

run(args["path"], args["output"], args["addPathCol"])

