# PyImageRoi
Capturing image ROI (Region of interest) with Python and OpenCV<br>

## Version 01
Folder ./version_01

You can capture multiple regions per image.<br>
The regions are saved in a text file with same name of  image file.<br>
Each line of text file is a one region.<br>
The region is X_start, Y_start, X_end, Y_end.<br>

Example:<br>
   342,   136,  1433,   781
   
Command:<br>
cd ./version_01
./python LoadImages.py -p ../image/

**Left Click** mouse to start marking an area<br/>
**Right Click** mouse to remove last area<br/>
**'N'** to next image<br/>
**'P'** to previus image<br/>

![Screen Shot](https://github.com/kabrau/PyImageRoi/blob/master/tmp/MyCatResult.jpg)

