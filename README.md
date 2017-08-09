# PyImageRoi
A simple tool to Labeling object bounding boxes or ROI (Region of interest) in images

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

## usage
LoadImages.py [-h] -p PATH [-f]
```
optional arguments:<br>
  -h, --help            show this help message and exit<br>
  -p PATH, --path PATH  images path<br>
  -f, --first           starts on the first image (default: Jump to first<br>
                        image without label)<br>
```

Each line of text file is a one region
>class_number x1 y1 width height

Example:
>0 342 136 100 200
   

**Left Click** mouse to start marking an area<br/>
**Right Click** mouse to remove last area<br/>
**'N'** to next image<br/>
**'P'** to previus image<br/>

![Screen Shot](https://github.com/kabrau/PyImageRoi/blob/master/tmp/MyCatResult.jpg)

