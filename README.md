# RVGLauncher
A Linux launcher for Re-Volt Open GL port

### Current features:
- only stock/dc cars can be used
- IO site based ratings for launching

### Dependencies
- python3
- kivy

### Usage

Create one rvgl install where you delete all car folders (or the 'cars' folder itself). Copy this path to the variable in line 31 (in place of MODIFYTOYOURPATH). The "installs" part doesn't matter, since that isn't implemented yet. Run the app by:
- changing the directory to the project folder (`cd /home/hajducsekb/RVGLauncher-master`, for example)
- run it with python (in most cases, `python3 rvglauncher.py`)

The directory where you store your cars can be linked in the app. This one won't be modified by the Launcher, it only reads it. Don't press the remove button unless you are using a dummy rvgl folder for running the game (since you've deleted the cars folder, you're probably doing this though). 

I may have missed something, in that case sorry.

Detailed description and more security features against removal of the wrong folder might come later. 
