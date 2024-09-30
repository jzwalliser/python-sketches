import tkinter
import tkinter.messagebox


class TagButton(tkinter.Button):
    def __init__(self,*args,tag=None,command=None,**kwargs):
        self.tag = tag
        def tag_command():
            command(self.tag)
        
        cmd = command
        if command != None:
            cmd = tag_command
        
        super().__init__(*args,command=cmd,**kwargs)

root = tkinter.Tk()

matrix = []
buttons = []

def gettag(tag):
    print(tag)
    
frame1 = tkinter.Frame(root)
frame1.pack()

grid = (9,9)
mine = 9

def init():
    global matrix
    for i in range(mine):
        pos = (random.randint(0,grid[0] - 1),random.randint(0,grid[1] - 1))

for i in range(grid[0]):
    for j in range(grid[1]):
        button = TagButton(frame1,tag=(i,j),command=gettag)
        button.grid(row=i,column=j,ipadx="6px",ipady="1px")
        buttons.append(button)

root.mainloop()
