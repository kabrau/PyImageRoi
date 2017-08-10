import argparse
import os, sys
import PIL
from PIL import Image
from PIL.ExifTags import TAGS

def need_Rotate(img):
    rotate = False
    data = img._getexif()
    if data is not None:
        exif_data = {
            TAGS[k]: v
            for k, v in data.items()
                if k in TAGS
        }
        rotate = (exif_data['Orientation']==6)

    return rotate


#=============================================================================
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--path", required=True, help="images path")
ap.add_argument("-s", "--maxSize", required=True, type=int, help='resize image (width ou height) to MAX SIZE')

args = vars(ap.parse_args())

path = args["path"]
maxSize = args["maxSize"]

#--- RUN ----
valid_images = [".jpg",".gif",".png",".tga",".jpeg"]

for filename in os.listdir(path):
    ext = os.path.splitext(filename)[1]
    if ext.lower() not in valid_images:
        continue

    try:
        fileNamePath = os.path.join(path,filename)
        img = Image.open(fileNamePath)

        if (img.size[0]>maxSize or img.size[1]>maxSize):
            if need_Rotate(img):
                img = img.rotate(270, expand=True)

            if (img.size[0]>img.size[1]):
                wpercent = (maxSize / float(img.size[0]))
                sizeHeight = int((float(img.size[1]) * float(wpercent)))
                imgResized = img.resize((maxSize, sizeHeight), PIL.Image.ANTIALIAS)
                imgResized.save(fileNamePath)
                print(filename,":", img.size[0],"x", img.size[1], '=> Updated to ',(maxSize, sizeHeight))
            else:
                wpercent = (maxSize / float(img.size[1]))
                sizeWidth = int((float(img.size[0]) * float(wpercent)))
                imgResized = img.resize((sizeWidth, maxSize), PIL.Image.ANTIALIAS)
                imgResized.save(fileNamePath)                
                print(filename,":", img.size[0],"x", img.size[1], '=> Updated to ',(sizeWidth, maxSize))

        elif need_Rotate(img):
            img = img.rotate(270, expand=True)
            img.save(fileNamePath)                
            print(filename,":", img.size[0],"x", img.size[1], '=> Rotated')
        else:
            print(filename,":", img.size[0],"x", img.size[1], '=> OK')

    except IOError:
        print("cannot create thumbnail for '%s'" % filename)

