import os
import cv2
import argparse
import numpy as np
#print(cv2.__version__)

def outputFileName(filename, pathOut, frame = 0):
    name, ext = os.path.splitext(filename)
    return os.path.join(pathOut,name+("-(F%05d)"%frame)+".jpeg").replace("\\","/")

#=============================================================================
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p","--videosPath", required=True, help="videos input path")
ap.add_argument("-o","--outputPath", required=True, help="images output path")
ap.add_argument("-f", "--fps", required=False, default=3, type=int, help='extract frames por seconds')
ap.add_argument("orientation", choices=['portrait','landscape'], help='portrait (default) or landscape')

ap.add_argument("-n", "--new", required=False, dest='justNew', action='store_const', const=True, default=False,
                      help='Extracts only from videos without extraction (new video)')

args = vars(ap.parse_args())

pathIn = args["videosPath"]
pathOut = args["outputPath"]
fpsOut = args["fps"]
orientation = args["orientation"]
justNew = args["justNew"]

#--- RUN ----
valid_images = [".mp4", ".avi"]

for filename in os.listdir(pathIn):
    ext = os.path.splitext(filename)[1]
    if ext.lower() not in valid_images:
        continue

    print("Video: ",filename)
    if justNew:
        if (os.path.isfile(outputFileName(filename, pathOut))):
            print("Images already extracted")
            continue

    try:
        vidcap = cv2.VideoCapture( os.path.join(pathIn,filename) )

        video_width = vidcap.get(cv2.CAP_PROP_FRAME_WIDTH)
        video_height = vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        video_fps = vidcap.get(cv2.CAP_PROP_FPS)
        video_frameCount =vidcap.get(cv2.CAP_PROP_FRAME_COUNT)

        step = 1
        if (video_fps>fpsOut):
            step = int(video_fps/fpsOut)

        success = True
        count = step
        frame = 0
        salved = 0
        while success:
            success,image = vidcap.read()
            if (count==step):
                count = 0 
                if (success):
                    fileNameOut = outputFileName(filename, pathOut, frame) 

                    if (orientation=="portrait"):
                        if (image.shape[0]<image.shape[1]):
                            image = np.rot90(image,3)

                    if (orientation=="landscape"):
                        if (image.shape[0]>image.shape[1]):
                            image = np.rot270(image,3)

                    cv2.imwrite(fileNameOut, image)     # save frame as JPEG file
                    salved = salved +1
            frame = frame + 1
            count = count + 1

        print("Total frames",video_frameCount," / Extracted",salved)

    except IOError:
        print("cannot create thumbnail for '%s'" % filename)

#vidcap = cv2.VideoCapture('E:/Datasets/pedestrian_signal/videos/VID-20170806-WA0018.mp4')


#print("width",vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))
#print("height",vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#print("fps",vidcap.get(cv2.CAP_PROP_FPS))
#print("frame count",vidcap.get(cv2.CAP_PROP_FRAME_COUNT))


#vidcap2 = cv2.VideoCapture('E:/Datasets/pedestrian_signal/videos/VID-20170809-WA0000.mp4')


#success,image = vidcap.read()
#count = 0
#success = True
#while success:
#  success,image = vidcap.read()
#  print('Read a new frame: ', success)
#  cv2.imwrite("E:/Datasets/pedestrian_signal/videos/frame%d.jpg" % count, image)     # save frame as JPEG file
#  count += 1



