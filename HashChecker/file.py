import tkinter
import tkinter.ttk
import tkinter.messagebox
import tkinter.filedialog
#import tkdnd
import hashlib
import ctypes
import threading
import inspect
#import pyperclip
root = tkinter.Tk()
thread = None
chunksize = 1000000
notebook = tkinter.ttk.Notebook(root)
frame1 = tkinter.ttk.Frame()
frame1.pack()
selectfile = tkinter.ttk.Frame(frame1)
selectfile.pack()
path = tkinter.ttk.Entry(selectfile)
path.grid(row=0,column=0)
def choose():
    file = tkinter.filedialog.askopenfilename()
    if file:
        path.delete(0,tkinter.END)
        path.insert(0,file)
choosefile = tkinter.ttk.Button(selectfile,text="选择文件",command=choose)
choosefile.grid(row=0,column=1)

def start():
    try:
        descriptor = open(path.get(),"rb")
    except:
        tkinter.messagebox.showerror("错误","无法打开 \"" + path.get() + "\"。")
    else:
        for i in checkbuttons:
            i.configure(state=tkinter.DISABLED)
        
        choosefile.configure(state=tkinter.DISABLED)
        path.configure(state=tkinter.DISABLED)
        work.configure(state=tkinter.DISABLED)
        output.configure(state=tkinter.NORMAL)
        output.delete(0.0,tkinter.END)
        output.configure(state=tkinter.DISABLED)
        
        try:
            byte = descriptor.read()
        except:
            tkinter.messagebox.showerror("错误","无法打开 \"" + path.get() + "\"。")
            descriptor.close()
            return
        else:
            stop.configure(state=tkinter.NORMAL)
        
        length = len(byte)
        print(length)
        descriptor.close()
        
        for i in algorithms:
            if i.get() != "":
                hashdigest = hashlib.new(i.get())
                for j in range(0,length,chunksize):
                    hashdigest.update(byte[j:j + chunksize])
                    progressbar.configure(value=(j + 1) / length * 100)
                progressbar.configure(value=100)
                output.configure(state=tkinter.NORMAL)
                output.insert(tkinter.END,i.get() + ": ")
                output.insert(tkinter.END,hashdigest.hexdigest())
                output.insert(tkinter.END,"\n")
                output.configure(state=tkinter.DISABLED)
    finally:
        for i in checkbuttons:
            i.configure(state=tkinter.NORMAL)
        choosefile.configure(state=tkinter.NORMAL)
        path.configure(state=tkinter.NORMAL)
        work.configure(state=tkinter.NORMAL)
        stop.configure(state=tkinter.DISABLED)

def digest():
    global thread
    thread = threading.Thread(target=start)
    thread.start()
work = tkinter.ttk.Button(selectfile,text="开始",command=digest)
work.grid(row=0,column=2)


def kill():
    for i in checkbuttons:
        i.configure(state=tkinter.NORMAL)
    choosefile.configure(state=tkinter.NORMAL)
    path.configure(state=tkinter.NORMAL)
    work.configure(state=tkinter.NORMAL)
    stop.configure(state=tkinter.DISABLED)
    if thread.is_alive():
        killthread(thread.ident,SystemExit)

def killthread(tid,exctype): #杀线程的代码来源于：https://tomerfiliba.com/recipes/Thread2
    try:
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("Invalid Thread ID")
        elif res != 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")
    except Exception as err:
        print(err)

stop = tkinter.ttk.Button(selectfile,text="停止",command=kill,state=tkinter.DISABLED)
stop.grid(row=0,column=3)
algorithms = []
hashes = ["md5","blake2s","sha3_224","sha3_384","sha256","sha3_512","sha1","sha512","blake2b","sha384","sha3_256","sha224"]
checkbuttons = []
checkbuttonframe = tkinter.ttk.Frame(frame1)
checkbuttonframe.pack()
for i in range(len(hashes)):
    strvar = tkinter.StringVar()
    algorithms.append(strvar)
    check = tkinter.Checkbutton(checkbuttonframe,text=hashes[i].upper(),variable=strvar,onvalue=hashes[i],offvalue="")
    checkbuttons.append(check)
    check.grid(row=i // 6,column=i % 6)

output = tkinter.Text(frame1,relief="flat")
output.pack()
progressbar = tkinter.ttk.Progressbar(frame1)
progressbar.pack(fill=tkinter.BOTH)

def copy():
    pyperclip.copy(output.get(0.0,tkinter.END))
root.mainloop() #拖拽文件,对比文件,多文件列表,对比剪贴板,显示文件名,大小,日期
