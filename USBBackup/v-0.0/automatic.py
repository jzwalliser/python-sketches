import os
import codecs
import shutil
import traceback
import time

source = open("usb.txt")
dest = open("to.txt")
ftypes = open("filetypes.txt")
filt = open("filter.txt")
s = source.read()
f = ftypes.read().split()
d = dest.read()
filte = filt.read()
filt.close()
length = len(s)
dest.close()
ftypes.close()
source.close()
logs = ""

files = []

def getfolder(string):
    for i in range(len(string)):
        if string[len(string) - i - 1] == "/":
            return string[0:len(string) - i - 1]

def dfs(file):
    global files
    try:
        listdir = os.listdir(file)
    except:
        return
    for i in range(len(listdir)):
        files.append(file + "/" + listdir[i])
        if os.path.isdir(file + "/" + listdir[i]):
            dfs(file + "/" + listdir[i])

def copy(lst):
    global logs
    for i in lst:
        try:
            os.makedirs(getfolder(d + i[length:]))
            print("Directory created:",getfolder(d + i[length:]))
            logs += "Directory created: " + str(getfolder(d + i[length:])) + "\r\n"
        except:
            pass
        try:
            if not os.path.isdir(i):
                if "filetypes" in filte:
                    for m in f:
                        if i.endswith(m):
                            shutil.copy(i,d + i[length:])
                            print("File Copied:",i,"=>",d + i[length:])
                            logs += "File Copied: " + i + " => " + d + i[length:] + "\r\n"
                        else:
                            print("Filtered out:",i)
                            logs += "Filtered out: " + i + "\r\n"
                else:
                    shutil.copy(i,d + i[length:])
                    print("File Copied:",i,"=>",d + i[length:])
                    logs += "File Copied: " + i + " => " + d + i[length:] + "\r\n"
        except Exception as err:
            print("Fail:",i,"=>",d + i[length:],err)
            logs += "Fail: " + i + " => " + d + i[length:] + " " + err + "\r\n"

while True:
    try:
        os.listdir(s)
    except:
        pass
    else:
        break

dfs(s)
copy(files)
log = open("logs.txt","wb")
log.write(logs.encode("utf-8"))
log.close()
print("Output written to logs.txt.")
time.sleep(4)
