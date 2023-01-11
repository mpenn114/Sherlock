# Sherlock
This repository contains a code package, Sherlock, which provides an easy-to-use tool for processing camera trapping images.

Its aim is to remove false positive images - that is, principally, images where the camera has been triggered by a very small disturbances, such as a plant blowing in the wind. If images containing a specific species is being targeted, it also allows for the user to easily customise parameters to set the colour of the deisred animals. This can help to filter out images containing other animals, and thus increase the accuracy of the code.

This code is aimed to be usable by someone with no prior coding experience. To help this, a guide to installing Python (the language which Sherlock is written in) is provided at the end of this readme.

<h3> Input Format </h3>

This code can process JPG images (NB: it should be possible to edit the code to accept any image format). These images should be stored in folders/subfolders, with a single "master folder" containing all of these folders. Examples of acceptable folder structures are below:

[Master Folder] -> Images                                   (that is, an image would have the path .../MasterFolder/0001.JPG)

[Master Folder] -> [Location Folders] -> Images             (e.g. .../MasterFolder/Aberystwyth/0001.JPG)

[Master Folder] -> [Location Folders] -> [Sub-location Folders] -> Images   (e.g. .../MasterFolder/Aberystwyth/Constitution Hill/0001.JPG)

[Master Folder] -> [Location Folders] -> [Sub-location Folders] > [Camera Number] -> Images  (e.g. .../MasterFolder/Aberystwyth/Constitution Hill/Camera1/0001.JPG)

In all of these cases, it is simply necessary to specify the master folder. Note that it is also possible to have a mixture of these cases (e.g. some locations may not have sub-locations)

It is important that the JPG images in each image folder are named consecutively as 0001.JPG, 0002.JPG, ... (note, the number of leading zeros is not important).

<h3> Output Format </h3>

The code can produce different kinds of outputs, depending on the needs of the user. 

The primary output is, for each folder of images, a folder containing CSV files, labelled as "CSV_Outputs[Runcode]". These files are "Potential_Animals" (a list of all images that the code believes may contain animals); "Unlikely_Animals" (a list of all images that the code believes do not contain an animal); "Errors" (a list of images that could not be processed); "Close to Animals" (a list of images such that images close to them - in terms of image number and time - were identified as potential animals); "Overall Animals" (the combination of the lists in "Potential_Animals" and "Close_to_Animals") and "False_Negatives" (if the code is in "testing mode", explained below, a list of all the false negatives)

It is also possible to get the code to write any potential animal images into a new folder, called "PotentialAnimals[Runcode]" where any of the images that are identified as animals, along with those that are close to them, are re-written with red boxes indicating the locations in which animals were thought to be. Note that this does not edit the original images in any way. However, it can be turned off if desired (as these images will be reasonably large files)

Finally, the code can be put into "testing mode". This can be done by changing one of the parameters (explained at the start of the code file), and seeks to compare the results of the code with human-inputted results. A list of image numbers containing animals should be created, called "Animaldata.csv", and a list of image numbers not containing animals should be created, called "nonAnimaldata.csv". These should then be saved in the same folder as the images, and their inclusion will allow the code to create CSV outputs that compare the two sets of results. The code can also compare results according to a number of different characteristics of the image, such as time and location, provided that the format matches that of the example CSV which is included in this Github.

<h3> Installing Python, Anaconda and Jupyter Lab </h3>

Anaconda (and thus, Python) can be installed by visiting:

Windows: https://docs.anaconda.com/anaconda/install/windows/

Mac: https://docs.anaconda.com/anaconda/install/mac-os/

Linux: https://docs.anaconda.com/anaconda/install/linux/

Once Anaconda has been installed, you should be able to find "Anaconda Prompt", and open it to get a command window. Type 

conda install -c conda-forge jupyterlab

into this window and press enter to install Jupyter Lab

<h3> Opening Jupyter Lab </h3>

To open Jupyter Lab, open Anaconda Prompt, type in 

jupyter lab

and then press enter. It should open in your web browser (note: you do not need an Internet connection to do this, or to run any of this code, except the section immediately following)

<h3> Opening Sherlock </h3>

You can copy the code for Sherlock onto your computer by opening a new notebook (by clicking the "Python 3" button below "Notebook" in the right hand window. Then, there should be a textbox with your cursor inside it. If you have Git installed on your computer (which you can install from here https://github.com/git-guides/install-git), you can copy the code for Sherlock by copying

!git clone https://github.com/mpenn114/Sherlock

into this textbox, and then pressing the run button (which is a button in the row of buttons above the textbox - it looks like a "play" button). You should then be able to see a folder called Sherlock on the left hand side of the screen. Double-click on this folder to open it, and then double-click on the file "Sherlock.ipynb" to open the notebook for Sherlock. This should then appear on the right hand window.

Otherwise, you can download the code from this repository as a zip file. After extracting this code (right click on the zip file and click "Extract All"), you then will need to copy the notebook "Sherlock.ipynb" to the folder that Python opens with when you start Jupyter Lab. On Windows, this will generally be "C:/Users/[Your username]".

This file then contains all the information needed to run the code at the top. The actual code is below this initial text and, once you are happy with the inputs and parameters, you can run it by pressing the clicking somewhere on it, and then pressing the "run" button.

Note: If you are using an old Mac operating system (iOS 13 or earlier) then you may have an error when running the code. This can be fixed by removing the line 

!pip install opencv-python

from the code and replacing it with the two lines

!pip uninstall opencv-python --y
!pip install opencv-python==4.4.0.46

