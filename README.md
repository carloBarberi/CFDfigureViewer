# CFDfigureViewer

## Description
The repository is based on the imageComparer script. This code allows the user to open and view the images contained in two different folders so that it is possible to quickly compare them, as in the case of slices obtained from 2 different CFD simulations.

## Disclaimers
+ The script has been tested on Windows machines only
+ **Images must be placed in specific folders and must have the same name in order to be compared (as will be described later). Also the folder in which the images are stored must have the same name for the two simulations**. To facilitate this, some folders have been included to serve as examples. Therefore the script can be launched immediately to test how it works
+ <ins>I recommend using this script in combination with [paraviewMacros](https://github.com/carloBarberi/paraviewMacros). This repository allows you to save photos in the correct folders and with the correct names for `imageComparer.py` </ins>

## Installation
In order to use the script it is necessary to download this repository and insert the results of the simulations into the `2 - PostProcessing` folder.
Inside `2 - PostProcessing` there are two folders that serve as examples.

## Before Usage
+ Libraries needed to launch the script:
    - Colorama
    - pygame
+ The following variables can be changed in `imageComparer`:
    - `CFD_folder`: put the name of the folder where the simulation are located. By default it is `2 - PostProcessing`. This folder must be in the same folder where the script is located
    - `figure_folder`: name of the folder inside `2 - PostProcessing\simulation_1\` in which the different folders with the figures are present. By default the figures are in the following path: `2 - PostProcessing\simulation_1\0_Figures\` so `figure_folder = '0_Figures'`
    - `screen_scaling_factor`: it is a scaling factor that is used if a screen zoom has been set in the Windows settings. In this case the value to enter is value%/100. By default it is set to 1, so 100%
+ Images within folders MUST contain a number in the name, so that they can be sorted in ascending order and displayed to the user in the correct order

## How it works
1. The script asks the user which two simulations to open. The folders that appear are the ones inside `2 - PostProcessing`, so they can be copied and pasted
2. At this point the script shows the folders in which the images are present within `figure_folder`, and which are common to the two simulations. Only folders that are not empty are shown. The user enters the number and pygame is launched to show the images
3. With the arrows it is possible to scroll between the images, while with `q` the user can move from one simulation to another. The photo directory is shown in the bottom left corner (in the examples it is not possible to see it because the background and text are black)
4. `ESC` closes pygame, and gives the user the option to select another set of images
5. By entering *99*, the user returns to the simulation selection
5. By entering *0*, the script ends