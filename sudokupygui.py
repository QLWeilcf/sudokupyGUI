import tkinter as tk
from time import sleep
from random import randint
from tkinter import _tkinter
from tkinter import messagebox

root=tk.Tk()
root.geometry('310x350+400+100') #大小和位置
root.title('Sudoku')
#全局变量
btnlst=[] # 每一个输入框
evs=[] #和btnlst对应的变量列表 仅get，set操作


def initOneSudo(s0): #根据初始数独和挖空个数，生成一个一维的数独列表
    s1=xyTo81(s0) #s0是二维的
    u=randint(0,8)
    if u!=0:
        s1=resetsd(s1,u)
    m=randint(18,41) #挖空个数。目前允许多解
    wlst=[] #挖空位置 
    while len(wlst)<m:
        i=randint(0,80)
        while i in wlst:
            i+=2 #或者这里继续用随机数
            if i>80:
                i-=30
        s1[i]=0
        wlst.append(i)
    return s1
def resetsd(s1,u):
    s11=[]
    uw=[7,9,1,8,2,4,3,5,6]
    uw=resetuw(uw,u)
    for k in range(81):
        s11.append(uw[s1[k]-1])
    return s11
def resetuw(uw,u): #u<len(uw)
    wu=uw[u:]
    wu.extend(uw[:u])
    return wu

def xyTo81(lst): #[[1,2,3],[4,5,6]] -> [1,2,3,4,5,6]
    olst=[]
    for i in lst:
        olst.extend(i)
    return olst
def nighty2xy(olst,n=9): #[1,2,3,4,5,6] ->[[1,2,3],[4,5,6]]
    if len(olst)!=n*n:
        return False
    lst=[]
    for i in range(n):
        lst.append(olst[i*n:(i+1)*n])
    return lst
def zeroToNAstr(s1,t=0): #t=0：0全部替换为'',t=1:''全部替换为0
    s2=[]
    if len(s1)==9 and t==0:
        for i in s1:
            s3=[]
            for j in i:
                if j==0:
                    s3.append('')
                else:
                    s3.append(j)
            s2.append(s3.copy())
    elif len(s1)==9 and t==1:
        for i in s1:
            s3=[]
            for j in i:
                if j=='':
                    s3.append(0)
                else:
                    s3.append(j)
            s2.append(s3)
    elif len(s1)==81 and t==0:
        for i in s1:
            if i==0:
                s2.append('')
            else:
                s2.append(i)
    elif len(s1)==81 and t==1:
        for i in s1:
            if i=='':
                s2.append(0)
            else:
                s2.append(i)
    else:
        print('error')
        raise Exception('非合法输入')
    return s2

def initSudo(s1,evs):
    sk1=xyTo81(s1)
    if evs==[]:
        for j in range(0,81):
            evs.append(tk.IntVar(root,sk1[j]))
    else:
        for j in range(0,81):
            evs[j].set(sk1[j])
    return evs
# 数独求解的类
class sovSudoku:
    def __init__(self,board=[]):
        self._b=board.copy()  #直接写=board会直接修改传进来的列表
        self._t=0 #递归调用次数
    def updateSudo(self,cb): #传入一个数独盘面
        if len(cb)==9 and len(cb[0])==9:
            self._b=cb
        elif len(cb)>=9 and len(cb[0])>=9:
            _cb=[]
            for i in range(9):
                _cb.append(cb[:9])
            self._b=_cb
        else:
            print('files size not shape',len(cb),len(cb[0]))
    def initFromFile(self,f): #从文件生成盘面
        cb=[]
        with open(f,'r') as rf:
            for l in rf.readlines():
                cb.append([int(i) for i in l.split(',')])
        self.updateSudo(cb)
    def checkNotSame(self,x,y,val):#检查每行、每列及宫内是否有和b[x,y]相同项
        for row_item in self._b[x]: #第x行
            if row_item==val:
                return False
        for rows in self._b:#y所在列
            if rows[y]==val:
                return False
        ax=x//3*3 #把0~3中的值映射到[0,3]
        ab=y//3*3
        for r in range(ax,ax+3):
            for c in range(ab,ab+3):#注意r==x & c==y的情况下，其实没必要，val不会是0
                if self._b[r][c]==val:
                    return False
        return True
    def getNext(self,x,y): #得到下一个未填项,从x,y往下数，值等于0就返回新下标
        for ny in range(y+1,9): #下标是[0,8]
            if self._b[x][ny]==0:
                return (x,ny)
        for row in range(x+1,9):
            for ny in range(0,9):
                if self._b[row][ny]==0:
                    return (row,ny)
        return (-1,-1) #不存在下一个未填项的情况
    def getPrem(self,x,y): #得到x，y处可以填的值
        prem=[]
        rows=list(self._b[x])
        rows.extend([self._b[i][y] for i in range(9)])
        cols=set(rows)
        for i in range(1,10):
            if i not in cols:
                prem.append(i)
        return prem
    def trysxy(self,x,y): #主循环，尝试x，y处的解答
        if self._b[x][y]==0: #不等于0的情况在调用外处理
            pv=self.getPrem(x,y)
            #for v in range(1,10): #默认：从1到9尝试
            for v in pv:
                self._t+=1 #递归次数+1
                if self.checkNotSame(x,y,v):# 符合 行列宫均满足v符合条件 的
                    self._b[x][y]=v
                    nx,ny=self.getNext(x,y) #得到下一个0值格
                    if nx==-1: #没有下一个0格了；and ny==-1可以写但没必要
                        return True
                    else:
                        _end=self.trysxy(nx,ny) #向下尝试,递归
                        if not _end:
                            self._b[x][y]=0 #回溯，继续for v循环
                            #只需要改x，y处的值，不改其他值
                        else:
                            return True
    def solve(self):
        #x,y=(0,0) if self._b[0][0]==0 else self.getNext(0,0)
        if self._b[0][0]==0:#更容易理解的写法
            self.trysxy(0,0)
        else:
            x,y=self.getNext(0,0)
            self.trysxy(x,y)
    def getSudoku(self):
        return self._b
    def getTNum(self):
        return self._t
    def __str__(self):
        return '{0}{1}{2}'.format('[',',\n'.join([str(i) for i in self._b]),']')
def isValidSudoku(board):
    if board[0][0]!=0:
        return validCheck(0,0,board)
    else:
        nx,ny=getNext(0,0,board)
        if nx==-1:
            return -1
        return validCheck(nx,ny,board)
def validCheck(x,y,b):#检查数独是否合法
    v=b[x][y]
    for r in range(0,9):
        if r!=x:
            if b[r][y]==v:
                return False
        if r!=y:
            if b[x][r]==v:
                return False
    ax=x//3*3
    ab=y//3*3
    for r in range(ax,ax+3):
        for c in range(ab,ab+3):
            if b[r][c]==v and r!=x and c!=y:
                return False
    nx,ny=getNext(x,y,b)
    if nx==-1:
        return True
    return validCheck(nx,ny,b)
def getNext(x,y,b):
    for ny in range(y+1,9):
        if b[x][ny]!=0:
            return (x,ny)
    for r in range(x+1,9):
        for ny in range(0,9):
            if b[r][ny]!=0:
                return (r,ny)
    return (-1,-1)

### 主函数   s0:内置的基础数独
s0=[[8, 1, 2, 7, 5, 3, 6, 4, 9],
	[9, 4, 3, 6, 8, 2, 1, 7, 5],
	[6, 7, 5, 4, 9, 1, 2, 8, 3],
	[1, 5, 4, 2, 3, 7, 8, 9, 6],
	[3, 6, 9, 8, 4, 5, 7, 2, 1],
	[2, 8, 7, 1, 6, 9, 5, 3, 4],
	[5, 2, 1, 9, 7, 4, 3, 6, 8],
	[4, 3, 8, 5, 2, 6, 9, 1, 7],
	[7, 9, 6, 3, 1, 8, 4, 5, 2]]
s1=initOneSudo(s0)  #81
s1=nighty2xy(s1,n=9)

s1cp=s1.copy()
s2=zeroToNAstr(s1,0) #9*9
evs=initSudo(s2,[])

i=0
for r in range(9):
    for c in range(9):
        if r>2 and r<6 and c>2 and c<6:
            btnlst.append(tk.Entry(root,textvariable=evs[i],justify='center'))
        elif r>2 and r<6:
            btnlst.append(tk.Entry(root,textvariable=evs[i],justify='center'))
            btnlst[i]['background']='#AFEEEE'
        elif c>2 and c<6:
            btnlst.append(tk.Entry(root,textvariable=evs[i],justify='center'))
            btnlst[i]['background']='#AFEEEE'
        else:
            btnlst.append(tk.Entry(root,textvariable=evs[i],justify='center'))
        btnlst[i].place(x=5+c*30,y=0+r*30,width=30,height=30)
        i+=1
#5~305
#0~300
def getSudo(evs,st=0): #盘面输入包含不合理字符（非[0,9]的整数，置空，执行下一步，执行完毕会弹出消息框
    #1：直接弹出消息框，return 0
    s5=[0 for _ in range(81)] #81
    msg=['','','']
    for j in range(0,81):
        try:
            jget=evs[j].get()
            if jget>9 or jget<0:
                msg[0]='获取盘面的值出现错误，请检查输入，是否包含非[0,9]的整数'
            s5[j]=jget
        except _tkinter.TclError as e: #输入为空或者非数值类型的输入的情况
            if 'but got ""' in str(e):
                msg[1]='有未输入的格子'
            else:
                print(e)
                msg[2]='获取盘面的值出现错误，请检查输入，是否包含非[0,9]的整数,计算时已置空'
        except Exception as e:
            print(e)
    s5=nighty2xy(s5,9)
    return s5,msg #9*9


def btnClick(x): #按钮点击的回调函数
    global evs,s1,s1cp
    if x=='c': #清空
        for i in range(81):
            evs[i].set('')
    elif x=='n':
        s1=initOneSudo(s0) #81
        s1cp=nighty2xy(s1,n=9)
        for k1 in range(81):
            if s1[k1]==0:
                evs[k1].set('')
            else:
                evs[k1].set(s1[k1])
    elif x=='m': #电脑解；这里涉及用户输入，确实需要的约束判断挺多的
        s5,msg=getSudo(evs,0) #9*9
        if msg[0]!='':
            messagebox.showinfo('提示',msg[0])
        elif msg[1]!='': #有空值来验证
            s6=s5.copy()
            isvs=isValidSudoku(s6)
            if isvs==-1:
                messagebox.showinfo('提示','当前盘面为空，请先手动输入一个合法盘面或点生成数独')
            elif isvs:
                ss=sovSudoku(s1cp)
                ss.solve()
                s3=ss.getSudoku() #[[1,2],[3,4]]
                s4=xyTo81(s3)
                for k1 in range(81): #从s3写入盘面
                    if s4[k1]==0:
                        evs[k1].set('')
                    else:
                        evs[k1].set(s4[k1])
            else:
                messagebox.showinfo('提示','当前盘面包含不满足数独条件的值，请检查')
        else:#填完了的情况
            s6=s5.copy()
            isvs=isValidSudoku(s6)
            if isvs==-1:
                messagebox.showinfo('提示','当前盘面为空，请先手动输入一个合法盘面或点生成数独')
            elif isvs:
                messagebox.showinfo('恭喜','恭喜，当前数独已解答正确！')
            else:
                messagebox.showinfo('提示','当前盘面包含不满足数独条件的值，请检查')
    elif x=='s': #验证盘面
        s5,msg=getSudo(evs,0) #9*9
        if msg[0]!='':
            messagebox.showinfo('提示',msg[0])
        elif msg[1]!='': #有空值来验证
            s6=s5.copy()
            isvs=isValidSudoku(s6)
            if isvs==-1:
                messagebox.showinfo('提示','当前盘面为空，请先手动输入一个合法盘面或点生成数独')
            elif isvs:
                messagebox.showinfo('提示','当前盘面满足数独条件,请继续作答或选择电脑解答')
            else:
                messagebox.showinfo('提示','当前盘面包含不满足数独条件的值，请检查')
        else:#填完了的情况
            s6=s5.copy()
            isvs=isValidSudoku(s6)
            if isvs:
                messagebox.showinfo('恭喜','恭喜，当前数独已解答正确！')
            else:
                messagebox.showinfo('提示','当前盘面包含不满足数独条件的值，请检查')


#随机生成 电脑解 验证答案
ranInitBtn=tk.Button(root,text='生成数独',command=lambda x='n':btnClick(x)) #new one sudo
ranInitBtn.place(x=5,y=310,width=60,height=30)
comBtn=tk.Button(root,text='验证盘面',command=lambda x='s':btnClick(x))
comBtn.place(x=70,y=310,width=60,height=30)
calsBtn=tk.Button(root,text='电脑解',command=lambda x='m':btnClick(x))
calsBtn.place(x=135,y=310,width=60,height=30)
clearBtn=tk.Button(root,text='清空',command=lambda x='c':btnClick(x))
clearBtn.place(x=200,y=310,width=60,height=30)

root.mainloop()