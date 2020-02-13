# RVGLauncher
A Linux launcher for Re-Volt Open GL port

![RVGLauncher Screenshot](https://i.imgur.com/XYUqWsC.png)

### Current features:
- launch with command line arguments
- launch with select class stock and/or IO cars only (Bonus doesn't work yet) (**credits to Mr. Burguers for helping me create a list of cars!**)
- launch with custom list of cars
- fix cases!

### Dependencies
- python3
- kivy

### Installation

`cd [yourchoiceofinstallpath]`

`git clone https://github.com/hajducsekb/RVGLauncher.git`

`cd ./RVGLauncher`

`python3 rvglauncher.py`

**Dependencies (Debian Based):**

`sudo apt install python3-pip`

`pip3 install --user kivy` or `python3 -m pip install --user kivy`

### Usage

You need to create an RVGL install in which you remove the cars folder if you want to use the class based car options. You can also just rename the cars folder to something like "allcars" or ".cars".  Run the app by:
- changing the directory to the downloaded folder (`cd /home/hajducsekb/RVGLauncher`, for example)
- run it with python (`python3 rvglauncher.py`)

The directory where you store your cars should be linked in the app itself (this can be the "allcars" or ".cars" I've mentioned before - for example: /home/hajducsekb/RVGL/.cars). For reference: this path is stored in `carspath.txt`. This one won't be modified by the Launcher, it only gets read. Also set the path to your rvgl install (the one where the executable lies). This is stored in `rvglpath.txt`. The default paths for cars and rvgl are from two different installs of mine - feel free to do this yourself, the cars folder can be anywhere where you store cars.

On the main screen, stocks are selected by default. Please only use those for now, as IO and bonus don't have the proper lists (you can edit them yourself in the `stockcars.txt`).

**Setting up a custom folder list:** If you want to set up a custom list of cars, it's fairly simple to do. There are 3 examples. You need to add each different list in a new line in the `customlists.txt` file. The name of the list comes first - for this, you should use alphabetical and numerical characters, unless you really want to test the app. After the name, there is a colon (`:`). Then, you can list the car folders (don't leave any spaces, unless, it is actually in the folder name). Seperate cars by commas. Feel free to add and remove any as you want, but if you have too many lists, the UI will get really unreadable.

**In-app settings:** In the settings, you can set the Command Line Arguments. There is a help menu, where you can see the ones I thought were most commonly used. These arguments get saved to `launchparams.txt` when you go back to the home screen.

**Dev Tools:** You need to set a custom install for this menu. The only tool available right now is renaming track folders. This renames files in the main track folder and also the files in the reversed subfolder. You can't go back to the Home screen, the function for this only exists in Settings, this will be fixed lol.

### How custom car folders work?

The app uses soft symlinking via bash. (`ln -s`) **This is the reason it is not available on Windows.** The way it works is it creates a link in the rvgl cars folder to the allcars folder you've set. These links only contain information related to the link itself, so they are pretty small in file size. However, since the path becomes the same as if the content was actually there, rvgl (and the whole system) sees it normally. I couldn't find anything similar on Windows/NTFS.

### Plans

- create re-volt.log with timestamps to not get overwritten - this could be done using ">> re-voltTIMESTAMP.log"
- manage updates using the official install_rvgl.py (would need to launch app via command line, because install_rvgl.py need confirmation)
- get symlinking working for tracks as well
- integrate points calculator?
- check for live streams?
- randomizer integration?

These are just plans, though, so there's no guarantee whatsoever that they will be implemented. Cheers!
