import tkinter
import tkinter.ttk
import tkinter.filedialog
import etk
import codecs
import chardet
import traceback
import pathlib
#import tkdnd

def convert(src,dest,targetcodec):
    dest = prevent_collision(dest)
    try:
        content = open(src,"rb")
    except:
        return 2 #无法读取
    try:
        codec = chardet.detect(content.read())["encoding"]
        #print(codec)
        content.close()
    except:
        traceback.print_exc()
        content.close()
        return 2
    try:
        status = 0 #状态正常
        openfile = codecs.open(src,"r",codec)
    except:
        return 2 #无法读取
    try:
        content = openfile.read()
    except:
        openfile.close()
        status = 1 #解码错误
        openfile = codecs.open(src,"r",codec,errors="ignore")
        try:
            content = openfile.read()
        except:
            openfile.close()
            return 4
        openfile.close()
    try:
        dump = codecs.open(dest,"w",targetcodec)
    except:
        traceback.print_exc()
        return 3 #无法写入
    try:
        dump.write(content)
    except:
        dump.close()
        status = 1 #解码错误
        dump = codecs.open(dest,"w",targetcodec,errors="ignore")
        dump.write(content)
    else:
        dump.close()
    return status

errcode = [-1,"解码错误，生成的文件可能出现乱码或丢失字符。","无法读取文件。","无法写入新文件。","无法解码。"]

def prevent_collision(path):
    filepath = pathlib.Path(path)
    suffix = filepath.suffix
    rename = 0
    name = path[:-len(suffix)]
    #print(name)
    if filepath.exists():
        while filepath.exists():
            #print(name + str(rename))
            rename += 1
            filepath = pathlib.Path(name + str(rename) + suffix)
            
            
        return name + str(rename) + suffix
    else:
        return path

root = tkinter.Tk()

tasks = []
def edit():
    global tasks
    data = etk.edit_list(root,init=tasks,filechooser=True)
    tasks.clear()
    tasklist.delete(0,tkinter.END)
    for i in data:
        tasks.append(i)
    for i in data:
        tasklist.insert(tkinter.END,i)

def startconvert():
    print(tasks)
    for i in range(tasks):
        pass

def selectfolder():
    folder = tkinter.messagebox.askfolder()
    if folder:
        outputfolder.delete(0,tkinter.END)
        outputfolder.insert(folder,tkinter.END)
    
#listbox = tkinter.Listbox(root)
editlist = tkinter.Button(root,text="编辑任务列表",command=edit)
tasklist = tkinter.Listbox(root)
editlist.pack()
tasklist.pack()
output = tkinter.Frame(root)
outputfolder = tkinter.Entry(output)
outputfolder.grid(row=0,column=0)
choosefolder = tkinter.Button(output,text="选择输出文件夹")
choosefolder.grid(row=0,column=1)
output.pack()


#start = tkinter.Button(root,text="开始",command=start)
#output = tkinter.scrolledtext.Scrolledtext(root)

convert("file.py","abc.txt","gb2312")
