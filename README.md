# Sherlock
This repository contains a code package, Sherlock, which provides an easy-to-use tool for processing camera trapping images.

Its aim is to remove false positive images - that is, principally, images where the camera has been triggered by a very small disturbances, such as a plant blowing in the wind. If images containing a specific species is being targeted, it also allows for the user to easily customise parameters to set the colour of the deisred animals. This can help to filter out images containing other animals, and thus increase the accuracy of the code.

This code is aimed to be usable by someone with no prior coding experience. To help this, a guide to installing Python (the language which Sherlock is written in) is provided below, and the steps needed to use this code are explained in detail.

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

You can copy the code for Sherlock onto your computer by opening a new notebook (by clicking the "Python 3" button below "Notebook" in the right hand window. Then, there should be a textbox with your cursor inside it. You can copy the code for Sherlock by copying

!git clone https://github.com/mpenn114/Sherlock

into this textbox, and then pressing the run button (which is a button in the row of buttons above the textbox - it looks like a "play" button. You should then be able to see a folder called Sherlock on the left hand side of the screen. Double-click on this folder to open it, and then double-click on the file "Sherlock.ipynb" to open the notebook for Sherlock. This should then appear on the right hand window.

This file then contains all the information needed to run the code at the top. The actual code is below this initial text and, once you are happy with the inputs and parameters, you can run it by pressing the clicking somewhere on it, and then pressing the "run" button.

