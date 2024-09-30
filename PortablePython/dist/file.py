import threading
import time
import tkinter
import random

root = tkinter.Tk()
size = (50,50) #长*宽
unit = 10 #单位边长
frame = tkinter.Frame(root,relief="solid")
frame.place(x=0,y=0,height=size[0] * unit,width=size[1] * unit)
head = (0,0) #当前蛇头的位置
direction = 1
newdirection = 1
directions = [(0,-1),(0,1),(1,0),(-1,0)] #方向，分别为上、下、左、右
interval = 0.1 #蛇每移动一步等待时间
positions = [] #蛇身所在位置
pause = False #标记游戏是否暂停
score = 0 #分数
dead = False #游戏是否结束
food = (0,0) #食物所在位置
body = []
bodyobj = tkinter.Button
args = {"bg":"yellow"}

def init():
    global head
    global body
    global dead
    global positions
    dead = False
    head = (2,0) #蛇头初始位置在(2,0)
    for i in range(3): #刚开始蛇有3节身体
        node = bodyobj(frame,args)
        place(node,(i,0))
        positions.append((i,0)) #记录位置
        body.append(node) #将身体的每一节都放在一个列表中,备用
        mkfood()

def place(obj,pos): #方便绘制蛇
    obj.place(x=pos[0] * unit,y=pos[1] * unit,height=unit,width=unit)
    #print(pos[0] * unit,pos[1] * unit)

def loop():
    global head
    global body
    global dead
    global positions
    global score
    global direction
    while True:
        if not dead:
            positions.pop(0) #将蛇尾的坐标删除
            node = body[0] #将蛇尾的按钮出列
            body.pop(0)
            head = (head[0] + directions[direction][0],head[1] + directions[direction][1]) #计算当前蛇头的位置
            print(direction)
            if head[0] < 0: #如果蛇左越界
                head = (head[0] + size[0],head[1]) #那么蛇从右边出来
            if head[1] < 0: #如果蛇上越界
                head = (head[0],head[1] + size[1]) #处理由越界和上越界
            head = (head[0] % size[0],head[1] % size[1])
            
            if head in positions: #如果蛇撞到了自己的身体
                dead = True #那么游戏结束
                death() #善后
                break
            positions.append(head) #将新的位置加入列表中
            place(node,head) #刚才的蛇尾放到蛇头
            body.append(node) #处理完蛇头那个按钮后，将其放到队尾
            print(head)
            if head == food: #如果吃到食物
                mkfood() #刷新食物位置
                score += 1 #加一分
                positions.insert(0,(0,0)) #当前蛇头的位置
                body.insert(0,bodyobj(frame,args)) #将坐标和一节身体都放在队头，这样在下一次循环中，就会被马上处理
                showscore.configure(text=score) #显示最新分数
            time.sleep(interval) #等待一会儿
            direction = newdirection
            while pause: #如果游戏被暂停,则阻塞线程
                time.sleep(0.2) #每隔2秒检查一次游戏状态

def mkfood(): #用于确定食物的坐标
    global food
    while True: #不停地循环，直到找到可以放置食物的地方
        x = random.randint(0,size[0] - 1) #先随机食物的坐标
        y = random.randint(0,size[1] - 1)
        if (x,y) not in body: #方向，分别为上、下、左、右
            food = (x,y) #那这就是个合法的坐标
            dot.place(x=x * unit + 1,y=y * unit + 1,width = unit - 2,height = unit - 2) #可以把食物放在这个地方
            break #并结束循环
dot = tkinter.Label(root,text="",background="red") #食物
def death(): #善后
    pass
showscore = tkinter.Label(root,text=0) #用于显示分数
showscore.place(x=0,y=0)
focuspoint = tkinter.Frame(root,takefocus=True) #用于接收玩家的键盘输入
focuspoint.place(x=0,y=0)
focuspoint.focus_set() #获取焦点
def changedirection(event): #蛇每移动一步等待时间
    global newdirection
    disallow = [1,0,3,2] #只可以往当前方向的垂直方向走，如现在蛇向右走，那么改变方向时，蛇只能向上或向下而不能往回走
    dictionary = {"Up":0,"Down":1,"Left":3,"Right":2,"W":0,"A":3,"S":2,"D":1,"w":0,"a":3,"s":2,"d":1} #键盘映射方向
    print(event.keysym)
    if event.keysym in dictionary.keys():
        if disallow[dictionary[event.keysym]] != direction: #如果没有往回
            newdirection = dictionary[event.keysym] #那么就改变方向

focuspoint.bind("<Key>",changedirection) #绑定事件
init() #初始化
thread = threading.Thread(target=loop) #对于游戏主循环，则需另外开一个线程，否则会卡死主界面
thread.start() #开始游戏！
root.mainloop()
"""
Todo:
1. 把食物改成圆的
2. 把place改为pack
3. 增加超级食物
4.增加墙，公寓等
"""

