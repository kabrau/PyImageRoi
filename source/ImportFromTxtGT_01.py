import argparse
from libraryTools import imageRegionOfInterest
from win32api import GetSystemMetrics

# Attached the mappings between attribute names and label values.

# blur:
#   clear->0
#   normal blur->1
#   heavy blur->2

# expression:
#   typical expression->0
#   exaggerate expression->1

# illumination:
#   normal illumination->0
#   extreme illumination->1

# occlusion:
#   no occlusion->0
#   partial occlusion->1
#   heavy occlusion->2

# pose:
#   typical pose->0
#   atypical pose->1

# invalid:
#   false->0(valid image)
#   true->1(invalid image)

# The format of txt ground truth.
# File name
# Number of bounding box
# x1, y1, w, h, blur, expression, illumination, invalid, occlusion, pose

pathImages = "E:/datasets/FaceDataset/Wider/WIDER_train/images/"
filePath = "E:/datasets/FaceDataset/Wider/wider_face_split/wider_face_train_bbx_gt.txt"

def run(pathImages, filePath):

    obj = imageRegionOfInterest(pathImages)
    filehandle = open(filePath, "r")
    while True:  
        # read a single line
        line = filehandle.readline()
        if not line:
            break

        name = line[0:-1]
        #print(name)

        obj.points.clear()
        qtd = int(filehandle.readline())
        for i in range(qtd):
            box = filehandle.readline().split(' ')
            obj.setFileImage(pathImages+name)
            obj.setTxtFileName()
            obj.loadFromFile()
            x1y1 = (int(box[0]),int(box[1]))
            x2y2 = (int(box[0])+int(box[2]),int(box[1])+int(box[3]))
            obj.points.append( [x1y1, x2y2, "0"] )
        
        obj.savePoints()


#=============================================================================
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--path", required=True, help="images path")
ap.add_argument("-f", "--file", required=True, help="ground truth file")
args = vars(ap.parse_args())

run(args["path"], args["file"])

# python CreateBoundingBoxes.py -p E:\datasets\FaceDataset\Wider\WIDER_train\images\0--Parade -className face       
# python importFromTxtGT_01.py -p E:/datasets/FaceDataset/Wider/WIDER_train/images/ -f E:/datasets/FaceDataset/Wider/wider_face_split/wider_face_train_bbx_gt.txt
