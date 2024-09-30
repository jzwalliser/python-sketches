import tkinter
import random
import tkinter.ttk
import tkinter.scrolledtext
import tkinter.messagebox
import time
import threading
import etk

root = tkinter.Tk()

notebook = tkinter.ttk.Notebook()
notebook.pack()

randomnumber = tkinter.Frame(notebook)
notebook.add(randomnumber,text="随机数")

randomtable = tkinter.Frame(notebook)
notebook.add(randomtable,text="随机表")

running = False
numbers = []
sequence = 1
manual_list = []

def run_rand():
    global running
    while running:
        time.sleep(0.01)
        if once_var.get():
            if len(numbers) == 1:
                add_number(numbers[0])
                numbers.pop()
                running = False
                return
            if len(numbers) == 0:
                initialize()
            current = numbers[random.randint(0,len(numbers) - 1)]
            label.configure(text=current)
        else:
            if use_list_var.get():
                current = numbers[random.randint(0,len(numbers) - 1)]
                label.configure(text=current)
            else:
                current = random.randint(int(start.get()),int(end.get()))
                label.configure(text=current)
    add_number(current)
    if once_var.get():
        numbers.pop(numbers.index(current))
                
            

def add_number(num):
    global sequence
    record.configure(state=tkinter.NORMAL)
    record.insert(tkinter.END,"[" + str(sequence) + "] " + str(num) + "\n")
    record.configure(state=tkinter.DISABLED)
    label.configure(text=num)
    sequence += 1

def rand_num():
    global running
    err = False
    if not start.get().isdigit():
        start.delete(0,tkinter.END)
        err = True
    if not end.get().isdigit():
        end.delete(0,tkinter.END)
        err = True
    if use_list_var.get():
        err = False
    if err:
        return
    if manual_stop_var.get():
        if once_var.get:
            init.configure(text="初始化",state=tkinter.NORMAL)
            if len(numbers) == 0:
                init.configure(text="已初始化",state=tkinter.DISABLED)
        if running:
            running = False
        else:
            running = True
            thread = threading.Thread(target=run_rand)
            thread.start()
    else:
        if not once_var.get():
            init.configure(text="初始化",state=tkinter.DISABLED)
            if use_list_var.get():
                number = manual_list[random.randint(0,len(manual_list) - 1)]
            else:
                number = random.randint(int(start.get()),int(end.get()))
        else:
            init.configure(text="初始化",state=tkinter.NORMAL)
            index = random.randint(0,len(numbers) - 1)
            number = numbers.pop(index)
            if len(numbers) == 0:
                init.configure(text="已初始化",state=tkinter.DISABLED)
                initialize()
        add_number(number)


def initialize():
    if once_var.get():
        init.configure(text="初始化",state=tkinter.DISABLED)
    err = False
    if not start.get().isdigit():
        start.delete(0,tkinter.END)
        err = True
    if not end.get().isdigit():
        end.delete(0,tkinter.END)
        err = True
    if use_list_var.get():
        err = False
    if err:
        return
    numbers.clear()
    if use_list_var.get():
        for i in manual_list:
            numbers.append(i)
    else:
        for i in range(int(start.get()),int(end.get()) + 1):
            numbers.append(i)
            
def list_init():
    if not use_list_var.get():
        min_num.grid(row=0,column=0)
        start.grid(row=0,column=1)
        max_num.grid(row=0,column=2)
        end.grid(row=0,column=3)
        list_preview.grid_forget()
        create_list.configure(state=tkinter.DISABLED)
    else:
        min_num.grid_forget()
        start.grid_forget()
        max_num.grid_forget()
        end.grid_forget()
        list_preview.grid(row=0,column=0)
        create_list.configure(state=tkinter.NORMAL)
    update_list_preview()

'''def edit_list():
    global top_created
    def add_data(event=None):
        if entry.get() != "":
            listbox.insert(tkinter.END,entry.get())
            manual_list.append(entry.get())
            entry.delete(0,tkinter.END)
            
    def delete_data(event=None):
        if len(manual_list) == 0:
            return
        
        current_data = listbox.get(tkinter.ACTIVE)
        listbox.delete(tkinter.ACTIVE)
        manual_list.pop(manual_list.index(current_data))
        print(manual_list)

    def ok():
        quit_window()
        update_list_preview()

    def quit_window():
        global top_created
        top_created = False
        top.destroy()
    
    if not top_created:
        global top
        
        top_created = True
        top = tkinter.Toplevel()
        frame1 = tkinter.Frame(top)
        entry = tkinter.Entry(frame1,width=90)
        entry.bind("<Return>",add_data)
        entry.grid(row=0,column=0)
        add = tkinter.Button(frame1,text="添加",command=add_data)
        add.grid(row=0,column=1)
        frame1.pack()
        
        listbox = tkinter.Listbox(top,width=100,height=20)
        listbox.bind("<Delete>",delete_data)
        listbox.pack()
        
        frame2 = tkinter.Frame(top)
        delete = tkinter.Button(frame2,text="删除",command=delete_data)
        delete.grid(row=0,column=0)
        confirm = tkinter.Button(frame2,text="确定",command=ok)
        confirm.grid(row=0,column=1)
        cancel = tkinter.Button(frame2,text="取消",command=quit_window)
        cancel.grid(row=0,column=2)
        frame2.pack()

        for i in manual_list:
            listbox.insert(tkinter.END,i)
'''
def edit_list():
    data = etk.edit_list(root,init=manual_list)
    manual_list.clear()
    for i in data:
        manual_list.append(i)
    update_list_preview()
#edit_list()

def update_list_preview():
    preview_string = ""
    global manual_list
    for i in manual_list:
        preview_string += i + ", "
    if preview_string != "":
        list_preview.configure(text=preview_string[:-2])
    else:
        manual_list = ["（空）"]
        list_preview.configure(text="（空）")

start_value = "0"
end_value = "100"

def press_need_init(event):
    global start_value
    global end_value
    start_value = start.get()
    end_value = end.get()

def release_need_init(event):
    if start_value != start.get() or end_value != end.get():
        initialize()
        init.configure(text="已初始化",state=tkinter.DISABLED)
        print("init")

frame1 = tkinter.Frame(randomnumber)
label = tkinter.Label(frame1,text="0",font=("Default",50),width=8)
label.grid(row=0,column=0)
rand = tkinter.Button(frame1,text="随机",width=20,height=3,command=rand_num)
rand.grid(row=0,column=1)
frame1.pack(anchor=tkinter.W)

frame2 = tkinter.Frame(randomnumber)
min_num = tkinter.Label(frame2,text="最小：")
min_num.grid(row=0,column=0)
start = tkinter.Entry(frame2)
start.bind("<Key>",press_need_init)
start.bind("<KeyRelease>",release_need_init)
start.insert(tkinter.END,"0")
start.grid(row=0,column=1)
max_num = tkinter.Label(frame2,text="最大：")
max_num.grid(row=0,column=2)
end = tkinter.Entry(frame2)
end.bind("<Key>",press_need_init)
end.bind("<KeyRelease>",release_need_init)
end.insert(tkinter.END,"100")
end.grid(row=0,column=3)
list_preview = tkinter.Label(frame2,text="（空）",width=60,relief="groove")
frame2.pack(anchor=tkinter.W)

frame3 = tkinter.Frame(randomnumber)
manual_stop_var = tkinter.IntVar()
manual_stop = tkinter.Checkbutton(frame3,text="手动停止",variable=manual_stop_var)
manual_stop.grid(row=0,column=0)
once_var = tkinter.IntVar()
once = tkinter.Checkbutton(frame3,text="每次循环中数据只出现一次",variable=once_var,command=initialize)
once.grid(row=0,column=1,padx=10)
init = tkinter.Button(frame3,text="初始化",state=tkinter.DISABLED,command=initialize,width=10)
init.grid(row=0,column=2,padx=10)
use_list_var = tkinter.IntVar()
use_list = tkinter.Checkbutton(frame3,text="使用列表",variable=use_list_var,command=list_init)
use_list.grid(row=0,column=3,padx=10)
create_list = tkinter.Button(frame3,text="编辑列表",state=tkinter.DISABLED,command=edit_list)
create_list.grid(row=0,column=4)
frame3.pack(anchor=tkinter.W)

record = tkinter.scrolledtext.ScrolledText(randomnumber,state=tkinter.DISABLED)
record.pack(anchor=tkinter.W)

frame4 = tkinter.Frame(randomnumber)
clear_record = tkinter.Button(frame4,text="清空记录")
clear_record.grid(row=0,column=0)
save_record = tkinter.Button(frame4,text="保存记录")
save_record.grid(row=0,column=1)
frame4.pack(anchor=tkinter.W)



root.mainloop()
