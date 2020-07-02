from python_imagesearch.imagesearch import imagesearcharea
from python_imagesearch.imagesearch import region_grabber
from win32gui import GetWindowText, GetForegroundWindow
import keyboard
import mouse
import time
import datetime
import win32com.client
import os
speaker = win32com.client.Dispatch("SAPI.SpVoice")

#my_config = [{'name':'Greater Rift'},{'name':'Bounties'}]
my_conf=[]
keymap = {'./z.bmp':'z', './x.bmp':'x', './c.bmp':'c', './left.bmp':'left'}

start_time=datetime.datetime.now()
interval_map = {'v':[1400,start_time]}

def read_conf(my_config):
    iterdir = iter(os.walk("."))
    next(iterdir)
    for root, dirs, files in iterdir:
        my_config.append({'name':[root[2:]]})
        #print(root[2:])
        #print(files)
    return True

im_region=(627, 997, 1027, 1063)
precision=0.999
im_width = im_region[2] - im_region[0]
im_height = im_region[3] - im_region[1]
aux=-1
heat=-1
build=0
read_conf(my_conf)
while 1:
    if GetWindowText(GetForegroundWindow()) == "Diablo III" and aux == 1:
        if heat<8:
            keyboard.press_and_release('v')
            heat=heat+1
        im = region_grabber(im_region)
        #im.save("actionbar.png")
        for file in keymap:
            pos = imagesearcharea(file,0,0,im_width,im_height,precision,im)
            if pos[0] != -1:
                if len(keymap[file]) == 1:
                    keyboard.press_and_release(keymap[file])
                else:
                    keyboard.press('shift')
                    mouse.click(keymap[file])
                    keyboard.release('shift')            

        for item in interval_map:
            now=datetime.datetime.now()
            if int(((now - interval_map[item][1])*1000).seconds)  > interval_map[item][0]:
                keyboard.press_and_release(item)
                interval_map[item][1] = now
        time.sleep(0.1)
    if keyboard.is_pressed('shift+a'):
        heat=-1
        aux=aux*-1
        print(aux)
        if aux == 1:
            speaker.Speak('Starting '+str(my_conf[build]['name']))
        else:
            speaker.Speak('Waiting')
    if keyboard.is_pressed('shift+q'):
        if build == (len(my_conf)-1):
            build=0
        else:
            build=build+1
        speaker.Speak(my_conf[build]['name'])
    
