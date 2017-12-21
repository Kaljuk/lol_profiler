from urllib.request import urlopen
import json

def getData(region, nimi): # Siin saame info kasutaja kohta
    if region == "EUNE":
        region = "eun1"
    elif region == "EUW":
        region = "euw1"
    elif region == "NA":
        region = "na1"
    url = "https://"+region+".api.riotgames.com/lol/summoner/v3/summoners/by-name/"+nimi+"?api_key="+api_key
    json_data = urlopen(url)
    data = json.load(json_data)
    return data

def spec(id): # Siin saame infot käimasoleva mängu kohta (overall) [kui mängu pole, siis tuleb 404 error!]
    url = "https://na1.api.riotgames.com/lol/spectator/v3/active-games/by-summoner/"+str(id)+"?api_key="+api_key
    json_data = urlopen(url) 
    andmed = json.load(json_data)
    return andmed

def match_history(a_id,region): # siin saame viimased 100 mängu tagasi
    if region == "EUNE":
        region = "eun1"
    elif region == "EUW":
        region = "euw1"
    elif region == "NA":
        region = "na1"
    url = "https://"+region+".api.riotgames.com/lol/match/v3/matchlists/by-account/"+str(a_id)+"?api_key="+api_key
    json_data = urlopen(url)
    data = json.load(json_data)
    return data

def match_info(mäng_id,region): # siin saame infot ühe valitud mängu kohta (täpne) [kõik mida me küsida saame ehk kas sai firstblood v palju minione kille on jne]
    if region == "EUNE":
        region = "eun1"
    elif region == "EUW":
        region = "euw1"
    elif region == "NA":
        region = "na1"
    url = "https://"+region+".api.riotgames.com/lol/match/v3/matches/"+str(mäng_id)+"?api_key="+api_key
    json_data = urlopen(url)
    andmed = json.load(json_data)
    return andmed

def analüüs(arv,mänge,FBC,alive_time,creeps,jungle_creeps,mängude_aeg,vision,KDA,win_loss, summ_name,Andmed,tiimId,region):
    andmed = Andmed #see function võtab kõik muutujad, mida ma kohe allpool loon ning paneb nendsse andmed, mida ma pärast välja prindin
    for i in range(arv):
        mang_info_acc_nr = 0
        mang_info = match_info(game_id[i],region)
        for j in range(len(mang_info["participantIdentities"])): # loopime läbi et leida nimele vastava participantId
            if summ_name == mang_info["participantIdentities"][j]["player"]["summonerName"]:
                mang_info_acc_nr = j
                pass
            
    
        try:
            vision += mang_info["participants"][mang_info_acc_nr]["stats"]["visionScore"]
            KDA[0] += mang_info["participants"][mang_info_acc_nr]["stats"]["kills"]
            KDA[1] += mang_info["participants"][mang_info_acc_nr]["stats"]["deaths"]
            KDA[2] += mang_info["participants"][mang_info_acc_nr]["stats"]["assists"]
            creeps += mang_info["participants"][mang_info_acc_nr]["stats"]["totalMinionsKilled"]
            jungle_creeps += mang_info["participants"][mang_info_acc_nr]["stats"]["neutralMinionsKilled"]
            alive_time += mang_info["participants"][mang_info_acc_nr]["stats"]["longestTimeSpentLiving"]
            mängude_aeg += mang_info["gameDuration"]
            if mang_info["participants"][mang_info_acc_nr]["stats"]["win"]:
                win_loss += 1
            if mang_info["participants"][mang_info_acc_nr]["stats"]["firstBloodKill"]:
                FBC += 1
            if mang_info["participants"][mang_info_acc_nr]["stats"]["firstBloodAssist"]:
                FBC += 0.5
        except:
            mänge -= 1
    awe = (vision/arv)
    at = round(alive_time/arv)
    farm = round((creeps + jungle_creeps)/ (mängude_aeg/60),3)
    wl = str(round(win_loss/arv,2))
    for j in range(len(andmed["participants"])): # loopime läbi et leida nimele vastava participantId
        if summ_name == andmed["participants"][j]["summonerName"]:
            mang_info_acc_nr = j
            tiimId  = andmed["participants"][mang_info_acc_nr]["teamId"]
            pass

    print("MÄNGIJA:", summ_name)
    print("Mängib tiimis",tiimId)
    print("Agressiveness on:", str(FBC))
    print("Keskmiselt suudab elus olla",at,"sekundit")
    print("Average farm per minute :",farm)
    print("Environmental awareness",round(awe))
    print("KDA ration on:",str(round(KDA[0]/arv,2))+"/"+str(round(KDA[1]/arv,2))+"/"+str(round(KDA[2]/arv,2)))
    print("Win-loss ratio on", wl)
    return [summ_name, FBC,at,farm,awe,KDA,wl]
    
api_key = "RGAPI-3431e568-fe49-427c-b802-39997a5f0dd7"
põhjalikkus = False
teineSummoner = ""
tiimId = 0
win_loss = 0
KDA = [0,0,0]
vision = 0
mänge = 0
creeps = 0
jungle_creeps = 0
alive_time = 0
mängude_aeg = 0
FBC = 0
arv = 0
game_id = [] # järjend kus on viimased gameId-d
def viimnef(region,summ_name):# viimane functioon, mis kõik eelnevad funktsioonid välja kutsub ja programmi tööle paneb
    data = getData(region, summ_name)
    print(data)
    summ_id = data["id"]
    acc_id = data["accountId"]
    andmed = spec(summ_id)
    osalejad = []
    for i in range(len(andmed["participants"])): # saame list summoner nimedest 
        osalejad.append(andmed["participants"][i]["summonerName"])
    print(osalejad)
    mängude_ajalugu = match_history(acc_id,region)
    if põhjalikkus:
        arv = 30
        teineSummoner = input("Mis mängja kohta infot tahad?: ")
        for i in range(arv):
            game_id.append(mängude_ajalugu["matches"][i]["gameId"])
        print(analüüs(arv,mänge,FBC,alive_time,creeps,jungle_creeps,mängude_aeg,vision,KDA,win_loss,teineSummoner,andmed,tiimId,region))
    else:
        arv = 5
        for i in range(arv):
            game_id.append(mängude_ajalugu["matches"][i]["gameId"])
        for i in osalejad:
            analüüs(arv,mänge,FBC,alive_time,creeps,jungle_creeps,mängude_aeg,vision,KDA,win_loss,i,andmed,tiimId,region)
from tkinter import *
import tkinter as tk
from tkinter import ttk

import os
import time

## WINDOW
# Create window and specific config
win = Tk()
# Window size
win.geometry("600x400") 
#Remove dark borderline
win.overrideredirect(1) 
# Add window title
win.wm_title("LoL Profiler")
# Set background color
win.config(background = '#242424')


## CANVAS
can_w, can_h = 600,400
# Create a canvas to draw on
can = Canvas(win, width=can_w,height=can_h, highlightthickness=0)
can.pack()

# ----- Move window with mouse -----
# Get window location
def getWinLoc(window):
    return [int(i) for i in window.geometry().split('+')[1:3]]
# Get mouse loc
def getMouseLoc(window):
    return [win.winfo_pointerx(), win.winfo_pointery()]
# Init mouse and window locations
m_sx, m_sy = 0, 0
w_sx, w_sy = 0, 0
# ReInit mouse and window locations
def oneClick(event):
    #print('Click', event.x, event.y, 'Mouse', win.winfo_pointerx(), win.winfo_pointery(), 'Window', win.winfo_x(), win.winfo_y())
    global w_sx, w_sy, m_sx, m_sy
    m_sx, m_sy = getMouseLoc(win)
    w_sx, w_sy = getWinLoc(win)# = win.geometry().split('+')[1], win.geometry().split('+')[2]
# MovingMouse with the window    
def oneMove(event):
    # Hiire asukoht ja vahe ekraanil hiire ja hiire algse pos-i vahel
    m_x, m_y = getMouseLoc(win)
    v_x, v_y = m_x-m_sx, m_y-m_sy
    # Ekraani asukoha arvutamine
    w_x = w_sx + v_x
    w_y = w_sy + v_y
    # Move window
    win.geometry('+{x}+{y}'.format(x=w_x,y=w_y))

# # Create basic layout

# Object change coords
def searchBoxChangeOk(rect):
    addty = (ty)/100
    for i in range(100):
        x0,y0,x1,y1 = can.coords(rect)
        can.coords(rect, x0, y0+addty, x1, y1)
        can.update() # Update/Refresh visible canvas
        time.sleep(0.01)
# -- Colors --

# Theme1
mediumW, lGreen, Green, dGreen = '#F4F7ED','#86EE60','#2E6E65','#2B3752'
# Theme 2
aWhite, lYellow, lAqua, dAqua = '#dddfd4','#fae596','#173e43','#3fb0ac'
# Theme 3
lWhite, red = '#F5F5F5', '#E20049'

# Default dark background
can.configure(background=lAqua)

# -- TOPBAR AND WINDOW FUNCTIONS --
# [DRAW] Create topBar
t_bar = can.create_rectangle(0,0,can_w,can_h*0.05, fill=dAqua, width=0)
# [DRAW]Create close button box
t_bar_close_box = can.create_rectangle(can_w-can_h*0.05,0,can_w,can_h*0.05, fill=lAqua, width=0)
# Close X
dfc = 1
t_bar_x = can.create_line(dfc + can_w-can_h*0.05 ,0+dfc,can_w-dfc,can_h*0.05-dfc, fill=aWhite, width=0)
t_bar_x1 = can.create_line(can_w-dfc ,0+dfc, can_w-can_h*0.05 + dfc , can_h*0.05-dfc, fill=aWhite, width=0)
# Clickable box
t_close_box = can.create_rectangle(can_w-can_h*0.05,0,can_w,can_h*0.05, fill='', width=0)
# Change color when hovered
def tbarCol(e, c):
    newcol = lAqua if (c==0) else dAqua
    can.itemconfig(t_bar_close_box, fill=newcol)
can.tag_bind(t_close_box, '<Enter>', lambda x: tbarCol(x, 1))
can.tag_bind(t_close_box, '<Leave>', lambda x: tbarCol(x, 0))
can.tag_bind(t_close_box, '<Button-1>', lambda x: os._exit(0))


# Allow moving the window with the mouse on topBar
can.tag_bind(t_bar, '<Button-1>', oneClick)
can.tag_bind(t_bar, '<B1-Motion>', oneMove)

# Program name
can.create_text(can_h*0.025, can_h*0.025,text='LoL Profiler', anchor=tk.W, fill=lWhite)

# -END- TOPBAR AND WINDOW FUNCTIONS -END-

# -- MAIN PROGRAM INTERFACE --


# Show all player info templates

# # INPUT VARIABLES
# Needed for search
targetRegion = 'EUW' # Default region
targetSummoner = 'KopliKeiser'  # No default summonerName

# # OUTPUT VARIABLES
# Teams
outTeam_Ally = [dict()]*5 # Player and teammates
outTeam_AllyR= []*5
outTeam_Enemy = [dict()]*5# Enemey team

# [Draw] Current Profile view
can.create_rectangle(can_w*.05, can_h*.25, can_w*.75, can_h*.95, fill=lWhite, width=0)
# [Draw] Ally team
can.create_rectangle(can_w*.75, can_h*.25, can_w*.95, can_h*.95, fill=aWhite, width=0)

# [draw] List of the team members
teamboxh = 5
for i in range(len(outTeam_Ally)):
    outTeam_Ally[i] = can.create_rectangle(can_w*.75+5, can_h*.25+teamboxh+(i*20), can_w*.95-5, can_h*.25+teamboxh+(i*20)+10, fill=lGreen)
    print(outTeam_Ally)
teamboxh = 20
for i in range(len(outTeam_Ally)):
    can.create_rectangle(can_w*.75+5, can_h*.25+teamboxh+((5+i)*20), can_w*.95-5, can_h*.25+teamboxh+((5+i)*20)+10, fill=red)
    print(i, len(outTeam_Ally), outTeam_Ally)

# - SearchButton 
# SummonerName insert box
dfc = 1
inputBox = can.create_rectangle(0+dfc, can_h*0.05+dfc, can_w-dfc, can_h*0.2-dfc, fill=aWhite, width=0)
dfc = 3
summonerBox = can.create_rectangle(0+dfc+1, can_h*0.05+dfc+1, can_w-dfc-1, can_h*0.2-dfc-1, fill=mediumW, width=0)
# Write summoner name here
#summonerIn = can.create_text(0+dfc+1, can_h*0.2-dfc-1, text=targetSummoner, anchor=tk.SW, font=("Helvetica", 30))
w = ttk.Entry(can, font="Helvetica 30 bold")
w.place(x=0+dfc+1, y=can_h*0.2-dfc-1, anchor=tk.SW, height= (can_h*0.2-dfc-1)-(can_h*0.05+dfc+1), width=can_w*0.5)
# Region select box
SummonerIn = StringVar(can)
SummonerIn.set("EUW")
regionIn = OptionMenu(can, SummonerIn, "EUW", "NA", "EUNE")#,font="Helvetica 30", height=1, width=0)
regionIn.config(width=5, height=1, font="Helvetica 20")
regionIn.place(x=0+dfc+1+can_w*0.5, y=can_h*0.2-dfc-1, anchor=tk.SW)



## SEARCH FOR THE NAME
def otsiNime():
    reg = SummonerIn.get() # Get Selected region
    summ= w.get()          # Get Summoner name
    viimnef(reg,summ)
    # Initiate the function to profile all people
    
# Search for the summoner Button
meinButton = Button(can, text="Search", command=otsiNime, font="Helvetica 20")
meinButton.place(x=0+dfc+1+can_w*0.5 + 120, y=can_h*0.2-dfc-1, width=100, height=50,anchor=tk.SW)

can.tag_bind(meinButton, '<Button-1>', lambda x: otsiNime())


win.mainloop()

print("Done")