import pynput
import pyperclip
import time
import codecs

from pynput import mouse
import pynput.keyboard
from pynput.keyboard import Key
control = mouse.Controller()
keyboard = pynput.keyboard.Controller()

for i in range(1):
    control.position = (420,44)
    control.click(mouse.Button.left,1)
    keyboard.press(Key.ctrl)
    keyboard.press( 'c')
    keyboard.release( 'c')
    keyboard.release(Key.ctrl)
    time.sleep(0.3)
    qn = pyperclip.paste()[-5:]
    time.sleep(0.3)
    control.position = (700,800)
    control.click(mouse.Button.left,1)
    time.sleep(0.2)
    control.position = (988,301)
    control.click(mouse.Button.left,1)
    time.sleep(0.2)
    quest = pyperclip.paste()
    f = codecs.open(qn + " " + quest[2:quest.find("\r")] + ".txt","w","gb2312",errors="ignore")
    f.write(quest)
    f.close()

    keyboard.press(Key.ctrl)
    keyboard.press( 'w')
    keyboard.release( 'w')
    keyboard.release(Key.ctrl)
