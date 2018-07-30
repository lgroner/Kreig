# !/usr/bin/python3
from tkinter import *
import tkinter
import math
import time
#import tkMessageBox
class Unit:   ################## Class ####################
    def __init__(self, nat, name,type_, x, y,orders):
        self.nat=nat
        self.name=name
        self.type_=type_
        self.x=x;self.y=y
        self.pop=1000.0
        self.supply=1000.0
        self.fort = 1
        self.orders=orders
    def prtUnit(self):
        print(self.nat, self.name, self.type_.dispUtype(), self.x, self.y,self.pop,self.supply,
              self.orders.dispOrders())
    def move(self,tx,ty):
        d=dist(self.x,self.y,tx,ty)
        self.x+=dt*((tx-self.x)/d)*.1*self.type_.speed # ?????
        self.y+=dt*((ty-self.y)/d)*.1*self.type_.speed
        if self.x>mapDim:self.x=mapDim
        if self.x<0:self.x=0
        if self.y>mapDim:self.y=mapDim
        if self.y<0:self.y=0
        self.fort=1
    def fire(self,tgtUnit):
        d=dist(self.x,self.y,tgtUnit.x,tgtUnit.y)
        #print(self.nat,self.name,'TgtDefStr',tgtUnit.type_.defStr,'Dist',int(d),
        #     'Sup',int(self.supply),tgtUnit.nat,tgtUnit.name,'TgtPop',int(tgtUnit.pop),"PRE")
        if (self.nat==tgtUnit.nat):return    ##  ???????? orders have sides reversed.
        #print(self.nat,self.name,'TgtDefStr',tgtUnit.type_.defStr,'Dist',int(d),
        #     'Sup',int(self.supply),tgtUnit.nat,tgtUnit.name,'TgtPop',int(tgtUnit.pop),"POST NAT")
        
        if d==0 :return
        if self.supply<=0:
            self.supply=0;  return
        #print(self.nat,self.name,'TgtDefStr',tgtUnit.type_.defStr,'Dist',int(d),
        #     'Sup',int(self.supply),tgtUnit.nat,tgtUnit.name,'TgtPop',int(tgtUnit.pop),"POST D")
        if tgtUnit.pop<2:return
        #fireEffect=self.pop*self.type_.offStr*(.05*self.type_.range_)**2/(1000*tgtUnit.type_.defStr*d**2)
        fireEffect=dt*(self.pop/1000)*(.1*self.type_.offStr/tgtUnit.type_.defStr)*(1/tgtUnit.fort)/(self.type_.range_/d)**2
        self.supply-=3*dt*self.type_.offStr
        tgtUnit.pop-=fireEffect
        if tgtUnit.pop<0:tgtUnit.pop=0
    def fortify(self):
        if self.fort<5:self.fort+=1*dt
    def obey(self):
        #print("obey",self.orders.target.name)
        if self.orders.target!=0:
            self.fire(self.orders.target)
        if ((self.x-self.orders.destx)**2>1) or ((self.y-self.orders.desty)**2>1) :
            self.move(self.orders.destx,self.orders.desty)
        else:self.fortify()
    def status(self,i):
        rpt=   "Nat  Unit    \tPop  \tSup\tFort"
        rtext=map0.create_text(805,10,text=rpt,font=("Purisa",15),fill="Black",anchor="nw")
        rpt=self.nat+" "+self.name+"  \t"+str(int(self.pop))+"\t"+str(int(self.supply))+"\t"+str(int(self.fort))
        rtext=map0.create_text(805,37+35*i,text=rpt,font=("Purisa",15),fill=u.nat,anchor="nw")
        return rtext
def dist(self,u):
    return dist(self.x,self.y,u.x,u.y)
def dist(x1,y1,x2,y2):
    return math.sqrt((x2-x1)**2 +(y2-y1)**2)
def prtOob(oob):
    for u in oob:
        u.prtUnit()
def fireOrder():
    print (lb.curselection())
    return
def moveOrder():
    print("moveOrder")
    return
class Utype:   ################## Class ####################
    def __init__(self,offStr,defStr,speed,range_):
        self.offStr=offStr
        self.defStr=defStr
        self.speed=speed
        self.range_=range_
    def dispUtype(self):
        return [self.offStr,self.defStr,self.speed,self.range_]
class Orders:   ################## Class ####################
    def __init__(self, destx,desty,target,fort):
        self.destx=destx
        self.desty=desty
        self.target=target
        self.fort=1
    def dispOrders(self):
        return (self.destx, self.desty,self.target,self.fort)
class Ttype:   ################## Class ####################
    def __init__(self, color, vel, cover):
        self.color=color
        self.vel=vel
        self.cover=cover
##############   Start execution     #######################
plain=Ttype("yellow",1,1)     ### Terrain types
woods=Ttype("lightgreen",.5,.5)
hills=Ttype("tan",.25,.75)
water=Ttype("lightblue",.05,1)
road= Ttype("lightgrey",3,1)

ordBlue=Orders(12,12,0,0) # dest x, dest  y, fire target, fortify
ordRed =Orders(12,12,0,0) # dest x, dest  y, fire target, fortify 
inf=  Utype(1,1,1,1) # Unit Types(offensive strength,defensive strength, mobility, range)
cav=  Utype(1,1,3,1)
armor=Utype(3,3,3,2)
arty= Utype(5,1,.75,4)
####  Units ( side color, name,Utype, pos x, pos y, orders)
b1Inf=Unit("red","1_Inf",inf,11,8,ordBlue);    r1Inf=Unit("blue","1_Inf",inf,16,13,ordRed)
b2Inf=Unit("red","2_Inf",inf,8,11,ordBlue);   r2Inf=Unit("blue","2_Inf",inf,13,16,ordRed)
b1Cav=Unit("red","1_Cav",cav,9,8,ordBlue);    r1Cav=Unit("blue","1_Cav",cav,16,17,ordRed)
b1Armor=Unit("red","1_Arm",armor,13,8,ordBlue);r1Armor=Unit("blue","1_Arm",armor,13,18,ordRed)
b1Arty= Unit("red","1_Art",armor,7,1,ordBlue);r1Arty= Unit("blue","1_Art",armor,12,18,ordRed)
ordBlue.target=r1Inf;ordRed.target=b1Inf
rOob=[r1Inf,r2Inf,r1Cav,r1Armor,r1Arty]
bOob=[b1Inf,b2Inf,b1Cav,b1Armor,b1Arty]
units=rOob+bOob
#prtOob(rOob+bOob)
mapDim=25;celDim=40*20/mapDim    ###   Map   #######
map= [[0] * mapDim for i in range(mapDim)] # construct 2 d matrix of zeros
for i in range(mapDim):
    for j in range(mapDim):
        map[i][j]=(plain,plain,woods,woods,hills,plain,water)[(i+j)%7]
        if i==12 or j==12 or i==j+12 or i==j-12 or i+j==12 or i+j==35:
            map[i][j]=road
top = tkinter.Tk() ;
map0=tkinter.Canvas(top,bg="lightblue",height=800,width=1200)
for i in range(mapDim):
    for j in range(mapDim):
        map0.create_rectangle( celDim*i,celDim*j,celDim*i+celDim,celDim*j+celDim,      fill=map[i][j].color)
        map0.create_text(      celDim*i+celDim/2, celDim*j+celDim/2, text=str(i)+":"+str(j), fill="white")
utexts=[];ttexts=[];dt=.333

#### Control Panel ############
controlPanel=tkinter.Tk();
controlPanel.geometry("200x300")
controlPanel.title("Kreig")
controlPanel.attributes("-topmost",True)
#controlPanel.attributes("-color","lightblue")
lb0Label=Label(controlPanel,text="Firing Unit")
lb0Label.place(x=10,y=10)              
lb0=Listbox(controlPanel ,bg="Yellow",selectmode="SINGLE",width=10)
for u in units:
    lb0.insert(END,u.nat+u.name)    
lb0.place(x=10,y=30)#lb.pack
lb1Label=Label(controlPanel,text="Target Unit")
lb1Label.place(x=100,y=10)              
lb1=Listbox(controlPanel ,bg="Yellow",selectmode="SINGLE",width=10)
for u in units:
    lb1.insert(END,u.nat+u.name)    
lb1.place(x=100,y=30)#lb.pack
fireButton=Button(controlPanel,text="Fire",command=fireOrder,bg="yellow")
fireButton.place(x=10,y=210)
moveButton=Button(controlPanel,text="Move",command=moveOrder,bg="lightgreen")
moveButton.place(x=100,y=210)
moveLabel=Label(controlPanel,text="Destination x,y")
moveLabel.place(x=10,y=240)
destField=Entry(controlPanel,width=60,bg="lightgreen")
destField.place(x=10,y=260)
#lb.mainloop()

while True: # game loop
    i=0
    ##utexts=[];ttexts=[]
    for u in units: # display unit positions
        utexts=utexts+[map0.create_text(mapDim+celDim*u.x,mapDim+celDim*u.y,text=u.name,fill=u.nat)]
        u.obey()
        ttexts=ttexts+[u.status(i)]
        i+=1
    map0.update()
    time.sleep(.25)
    #print(utexts)
    for u in utexts: # unit texts
        map0.delete(u)
    for t in ttexts:  #  Terrain texts
        map0.delete(t)
    map0.pack()
#map.mainloop()

