# Tools to annotate images
* ChangeImagesMaxSize
* ExtractImagesFromVideo
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

## ExtractImagesFromVideo
A tool to extract images from videos

The images name is same video name with a sequential number, e.g.:
- video: VID-20170817-WA0003.mp4
- images: VID-20170817-WA0003-(F00001).txt, VID-20170817-WA0003-(F00002).txt, VID-20170817-WA0003-(F00003).txt

### RUN
ExtractImagesFromVideo.py [-h] -p VIDEOSPATH -o OUTPUTPATH [-f FPS] [-n] {portrait,landscape}
```
positional arguments:<br>
  {portrait,landscape}  portrait (default) or landscape <br><br>

optional arguments: <br>
  -h, --help                show this help message and exit <br>
  -p VIDEOSPATH, --videos   Path VIDEOSPATH videos input path <br>
  -o OUTPUTPATH, --output   Path OUTPUTPATH images output path <br>
  -f FPS, --fps FPS         extract frames por seconds <br>
  -n, --new                 Extracts only from videos without extraction (new videos) <br>
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
usage: CreateBoundingBoxes.py [-h] -p PATH [-f] [-c CLASS]<br>
                              [-className [CLASSNAME [CLASSNAME ...]]]
```
optional arguments:<br>
  -h, --help            show this help message and exit<br>
  -p PATH, --path PATH  images path<br>
  -f, --first           starts on the first image (default: Jump to first<br>
                        image without label)<br>
  -c CLASS, --class CLASS<br>
                        class number started (default = 0)<br>
  -className [CLASSNAME [CLASSNAME ...]]<br>
                        class name list (0..9 positions, max 10), e.g.<br>
                        -classes dog cat<br>
```

### USAGE   

**Left Click** mouse to start marking an area<br/>
**Right Click** mouse to remove last area<br/>
**'0..9'** change class to new boxe<br/>
**'N'** to next image<br/>
**'P'** to previus image<br/>
**'Q'** Exit<br/>


### Example
> python CreateBoundingBoxes.py -p ..\.\image -className cat plant <br>

![Screen Shot](https://github.com/kabrau/PyImageRoi/blob/master/tmp/MyCatResult.jpg)

```text
0 227 111 662 359
1 647 255 114 173
1 756 257 115 172
1 4 180 164 316
```

