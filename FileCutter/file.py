import tkinter
import tkinter.ttk
import tkinter.messagebox
import tkinter.filedialog
import os


current = 1
def fileslice():#grab,title
    global current
    current = 1
    top = tkinter.Toplevel()
    step1 = tkinter.Frame(top)
    file = tkinter.Frame(step1)
    filename = tkinter.Entry(file)
    def choosefile():
        name = tkinter.filedialog.askopenfilename()
        if name:
            filename.delete(0,tkinter.END)
            filename.insert(name,tkinter.INSERT)
    choose = tkinter.Button(file,text="选择文件",command=choosefile)
    title11 = tkinter.Label(step1,text="请选择需要切片的文件：")
    title12 = tkinter.Label(step1,text="请选择保存的位置：")
    folder = tkinter.Frame(step1)
    foldername = tkinter.Entry(folder)
    def choosefolder():
        name = tkinter.filedialog.askfolder()
        if name:
            foldername.delete(0,tkinter.END)
            foldername.insert(name,tkinter.INSERT)
    choosesave = tkinter.Button(folder,text="选择保存的文件夹",command=choosefolder)
    title11.pack()
    file.pack()
    filename.grid(row=0,column=0)
    choose.grid(row=0,column=1)
    title12.pack()
    folder.pack()
    foldername.grid(row=0,column=0)
    choosesave.grid(row=0,column=1)
    step1.grid(row=0,column=0)
    step2 = tkinter.Frame(top)
    info = tkinter.Label(step2)
    title2 = tkinter.Label(step2,text="设置切片大小：")
    size = tkinter.Frame(step2)
    sizelabel = tkinter.Label(size,text="切片大小：")
    sizeentry = tkinter.Entry(size)
    unitvar = tkinter.StringVar()
    unit = tkinter.OptionMenu(size,variable=unitvar,*["a","ab"]) #下拉菜单,父为sizee
    statistics = tkinter.Label(step2)
    def updatestat(event=None):
        chunksize = sizeentry.get() #获取大小
        if not exists(filename.get()): #exists方法
            tkinter.messagebox.showerror("错误","文件" + filename.get() + "不存在。请重新选择文件。")
            prev() #prev方法
            return
        if chunksize != 0:
            filesize = getsize(filename.get())#文件大小
            message = "将生成" + str(filesize //chunksize + int(bool(filesize % chunksize))) + "个文件切片" + ("，最后一个切片的大小为" + formatsize(filesize % chunksize)) * int(bool(filesize % chunksize))
            statistics.configure(text=message)
        else:
            statistics.configure(text="")
    #unit在接收到键盘释放时执行updatestat,unit在选中后执行updatestat
    title2.pack()
    info.pack()
    size.pack()
    sizelabel.grid(row=0,column=0)
    sizeentry.grid(row=0,column=1)
    statistics.pack()
    unit.grid(row=0,column=2)
    def init1():
        prevbutton.configure(state=tkinter.DISABLED)
    def init2():
        prevbutton.configure(state=tkinter.NORMAL)
        if not filename.get():
            tkinter.messagebox.showinfo("选择文件","请选择一个文件以继续。")
            prev()
            return
        if not foldername.get():
            tkinter.messagebox.showinfo("选择文件夹","请选择保存位置以继续。")
            prev()
            return
        if not exists(filename.get()):
            tkinter.messagebox.showerror() #错误同上
            prev()
            return
        info.configure(text="文件：" + filename.get()) #大小,日期之类
    step3 = tkinter.Frame(top)
    title3 = tkinter.Label(step3,text="请设置文件切片的命名方式：")
    usage = tkinter.Label(step3,text="使用<n>来代替序号。")
    naming = tkinter.Frame(step3)
    namelabel = tkinter.Label(naming,text="命名方式：")
    nameentry = tkinter.Entry(naming)
    namepreview = tkinter.Label(step3)
    def updatepreview(event=None):
        if "<n>" in nameentry.get():
            preview = ""
            for i in range(3):
                seq = nameentry.get()
                filesize = getsize()#文件大小
                chunksize = error #切片大小
                slices = filesize // chunksize + int(bool(filesize % chunksize))
                if eqwidth.get():
                    width = errot#log10(slice s)4rttttt4#格式化,同宽
                for j in range(seq.count("<n>")):
                    seq.replace("<n>",num)
                preview += seq + "\n"
            seq += "..."
        else:
            preview = "用<n>来代替序号。如part<n>将生成part1.txt，part2.txt，part3.txt。"
        namepreview.configure(text=preview)
    #checkbtn,init3,bind
    eqwidth = tkinter.IntVar()
    eqwidthbtn = tkinter.Checkbutton(step3,text="使序号等宽",variable=eqwidth,command=updatepreview)
    title3.pack()
    naming.pack()
    namelabel.grid(row=0,column=0)
    nameentry.grid(row=0,column=1)
    eqwidthbtn.pack()
    namepreview.pack()
    #nameentry在收到键盘释放执行updatepreview
    def init3():
        if not sizeentry.get().isdigit():
            tkinter.messagebox.showinfo("切片大小","请修改切片大小。")
            prev()
            return
        if "." in sizeentry.get():
            tkinter.messagebox.showinfo("小数")
        nameentry.delete(0,tkinter.END)
        nameentry.insert(tkinter.INSERT,"part<n>." + filename.get().split(".")[-1]) #没有后缀怎么办
    step4 = tkinter.Frame(top)
    summary = tkinter.Label(step4)
    summary.pack()
    def init4():pass

    bottombar = tkinter.Frame(top)

    def next_():
        global current
        cmds = [-1,init1,init2,init3,init4]
        steps = [-1,step1,step2,step3,step4]
        steps[current].grid_forget()
        current += 1
        steps[current].grid(row=0,column=0)
        cmds[current]()
    def prev():
        global current
        cmds = [-1,init1,init2,init3,init4]
        steps = [-1,step1,step2,step3,step4]
        steps[current].grid_forget()
        current -= 1
        steps[current].grid(row=0,column=0)
        cmds[current]()
    
    nextbutton = tkinter.Button(bottombar,text="下一步",command=next_)
    prevbutton = tkinter.Button(bottombar,text="上一步",command=prev)
    nextbutton.grid(row=0,column=0)
    prevbutton.grid(row=0,column=1)
    bottombar.grid(row=1,column=0)

root = tkinter.Tk()
btn = tkinter.Button(root,text="aaa",command=fileslice)
btn.pack()
fileslice()
root.mainloop()
