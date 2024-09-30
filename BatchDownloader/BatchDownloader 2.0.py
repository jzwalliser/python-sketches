import tkinter
import tkinter.messagebox
import tkinter.filedialog
import tkinter.scrolledtext
import tkinter.ttk
import urllib.request
import os
import codecs
import threading
import time
import sys
import pathlib
import pickle
#import pyperclip
import ctypes
import traceback

def choosedir(folder):
    path = tkinter.filedialog.askdirectory()
    if path:
        folder.delete(0,tkinter.END)
        folder.insert(tkinter.INSERT,path)

def loadfromtxt(window,tasks):
    files = tkinter.filedialog.askopenfilenames(filetypes=[("Text File","*.txt")])
    urls = errs = ""
    for i in files:
        try:
            urls += "\n" + read(i)
        except:
            errs += "\n" + i
    if files:
        add(urls,errs,window,tasks)
        
def read(file):
    descriptor = codecs.open(file,"r")
    content = descriptor.read()
    descriptor.close()
    return content

defaultaction = "ask"
def add(urls,errs,window,tasks):
    if defaultaction == "ask":
        top = tkinter.Toplevel()
        frame1 = tkinter.Frame(top)
        load = tkinter.ttk.Label(frame1,text="已加载的内容")
        load.pack()
        showcontent = tkinter.scrolledtext.ScrolledText(frame1)
        showcontent.insert("0.0",urls)
        showcontent.configure(state=tkinter.DISABLED)
        showcontent.pack()
        if errs:
            fail = tkinter.ttk.Label(frame,text="以下文件加载失败：\n" + errs)
            fail.pack()
        def overwritecontent():
            overwrite(urls,setdefault.get(),top,tasks)
        def appendcontent():
            append(urls,setdefault.get(),top,tasks)
        frame1.pack()
        frame2 = tkinter.Frame(top)
        overwritebutton = tkinter.ttk.Button(frame2,text="覆盖掉原来内容",command=overwritecontent)
        appendbutton = tkinter.ttk.Button(frame2,text="添加任务",command=appendcontent)
        overwritebutton.grid(row=0,column=0)
        appendbutton.grid(row=0,column=1)
        cancelbutton = tkinter.ttk.Button(frame2,text="取消",command=top.destroy)
        cancelbutton.grid(row=0,column=2)
        setdefault = tkinter.IntVar()
        default = tkinter.ttk.Checkbutton(frame2,text="默认动作",variable=setdefault,onvalue=1,offvalue=0)
        default.grid(row=0,column=3)
        frame2.pack()
        block(top,window)
    elif defaultaction == "overwrite":
        overwrite(urls,tasks=tasks)
    elif defaultaction == "append":
        append(urls,tasks=tasks)

def overwrite(url,setdefault=False,window=None,tasks=None):
    global defaultaction
    if setdefault:
        defaultaction = "overwrite"
    if window:
        window.destroy()
    tasks.delete(0.0,tkinter.END)
    tasks.insert(tkinter.INSERT,url)

def append(url,setdefault=False,window=None,tasks=None):
    global defaultaction
    if setdefault:
        defaultaction = "append"
    if window:
        window.destroy()
    tasks.insert("\n" + url,tkinter.INSERT)

class Download(tkinter.Frame):
    def __init__(self,master,url,filename,**kwargs):
        super().__init__(master,**kwargs)
        self.url = url
        self.filename = filename
        showfilename = tkinter.ttk.Label(self,text=getname(filename))
        self.retry = tkinter.ttk.Button(self,command=self.retrydownload)
        self.progressbar = tkinter.ttk.Progressbar(self)
        frame_status = tkinter.Frame(self)
        self.speed = tkinter.ttk.Label(frame_status,text="未开始")
        self.frac = tkinter.ttk.Label(frame_status)
        self.eta = tkinter.ttk.Label(frame_status)
        self.percent = tkinter.ttk.Label(frame_status)
        frame_url = tkinter.Frame(self)
        showurl = tkinter.ttk.Entry(frame_url)
        showurl.insert(0,url)
        showurl.configure(state=tkinter.DISABLED)
        copyurl = tkinter.ttk.Button(frame_url,text="复制",command=self.copy)
        self.status = "not_started"
        self.cancel = tkinter.ttk.Button(self,text="取消下载",command=self.killdownload,state=tkinter.DISABLED)
        showfilename.pack()
        self.progressbar.pack(fill=tkinter.X)
        frame_status.pack()
        self.speed.grid(row=0,column=0,ipadx=10)
        self.frac.grid(row=0,column=1,ipadx=10)
        self.percent.grid(row=0,column=2,ipadx=10)
        self.eta.grid(row=0,column=3,ipadx=10)
        frame_url.pack(fill=tkinter.X)
        showurl.grid(row=0,column=0,sticky=(tkinter.E,tkinter.W))
        copyurl.grid(row=0,column=1,sticky=(tkinter.E,tkinter.W))
        self.cancel.pack(fill=tkinter.X)

    def startdownload(self):
        def download():
            try:
                urllib.request.urlretrieve(self.url,self.filename,self.hook)
            except:
                self.fail()
                traceback.print_exc()
            else:
                self.finish()
        self.status = "downloading"
        self.speed.configure(text="连接中")
        self.thread = threading.Thread(target=download)
        self.starttime = time.time()
        self.lasttime = self.starttime
        self.thread.start()
        self.cancel.configure(state=tkinter.NORMAL)
        self.lastreceived = 0

    def hook(self,blocks,blocksize,totalsize): #注意totalsize=-1时
        if time.time() - self.lasttime > 1:
            received = blocks * blocksize
            percent = received * 100 // totalsize
            speed = received - self.lastreceived
            left = totalsize - received
            self.progressbar.configure(value=percent)
            self.frac.configure(text=formatfrac(received,totalsize))
            self.percent.configure(text=str(percent) + "%")
            self.speed.configure(text=formatspeed(speed))
            if speed:
                self.eta.configure(text="剩余约" + formateta(left / (speed)))
            self.lastreceived = received
            self.lasttime = time.time()
        
    def fail(self):
        self.status = "failed"
        self.retry.configure(text="重试")
        self.cancel.pack_forget()
        self.retry.pack()
        self.speed.configure(text="下载失败")
        self.percent.configure(text="")
        self.frac.configure(text="")
        self.eta.configure(text="")

    def retrydownload(self):
        self.retry.pack_forget()
        self.cancel.pack()
        self.startdownload()

    def finish(self):
        self.speed.configure(text="下载完成")
        self.percent.configure(text="    ")
        self.frac.configure(text="文件总大小：" + formatsize(self.lastreceived))
        self.speed.configure(text="平均速度：" + formatspeed(self.lastreceived / (time.time() - self.starttime)))
        self.eta.configure(text="总耗时：" + formateta(time.time() - self.starttime))
        self.status = "succeed"
        self.cancel.pack_forget()
        
        def openfolder():
            os.startfile(getfolder(self.filename))
        self.openfolderbutton = tkinter.ttk.Button(self,text="打开文件夹",command=openfolder)
        self.openfolderbutton.pack()

    def copy(self):
        pyperclip.copy(self.url)

    def killdownload(self):
        killthread(self.thread.ident,SystemExit)
        self.fail()
        self.retry.configure(text="重新下载")
        self.speed.configure(text="已取消")
        self.status = "aborted"

def getname(path):
    return path[-formatpath(path)[::-1].find("/"):]

def getfolder(path):
    return path[:len(getname(path))]

def formatfrac(received,totalsize):
    return formatsize(received) + "/" + formatsize(totalsize)

def formatspeed(speed):
    return formatsize(speed) + "/s"

def formateta(eta):
    if eta <= 60:
        return str(int(eta)) + "秒"
    if 60 < eta <= 300:
        return str(int(eta // 60)) + "分" + str(int(eta % 60)) + "秒"
    if 300 < eta <= 3600:
        return str(int(eta // 60)) + "分"
    if 3600 < eta <= 10800:
        return str(int(eta // 3600)) + "时" + str(int(eta % 3600 // 60)) + "分"
    if 10800 < eta <= 86400:
        return str(int(eta // 3600)) + "时"
    if 86400 < eta <=259200:
        return str(int(eta // 86400)) + "天" + str(int(eta % 86400 // 3600)) + "时"
    if eta > 259200:
        return str(int(eta // 86400)) + "天"

def formatsize(size):
    if size <= 1200:
        return str(size) + "B"
    if 1200 < size <= 10239:
        return str(size * 10 // 1024 / 10) + "KB"
    if 10239 < size <= 1228800:
        return str(size // 1024) + "KB"
    if 1228800 < size <= 10485759:
        return str(size * 10 // 1048576 / 10) + "MB"
    if size > 10485759:
        return str(size // 1048576) + "MB"

def formatpath(path):
    for i in range(path.count("\\")):
        path = path.replace("\\","/")
    return path

def formatdir(path):
    formatted = formatpath(path)
    if formatted[-1] != "/":
        formatted += "/"
    return formatted

def add_task():
    global defaultdownloadfolder #必要吗？
    top = tkinter.Toplevel()
    textpad = tkinter.scrolledtext.ScrolledText(top)
    def readclipboard():
        textpad.insert(pyperclip.paste(),tkinter.END)
    frame1 = tkinter.Frame(top)
    paste = tkinter.ttk.Button(frame1,text="从剪贴板复制",command=readclipboard)
    separate = tkinter.ttk.Label(frame1,text="或")
    def loadfile():
        loadfromtxt(top,textpad) #可能需要释放grab
    load = tkinter.ttk.Button(frame1,text="从文本文档加载",command=loadfile)
    frame1.pack()
    paste.grid(row=0,column=0)
    separate.grid(row=0,column=1)
    load.grid(row=0,column=2)
    textpad.pack()
    frame2 = tkinter.Frame(top)
    savepath = tkinter.ttk.Entry(frame2)
    def selectfolder():
        choosedir(savepath)
    select = tkinter.ttk.Button(frame2,text="选择保存的文件夹",command=selectfolder)
    frame2.pack()
    savepath.grid(row=0,column=0)
    select.grid(row=0,column=1)
    frame3 = tkinter.Frame(top)
    def okay():
        global defaultdownloadfolder
        if savepath.get():
            defaultdownloadfolder = savepath.get()
        else:
            tkinter.messagebox.showwarning("未选择保存的目录","请选择一个文件夹，用于保存下载的文件。")
            selectfolder()
            return
        saveas = pathlib.Path(formatpath(savepath.get()))
        if not saveas.exists():
            try:
                os.makedirs(formatpath(savepath.get()))
            except:
                tkinter.messagebox.showerror("无法保存文件到此处","无法创建文件夹" + formatpath(savepath.get()) + "。请重新选择文件夹。")
                selectfolder()
                return
        for i in textpad.get("0.0",tkinter.END).splitlines():
            filename = formatdir(savepath.get()) + retrname(i)
            assigntask(i,filename)
        top.destroy()
    ok = tkinter.ttk.Button(frame3,text="确定",command=okay)
    cancel = tkinter.ttk.Button(frame3,text="取消",command=top.destroy)
    frame3.pack()
    ok.grid(row=0,column=0)
    cancel.grid(row=0,column=1)
    savepath.insert(0,defaultdownloadfolder)

    def onclose():
        if textpad.get("0.0",tkinter.END).strip():
            close = tkinter.messagebox.askyesnocancel("添加任务","是否将链接添加到任务中？")
            if close:
                okay()
            if close == False:
                top.destroy()
        else:
            top.destroy()
    top.protocol("WM_DELETE_WINDOW",onclose)
    block(top,root)

def retrname(url):
    return getname(url).split("?")[0]

def start_everything():
    start_notstarted()
    start_aborted()
    start_failed()

def start_notstarted():
    for i in tasklist:
        if i.status == "not_started":
            i.startdownload()

def start_aborted():
    for i in tasklist:
        if i.status == "aborted":
            i.startdownload()

def start_failed():
    for i in tasklist:
        if i.status == "failed":
            i.startdownload()

def abort_download():
    for i in tasklist:
        if i.status == "downloading":
            i.killdownload()

root = tkinter.Tk()
topbar = tkinter.Frame(root)
newtask = tkinter.ttk.Button(topbar,text="新建任务",command=add_task)
start1 = tkinter.ttk.Button(topbar,text="开始所有任务",command=start_everything)
start2 = tkinter.ttk.Button(topbar,text="开始新添加的任务",command=start_notstarted)
start3 = tkinter.ttk.Button(topbar,text="重启已取消的任务",command=start_aborted)
start4 = tkinter.ttk.Button(topbar,text="重试失败的任务",command=start_failed)
abort = tkinter.ttk.Button(topbar,text="取消所有任务",command=abort_download)
space = tkinter.ttk.Label(topbar,text="                     ")
topbar.pack()
newtask.grid(row=0,column=0)
space.grid(row=0,column=1)
start1.grid(row=0,column=2)
start2.grid(row=0,column=3)
start3.grid(row=0,column=4)
start4.grid(row=0,column=5)
abort.grid(row=0,column=6)

def scroll(event):
    canvas.configure(scrollregion=canvas.bbox(tkinter.ALL))

greatcontainer = tkinter.Frame(root,background="#ff0000")
canvas = tkinter.Canvas(greatcontainer,width=700,height=400,background="white")
canvas.grid(row=0,column=0,ipadx=300,ipady=300)
scrollbar = tkinter.Scrollbar(greatcontainer,orient=tkinter.VERTICAL,command=canvas.yview)
scrollbar.grid(row=0,column=1,sticky=tkinter.NS)
canvas.configure(yscrollcommand=scrollbar.set)
taskcontainer = tkinter.Frame(canvas)
canvas.create_window((0,0),window=taskcontainer,anchor=tkinter.NW)
taskcontainer.bind("<Configure>",scroll)
greatcontainer.pack()

def closeroot():
    for i in tasklist:
        if i.status == "downloading":
            close = tkinter.messagebox.askyesno("仍有任务","仍有文件正在下载中，关闭程序将终止这些任务。是否继续？")
            if close:
                abort_download()
                root.destroy()
                urllib.request.cleanup()
                return
            else:
                return
    root.destroy()
                
root.protocol("WM_DELETE_WINDOW",closeroot)
bottombar = tkinter.Frame(root)
def load():
    saving = tkinter.filedialog.askopenfilename(filetypes=[("Pickle file","*.pickle")])
    if saving:
        try:
            data =  readpickle(saving)
        except:
            tkinter.messagebox.showerror("错误","无法加载" + saving + "。")
            return
        for i in data:
            assigntask(i[0],i[1].i[2]) #注意非法数据！

def export():
    top = tkinter.Toplevel()
    var_downloading = tkinter.IntVar()
    var_notstarted = tkinter.IntVar()
    var_aborted = tkinter.IntVar()
    var_failed = tkinter.IntVar()
    var_downloaded = tkinter.IntVar()
    options = tkinter.Frame(top)
    notstarted = tkinter.ttk.Checkbutton(options,text="未开始",variable=var_notstarted)
    aborted = tkinter.ttk.Checkbutton(options,text="已取消",variable=var_aborted)
    failed = tkinter.ttk.Checkbutton(options,text="失败",variable=var_failed)
    downloaded = tkinter.ttk.Checkbutton(options,text="已完成",variable=var_downloaded)
    downloading = tkinter.ttk.Checkbutton(options,text="正在下载",variable=var_downloading)
    title = tkinter.ttk.Label(top,text="请选择类别以保存为希望的格式")
    title.pack()
    options.pack()
    notstarted.grid(row=0,column=0)
    aborted.grid(row=0,column=1)
    failed.grid(row=0,column=2)
    downloaded.grid(row=0,column=3)
    downloading.grid(row=0,column=4)
    classified = {"not_started":[],"aborted":[],"failed":[],"succeed":[],"downloading":[]}
    for i in tasklist:
        classified[i.status].append((i.url,i.filename))
    def getitems():
        wanted = []
        if var_downloading.get(): #能否优化？
            for i in classified["downloading"]:
                wanted.append((i[0],i[1],"downloading"))
        if var_notstarted.get():
            for i in classified["not_started"]:
                wanted.append((i[0],i[1],"not_started"))
        if var_aborted.get():
            for i in classified["aborted"]:
                wanted.append((i[0],i[1],"downloading"))
        if var_failed.get():
            for i in classified["failed"]:
                wanted.append((i[0],i[1],"failed"))
        if var_downloaded.get():
            for i in classified["succeed"]:
                wanted.append((i[0],i[1],"succeed"))
        return wanted

    def saveastxt():
        file = tkinter.filedialog.asksaveasfilename(filetypes=[("Text File","*.txt")])
        if file:
            descriptor = codecs.open(file,"w","utf-8")
            for i in getitems():
                descriptor.write(i[0] + "\r\n")
            descriptor.close()

    def saveaspickle():
        file = tkinter.filedialog.asksaveasfilename(filetypes=[("Pickle File","*.pickle")])
        if file:
            writepickle(file,getitems())
            
    def saveascsv():
        file = tkinter.filedialog.asksaveasfilename(filetypes=[("Comma separated Values","*.csv")])
        if file:
            descriptor = codecs.open(file,"w","utf-8")
            translation = {"not_started":"未开始","aborted":"已取消","failed":"失败","succeed":"下载完成","downloading":"正在下载"}
            descriptor.write("地址,保存路径,状态\n")
            for i in getitems():
                descriptor.write(i[0] + "," + i[1] + "," + i[2] + "\n")
            descriptor.close()

    savemethods = tkinter.Frame(top)
    txt = tkinter.ttk.Button(savemethods,text="TXT文档",command=saveastxt)
    pkl = tkinter.ttk.Button(savemethods,text="Pickle文件",command=saveaspickle)
    csv = tkinter.ttk.Button(savemethods,text="CSV表格",command=saveascsv)
    askfile = tkinter.ttk.Label(top,text="选择保存的格式")
    askfile.pack()
    savemethods.pack()
    txt.grid(row=0,column=0)
    pkl.grid(row=0,column=1)
    csv.grid(row=0,column=2)
    description = tkinter.ttk.LabelFrame(top,text="我该选择什么格式？")
    introduction = tkinter.ttk.Label(description,text="TXT文档：纯文本文档，记录当前列表的所有下载链接。\nPickle文件：一种很方便的文件形式，记录了链接、保存位置及状态，也可在主页面中直接导入。请注意，不要随意加载此类文件，尤其是从网上下载的，它们可能包含恶意指令。\nCSV文件：表格，记录了链接、保存位置及状态，可方便生成报告。")
    introduction.pack()
    description.pack()
    block(top,root)

root.title("批量下载器")
loadfromfile = tkinter.ttk.Button(bottombar,text="加载列表",command=load)
exporttofile = tkinter.ttk.Button(bottombar,text="导出列表",command=export)
bottombar.pack()
loadfromfile.grid(row=0,column=0)
exporttofile.grid(row=0,column=1)

def readpickle(file):
    descriptor = open(file,"rb")
    content = pickle.load(descriptor)
    descriptor.close()
    return content

def writepickle(file,content):
    descriptor = open(file,"wb")
    pickle.dump(content,descriptor)
    descriptor.close()

def block(top,parent):
    top.grab_set()
    parent.wait_window(top)

tasklist = []
def assigntask(url,filename,status=None):
    downloader = Download(taskcontainer,url=url,filename=filename,width=10)
    tasklist.append(downloader)
    if status == "aborted": #能否优化？
        downloader.fail()
        downloader.retry.configure(text="重新下载")
        downloader.speed.configure(text="已取消")
        downloader.status = "aborted"
    if status == "fail":
        downloader.fail()
    if status == "succeed":
        file = pathlib.Path(formatpath(filename))
        if file.exists():
            downloader.finish()
        else:
            downloader.cancel.pack_forget()
            downloader.retry.pack()
            downloader.retry.configure(text="重新下载")
            downloader.speed.configure(text="文件已被删除或移动")
    downloader.pack(fill=tkinter.X,expand=True)

defaultdownloadfolder = "/home/jzwalliser/桌面"
def killthread(tid,exctype):
    try:
        ctypes.pythonapi.PythonThreadState_SetAsyncExc(ctypes.c_long(tid),ctypes.py_object(exctype))
    except:
        traceback.print_exc()

root.mainloop() #大功告成！

#1. 在加载pkl文件的时候注意非法输入
#2. 在所有节能出错的地方加个try-except
#3. 后面试着把thread 改成process
#4. 把代码整理一下，定义变量之类放到一起
#5. 加个state，即"destroyed"，方便删除任务
#6. 任务失败后，progressbar调为0
#7. 注意，文件大小可能是-1
#8. 主界面的按钮，应当调整为适当状态。
#9. 出现第三窗口时，第二窗口是否需要释放锁？
#10. CSV文件，行末需要加逗号吗？
#11. 是否能实现暂停？
#12. 设置User-Agent
#13. 加menu
#14. 导入txt时自动分析前缀是否http，https，ftp，file
#15. 下载出错后显示详细原因
#16. 邮件下载像可以将其删除、单独编辑
#17. 可能可以去掉append/overwrite选项
#18. 向类中添加"status"方法
