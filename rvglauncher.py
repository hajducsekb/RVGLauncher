from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty
from kivy.uix.popup import Popup
from kivy.factory import Factory
from glob import glob
import os
from shutil import rmtree
from kivy.config import Config
import sys
from pathlib import Path


#initial config
Config.set('graphics', 'width', '1024')
Config.set('graphics', 'height', '576')
Config.write()
appkv = Builder.load_file('rvlauncher.kv')

#directory of launcher 9executable
if getattr(sys, 'frozen', False):
    workingpath = os.path.dirname(sys.executable)
else:
    workingpath = os.path.dirname(os.path.abspath(__file__))

carclass = {}
customcarclass = {}
with open(os.path.join(workingpath, 'launchparams.txt'), 'r') as pathtxt:
        rvlaunchargs = pathtxt.read().replace('\n','')

with open(os.path.join(workingpath, 'stockcars.txt'), 'r') as carlist:
    carcontent = carlist.readlines()
    for row in carcontent:
        if 'version:' in row:
            curr_version = float(row.split(':')[1])
            print(curr_version)
        elif row != '':
            seperated = row.split(':')
            print(seperated)
            carclass[seperated[0]] = seperated[1].replace('\n', '')
if os.path.isfile(os.path.join(workingpath, 'customlists.txt')) == True:
    with open(os.path.join(workingpath, 'customlists.txt'), 'r') as customcarlist:
        carcontent = customcarlist.readlines()
        for row in carcontent:
            if row != '':
                seperated = row.split(':')
                print(seperated)
                customcarclass[seperated[0]] = seperated[1].replace('\n', '')
        print(customcarclass)

class HomeScreen(Screen):
    with open(os.path.join(workingpath, 'rvglpath.txt'), 'r') as pathtxt:
        rvglpath = StringProperty(pathtxt.read().replace('\n',''))
    with open(os.path.join(workingpath, 'carspath.txt'), 'r') as pathtxt:
        carpath = StringProperty(pathtxt.read().replace('\n',''))
    currentpath = ''
    def setPath(self, rvpath):
        self.currentpath = rvpath
        print(self.currentpath)
        print(rvpath)
    installPicker = DropDown()
    ClassList = []
    CustomClassList = []
    def __init__(self, **kwargs):
        super().__init__()
        #creating the dropdown with the rvgl installs
        '''for path in installs:
            btn = Button(text=str(path), size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.installPicker.select(btn.text))
            btn.bind(on_release=lambda btn: self.setPath(path))
            self.installPicker.add_widget(btn)
            print(path)'''
        self.installPicker.bind(on_select=lambda instance, x: setattr(self.ids.dropdownbtn, 'text', x))
        #creating labels and their respective checkboxes
        currentItem = 0
        for k, v in carclass.items():
            currentItem += 1
            label = Label(text=str(k))
            if currentItem % 3 == 1:
                checkbox = CheckBox(active=False, background_checkbox_down='stock.png', background_checkbox_normal='stock_inactive.png')
                self.ids.classrow.add_widget(label)
            elif currentItem % 3 == 2:
                checkbox = CheckBox(active=False, background_checkbox_down='io.png', background_checkbox_normal='io_inactive.png')
            else:
                checkbox = CheckBox(active=False, background_checkbox_down='bonus.png', background_checkbox_normal='bonus_inactive.png')
            self.ids.checkboxes.add_widget(checkbox)
            self.ClassList.append(checkbox)
        for k, v in customcarclass.items():
            label = Label(text=str(k))
            checkbox = CheckBox(active=False, background_checkbox_down='custom.png', background_checkbox_normal='custom_inactive.png')
            self.ids.customclassrow.add_widget(label)
            self.ids.customcheckboxes.add_widget(checkbox)
            self.CustomClassList.append(checkbox)
        print(self.ClassList)
        print(self.CustomClassList)
        for item in self.ClassList:
            print(item.active)

    def gameLaunch(self):
        self.rvglpath = self.ids.rvinstpath.text
        self.carpath = self.ids.carpath.text
        with open(os.path.join(workingpath, 'rvglpath.txt'), 'w') as pathtxt:
            pathtxt.write(self.rvglpath + '\n')
        with open(os.path.join(workingpath, 'carspath.txt'), 'w') as pathtxt:
            pathtxt.write(self.carpath + '\n')
        os.chdir(self.rvglpath)
        #from install_rvgl import update
        currentItem = 0
        if os.path.isdir(os.path.join(self.rvglpath, 'cars')) == False: 
            os.mkdir(os.path.join(self.rvglpath, 'cars'))
        for k, v in carclass.items():
            if self.ClassList[currentItem].active == True:
                carfolder = v.split(',')
                print(v)
                for car in carfolder:
                    os.system('ln -s ' + os.path.join(self.ids.carpath.text, car) + ' ' + os.path.join(self.rvglpath, 'cars', car))
            currentItem += 1
        req = ['misc', 'q', 'wincar', 'wincar2', 'wincar3', 'wincar4']
        for car in req:
            os.system('ln -s ' + os.path.join(self.ids.carpath.text, car) + ' ' + os.path.join(self.rvglpath, 'cars', car))
        os.system(os.path.join(self.rvglpath, 'rvgl -nointro ' + str(rvlaunchargs)))

    def clearCars(self):
        self.rvglpath = self.ids.rvinstpath.text
        if os.path.isdir(os.path.join(self.rvglpath, 'cars')):
            rmtree(os.path.join(self.rvglpath, 'cars'))
        else: 
            print(os.path.join(self.rvglpath, 'cars') + ' does not exist.')
            
    '''def fixcases(self):
        self.rvglpath = self.ids.rvinstpath.text
        os.system(os.path.join(self.rvglpath, 'fix_cases'))'''
    def fixcases(self):
        self.rvglpath = self.ids.rvinstpath.text
        for path in Path(os.path.join(self.rvglpath, 'levels')).rglob('*'):
            pathlist = str(path).split('/levels/')
            if pathlist[1] == pathlist[1].lower():
                pass
            else:
                os.rename(os.path.join(self.rvglpath, 'levels', str(pathlist[1])), os.path.join(self.rvglpath, 'levels', str(pathlist[1]).lower()))
                print('RENAMING TRACK')
                print(os.path.join(self.rvglpath, 'levels', str(pathlist[1])) + ' TO ' + os.path.join(self.rvglpath, 'levels', str(pathlist[1]).lower()))
            #print(path)
        for path in Path(os.path.join(self.rvglpath, 'cars')).rglob('*'):
            pathlist = str(path).split('/cars/')
            if pathlist[1] == pathlist[1].lower():
                pass
            else:
                os.rename(os.path.join(self.rvglpath, 'cars', str(pathlist[1])), os.path.join(self.rvglpath, 'cars', str(pathlist[1]).lower()))
                print('RENAMING CAR')
                print(os.path.join(self.rvglpath, 'cars', str(pathlist[1])) + ' TO ' + os.path.join(self.rvglpath, 'cars', str(pathlist[1]).lower()))
            #print(path)
        
    def GoToSettings(self):
        sm.transition.direction = 'right'
        sm.current = 'settings'
    def GoToDev(self):
        sm.transition.direction = 'left'
        sm.current = 'dev'
        
class SettingsScreen(Screen):
    currentpath = ''
    rvlaunchargs_local = rvlaunchargs
    
    def setPath(self, rvpath):
        self.currentpath = rvpath
        print(self.currentpath)
        print(rvpath)
    installPicker = DropDown()
    def GoToHome(self):
        global rvlaunchargs
        rvlaunchargs = self.ids.launchargtext.text
        with open(os.path.join(workingpath, 'launchparams.txt'), 'w') as pathtxt:
            pathtxt.write(rvlaunchargs + '\n')
        sm.transition.direction = 'left'
        sm.current = 'home'

    def cliHelp(self):
        popup = Popup(title='Command Line Help', content=Label(text='[b]sessionlog:[/b] Log race sessions to profiles folder\n[b]tvtime:[/b] Enable F5 and F6 cameras\n[b]savereplays:[/b] Automatically save replays when finishing\n[b]nouser:[/b] Launch with stock content only\n(See also: nousercars, nouserlevels, nouserskins, nousersfx)\n[b]nointro:[/b] Skip the game\'s intro logos\n[b]aspect <width> <height> <lens>:[/b] Aspect ratio and FOV\n[b]hidechat:[/b] Hide chat mid-race (still visible with F12/tab)\n[b]nopause:[/b] Keep the game running even in background\n[b]noshader:[/b] Use legacy renderer\n[b]showping:[/b] Use Ctrl + P for network stats in Multiplayer', markup = True, halign = 'center'),
              auto_dismiss=True,size_hint=(None, None), size=(600, 400))
        popup.open()
        
class DevScreen(Screen):
    
    def rename(self, filelist, oldname, newname):
        for file in filelist:
            if 'reversed' not in file:
                filename = file.split(os.path.join('levels', newname))[1]
                rvdir = file.split(os.path.join('levels', newname))[0]
                if oldname in filename:
                    newfile = filename.replace(oldname, newname)
                    print(os.path.join(rvdir, 'levels', newname, newfile))
                    newpath = os.path.join(rvdir, 'levels', newname.replace('/', ''), newfile.replace('/', ''))
                    os.rename(file, newpath)
            elif 'reversed' in file:
                filename = file.split(os.path.join('levels', newname, 'reversed'))[1]
                rvdir = file.split(os.path.join('levels', newname, 'reversed'))[0]
                if oldname in filename:
                    newfile = filename.replace(oldname, newname)
                    print(os.path.join(rvdir, 'levels', newname, 'reversed', newfile))
                    newpath = os.path.join(rvdir, 'levels', newname.replace('/', ''), 'reversed', newfile.replace('/', ''))
                    os.rename(file, newpath)
    
    def renamefolder(self):
        print('hello')
        oldname = self.ids.renamefrom.text.replace('\n', '')
        newname = self.ids.renameto.text.replace('\n', '')
        os.chdir(os.path.join(self.ids.devinstall.text, 'levels'))
        os.rename(oldname,newname)
        filelist = glob(os.path.join(self.ids.devinstall.text, 'levels', newname, '*'))
        self.rename(filelist, oldname, newname)
        if os.path.isdir(os.path.join(self.ids.devinstall.text, 'levels', newname, 'reversed')):
            filelist_rev = glob(os.path.join(self.ids.devinstall.text, 'levels', newname, 'reversed', '*'))
            self.rename(filelist_rev, oldname, newname)
            
    def GoToHome(self):
        sm.transition.direction = 'right'
        sm.current = 'home'
        
        
# create a dropdown with 10 buttons

# create a big main button

# show the dropdown menu when the main button is released
# note: all the bind() calls pass the instance of the caller (here, the
# mainbutton instance) as the first argument of the callback (here,
# dropdown.open.).

# one last thing, listen for the selection in the dropdown list and
# assign the data to the button text.
#dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))

sm = ScreenManager()
sm.add_widget(HomeScreen(name='home'))
sm.add_widget(SettingsScreen(name='settings'))
sm.add_widget(DevScreen(name='dev'))

class RVGLauncher(App):
    
    def build(self):
        return sm 

if __name__ == "__main__":
    RVGLauncher().run()
