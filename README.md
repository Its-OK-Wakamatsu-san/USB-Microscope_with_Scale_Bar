# Microscope.... using USB-Camera  with Scale-Bar.
![MicroScope_camera_](https://user-images.githubusercontent.com/131073488/232638774-941036c1-b2d0-416e-9a37-8034ef27601f.jpg)<p>
Fig.1　MicroScope_Cam_class101.py

## Overview
**The microscope cam software is created in Python to show scale in the image viewer. This document is its usage notes.**. <p>
## Function
  ```
(1) Image View: Still or Live image is displayed at 1/2 scaled image viewer.
(2) Camera Selector: Select Webcam or Microscope cam.
(3) Camera setting: Change the exposure etc. using the driver provided by the camera manufacture.
(4) Scale-Bar: Show and hide the Scale-Bar.
(5) Scale-Bar length: Change between 1um and 1000um to fit the objective lens magnification.
(6) Scale-Bar color: white, black, green, light blue, red
(7) Scale-Bar location: Move Scale-Bar where to mouse click.
(8) Save file: Save as jpg file. 
  ```
## Usage
   ```
  (1) Start PC: Start your PC.
  (2) Start program: Click MicroScope_Cam.py to start program. A Pop-Up Window for camera connection appears, so press the OK button. Start live camera view.
  (3) Image View: Pressing the “Play//Pause” button, change into Still or Live image.
  (4) Focus: Adjust the focus of your microscope while looking at the Live image view.
  (5) Exposure adjustment: Press the “Set Configuration” button. A function setting Pop Up Window appears. (Fig. 2 is our lab’s camera driver’s sample. Function is depend on your camera driver.) The exposure is set to Auto in the default. Auto-exposure images are not always good, and if they look slightly overexposed or underexposed, it's good to change the exposure manually to get a properly exposed image.
  (6) Scale-Bar and Objective Lens: When changed Objective Lens, select lens from “Objective Lens tab” to fit, and press “Objective Lens” button.
  (7) Scale-Bar location: Move Scale-Bar where to mouse click.
  (8) Scale-Bar: Scale-Bar shows on/off, Scale-Bar length, Scale-Bar color, as you like.
  (9) Save still image: Push the button “Save Image File” to save in jpg file.
  ```
  ![Driver](https://user-images.githubusercontent.com/131073488/233557365-10122650-103b-40a2-9279-da5d800b0f85.png) <p>
    Fig. 2　Camera profile setting window

## Notes  
You shall change these values to fit your camera.<p>
  ```
  (1) Camera spec. length(um)/pixel 	(4.2um/pixel written in program now.)
  (2) Relay Lens magnification		(0.7 written in program now.)
  ```
It is good to change these values to fit your monitor or lens. <p>
  ```
  (1) Program window size:		   1200x650
  (2) Image View window size:	    800x600
  (3) Image View window size: 		Camera CMOS size:1/2
  (4) Objective Lens magnification:	(selectable)
  ```
  
## Development Environment
### Hardware Environment
  ```
  (1) Camera: 1/2inch color CMOS, 
              1600x1200pixels, 
              4.2um/pixel, 
              10fps(max) (material(4))
  (2) Relay Lens (Eyepiece): 0.7x (material(3))
  (3) Objective Lens: 5x, 10x, 20x, 50x, 100x (material(1))
  ```
### Software Environment
  ```
  (1) OS: Windows10
  (2) Python: Version 3.8.10
  (3) Libraries: OpenCV, Pillow
  (4) Regarding the display of video, referred to material(5)
  ```
## Known issue
  ```
  (1) "get Camera profile" command is not working properly.  So, force write camera size.
  ```
## Related materials
  ```
  (1) Polarized light microscope
      https://www.microscope.healthcare.nikon.com/products/polarizing-microscopes/eclipse-lv100n-pol)
  (2) Field of View and Shooting Range of CCD Camera Adapter/Eyepiece for Microscope
      https://www-mecan-co-jp.translate.goog/microscope/Digital/USB/View-Range.htm?_x_tr_sl=ja&_x_tr_tl=en&_x_tr_hl=ja&_x_tr_pto=wapp
  (3) How to attach a C-mount camera to the eyepiece
      https://www-mecan-co-jp.translate.goog/microscope/Digital/USB/Join-Micro.html?_x_tr_sl=ja&_x_tr_tl=en&_x_tr_hl=ja&_x_tr_pto=wapp
  (4) USB Camera
      https://www-trinity--lab-co-jp.translate.goog/IUC_cam/shiyou.html?_x_tr_sl=ja&_x_tr_tl=en&_x_tr_hl=ja&_x_tr_pto=wapp
  (5) Display OpenCV camera video on Canvas
      https://imagingsolution-net.translate.goog/program/python/tkinter/display_opencv_video_canvas/?_x_tr_sl=ja&_x_tr_tl=en&_x_tr_hl=ja&_x_tr_pto=wapp
   ```
