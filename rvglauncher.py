from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import os
from shutil import rmtree
from kivy.config import Config



Config.set('graphics', 'width', '1024')
Config.set('graphics', 'height', '576')
Config.write()
appkv = Builder.load_file('rvlauncher.kv')

installs = ['/home/hajducsekb/rvgl_weekly/', '/home/hajducsekb/RVGL/']
carclass = {
    'Rookies': 'rc,mite,phat,moss,mud,beatall,volken,tc6,bigvolt,jg6rc',
    'Amateurs': 'candy,flag,gencar,tc9,tc12,mouse,tc5,jg3loco,tc11',
    'Advanced': 'tc4,sgt,bossvolt,jg2fulonx,matraxl,tc2,tc3,fone,r5,dino,rotor,tc8',
    'Semi-Pro': 'amw,adeon,jg1jg7,tc7,tc1',
    'Pro': 'cougar,sugo,panga,jg5purpxl,jg4snw35,toyeca'
}

class HomeScreen(Screen):
    rvglpath='MODIFYTOYOURPATH'
    currentpath = ''
    def setPath(self, rvpath):
        self.currentpath = rvpath
        print(self.currentpath)
        print(rvpath)
    installPicker = DropDown()
    ClassList = []
    def on_pre_enter(self):
        for path in installs:
            btn = Button(text=str(path), size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.installPicker.select(btn.text))
            btn.bind(on_release=lambda btn: self.setPath(path))
            self.installPicker.add_widget(btn)
            print(path)
        self.installPicker.bind(on_select=lambda instance, x: setattr(self.ids.dropdownbtn, 'text', x))
        for k, v in carclass.items():
            label = Label(text=str(k))
            checkbox = CheckBox(active=True)
            self.ids.classrow.add_widget(label)
            self.ids.checkboxes.add_widget(checkbox)
            self.ClassList.append(checkbox)
        print(self.ClassList)
        for item in self.ClassList:
            print(item.active)

    def gameLaunch(self):
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
        os.system(os.path.join(self.rvglpath, 'rvgl -nointro'))

    def clearCars(self):
        rmtree(os.path.join(self.rvglpath, 'cars'))
        
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

class RVGLauncher(App):
    
    def build(self):
        return sm 

if __name__ == "__main__":
    RVGLauncher().run()