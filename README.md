# PyImageRoi
A simple tool for
- Labeling object bounding boxes in images.
- Capture image ROI (Region of interest).

Implemented with Python 3.5. and OpenCV

- You can capture multiple regions per image.<br>
- The regions are saved in a text file with same name of image file.<br>
Example: <br>
cat.jpg  <= image <br>
cat.txt  <= label <br>

**usage:** LoadImages.py [-h] -p PATH [-v {YOLO,SIMPLE}] [-f]<br>

optional arguments:<br>
  -h, --help            show this help message and exit<br>
  -p PATH, --path PATH  images path<br>
  -v {YOLO,SIMPLE}, --version {YOLO,SIMPLE}<br> 
                        label version<br>
  -f, --first           starts on the first image (default: Jump to first<br>
                        image without label)<br>

Each line of text file is a one region.<br>
Version **YOLO**<br>
The region is class_number x1 y1 width height<br><br>
Example:<br>
0 342 136 100 200

Version **SIMPLE**<br>
The region is X_start, Y_start, X_end, Y_end.<br><br>
Example:<br>
   342,   136,  1433,   781
   

**Left Click** mouse to start marking an area<br/>
**Right Click** mouse to remove last area<br/>
**'N'** to next image<br/>
**'P'** to previus image<br/>

![Screen Shot](https://github.com/kabrau/PyImageRoi/blob/master/tmp/MyCatResult.jpg)

