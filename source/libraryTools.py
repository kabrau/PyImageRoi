# Capturing image ROI with Python and OpenCV
# 31/01/2017 - Marcelo Cabral 

import cv2
import os
import sys
import numpy as np

class imageRegionOfInterest:

    global mouse_select_area
    Instance = None
    
    def __init__(self, _path):
        self.path = _path
        self.points = []
        self.image = None
        self.originalImage = None
        self.windowName = ""
        self.fileName = ""

        self.isSavePoints = False
        self.pathToSave = _path
        self.fileNameTxt = ""

        self.classNumber = ""
        self.classNameList = None

        #to MouseSelect
        self.ptInitial = None
        self.ptFinal = None
        self.startedSelectArea = False

        self.colorList = [(0,255,0),
                          (0,0,255),
                          (255,0,0),
                          (25,25,112),
                          (112,0,25),
                          (102,205,170), 
                          (255,255,0), 
                          (153,50,204), 
                          (100,149,237), 
                          (0,255,255), 
                          (184,134,11)]
        

        imageRegionOfInterest.Instance = self         

    def setTxtFileName(self):
        base_file, ext = os.path.splitext(self.fileName)
        self.fileNameTxt = os.path.join( self.pathToSave, base_file+".txt")

    def loadBoxFromTxt(self):
        self.setTxtFileName()
        points = []
        if (os.path.isfile(self.fileNameTxt)):
            try:
                if (os.stat(self.fileNameTxt).st_size>0):
                    l = np.loadtxt(self.fileNameTxt,dtype=int, delimiter=' ')
                    if len(l.shape)==1:
                        points.append([l[1],l[2],l[1]+l[3],l[2]+l[4],str(l[0])])
                    else:
                        for row in l:
                            if len(row)==5:
                                points.append([row[1],row[2],row[1]+row[3],row[2]+row[4],str(row[0])])
            except:
                print ("Unexpected error:", sys.exc_info()[0])       
        return points

    def setFileImage(self, _filename):
        self.fileName = _filename

    def loadFromFile(self):
        self.image = cv2.imread(os.path.join(self.path,self.fileName))    
        self.originalImage = self.image.copy()

    def extractBox(self, pathName, fileName, point):
        image = self.image[point[1]:point[3],point[0]:point[2]]
        print(pathName,fileName, point, image.shape)
        if not os.path.exists(pathName):
            os.makedirs(pathName)
        cv2.imwrite(os.path.join(pathName,fileName), image)

    def loadImage(self, _filename):

        self.setFileImage(_filename)
        self.loadFromFile()

        if (self.windowName != ""):
            cv2.destroyWindow(self.windowName)
        self.windowName = self.fileName


       
        #base_file, ext = os.path.splitext(self.fileName)
        #self.fileNameTxt = os.path.join( self.pathToSave, base_file+".txt") 

        self.points = []
        points = self.loadBoxFromTxt()        
        for point in points:
            #print(point[0],point[1],point[2],point[3],point[4])
            self.setInicialPoint(point[0],point[1])
            self.setFinalPoint(point[2],point[3],point[4])

        #if (os.path.isfile(self.fileNameTxt)):
        #    try:
        #        if (os.stat(self.fileNameTxt).st_size>0):
        #            l = np.loadtxt(self.fileNameTxt,dtype=int, delimiter=' ')
        #            if len(l.shape)==1:
        #                self.setInicialPoint(l[1],l[2])
        #                self.setFinalPoint(l[1]+l[3],l[2]+l[4],str(l[0]))
        #            else:
        #                for row in l:
        #                    if len(row)==5:
        #                        self.setInicialPoint(row[1],row[2])
        #                        self.setFinalPoint(row[1]+row[3],row[2]+row[4],str(row[0]))
        #    except:
        #        print ("Unexpected error:", sys.exc_info()[0])
            
        self.showImage()

    def showImage(self):
        cv2.namedWindow(self.windowName)
        cv2.setMouseCallback(self.windowName, mouse_select_area)
        cv2.moveWindow(self.windowName, 1, 1)
        self.refresh()

    def textPoint(self, pt1):
        return (pt1[0], pt1[1]-4)


    def loadClassName(self,classNumber):
        className = 'C'+classNumber
        if self.classNameList is not None:
            i = int(classNumber)
            if len(self.classNameList)>i:
               className = self.classNameList[i]

        return className


    def refresh(self):
        self.image = self.originalImage.copy()
        for pt in self.points:
            cor = int(pt[2])
            cv2.putText(self.image,self.loadClassName(pt[2]),self.textPoint(pt[0]), cv2.FONT_HERSHEY_SIMPLEX, 0.8, self.colorList[cor],2)
            cv2.rectangle(self.image, pt[0], pt[1], self.colorList[cor], 2)

        cv2.imshow(self.windowName, self.image)
            
    def setInicialPoint(self, x, y):
        self.ptInitial = (x, y)
        self.startedSelectArea = True

    def showTemporarySelectArea(self, x, y):
        if (self.startedSelectArea):
            img = self.originalImage.copy()
            cor = int(self.classNumber)
            cv2.putText(img,self.loadClassName(self.classNumber),self.textPoint(self.ptInitial), cv2.FONT_HERSHEY_SIMPLEX, 0.8, cor,2)
            cv2.rectangle(img, self.ptInitial, (x, y), cor, 2)
            cv2.imshow(self.windowName, img)

    def setFinalPoint(self, x, y, classNumber):
        if (self.startedSelectArea):
            if (classNumber==""):
                classNumber=self.classNumber
            self.ptFinal = (x, y)
            self.startedSelectArea = False

            if (self.ptInitial[0]<self.ptFinal[0]):
                x1 = self.ptInitial[0]
                x2 = self.ptFinal[0]
            else:
                x2 = self.ptInitial[0]
                x1 = self.ptFinal[0]

            if (self.ptInitial[1]<self.ptFinal[1]):
                y1 = self.ptInitial[1]
                y2 = self.ptFinal[1]
            else:
                y2 = self.ptInitial[1]
                y1 = self.ptFinal[1]

            self.points.append( [(x1,y1), (x2,y2), classNumber] )
            self.refresh()

    def cancelLastPoint(self):
        if len(self.points) > 0:
            del self.points[-1]
            self.refresh()

    def savePoints(self):
        l = []
        for pt in self.points:
            l.append([int(pt[2]), pt[0][0], pt[0][1], pt[1][0]-pt[0][0], pt[1][1]-pt[0][1] ])
        #np.savetxt(self.fileNameTxt, np.asarray(l),fmt='%6.0f', delimiter =' ',newline='\n')  
        np.savetxt(self.fileNameTxt, np.asarray(l),fmt='%d', delimiter =' ',newline='\n')  


def mouse_select_area(event, x, y, flags, param):
    #start select area
    if event == cv2.EVENT_LBUTTONDOWN:
        imageRegionOfInterest.Instance.setInicialPoint(x,y)

    #show temporaty select area
    elif event == cv2.EVENT_MOUSEMOVE:
        imageRegionOfInterest.Instance.showTemporarySelectArea(x,y)

    #acept select area
    elif event == cv2.EVENT_LBUTTONUP:
        imageRegionOfInterest.Instance.setFinalPoint(x,y,"")

    #cancel select area
    elif event == cv2.EVENT_RBUTTONDOWN:
        imageRegionOfInterest.Instance.cancelLastPoint()


