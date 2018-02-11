##########################################################
#                    M E R A G O N                       #
#                         -*-                            #
#                 La foret interdite                     #
#                                                        #
#            Gaetan BESSOT & Brice HEILMANN              #
#                                                        #
#                                                        #
#              Baccalaureat, Epreuve ISN.                #
#                      2016-2017                         #
##########################################################

#Import library
from tkinter import *
from random import *
from os.path import exists
from os import remove
from shutil import copyfile
from random import randrange

##########################################################
#                                                        #
#                        Player                          #
#                                                        #
##########################################################

## File method ##
def player_getInfo():
    if(exists("data/player.txt") == False):
        copyfile("data/player_base.txt", "data/player.txt")
    with open("data/player.txt", "r") as playerFile:
        data = playerFile.readlines()
    playerData = [[],[]]
    for i in range(len(data)):
        line = data[i].replace("\n", "").split(" ")
        key = line[0]
        value = line[1]
        playerData[0].append(key)
        playerData[1].append(value)
    return playerData

def player_setInfo():
    with open("data/player.txt", "w") as playerFile:
        for i in range(len(playerData[0])):
            key = playerData[0][i]
            value = str(playerData[1][i])
            playerFile.write(key+" "+value+"\n")

## Player method ##
def player_getName():
    x = playerData[0].index("name")
    return playerData[1][x]

def player_getPv():
    x = playerData[0].index("pv")
    return (int)(playerData[1][x])

def player_getPm():
    x = playerData[0].index("pm")
    return (int)(playerData[1][x])

def player_getMap():
    x = playerData[0].index("mapId")
    return (playerData[1][x])

def player_getX():
    x = playerData[0].index("x")
    return (int)(playerData[1][x])

def player_getY():
    x = playerData[0].index("y")
    return (int)(playerData[1][x])

def player_setName(new_name):
    x = playerData[0].index("name")
    playerData[1][x] = new_name
    player_setInfo()

def player_setPv(new_pv):
    x = playerData[0].index("pv")
    playerData[1][x] = new_pv
    player_setInfo()

def player_setPm(new_pm):
    x = playerData[0].index("pm")
    playerData[1][x] = new_pm
    player_setInfo()

def player_setMap(new_map):
    x = playerData[0].index("mapId")
    playerData[1][x] = new_map
    player_setInfo()

def player_setX(new_x):
    x = playerData[0].index("x")
    playerData[1][x] = new_x
    player_setInfo()

def player_setY(new_y):
    x = playerData[0].index("y")
    playerData[1][x] = new_y
    player_setInfo()

playerData = player_getInfo()

##########################################################
#                                                        #
#                       Events                           #
#                                                        #
##########################################################

def event_spawn():
    print("Spawn point.")

def event_loadLevel(destination):
    global finalMatrix, img3
    canv.delete("all")
    destroyMessagebox(0)    
    finalMatrix = createMatrix("levels/{}.txt".format(destination))
    renderMatrix()
    img3 = renderCharacter(1)
    player_setMap(destination)
    canv.update()
    event_messagebox("Vous vous enfoncez dans la fôret.",False,0,0)
    

def event_fight():
    global pInFight
    isFight = randrange(1,6)
    if(isFight <= 2):
        print("You are attacked.")
        pInFight = True
        
        canv.delete("all")
        width,height = getDimensions()
        canv.create_rectangle(0,0,width*100,height*100-100,fill="#327427")

        #Select random monster
        monster = []
        with open("data/monsters.txt", "r") as monsterFile:
            data = monsterFile.readlines()
        monsterData = [[],[]]
        mSelect = randrange(1,len(data)+1)
        for i in range(len(data)):
            line = data[i].replace("\n", "").split(" ")
            key = line[0]
            if(int(key) == mSelect):
                monster = line
        global mId,mName,mSprite,mPv,mDamage
        mId,mName,mSprite,mPv,mDamage = monster
        mId,mPv,mDamage=int(mId),int(mPv),int(mDamage)
        t_mPv = mPv
        
        #Monster
        canv.create_oval(width*100-300,250,width*100-50,325,fill="#61b254",outline="#61b254")
        monsterFrame = canv.create_rectangle(width*100-500,50,width*100-300,100,fill="#C4C4C4")
        monsterName = Label(fenetre, text=mName,bg="#C4C4C4",font=("System",13))
        monsterName.place(x=width*100-495,y=55)
        monsterLifeBar = canv.create_rectangle(width*100-495,90,width*100-305,95,fill="#58df42") #190 width
        monsterSprite = canv.create_image(width*100-175, 175, image = eval(mSprite))

        #Player
        playerFrame = canv.create_rectangle(300,height*100-200,500,height*100-150,fill="#C4C4C4")
        playerName = Label(fenetre, text=player_getName(),bg="#C4C4C4",font=("System",13))
        playerName.place(x=305,y=height*100-195)
        playerLifeBar = canv.create_rectangle(305,height*100-155,495-(190-((player_getPv()/100)*190)),height*100-160,fill="#58df42") #190 width
        if(player_getPv() <= 66):
            canv.itemconfig(playerLifeBar,fill="#e5b43d")
        if(player_getPv() <= 33):
            canv.itemconfig(playerLifeBar,fill="#dd0000")
        playerSprite = canv.create_image(200, height*100-150, image = pUp)

        def setPAttack():
            global playerAttack,playerBlock
            playerAttack = True
            playerBlock = False
            damage()
        def setPBlock():
            global playerBlock,playerAttack
            playerBlock = True
            playerAttack = False
            damage()
            
        def damage():
            global playerAttack,playerBlock,mPv,img3,finalMatrix,pInFight
            monsterAttack,monsterBlock = False, False
            mChoice = randrange(1,4)
            if(mChoice == 1):
                if(playerBlock == False):
                    player_setPv(player_getPv()-mDamage)
                    canv.coords(playerLifeBar,305,height*100-155,495-(190-((player_getPv()/100)*190)),height*100-160)
                    if(player_getPv() <= 66):
                        canv.itemconfig(playerLifeBar,fill="#e5b43d")
                    if(player_getPv() <= 33):
                        canv.itemconfig(playerLifeBar,fill="#dd0000")
                        
                    mPv-=player_getPm()
                    canv.coords(monsterLifeBar,width*100-495,90,width*100-305-(190-((mPv/t_mPv)*190)),95)
                    if(mPv <= 66):
                        canv.itemconfig(monsterLifeBar,fill="#e5b43d")
                    if(player_getPv() <= 33):
                        canv.itemconfig(monsterLifeBar,fill="#dd0000")
            elif(mChoice == 2):
                if(playerAttack == True):
                    mPv-=player_getPm()
                    canv.coords(monsterLifeBar,width*100-495,90,width*100-305-(190-((mPv/t_mPv)*190)),95)
                    if(mPv <= 66):
                        canv.itemconfig(monsterLifeBar,fill="#e5b43d")
                    if(player_getPv() <= 33):
                        canv.itemconfig(monsterLifeBar,fill="#dd0000")                
            if(player_getPv() <= 0):
                print("Vous êtes mort !")
                pInFight = False
                canv.delete("all")
                monsterName.destroy()
                playerName.destroy()
                destroyMessagebox(0)
                restartGame()
            if(mPv <= 0):
                print("Le montre est vaincu !")
                pInFight = False
                monsterName.destroy()
                playerName.destroy()
                canv.delete("all")
                destroyMessagebox(0)    
                finalMatrix = createMatrix("levels/{}.txt".format(player_getMap()))
                renderMatrix()
                img3 = renderCharacter(0)
                canv.update()
        playerAttack,playerBlock = False, False
        event_messagebox("Un monstre attaque ! Que faites-vous ?",True,2,[["Attaquer",setPAttack],["Parer",setPBlock]])

def event_messagebox(text,button,nbButton,buttonName):
    if len(text) >= 32:
        x1 = 195
        y1 = 515
    else:
        x1 = 230
        y1 = 530
    msgBox = Message(fenetre, text = text, width = 300, font = ("System",3), bg = "black", fg = "white")
    msgBox.place(x = x1, y = y1)
    msgbox.append(msgBox)
    if(button):
        addButton(x1,nbButton,buttonName)

##########################################################
#                                                        #
#                        Main                            #
#                                                        #
##########################################################

## Level functions ##
def restartGame():
    global finalMatrix, img3, playerData
    remove("data/player.txt")
    playerData = player_getInfo()
    finalMatrix = createMatrix("levels/{}.txt".format(player_getMap()))
    renderMatrix()
    img3 = renderCharacter(1)
    player_setMap("level1")
    canv.update()

def getData(x,y):
    return finalMatrix[y][x]

def getDimensions():
    return (len(finalMatrix[0]), len(finalMatrix))

def addButton(x1, nbButton, buttonName):
    global playerAttack,playerBlock
    if x1 == 195:
        y2 = 570
    else:
        y2 = 555
    if nbButton == 1:
        B1 = Button(fenetre, text = buttonName[0][0], fg = "black", bg = "white", command = buttonName[0][1])
        B1.place(x = 280, y = y2)
        btn.append(B1)
    if nbButton == 2:
        B1 = Button(fenetre, text = buttonName[0][0], fg = "black", bg = "white", command = buttonName[0][1])
        B1.place(x = 235, y = y2)
        B2 = Button(fenetre, text = buttonName[1][0], fg = "black", bg = "white", command = buttonName[1][1])
        B2.place(x = 370, y = y2)
        btn.append(B1)
        btn.append(B2)
    if nbButton == 4:
        B1 = Button(fenetre, text = buttonName[0][0], fg = "black", bg = "white", command = buttonName[0][1])
        B1.place(x = 235, y = y2-25)
        B2 = Button(fenetre, text = buttonName[1][0], fg = "black", bg = "white", command = buttonName[1][1])
        B2.place(x = 235, y = y2)
        B3 = Button(fenetre, text = buttonName[2][0], fg = "black", bg = "white", command = buttonName[2][1])
        B3.place(x = 370, y = y2-25)
        B4 = Button(fenetre, text = buttonName[3][0], fg = "black", bg = "white", command = buttonName[3][1])
        B4.place(x = 370, y = y2)
        btn.append(B1)
        btn.append(B2)
        btn.append(B3)
        btn.append(B4)
    
def destroyMessagebox(evt):
    for k in range(len(msgbox)):
        msgbox[k].destroy()
    for i in range(len(btn)):
        btn[i].destroy()

def createMatrix(levelFile):
    finalMatrix = []
    with open(levelFile, "r") as file:
        matrix = "".join(file.read()).split("-")
    for i in range(3):
        matrix[i] = "".join(matrix[i]).strip().split("\n")
        for j in range(len(matrix[0])):
            matrix[i][j] = "".join(matrix[i][j]).strip().split(" ")
    for y in range(len(matrix[0])):
        finalMatrix.append([])
        for x in range(len(matrix[0][0])):
            finalMatrix[-1].append((matrix[0][y][x],int(matrix[1][y][x]),int(matrix[2][y][x])))
    return finalMatrix

def renderMatrix():
    xp = player_getX()
    yp = player_getY()
    width, height = getDimensions()
    for y in range(height):
        for x in range(width):
            data = getData(x,y)
            tex = data[0]
            xc = 100*x+50
            yc = 100*y+50
            if tex == "g":
                img1 = canv.create_image(xc, yc, image = grass)
            if tex == "w":
                img2 = canv.create_image(xc, yc, image = water)
            if tex == "b":
                img3 = canv.create_image(xc, yc, image = bush)
            if tex == "t":
                img4 = canv.create_image(xc, yc, image = tree)

def renderCharacter(respawn):
    width, height = getDimensions()
    if(exists("data/player.txt") and not respawn):
        xc = 100*player_getX()+50
        yc = 100*player_getY()+50
        img3 = canv.create_image(xc, yc, image = pDown)
        xp = player_getX()
        yp = player_getY()
    else:
        for y in range(height):
            for x in range(width):
                data = getData(x,y)
                pos = data[2]
                xc = 100*x+50
                yc = 100*y+50
                if pos == 1:
                    img3 = canv.create_image(xc, yc, image = pDown)
                    player_setX(x)
                    player_setY(y)
    return img3

## Move functions ##
def runEvent(eventId):
    with open("data/events.txt", "r") as file:
        data = eventFile.readlines()
    eventData = [[],[]]
    for i in range(len(data)):
        line = data[i].replace("\n", "").split(" ")
        key = line[0]
        value = line[1]
        args = ",".join(line[2:])
        if(int(key) == eventId):
            exec("event_{}({})".format(value,args))

def move(evt):
    if(pInFight):
        return
    width,height = getDimensions()
    xp = player_getX()
    yp = player_getY()
    if evt.keycode == 39:
        canv.itemconfig(img3, image = pRight)
        if xp+1 < width and getData(xp+1,yp)[1] == 0:
            xp = xp+1
            player_setX(xp)
            xpc = (xp*100)+50
            ypc = (yp*100)+50
            canv.coords(img3, xpc, ypc)
            print(xp,yp)
        else:
            print("You can't walk here !")
    if evt.keycode == 37:
        canv.itemconfig(img3, image = pLeft)
        if xp-1 >= 0 and getData(xp-1, yp)[1] == 0:
            xp = xp-1
            player_setX(xp)
            xpc = (xp*100)+50
            ypc = (yp*100)+50
            canv.coords(img3, xpc, ypc)
            print(xp,yp)
        else:
            print("You can't walk here !")
    if evt.keycode == 38:
        canv.itemconfig(img3, image = pUp)
        if yp-1 >= 0 and getData(xp, yp-1)[1] == 0:
            yp = yp-1
            player_setY(yp)
            xpc = (xp*100)+50
            ypc = (yp*100)+50
            canv.coords(img3, xpc, ypc)
            print(xp,yp)
        else:
            print("You can't walk here !")
    if evt.keycode == 40:
        canv.itemconfig(img3, image = pDown)
        if yp+1 < height and getData(xp, yp+1)[1] == 0:
            yp = yp+1
            player_setY(yp)
            xpc = (xp*100)+50
            ypc = (yp*100)+50
            canv.coords(img3, xpc, ypc)
            print(xp,yp)
        else:
            print("You can't walk here !")
    runEvent(getData(xp,yp)[2])

##def music():
##    pygame.mixer.init() 
##    pygame.mixer.music.load("Captain America End Credits Theme.ogg")
##    pygame.mixer.music.play(-1)
##    pygame.mixer.music.set_volume(0.1)

with open("levels/{}.txt".format(player_getMap()), "r") as levelFile:
    matrix = "".join(levelFile.read()).split("-")
matrix_y = "".join(matrix[0]).strip().split("\n")
matrix_x = "".join(matrix_y[0]).strip().split(" ")
height = len(matrix_y)
width = len(matrix_x)
levelFile.close()
levelFile = "levels/{}.txt".format(player_getMap())

pInFight = False
msgbox = []
btn = []
msg = [] 

fenetre=Tk()

print("Creating map ...")
finalMatrix = createMatrix(levelFile)

print("Creating window ...")
width,height = getDimensions()
fenetre.title("Meragon -:- La forêt interdite")
fenetre.geometry((str)(width*100)+"x"+(str)(height*100))
fenetre.resizable(False,False)
canv = Canvas(fenetre,bg = "black", height = height*100, width = width*100)

print("Set textures ...")
#Character textures
pUp = PhotoImage(file = "tex/character/up.png")
pDown = PhotoImage(file = "tex/character/down.png")
pLeft = PhotoImage(file = "tex/character/left.png")
pRight = PhotoImage(file = "tex/character/right.png")
#Map textures
grass = PhotoImage(file = "tex/grass.png")
water = PhotoImage(file = "tex/water.png")
bush = PhotoImage(file = "tex/bush.png")
tree = PhotoImage(file = "tex/tree.png")
#Monsters textures
spider = PhotoImage(file = "tex/spider.png")
troll = PhotoImage(file = "tex/troll.png")
wolf = PhotoImage(file = "tex/wolf.png")

print("Bind controls ...")
fenetre.bind_all('<Right>', move)
fenetre.bind_all('<Left>', move)
fenetre.bind_all('<Down>', move)
fenetre.bind_all('<Up>', move)

fenetre.bind_all('<Delete>', destroyMessagebox)

print("Rendering map ...")
renderMatrix()

print("Create character ...")
img3 = renderCharacter(1)

#music()

canv.pack() 

fenetre.mainloop()

player_setInfo()
print("Saved.")
