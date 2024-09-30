#作者：Jzwalliser
#日期：2024/2/3

import tkinter
import tkinter.ttk
import tkinter.filedialog
import tkinter.messagebox
import tkinter.scrolledtext
import pyzbar
import pyzbar.pyzbar
import PIL
import PIL.Image
import pyperclip
import sys
import os

def getpath(file): #获取当前目录
    if getattr(sys,'frozen',None): #是否打包了？
        return os.path.join(sys._MEIPASS,file) #打包了，那就返回临时的工作路径
    else: #还没打包
        return os.path.join(os.path.abspath("."),file) #返回当前路径

def readqr(pic): #读取二维码
    content = [] #读取到的内容
    picture = PIL.Image.open(pic) #打开图片
    qrcode = pyzbar.pyzbar.decode(picture) #扫描二维码
    for qr in qrcode:
        url = qr.data.decode('utf-8') #解码
        content.append(url)
    return content

def showqr():
    filename = tkinter.filedialog.askopenfilename() #打开文件对话框
    copycontent.configure(text="复制内容")
    if filename != "": #如果有打开文件
        try:
            content = readqr(filename)
        except: #如果图片无法读取
            tkinter.messagebox.showerror("错误","无法读取图片\"" + filename + "\"。")
        else: #图片正常，可以读取
            if content != []: #如果这是个二维码
                for i in content:
                    textpad.configure(state=tkinter.NORMAL) #解锁
                    textpad.insert(tkinter.INSERT,i + '\n\n') #插入内容
                    textpad.configure(state=tkinter.DISABLED) #上锁
            else:
                tkinter.messagebox.showinfo("无内容","该二维码中没有任何内容。（你确定这张图是二维码？）")

def copy(): #复制
    pyperclip.copy(textpad.get("0.0",tkinter.END)) #获取文本框中的扫描结果
    copycontent.configure(text="已复制") #提示用户已复制

root = tkinter.Tk() #创建窗口
root.title("二维码扫描器")
root.iconbitmap(getpath("icon_clear.ico"))
textpad = tkinter.scrolledtext.ScrolledText(root)
textpad.pack()
textpad.configure(state=tkinter.DISABLED) #用户不应该写入文本框
openqrcode = tkinter.ttk.Button(root,text="打开图片",command=showqr,width=80)
openqrcode.pack()
copycontent = tkinter.ttk.Button(root,text="复制内容",command=copy,width=80)
copycontent.pack()
root.mainloop()
