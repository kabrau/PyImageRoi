# Tools to annotate images
* ChangeImagesMaxSize
* ExtractImagesFromVideo
* CreateBoundingBoxes
* ExportToClassification

## ChangeImagesMaxSize
A tool to change images max size into folder

### RUN
```
usage: ChangeImagesMaxSize.py [-h] -p PATH -s MAXSIZE

optional arguments:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  images path
  -s MAXSIZE, --maxSize MAXSIZE
                        resize image (width ou height) to MAX SIZE
```

## ExtractImagesFromVideo
A tool to extract images from videos

The images name is same video name with a sequential number, e.g.:
- video: VID-20170817-WA0003.mp4
- images: VID-20170817-WA0003-(F00001).txt, VID-20170817-WA0003-(F00002).txt, VID-20170817-WA0003-(F00003).txt

### RUN
```
usage: ExtractImagesFromVideo.py [-h] -p VIDEOSPATH -o OUTPUTPATH [-f FPS]
                                 [-n]
                                 {portrait,landscape}

positional arguments:
  {portrait,landscape}  portrait (default) or landscape

optional arguments:
  -h, --help            show this help message and exit
  -p VIDEOSPATH, --videosPath VIDEOSPATH
                        videos input path
  -o OUTPUTPATH, --outputPath OUTPUTPATH
                        images output path
  -f FPS, --fps FPS     extract frames por seconds
  -n, --new             Extracts only from videos without extraction (new
                        video)              Extracts only from videos without extraction (new videos) <br>
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
```
usage: CreateBoundingBoxes.py [-h] -p PATH [-f] [-c CLASS]
                              [-className [CLASSNAME [CLASSNAME ...]]]

optional arguments:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  images path
  -f, --first           starts on the first image (default: Jump to first
                        image without label)
  -c CLASS, --class CLASS
                        class number started (default = 0)
  -className [CLASSNAME [CLASSNAME ...]]
                        class name list (0..9 positions, max 10), e.g.
                        -classes dog cat
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

## ExportToClassification
A tool to extract box from images and save imagebox to classification

### RUN
```
usage: ExportToClassification.py [-h] -p PATH -d DEST

optional arguments:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  images path
  -d DEST, --dest DEST  destination images path
```

### Example
> python ExportToClassification.py -p ..\.\image -f ..\.\image <br>
```
..\.\tmp\0 MyCat-0.jpg [227, 111, 889, 470, '0'] (359, 662, 3)
..\.\tmp\1 MyCat-1.jpg [647, 255, 761, 428, '1'] (173, 114, 3)
..\.\tmp\1 MyCat-2.jpg [756, 257, 871, 429, '1'] (172, 115, 3)
..\.\tmp\1 MyCat-3.jpg [4, 180, 168, 496, '1'] (316, 164, 3)
```

![my cat](https://github.com/kabrau/PyImageRoi/blob/master/tmp/0/MyCat-0.jpg)
![plant 1](https://github.com/kabrau/PyImageRoi/blob/master/tmp/1/MyCat-1.jpg)
![plant 2](https://github.com/kabrau/PyImageRoi/blob/master/tmp/1/MyCat-2.jpg)
![plant 3](https://github.com/kabrau/PyImageRoi/blob/master/tmp/1/MyCat-3.jpg)

