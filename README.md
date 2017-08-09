# PyImageRoi
A simple tool for
- Labeling object bounding boxes in images.
- Capture image ROI (Region of interest).

Implemented with Python 3.5. and OpenCV
You can capture multiple regions per image.<br>
The regions are saved in a text file with same name of image file.<br>

Example: <br>
cat.jpg  <= image <br>
cat.txt  <= label <br>

Each line of text file is a one region.<br>
The region is X_start, Y_start, X_end, Y_end.<br>

Example:<br>
   342,   136,  1433,   781
   
Command:<br>
cd ./version_01<br>
./python LoadImages.py -p ../image/

**Left Click** mouse to start marking an area<br/>
**Right Click** mouse to remove last area<br/>
**'N'** to next image<br/>
**'P'** to previus image<br/>

![Screen Shot](https://github.com/kabrau/PyImageRoi/blob/master/tmp/MyCatResult.jpg)

