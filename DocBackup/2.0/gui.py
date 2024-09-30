#coding=utf-8
import tkinter
import tkinter.ttk
import tkinter.filedialog
import tkinter.messagebox
import os
import time
import codecs

os.startfile("silent.vbs")
time.sleep(1)

root = tkinter.Tk()
l = tkinter.Label(root,text="已关闭希沃管家后台进程。")
l.pack()
l2 = tkinter.Label(root,text="by ZHZX G1-3 SJZ jzwalliser")
l2.pack()

def choose():
    folder = tkinter.filedialog.askdirectory()
    write = codecs.open("dest.txt","w","utf-8")
    write.write(folder + "/")
    write.close()
    tkinter.messagebox.showinfo("","点击确定，然后本应用程序将会隐藏窗口，在后台运行。任何打开的文档、表格、PPT都将被复制到您刚才选择的文件夹中。\n请勿重复打开该应用程序。\n时间仓促，因此应用比较粗糙。请勿介意，能用就好。\n一个文档被打开后，可能需要10-20秒才会识别到它，因此不要心急。\n最后，如果需要关闭本应用的后台进程，请用管理员权限运行refresh！注意，管理员权限！（右键refresh，以管理员身份运行）这样就不会再复制文档。\nZHZH G1-3 SJZ")
    os.startfile("backup.exe")
    root.withdraw()

button = tkinter.ttk.Button(root,text="选择保存的文件夹",command=choose)
button.pack()
root.mainloop()
