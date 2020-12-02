# ImageStitcher

## Overview

This project is to extract the whole boundary of the object by stitching the frame captured by the camera while tracing
the edges. The step motors of x, y axis are controlled by Arduino which receives the signal from the PC. The GUI for this 
project is developed by Kivy framework.

## Structure

- arduino

    The arduino code for controlling the step motor

- gui

    The source code for GUI

- src
    
    The source code for edge tracking, stitching image, motor direction estimation and the communication with Arduino.
    
- utils

    The source code to manage files and folders in this project
    
- app

    The main execution file
    
- requirements

    All the dependencies for this project
    
- settings
 
    Several settings for this project including Arduino communication port, some threshold values, etc.

## Installation

- Environment
    
    Ubuntu 18.04, Windows 10, Python 3.6+

- Dependency Installation
 
    Please go ahead to this project and run the following command in terminal
    ```
    pip3 install -r requirements.txt
    ```
    * Kivy Installation on Windows 10
    
    ```
    pip uninstall kivy
    pip install --upgrade pip wheel setuptools
    pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew
    pip install kivy.deps.gstreamer
    pip install kivy.deps.angle
    pip install kivy
    ```
     
- Arduino Communication Port Permission on Ubuntu.

    After recognizing the communication port, please run the following command in terminal.
    ```
    sudo chmod 666 /dev/{ttyUSB0}
    ```
    
## Execution

- Please upload Arduino code into your Arduino UNO device in arduino/TB6600_2motor_control.ino.

- Please set ARDUINO_PORT variable in settings file according to the environment.

- Please run the following command in this project directory in terminal

    ```
    python3 app.py
    ```

- When the GUI opens, you can set the correct threshold value to support us with the boundary edge of object 
by moving slider. Then after setting the correct threshold value for edge, you can click Start button to move the step motor
,stitch images and edge tracking at the same time. After motor movement is completed, when you click Stitch button, you can
look at the edge result.