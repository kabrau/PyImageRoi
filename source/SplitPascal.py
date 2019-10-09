import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET
import argparse
from shutil import copyfile

#---------------------------------------------------------------------------------------------
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


def run(path, imagepath, splitpath):

    classes = {}
    testClass = {}                     
    validClass = {}     

    testClassFinal = {}                     
    validClassFinal = {}     
    trainClassFinal = {} 

    images_total_qtd = 0
    images_test_qtd = 0
    images_valid_qtd = 0
    images_train_qtd = 0

    for xml_file in glob.glob(path + '/*.xml'):
        images_total_qtd += 1

        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            if member[0].text in classes.keys():
                classes[member[0].text] += 1
            else:
                classes[member[0].text] = 1    
                testClass[member[0].text] = 0
                validClass[member[0].text] = 0
                testClassFinal[member[0].text] = 0
                validClassFinal[member[0].text] = 0
                trainClassFinal[member[0].text] = 0

    print()
    print("ClassName, Total")
    for className, total in classes.items():
        qtdTest = int(total*0.15)

        testClass[className] = qtdTest
        validClass[className] = qtdTest

        print(className, total, qtdTest)

    print()
    print("Images:")
    print(images_total_qtd)

    createFolder(os.path.join(splitpath, "test"))
    createFolder(os.path.join(splitpath, "test.ann"))
    createFolder(os.path.join(splitpath, "valid"))
    createFolder(os.path.join(splitpath, "valid.ann"))
    createFolder(os.path.join(splitpath, "train"))
    createFolder(os.path.join(splitpath, "train.ann"))

    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        imageFileName = root.find('filename').text
        print(imageFileName)
        className = ""
        for member in root.findall('object'):
            className = member[0].text

        if testClassFinal[className] < testClass[className]:   
            images_test_qtd += 1     
            copyfile(xml_file,  os.path.join(splitpath, "test.ann", os.path.basename(xml_file)))
            copyfile(os.path.join(imagepath, imageFileName),  os.path.join(splitpath, "test", imageFileName))
            for member in root.findall('object'):
                testClassFinal[member[0].text] += 1

        elif validClassFinal[className] < validClass[className]:        
            images_valid_qtd += 1     
            copyfile(xml_file,  os.path.join(splitpath, "valid.ann", os.path.basename(xml_file)))
            copyfile(os.path.join(imagepath, imageFileName),  os.path.join(splitpath, "valid", imageFileName))
            for member in root.findall('object'):
                validClassFinal[member[0].text] += 1

        else:
            images_train_qtd += 1     
            copyfile(xml_file,  os.path.join(splitpath, "train.ann", os.path.basename(xml_file)))
            copyfile(os.path.join(imagepath, imageFileName),  os.path.join(splitpath, "train", imageFileName))
            for member in root.findall('object'):
                trainClassFinal[member[0].text] += 1

    print()
    print("Total images train ",images_train_qtd)
    for className, total in trainClassFinal.items():
        print(className, total)

    print()
    print("Total images valid ",images_valid_qtd)
    for className, total in validClassFinal.items():
        print(className, total)

    print()
    print("Total images test ",images_test_qtd)
    for className, total in testClassFinal.items():
        print(className, total)        

    return


#=============================================================================
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--imagepath", required=True, help="images path")
ap.add_argument("-p", "--path", required=True, help="annotations path")
ap.add_argument("-s", "--splitpath", required=True, help="split path to train.ann valid.ann test.ann train valid test")

args = vars(ap.parse_args())

run(args["path"], args["imagepath"], args["splitpath"])

