import tkinter
import tkinter.filedialog



def edit_list(root,init=None,filechooser=False):
    list_ = []
    def add_data(event=None):
        if entry.get() != "":
            listbox.insert(tkinter.END,entry.get())
            list_.append(entry.get())
            entry.delete(0,tkinter.END)
            
    def delete_data(event=None):
        '''if len(manual_list) == 0:
            return'''
        
        current_data = listbox.get(tkinter.ACTIVE)
        listbox.delete(tkinter.ACTIVE)
        list_.remove(current_data)
#        print(manual_list)

    def quit_window():
        top.destroy()
        
    def ok():
        quit_window()

    def choose_files():
        files = tkinter.filedialog.askopenfilenames()
        for i in files:
            list_.append(i)
            listbox.insert(tkinter.END,i)
            
    
    top = tkinter.Toplevel()
    frame1 = tkinter.Frame(top)
    entry = tkinter.Entry(frame1,width=90)
    entry.bind("<Return>",add_data)
    entry.grid(row=0,column=0)
    add = tkinter.Button(frame1,text="添加",command=add_data)
    add.grid(row=0,column=1)
    if filechooser:
        choosefiles = tkinter.Button(frame1,text="选择文件",command=choose_files)
        choosefiles.grid(row=0,column=2)
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

    '''for i in list_:
        listbox.insert(tkinter.END,i)
        '''
    if init:
        for i in init:
            list_.append(i)
            listbox.insert(tkinter.END,i)
    
    top.grab_set()
    root.wait_window(top)
    return list_

if __name__ == "__main__":
    root = tkinter.Tk()
    def abcd():
        print(edit_list(root,init=[1,2,3]))

    bt = tkinter.Button(root,command=abcd).pack()
    root.mainloop()
