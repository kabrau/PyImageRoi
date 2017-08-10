# Tools to annotate images
* ChangeImagesMaxSize
* CreateBoundingBoxes

## ChangeImagesMaxSize
A tool to change images max size into folder

### RUN
ChangeImagesMaxSize.py [-h] -p PATH -s SIZE
```
optional arguments: <br>
  -h, --help                    show this help message and exit <br>
  -p PATH, --path PATH          images path <br>
  -s MAXSIZE, --maxSize MAXSIZE resize image (width ou height) to MAX SIZE <br>
```

## CreateBoundingBoxes
A tool to Labeling object bounding boxes or ROI (Region of interest) in images

- multiple boxes per image
- multiple classes per image

The regions are saved in a text file with same name of image file, e.g.
```
IMG-20170807-WA0001.jpg
IMG-20170807-WA0001.txt
locaisvstdss.jpg
locaisvstdss.txt
phpiqa6ae.752.502.s.jpg
phpiqa6ae.752.502.s.txt
```

** Important: ** Do not put two pictures with the same name and different extensions in the same folder.

Each line of text file is a one region
>class_number x1 y1 width height

Example:
>0 342 136 100 200

### RUN
CreateBoundingBoxes.py [-h] -p PATH [-f]
```
optional arguments:<br>
  -h, --help            show this help message and exit<br>
  -p PATH, --path PATH  images path<br>
  -f, --first           starts on the first image (default: Jump to first<br>
                        image without label)<br>
```

### USAGE   

**Left Click** mouse to start marking an area<br/>
**Right Click** mouse to remove last area<br/>
**'N'** to next image<br/>
**'P'** to previus image<br/>
**'Q'** Exit<br/>

![Screen Shot](https://github.com/kabrau/PyImageRoi/blob/master/tmp/MyCatResult.jpg)

