#author:Jzwalliser
import time
import os
import codecs
import shutil
import pathlib
import traceback
import sys
import filecmp

start = time.time()
stdout = sys.stdout

class Redirect(): #用于重定向输出，实现同时输出到标准输出（stdout），并将输出保存到字符串
    def __init__(self,dumplogs):
        self.content = ""
        if dumplogs:
            try:
                self.logs = codecs.open("logs.txt","a","utf-8",buffering=0)
            except:
                pass
        self.dumplogs = dumplogs
    def write(self,something):
        try:
            stdout.write(something) #输出到stdout
        except:
            pass
        self.content += something #保存输出
        if self.dumplogs:
            try:
                self.logs.write(something)
            except:
                pass
    def read(self):
        return self.content #读取输出
    def flush(self): #收尾
        stdout.flush()





def read(file,codec="utf-8"): #用于简化读取
    try:
        io = codecs.open(file,"r",codec)
    except:
        print("[!] Unable to read",file + ".\nDetails:")
        traceback.print_exc()
        return ""
    else:
        content = io.read()
        io.close()
        return content

policy = read("policy.txt") #规则文件
filetypes = read("filetypes.txt") #文件类型
keyword = read("keyword.txt") #关键字
filename = read("filename.txt") #文件名
optimize = read("optimize.txt")
loop = read("loop.txt")
dumplogs = read("dumplogs.txt")

redirect = Redirect(eval(dumplogs)) #实例化
sys.stdout = redirect #重定向

print("[*] Author: Jzwalliser")
print("[*] USBBackup Tool")

src = read("source.txt").split() #源文件（夹）
dest = read("dest.txt") #目标文件（夹），即复制到哪里
print()

if src == []:
    print("[!] Source file (folder) not defined.")
    sys.exit()
if dest == "":
    print("[!] Destination file (folder) not defined.")
    sys.exit()

def copy(src,dest): #用于简化整个复制过程，会自动判断文件夹是否存在
    folder = getparent(dest)
    path = pathlib.Path(folder)
    if not path.exists(): #若文件夹不存在，则直接shutil.copy会报错
        try:
            os.makedirs(folder) #所以提前建立文件夹
        except:
            print("[!] Error creating directory \"",f + "\". \nDetails:")
            traceback.print_exc()
    try:
        destfile = pathlib.Path(dest)
        if eval(optimize):
            if destfile.exists():
                if not filecmp.cmp(src,dest):
                    shutil.copy(src,dest) #建完文件夹再复制，这样就不容易异常了
                    print("[+] Copied:",src)
                else:
                    print("[+] Optimization enabled. Skipped repeated file:",src)
            else:
                shutil.copy(src,dest) #建完文件夹再复制，这样就不容易异常了
                print("[+] Copied:",src)
        else:
            shutil.copy(src,dest) #建完文件夹再复制。这样就不容易异常了
            print("[+] Copied:",src)
            
    except:
        print("[!] Error copying \"",str(path) + "\". \nDetails:")
        traceback.print_exc() #打印错误信息
        

def getparent(path): #Todo：看看能否再优化
    for i in reversed(range(len(path))):
        if path[i] == "/":
            return path[:i + 1]

def dfs(src,relative,dest): #用于简化读取
    path = pathlib.Path(src + relative)
    if path.is_dir(): #如果是文件夹
        try:
            children = os.listdir(src + relative) #获取文件夹下的文件
        except:
            print("[!] Unable to read folder \"",str(path) + "\". \nDetails:")
            traceback.print_exc()
        else:
            for i in children: #遍历文件夹下的文件
                dfs(src,relative + "/" + i,dest) #深搜处理每一项
            
    else: #如果是文件
        fsize = os.path.getsize(src + relative) #获取文件大小
        if path.suffix != "":
            ftype = path.suffix[1:].lower() in filetypes #获取文件名后缀。并去掉"."
        else:
            ftype = "<nosuf>" in filetypes
        kword = keyword in path.name #判断文件名中是否包含关键字
        fname = filename == path.stem #判断文件名是否一样；忽略后缀名，即后缀名可以不一样
        absfname = filename == path.name #文件名完全一样
        everything = True
        try:
            copyfile = eval(policy) #解析自定义规则
        except:
            print("[!] Error analyzing policy.\nDetails:")
            traceback.print_exc() #打印错误信息
            sys.exit()
        
        if copyfile: #当前文件是否符合用户自定义的规则
            copy(src + relative,dest + relative) #如果是，那就复制
        else: #否则就不管
            print("[+] Filtered out:",path)
            

for i in range(len(src)):
    for j in range(src[i].count("\\")): #统一分割符为正斜杠
        src[i] = src[i].replace("\\","/")

for i in range(dest.count("\\")): #统一分割符为正斜杠
    dest = dest.replace("\\","/")

for i in range(len(src)):
    if src[i].endswith("/"): #仅用于美化路径名，方便调试
        src[i] = src[i][:-1]

if dest.endswith("/"): #仅用于美化路径名，方便调试
    dest = dest[:-1]
    
if policy == "": #若用户没有自定义规则，则复制所有内容
    policy = "1"

done = []
while len(src) or loop == "loop":
    for i in src:
        print("[+] Waiting for \"",i,"\"",sep="")
    for i in range(len(src)):
        path = pathlib.Path(src[i])
        if path.exists(): #用于判断USB是否插入电脑
            print("[+] Target \"",src[i],"\" found. Now copying...",sep="")
            dfs(src[i],"/",dest) #开始复制！
            if loop != "const":
                done.append(src[i])
                src.pop(i)
            else:
                print("[+] Const mode enabled.")
            break
    
    if loop == "loop":
        print("[+] Loop mode enabled.")
        for i in range(len(done)):
            path = pathlib.Path(done[i])
            if not path.exists():
                src.append(done[i])
                done.pop(i)
    
    time.sleep(2) #防止程序炸CPU

