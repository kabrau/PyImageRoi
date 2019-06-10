[Explanation in Portuguese](https://bit.ly/2uoySQU)

# Tools to annotate images
* ChangeImagesMaxSize
* ExtractImagesFromVideo
* CreateBoundingBoxes
* ExportToClassification
* ExportToCSV
* ExportToPascal (&#x1F53C; 2019-03-14)
* Generate TFRecord - API Tensorflow (&#x1F53C; 2019-03-19)
* Import from txt ground truth - format Wider Face (&#x1F53C; 2019-03-14)

# Tools to measures
* mAP

## Citation
```
@misc{marcelo_cabral_ghilardi_2019_2604909,
  author       = {Marcelo Cabral Ghilardi},
  title        = {kabrau/PyImageRoi: Tools to annotate images},
  month        = mar,
  year         = 2019,
  doi          = {10.5281/zenodo.2604909},
  url          = {https://doi.org/10.5281/zenodo.2604909}
}
```

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
(adjusts the displayed image size to the screen size)

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
>class_number x1 y1 width height image_width image_height

Example:
>1 426 679 55 99 1080 1920  
>1 440 839 30 59 1080 1920



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
                        -className dog cat
```

### USAGE   

**Left Click** mouse to start marking an area<br/>
**Right Click** mouse to remove last area<br/>
**'0..9'** change class to new boxe (aaccent key = 0, too)<br/>
**'N'** or **'space-bar'** to next image<br/>
**'P'** to previus image<br/>
**'Q'** Exit<br/>


### Example
> python CreateBoundingBoxes.py -p ..\.\image -className cat plant <br>

![Screen Shot](https://github.com/kabrau/PyImageRoi/blob/master/tmp/MyCatResult.jpg)

```text
0 227 111 662 359 1024 576 
1 647 255 114 173 1024 576 
1 756 257 115 172 1024 576 
1 4 180 164 316 1024 576 
```

## ExportToClassification
A tool to extract box from images and save imagebox to classification.
Save the separated images by classes, each class in a subfolder.

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


## ExportToCSV
A tool to create a cvs file with de bounding boxes

note: Use 1 classname only 


### RUN
```
usage: ExportToCSV.py [-h] -p PATH -c CVS_FILE

optional arguments:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  images path
  -c CVS_FILE, --cvs_file CVS_FILE
                        cvs file
```

### Example
> python ExportToCSV.py -p E:\Datasets\pedestrian_signal\images\test -c E:\Datasets\pedestrian_signal\images\test.csv <br>
```
filename,width,height,class,xmin,ymin,xmax,ymax
16431531.jpg,640,426,sinaleira,317,92,345,140
16431540.jpg,640,426,sinaleira,449,106,475,148
17074299.jpg,620,412,sinaleira,566,199,586,228
19156210.jpg,620,412,sinaleira,181,112,206,161
20170701_105311.jpg,768,1024,sinaleira,323,424,352,471
20170701_105442.jpg,768,1024,sinaleira,311,412,346,463
```

## ExportToPascal
TOOL to Create a XML files (PASCAL FORMAT)

### RUN
```
usage: ExportToPascal.py [-h] -p PATH -a ANNPATH 
                              [-className [CLASSNAME [CLASSNAME ...]]]

optional arguments:  
  -h, --help            show this help message and exit  
  -p PATH, --path PATH  images path  
  -a ANNPATH, --annpath ANNPATH  
                        annotation path  
  -className [CLASSNAME [CLASSNAME ...]]
                        class name list (0..9 positions, max 10), e.g.
                        -className dog cat
```

### Example
> python ExportToPascal.py -p "E:\Datasets\pedestrian_signal\images" -a "E:\Datasets\pedestrian_signal\images.ann_gostop" -className go stop off <br>

Ps: At the end, it shows total images and classes


## ExportToPascal.5971774
Specific converter for PedestrianLights dataset available at: http://www.uni-muenster.de/PRIA/en/forschung/index.shtml  
TOOL to Create a XML files (PASCAL FORMAT)  

### RUN
```
usage: usage: ExportToPascal.5971774.py [-h] -p PATH -o GTFILE -a ANNPATH   

optional arguments:  
  -h, --help            show this help message and exit  
  -p PATH, --path PATH  images path  
  -o GTFILE, --gtfile GTFILE  
                        original ground truth file  
  -a ANNPATH, --annpath ANNPATH  
                        annotation path  
```

### Example
> python ExportToPascal.5971774.py -p "E:\Datasets\pedestrianlights-5971774\pedestrianlights\download\imagesequences\01" -o "E:\Datasets\pedestrianlights-5971774\pedestrianlights\download\imagesequences\01\groundtruth.txt" -a "E:\Datasets\pedestrianlights-5971774\pedestrianlights\download\imagesequences\01.ann.GoStop" <br>

Ps: At the end, it shows total images and classes


## Generate TFRecord - API Tensorflow
- **First**, convert from PASCAL to CSV, use: ExportPascal2csv.py
- **Second**, generate TFRecord, use: Generate_TFRecord.py 

### RUN
```
usage: ExportPascal2csv.py [-h] -p PATH -o OUTPUT [-a]

optional arguments:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  annotations path
  -o OUTPUT, --output OUTPUT
                        csv output file
  -a, --addPathCol      add path collumn  
```
```
usage: Generate_TFRecord.py [-h] -c CSV_INPUT -o OUTPUT_PATH [-i IMAGES_PATH]

optional arguments:
  -h, --help            show this help message and exit
  -c CSV_INPUT, --csv_input CSV_INPUT
                        Path to the CSV input
  -o OUTPUT_PATH, --output_path OUTPUT_PATH
                        Path to output TFRecord
  -i IMAGES_PATH, --images_path IMAGES_PATH
                        Path for Images, If dont have into CSV
```

### Example
> python ExportPascal2csv.py -p E:\datasets\FaceDataset\Wider\WIDER_train\train.ann -o E:\datasets\FaceDataset\Wider\WIDER_train\train.csv -a

> python Generate_TFRecord.py --csv_input=E:\datasets\FaceDataset\Wider\WIDER_train\train.csv  --output_path=E:\datasets\FaceDataset\Wider\WIDER_train\train.record 



## mAP
Tool to calc mAP in Object Detection

Returns in the console the mAP values   
And inside each method folder create a subfolder named _chart with a pdf of the Precision Recall method

You need a folder with Pascal VOC annotations, parameter --annpath

And a root folder with one ou more  methods result folder, parameter --resultpath
e.g:   
> c:\results  <= root   
> c:\results\faster   <= method result folder   
> c:\results\ssd      <= method result folder   
> c:\results\yolo     <= method result folder   

Inside each method result folder, you need results files by classes   
e.g:   
cat.txt   
dog.txt   
mouse.txt   

In the results files by class, the content is in this format:   
filename confidence x1 y1 x2 y2   
e.g:   
file001 0.99862 441.5266 429.1418 504.2249 548.0778  
file005 0.99757 466.8359 433.5500 531.3656 545.9105   
file007 0.95728 495.3467 440.6576 554.5069 558.3262   



### RUN
```
usage: mAP.py [-h] -a ANNPATH -r RESULTPATH -c [CLASS [CLASS ...]] -i IOU [-v [VERBOSE]]  
  
  
optional arguments:  
  -h, --help            show this help message and exit   
  -a ANNPATH, --annpath ANNPATH  
                        Pascal VOC annotation path  
  -r RESULTPATH, --resultpath RESULTPATH  
                        Path of method results  
  -c [CLASS [CLASS ...]], --class [CLASS [CLASS ...]]  
                        list of class, e.g. --classes dog cat mouse  
  -i IOU, --IOU IOU     IOU confidence threshold, e.g. 0.5  
  -v [VERBOSE], --verbose [VERBOSE]  
                        show verbose  
```

### Example
> python mAP.py -a E:\Datasets\signal\test.ann.GoStop -r E:\GitHub\PedestrialTrafficLight\accurace_calc\results\3C\ -c cat dog mouse -i 0.5


## Import from txt ground truth - format Wider Face

Wider Face - A Face Detection dataset to Benchmark 
http://mmlab.ie.cuhk.edu.hk/projects/WIDERFace/index.html

### The format of txt ground truth.
File name  
Number of bounding box  
x1, y1, w, h, blur, expression, illumination, invalid, occlusion, pose  

### RUN
```
usage: ImportFromTxtGT_01.py [-h] -p PATH -f FILE

optional arguments:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  images path
  -f FILE, --file FILE  ground truth file
```

### Example
> python importFromTxtGT_01.py -p E:/datasets/FaceDataset/Wider/WIDER_train/images/ -f E:/datasets/FaceDataset/Wider/wider_face_split/wider_face_train_bbx_gt.txt

