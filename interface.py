import tkinter as tk
from tkinter import Tk, Label, Button, Frame, Listbox, Entry
from constants import *

from PIL import Image, ImageTk
from functools import partial


EXTERNAL_PADDING = TITILE_SIZE
END_SECTION_PADDING = SUBSUBTITLE_SIZE*3/4
TITLE_SECTION_PADDING = (SUBSUBTITLE_SIZE/4)/2

BG_VISUALS = BGCOLOR
BG_PADDINGS = BGCOLOR

def changeSelection(index: int, options: list, e):
    selectedIndex = options[-1].get()
    if selectedIndex!=-1:
        options[selectedIndex]["button"].config(image=options[selectedIndex]["img"])
    options[-1].set(index)
    options[index]["button"].config(image=options[index]["imgS"])

def hoverImg(index: int, options: list, e):
    options[index]["button"].config(cursor="hand2")
    options[index]["label"].config(fg=MAINCOLOR)


def unhoverImg(index: int, options: list, e):
    options[index]["button"].config(cursor="")
    options[index]["label"].config(fg=TEXT_COLOR)




main = Tk()
main.geometry("750x750")
main.title(GAME_NAME)
mainFrame = Frame(main, bg=BG_PADDINGS, padx=EXTERNAL_PADDING*1.5, pady=EXTERNAL_PADDING)
mainFrame.pack(expand=True, fill="both")


def offFoucs(event):
    event.widget.focus_set()


main.bind("<Button-1>", offFoucs)


# Title
titleFrame = Frame(mainFrame, bg=BG_VISUALS)
titleFrame.pack(fill="x")

title = Label(titleFrame, text=GAME_NAME.upper(), bg=BGCOLOR, fg=MAINCOLOR, font=("Segoe UI", TITILE_SIZE, "bold"))
title.pack()

titleBotPadding = Frame(mainFrame, bg=BG_PADDINGS)
titleBotPadding.pack(pady=END_SECTION_PADDING)

selectorsFrame = Frame(mainFrame, bg=BG_PADDINGS)
selectorsFrame.pack(fill="x")

# Space selection
spaceFrame = Frame(selectorsFrame, bg=BG_VISUALS)
spaceFrame.pack(fill="x")

spaceText = Label(spaceFrame, text="select space", bg=BGCOLOR, fg=TEXT_COLOR, font=("Segoe UI", SUBTITLE_SIZE, "bold"))
spaceText.pack()

spaceTopPadding = Frame(spaceFrame, bg=BG_VISUALS)
spaceTopPadding.pack(pady=TITLE_SECTION_PADDING)

spaceSelectorsFrame = Frame(spaceFrame, bg=BGCOLOR)
spaceSelectorsFrame.pack(fill="x")


spaceVariable = tk.IntVar()
spaceVariable.set(-1)
spaceList = [{"name":TORUS_PUBLIC_NAME.upper()},{"name": RP2_PUBLIC_NAME.upper()},  {"name":KLEIN_PUBLIC_NAME.upper()}, spaceVariable]

for i in range(len(spaceList)-1):
    spaceList[i]["frame"] = Frame(spaceSelectorsFrame, bg=BGCOLOR)
    spaceList[i]["frame"].grid(row = 0, column=i, sticky="ew")
    spaceSelectorsFrame.grid_columnconfigure(i, weight=1, uniform="space")
    spaceList[i]["label"] = Label(spaceList[i]["frame"], text=spaceList[i]["name"], bg=BGCOLOR, fg=TEXT_COLOR, font=("Segoe UI", SUBSUBTITLE_SIZE))
    spaceList[i]["label"].pack()

    img = Image.open("img.png").resize(IMG_SIZE)
    spaceList[i]["img"] = ImageTk.PhotoImage(img)

    imgS = Image.open("imgS.png").resize(IMG_SIZE)
    spaceList[i]["imgS"] = ImageTk.PhotoImage(imgS)


    spaceList[i]["button"] = tk.Label( spaceList[i]["frame"], image=spaceList[i]["img"], bg=BGCOLOR, bd=0)
    spaceList[i]["button"].pack()

    spaceList[i]["button"].bind("<Button-1>", partial(changeSelection, i, spaceList))

    spaceList[i]["button"].bind("<Enter>", partial(hoverImg, i, spaceList))
    spaceList[i]["button"].bind("<Leave>", partial(unhoverImg, i, spaceList))
    

spaceBotPadding = Frame(spaceFrame, bg=BG_VISUALS, height=END_SECTION_PADDING)
spaceBotPadding.pack(fill="x")





spaceMapPadding = Frame(selectorsFrame, bg=BG_PADDINGS)
spaceMapPadding.pack(pady=END_SECTION_PADDING)



# Map selection
mapFrame = Frame(selectorsFrame, bg=BG_VISUALS)
mapFrame.pack(fill="x")

mapText = Label(mapFrame, text="select map", bg=BGCOLOR, fg=TEXT_COLOR, font=("Segoe UI", SUBTITLE_SIZE, "bold"))
mapText.pack()

mapTopPadding = Frame(mapFrame, bg=BG_VISUALS)
mapTopPadding.pack(pady=TITLE_SECTION_PADDING)

mapSelectorsFrame = Frame(mapFrame, bg=BGCOLOR)
mapSelectorsFrame.pack(fill="x")

mapVariable = tk.IntVar()
mapVariable.set(-1)
mapsList = [{"name": MAP1_PUBLIC_NAME.upper()}, {"name":MAP2_PUBLIC_NAME.upper()}, mapVariable]

for i in range(len(mapsList)-1):
    mapsList[i]["frame"] = Frame(mapSelectorsFrame, bg=BGCOLOR)
    mapsList[i]["frame"].grid(row = 0, column=i, sticky="ew")
    mapSelectorsFrame.grid_columnconfigure(i, weight=1, uniform="map")
    mapsList[i]["label"] = Label(mapsList[i]["frame"], text=mapsList[i]["name"], bg=BGCOLOR, fg=TEXT_COLOR, font=("Segoe UI", SUBSUBTITLE_SIZE))
    mapsList[i]["label"].pack()

    img = Image.open("img.png").resize(IMG_SIZE)
    mapsList[i]["img"] = ImageTk.PhotoImage(img)

    imgS = Image.open("imgS.png").resize(IMG_SIZE)
    mapsList[i]["imgS"] = ImageTk.PhotoImage(imgS)


    mapsList[i]["button"] = tk.Label( mapsList[i]["frame"], image=mapsList[i]["img"], bg=BGCOLOR, bd=0)
    mapsList[i]["button"].pack()

    mapsList[i]["button"].bind("<Button-1>", partial(changeSelection, i, mapsList))

    mapsList[i]["button"].bind("<Enter>", partial(hoverImg, i, mapsList))
    mapsList[i]["button"].bind("<Leave>", partial(unhoverImg, i, mapsList))

spaceMapPadding = Frame(mapFrame, bg=BG_VISUALS, height=END_SECTION_PADDING)
spaceMapPadding.pack(fill="x")





mapPlayerPadding = Frame(selectorsFrame, bg=BG_PADDINGS)
mapPlayerPadding.pack(pady=END_SECTION_PADDING)


# Players

playersFrame = Frame(selectorsFrame, bg=BG_VISUALS)
playersFrame.pack(fill="x", expand=True)

playersFrame.columnconfigure(0, weight=4, uniform="players")
playersFrame.columnconfigure(1, weight=1, uniform="players")
playersFrame.columnconfigure(2, weight=4, uniform="players")



# Rival selection
rivalFrame = Frame(playersFrame, bg=BG_VISUALS)
rivalFrame.grid(row=0, column=0, sticky="nsew")

rivalText = Label(rivalFrame, text="select rival", bg=BGCOLOR, fg=TEXT_COLOR, font=("Segoe UI", SUBTITLE_SIZE, "bold"))
rivalText.pack()


rivalSuperiorIndicator = Frame(rivalFrame, bg=BGCOLOR, height=2)
rivalSuperiorIndicator.pack_propagate(False)
rivalSuperiorIndicator.pack(fill="x")

listFrame = Frame(rivalFrame, bg=BGCOLOR, height=165)
listFrame.pack_propagate(False)
listFrame.pack(fill="x", padx=30)


def manageScrollIndicators():
    scrollPosition = rivalList.yview()
    if scrollPosition[0]!=0:
        rivalSuperiorIndicator.config(bg=ALTERNATIVE_COLOR_1)
    else:
        rivalSuperiorIndicator.config(bg=BGCOLOR)
    if scrollPosition[1]!=1:
        rivalInferiorIndicator.config(bg=ALTERNATIVE_COLOR_2)
    else:
        rivalInferiorIndicator.config(bg=BGCOLOR)

def mousewheelManager(event):
    if event.delta > 0:
        rivalList.yview_scroll(-1, "units")
    else:
        rivalList.yview_scroll(1, "units")
    
    manageScrollIndicators()

    return "break"

items = ["", "0:00 | None", "6:66 | Uwuvevwevew En", "1:24 | Clara", "3:47 | Lluís", "1:11 | Aleix", "2:93 | Marta", "5:12 | Drus", "1:29 | Adrià", "7:99 | Marc", "0:11 | Lara"]

rivalList = Listbox(
    listFrame,
    font=("Segoe UI", SUBTITLE_SIZE),
    bg=BGCOLOR,
    fg=DETAILS_COLOR,
    selectbackground=BGCOLOR,
    selectforeground=MAINCOLOR,
    highlightthickness=0,
    relief="flat",
    height=4
)
for item in items:
    rivalList.insert("end", item)
rivalList.place(x=0, y=-20, relwidth=1, relheight=1.2)
rivalList.bind("<MouseWheel>", mousewheelManager)

rivalInferiorIndicator = Frame(rivalFrame, bg=BGCOLOR, height=2)
rivalInferiorIndicator.pack_propagate(False)
rivalInferiorIndicator.pack(fill="x")


manageScrollIndicators()

# middle space

middleFrame = Frame(playersFrame, bg=BG_PADDINGS)
middleFrame.grid(row=0, column=1, sticky="nsew")

# final steps

finalFrame = Frame(playersFrame, bg=BG_PADDINGS)
finalFrame.grid(row=0, column=2, sticky="nsew")

def checkLen(new_text):
    if len(new_text) < PLAYER_NAME_LEN:
        return True
    return False


# Player name
nameFrame = Frame(finalFrame, bg=BG_VISUALS)
nameFrame.pack(fill="x")

    # Block large names
validation_register = nameFrame.register(checkLen)

nameText = Label(nameFrame, text="choose your name", bg=BGCOLOR, fg=TEXT_COLOR, font=("Segoe UI", SUBTITLE_SIZE, "bold"))
nameText.pack()

nameTopPadding = Frame(nameFrame, bg=BG_VISUALS)
nameTopPadding.pack(pady=TITLE_SECTION_PADDING)

entryFrame = Frame(nameFrame, bg=BGCOLOR)
entryFrame.pack()

nameEntry = Entry(entryFrame, width=13, font=("Segoe UI", SUBTITLE_SIZE, "bold"), bg=BGCOLOR, fg=TEXT_COLOR ,insertbackground=BGCOLOR,
                  borderwidth=0, relief="flat", justify="center", validate="key", validatecommand=(validation_register, '%P'))

nameEntry.pack()

underline = tk.Frame(entryFrame, height=2, bg=DETAILS_COLOR)
underline.pack(fill="x")

def showUnderline(event):
    underline.config(bg=MAINCOLOR)
    nameEntry.config(fg=TEXT_COLOR)

def hideUnderline(event):
    underline.config(bg=DETAILS_COLOR)
    nameEntry.config(fg=MAINCOLOR)


nameEntry.bind("<FocusIn>", showUnderline)
nameEntry.bind("<FocusOut>", hideUnderline)

nameBotPadding = Frame(finalFrame, bg=BG_VISUALS, height=2*END_SECTION_PADDING)
nameBotPadding.pack(fill="x")

# Margin

titleBotPadding = Frame(finalFrame, bg=BG_PADDINGS, height=2*END_SECTION_PADDING)
titleBotPadding.pack(fill="x")

# Start button

buttonFrame = Frame(finalFrame, bg=BG_VISUALS)
buttonFrame.pack()

pixel_virtual = tk.PhotoImage(width=1, height=1)
startButon = Button(buttonFrame, bg=DETAILS_COLOR, fg=BGCOLOR, cursor="hand2", activebackground=MAINCOLOR_DARK,
                    text="START", relief="raised", border=5, font=("Segoe UI", SUBTITLE_SIZE, "bold"), image=pixel_virtual,
                compound="c", width=200, height=50)
startButon.pack(side="bottom")

def onEnterButton(e):
    startButon.config(bg=MAINCOLOR)

def onLeaveButton(e):
    startButon.config(bg=DETAILS_COLOR)

startButon.bind("<Enter>", onEnterButton)
startButon.bind("<Leave>", onLeaveButton)

main.mainloop()