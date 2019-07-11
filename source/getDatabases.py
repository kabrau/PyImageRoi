import os  
import sys
import zipfile
import tarfile
import glob
from CityscapeMask2Pascal import cityscapeMask2Pascal
from xml.etree import ElementTree as et

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


#---------------------------------------------------------------------------------------------
def CityscapeDatasetAnn(databaseName, cityscapeFolder, zipFolder, tmpFolder):

    print()
    print("{} annotations".format(databaseName))

    zipFile = "gtFine_trainvaltest.zip"
    if not os.path.isfile(os.path.join(zipFolder,zipFile)):
        print()
        print("=== Atention ===")
        print("Please, first you need download {} to {}".format(zipFile, zipFolder) )
        print("https://www.cityscapes-dataset.com/downloads/" )
        sys.exit()       

    extractedFolder = os.path.join(tmpFolder,"gtFine/")
    if os.path.exists(extractedFolder):
        print("ZIP was already extracted to {}".format(extractedFolder))
    else:
        print("Extracting {} to {}".format(os.path.join(zipFolder,zipFile), tmpFolder))
        zip_ref = zipfile.ZipFile(os.path.join(zipFolder,zipFile), 'r')
        zip_ref.extractall(tmpFolder)
        zip_ref.close()

    for folderType in ["train","val"]:
        extractedFolderAnn = os.path.join(extractedFolder, folderType)
        outputFolderAnn = os.path.join(cityscapeFolder,folderType+".ann")
        createFolder(outputFolderAnn)        
        imagesFolderType = os.path.join(cityscapeFolder,folderType)

        cityscapeMask2Pascal(databaseName, extractedFolderAnn, outputFolderAnn, imagesFolderType)

    

#---------------------------------------------------------------------------------------------
def CityscapeDataset(datasetFolder, zipFolder, tmpFolder):
    print("=====================================================================")
    print("Cityscape dataset")
    print("=====================================================================")

    zipFile = "leftImg8bit_trainvaltest.zip"
    if not os.path.isfile(os.path.join(zipFolder,zipFile)):
        print()
        print("=== Atention ===")
        print("Please, first you need download {} to {}".format(zipFile, zipFolder) )
        print("https://www.cityscapes-dataset.com/downloads/" )
        sys.exit()

    extractedFolder = os.path.join(tmpFolder,"leftImg8bit/")
    if os.path.exists(extractedFolder):
        print("ZIP was already extracted to {}".format(extractedFolder))
    else:
        print("Extracting {} to {}".format(os.path.join(zipFolder,zipFile), tmpFolder))
        zip_ref = zipfile.ZipFile(os.path.join(zipFolder,zipFile), 'r')
        zip_ref.extractall(tmpFolder)
        zip_ref.close()

    cityscapeFolder = os.path.join(datasetFolder,"Cityscape")
    print("Cityscape dataset Folder {}".format(cityscapeFolder))
    createFolder(cityscapeFolder)

    for folderType in ["train","val"]:

        cityscapefolderType = os.path.join(cityscapeFolder,folderType)
        createFolder(cityscapefolderType)
        print("Moving file from {} to {}".format(extractedFolder+folderType, cityscapefolderType))
        for fileName in glob.glob(extractedFolder+folderType+'/**/*.png'):
            destiny = os.path.join( cityscapefolderType, os.path.split(fileName)[1])
            #print("copy file from {} to {}".format(fileName,destiny))
            os.rename(fileName, destiny)

    #-- Annotations
    CityscapeDatasetAnn("Cityscape",cityscapeFolder, zipFolder, tmpFolder)


#---------------------------------------------------------------------------------------------
def FoggyCityscapeDataset(datasetFolder, zipFolder, tmpFolder):
    print("=====================================================================")
    print("Foggy Cityscape dataset")
    print("=====================================================================")


    zipFile = "leftImg8bit_trainvaltest_foggy.zip"
    if not os.path.isfile(os.path.join(zipFolder,zipFile)):
        print()
        print("=== Atention ===")
        print("Please, first you need download {} to {}".format(zipFile, zipFolder) )
        print("https://www.cityscapes-dataset.com/downloads/" )
        sys.exit()

    extractedFolder = os.path.join(tmpFolder,"leftImg8bit_foggy/")
    if os.path.exists(extractedFolder):
        print("ZIP was already extracted to {}".format(tmpFolder))
    else:
        print("Extracting {} to {}".format(os.path.join(zipFolder,zipFile), tmpFolder))
        zip_ref = zipfile.ZipFile(os.path.join(zipFolder,zipFile), 'r')
        zip_ref.extractall(tmpFolder)
        zip_ref.close()

    for intensity in ["0.02"]:
        print("Intensity {}".format(intensity))

        foggyCityscapeFolder = os.path.join(datasetFolder,"FoggyCityscape",intensity)
        print("foggy Cityscape dataset intensity {} Folder {}".format(intensity, foggyCityscapeFolder))
        createFolder(foggyCityscapeFolder)

        for folderType in ["train","val"]:

            foggyCityscapefolderType = os.path.join(foggyCityscapeFolder,folderType)
            createFolder(foggyCityscapefolderType)
            print("Moving file from {} to {}".format(extractedFolder+folderType,foggyCityscapefolderType))

            for fileName in glob.glob(extractedFolder+folderType+'/**/*'+intensity+'.png'):
                destiny = os.path.join( foggyCityscapefolderType, os.path.split(fileName)[1])
                #print("copy file from {} to {}".format(fileName,destiny))
                os.rename(fileName, destiny)

            foggyCityscapeFolderfolderTypeAnn = os.path.join(foggyCityscapeFolder,folderType+".ann")
            createFolder(foggyCityscapeFolderfolderTypeAnn)


        #-- Annotations
        CityscapeDatasetAnn("FoggyCityscape",foggyCityscapeFolder, zipFolder, tmpFolder)

#---------------------------------------------------------------------------------------------
def KittiDataset(datasetFolder, zipFolder, tmpFolder):
    print("=====================================================================")
    print("Kitti dataset")
    print("=====================================================================")
    tmpFolder = os.path.join(tmpFolder,"kitti")

    zipFiles = ["data_object_image_2.zip","data_object_label_2.zip","vod-converter-master.zip"]
    first = True
    for zipFile in zipFiles:
        if not os.path.isfile(os.path.join(zipFolder,zipFile)):
            if first:
                print()
                print("=== Atention ===")
                print("Please, first you need download {} to {}".format(zipFile, zipFolder) )
            first = False
            print("http://www.cvlibs.net/datasets/kitti/eval_object.php?obj_benchmark=3d")
            print("https://github.com/umautobots/vod-converter")
    if not first:
        sys.exit()

    extractedFolder = os.path.join(tmpFolder,"training")
    if os.path.exists(extractedFolder):
        print("ZIP was already extracted to {}".format(extractedFolder))
    else:
        zipFiles = ["data_object_image_2.zip","data_object_label_2.zip","vod-converter-master.zip"]
        for zipFile in zipFiles:
            print("Extracting {} to {}".format(os.path.join(zipFolder,zipFile), tmpFolder))
            zip_ref = zipfile.ZipFile(os.path.join(zipFolder,zipFile), 'r')
            zip_ref.extractall(tmpFolder)
            zip_ref.close()

    print("Creating file train.txt")
    text_value = ""
    for fileName in glob.glob(extractedFolder+'/**/*.png'):
        text_value = text_value+ fileName.split("\\")[-1:][0].split(".")[0] + "\n"
    text_file = open(os.path.join(tmpFolder,"train.txt"), "w")
    text_file.write(text_value)
    text_file.close()

    print("Annotation convert")
    sys.path.insert(0,os.path.join(tmpFolder,"vod-converter-master"))
    sys.path.insert(0,os.path.join(tmpFolder,"vod-converter-master","vod_converter"))
    from vod_converter import main as kittiConverter

    kittiConverter.main(from_path=tmpFolder, from_key="kitti",
                                        to_path=tmpFolder, to_key="voc",
                                        select_only_known_labels=False,
                                        filter_images_without_labels=False)

    kittiFolder = os.path.join(datasetFolder,"Kitti")
    createFolder(kittiFolder)

    folderType = "train"
    kittifolderType = os.path.join(kittiFolder,folderType)
    createFolder(kittifolderType)

    extractedFolder = os.path.join(tmpFolder,"VOC2012","JPEGImages")
    print("Moving file from {} to {}".format(extractedFolder, kittifolderType))

    for fileName in glob.glob(extractedFolder+'/*.png'):
        destiny = os.path.join( kittifolderType, os.path.split(fileName)[1])
        os.rename(fileName, destiny)

    kittifolderType = kittifolderType + ".ann"
    createFolder(kittifolderType)

    extractedFolder = os.path.join(tmpFolder,"VOC2012","Annotations")
    print("Moving file from {} to {}".format(extractedFolder, kittifolderType))

    for fileName in glob.glob(extractedFolder+'/*.xml'):
        destiny = os.path.join( kittifolderType, os.path.split(fileName)[1])
        os.rename(fileName, destiny)
                              
#---------------------------------------------------------------------------------------------
def Sim10KDataset(datasetFolder, zipFolder, tmpFolder):
    print("=====================================================================")
    print("Sim10K dataset")
    print("=====================================================================")
    tmpFolder = os.path.join(tmpFolder,"Sim10K")

    zipFiles = ["repro_10k_annotations.tgz","repro_10k_images.tgz"]
    first = True
    for zipFile in zipFiles:
        if not os.path.isfile(os.path.join(zipFolder,zipFile)):
            if first:
                print()
                print("=== Atention ===")
                print("Please, first you need download {} to {}".format(zipFile, zipFolder) )
            first = False
            print("https://fcav.engin.umich.edu/sim-dataset/")
    if not first:
        sys.exit()

    extractedFolder = os.path.join(tmpFolder,"VOC2012")
    if os.path.exists(extractedFolder):
        print("ZIP was already extracted to {}".format(extractedFolder))
    else:
        zipFiles = ["repro_10k_images.tgz","repro_10k_annotations.tgz"]
        for zipFile in zipFiles:
            print("Extracting {} to {}".format(os.path.join(zipFolder,zipFile), tmpFolder))
            zip_ref = tarfile.open(os.path.join(zipFolder,zipFile), 'r')
            zip_ref.extractall(tmpFolder)
            zip_ref.close()    
            
        extractedFolder = os.path.join(tmpFolder,"VOC2012","Annotations")
        print("Adjust filename proper into xml files")
        for xml_file in glob.glob(extractedFolder+'/*.xml'):
            tree = et.parse(xml_file)
            #print(xml_file, tree.find('.//filename').text)
            tree.find('.//filename').text = os.path.split(xml_file)[1].split(".")[0]+".jpg"
            #print(xml_file, tree.find('.//filename').text)
            tree.write(xml_file)


    Sim10kFolder = os.path.join(datasetFolder,"Sim10k")
    createFolder(Sim10kFolder)

    folderType = "train"
    Sim10kFolderType = os.path.join(Sim10kFolder,folderType)
    createFolder(Sim10kFolderType)

    extractedFolder = os.path.join(tmpFolder,"VOC2012","JPEGImages")
    print("Moving file from {} to {}".format(extractedFolder, Sim10kFolderType))

    for fileName in glob.glob(extractedFolder+'/*.jpg'):
        destiny = os.path.join( Sim10kFolderType, os.path.split(fileName)[1])
        os.rename(fileName, destiny)

    Sim10kFolderType = Sim10kFolderType + ".ann"
    createFolder(Sim10kFolderType)

    extractedFolder = os.path.join(tmpFolder,"VOC2012","Annotations")
    print("Moving file from {} to {}".format(extractedFolder, Sim10kFolderType))

    for fileName in glob.glob(extractedFolder+'/*.xml'):
        destiny = os.path.join( Sim10kFolderType, os.path.split(fileName)[1])
        os.rename(fileName, destiny)

#---------------------------------------------------------------------------------------------
if __name__ == "__main__":
    
    print("=====================================================================")
    datasetFolder = "F:/datasets/"
    print("Set Datasets folder = {}".format(datasetFolder))
    print("=====================================================================")
    
    if sys.version_info.major<3 or (sys.version_info.major==3 and sys.version_info.minor<7) :
       print("This code need python version >= 3.7.X")
       sys.exit() 

    zipFolder = os.path.join(datasetFolder,"zip")
    print("ZIP Folder {}".format(zipFolder))
    createFolder(zipFolder)

    tmpFolder = os.path.join(datasetFolder,"tmp")
    print("TMP Folder {}".format(tmpFolder))
    createFolder(tmpFolder)

    print()
    #CityscapeDataset(datasetFolder, zipFolder, tmpFolder)

    print()
    #FoggyCityscapeDataset(datasetFolder, zipFolder, tmpFolder)

    print()
    #KittiDataset(datasetFolder, zipFolder, tmpFolder)

    print()
    Sim10KDataset(datasetFolder, zipFolder, tmpFolder)

