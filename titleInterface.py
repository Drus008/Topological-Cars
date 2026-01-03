from tkinter import Tk, Label, Button, Frame, Listbox, Entry, Canvas
from functools import partial
from PIL import ImageTk
import tkinter as tk


from filesManager import checkFolders, getRecords, loadImage
from transitions import beginGame
from constants import *

EXTERNAL_PADDING = TITLE_SIZE
INTERNAL_PADDING = TITLE_SIZE/2
INTERSECTION_PADDING = TITLE_SIZE*3/4

BORDER_THICK = 2


END_SECTION_PADDING = SUBSUBTITLE_SIZE*3/4
TITLE_SECTION_PADDING = (SUBSUBTITLE_SIZE/4)/2

BG_VISUALS = BGCOLOR
BG_PADDINGS = BGCOLOR_2


INTERIOR_WIDTH = DIMX-2*EXTERNAL_PADDING



def createInterface(main:Tk):

    def loadRivals():
        mapId = mapsList[-1].get()
        spaceId = spaceList[-1].get()
        if mapId==-1 or spaceId==-1:
            return
        map = mapsList[mapId]["privateName"]
        space = spaceList[spaceId]["privateName"]
        rivalList.delete(2, tk.END)
        records = getRecords(space, map)
        global racers
        racers = records
        print(records)
        for record in records:
            rivalList.insert("end", record["time"]+" | "+str(record["name"]))


    def changeSelection(index: int, options: list, e):
        selectedIndex = options[-1].get()
        if selectedIndex!=-1:
            options[selectedIndex]["button"].config(image=options[selectedIndex]["img"])
        options[-1].set(index)
        options[index]["button"].config(image=options[index]["imgS"])

        loadRivals()

    def hoverImg(index: int, options: list, e):
        options[index]["button"].config(cursor="hand2")
        options[index]["label"].config(fg=MAINCOLOR)


    def unhoverImg(index: int, options: list, e):
        options[index]["button"].config(cursor="")
        options[index]["label"].config(fg=TEXT_COLOR)


    def offFocus(event):
        event.widget.focus_set()
    main.bind("<Button-1>", offFocus)


    #main.resizable(False, False)
    main.title(GAME_NAME)
    mainCanvas = Canvas(bg=BGCOLOR)
    mainCanvas.pack(expand=True, fill="both")

    from decoration import decorationFamily

    D = decorationFamily(mainCanvas, 100)

    # Title
    totalHeight = EXTERNAL_PADDING
    TITLE_FRAME_HEIGHT = TITLE_SIZE*2

    titleFrame = Frame(mainCanvas, bg=BG_VISUALS, width=INTERIOR_WIDTH, height=TITLE_FRAME_HEIGHT, highlightbackground=DETAILS_COLOR, highlightthickness=BORDER_THICK, highlightcolor=DETAILS_COLOR)
    titleFrame.place(x=EXTERNAL_PADDING, y=totalHeight)
    totalHeight = EXTERNAL_PADDING+TITLE_FRAME_HEIGHT + INTERSECTION_PADDING + BORDER_THICK
    titleFrame.pack_propagate(False)

    title = Label(titleFrame, text=GAME_NAME.upper(), bg=BGCOLOR, fg=MAINCOLOR, font=("Segoe UI", TITLE_SIZE, "bold"))
    title.pack(expand=True)




    SELECTION_FRAME_HEIGHT = 160
    # Map selection
    mapFrame = Frame(mainCanvas, bg=BG_VISUALS, width=INTERIOR_WIDTH, height=SELECTION_FRAME_HEIGHT, highlightbackground=DETAILS_COLOR, highlightthickness=BORDER_THICK, highlightcolor=DETAILS_COLOR)
    mapFrame.pack_propagate(False)
    mapFrame.place(x=EXTERNAL_PADDING, y=totalHeight)
    totalHeight = totalHeight + SELECTION_FRAME_HEIGHT + INTERSECTION_PADDING + BORDER_THICK

    mapText = Label(mapFrame, text="select map", bg=BGCOLOR, fg=TEXT_COLOR, font=("Segoe UI", SUBTITLE_SIZE, "bold"))
    mapText.pack()

    mapTopPadding = Frame(mapFrame, bg=BG_VISUALS)
    mapTopPadding.pack(pady=TITLE_SECTION_PADDING)

    mapMainCanvas = Frame(mapFrame, bg=BGCOLOR)
    mapMainCanvas.pack(fill="x")

    mapVariable = tk.IntVar()
    mapVariable.set(-1)
    mapsList = [{"name": MAP1_PUBLIC_NAME.upper(), "privateName":MAP1_PRIVATE_NAME}, {"name":MAP2_PUBLIC_NAME.upper(), "privateName":MAP2_PRIVATE_NAME}, mapVariable]

    for i in range(len(mapsList)-1):
        mapsList[i]["frame"] = Frame(mapMainCanvas, bg=BGCOLOR)
        mapsList[i]["frame"].grid(row = 0, column=i, sticky="ew")
        mapMainCanvas.grid_columnconfigure(i, weight=1, uniform="map")
        mapsList[i]["label"] = Label(mapsList[i]["frame"], text=mapsList[i]["name"], bg=BGCOLOR, fg=TEXT_COLOR, font=("Segoe UI", SUBSUBTITLE_SIZE))
        mapsList[i]["label"].pack()

        img = loadImage("img").resize(IMG_SIZE)
        mapsList[i]["img"] = ImageTk.PhotoImage(img)

        imgS = loadImage("imgS").resize(IMG_SIZE)
        mapsList[i]["imgS"] = ImageTk.PhotoImage(imgS)


        mapsList[i]["button"] = Label( mapsList[i]["frame"], image=mapsList[i]["img"], bg=BGCOLOR, bd=0)
        mapsList[i]["button"].pack()

        mapsList[i]["button"].bind("<Button-1>", partial(changeSelection, i, mapsList))

        mapsList[i]["button"].bind("<Enter>", partial(hoverImg, i, mapsList))
        mapsList[i]["button"].bind("<Leave>", partial(unhoverImg, i, mapsList))




    # Space selection
    spaceFrame = Frame(mainCanvas, bg=BG_VISUALS, width=INTERIOR_WIDTH, height=SELECTION_FRAME_HEIGHT, highlightbackground=DETAILS_COLOR, highlightthickness=BORDER_THICK, highlightcolor=DETAILS_COLOR)
    spaceFrame.pack_propagate(False)
    spaceFrame.place(x=EXTERNAL_PADDING, y=totalHeight)
    totalHeight = totalHeight + SELECTION_FRAME_HEIGHT + INTERSECTION_PADDING + BORDER_THICK

    spaceText = Label(spaceFrame, text="select space", bg=BGCOLOR, fg=TEXT_COLOR, font=("Segoe UI", SUBTITLE_SIZE, "bold"))
    spaceText.pack()

    spaceTopPadding = Frame(spaceFrame, bg=BG_VISUALS)
    spaceTopPadding.pack(pady=TITLE_SECTION_PADDING)

    spaceMainCanvas = Frame(spaceFrame, bg=BGCOLOR)
    spaceMainCanvas.pack(fill="x")


    spaceVariable = tk.IntVar()
    spaceVariable.set(-1)
    spaceList = [{"name":TORUS_PUBLIC_NAME.upper(), "privateName": TORUS_PRIVATE_NAME},{"name": RP2_PUBLIC_NAME.upper(), "privateName": RP2_PRIVATE_NAME},  {"name":KLEIN_PUBLIC_NAME.upper(), "privateName": KLEIN_PRIVATE_NAME}, spaceVariable]

    for i in range(len(spaceList)-1):
        spaceList[i]["frame"] = Frame(spaceMainCanvas, bg=BGCOLOR)
        spaceList[i]["frame"].grid(row = 0, column=i, sticky="ew")
        spaceMainCanvas.grid_columnconfigure(i, weight=1, uniform="space")
        spaceList[i]["label"] = Label(spaceList[i]["frame"], text=spaceList[i]["name"], bg=BGCOLOR, fg=TEXT_COLOR, font=("Segoe UI", SUBSUBTITLE_SIZE))
        spaceList[i]["label"].pack()

        img = loadImage("img").resize(IMG_SIZE)
        spaceList[i]["img"] = ImageTk.PhotoImage(img)

        imgS = loadImage("imgS").resize(IMG_SIZE)
        spaceList[i]["imgS"] = ImageTk.PhotoImage(imgS)


        spaceList[i]["button"] = Label( spaceList[i]["frame"], image=spaceList[i]["img"], bg=BGCOLOR, bd=0)
        spaceList[i]["button"].pack()

        spaceList[i]["button"].bind("<Button-1>", partial(changeSelection, i, spaceList))

        spaceList[i]["button"].bind("<Enter>", partial(hoverImg, i, spaceList))
        spaceList[i]["button"].bind("<Leave>", partial(unhoverImg, i, spaceList))
        

    spaceBotPadding = Frame(spaceFrame, bg=BG_VISUALS, height=END_SECTION_PADDING)
    spaceBotPadding.pack(fill="x")





    # Players
    PLAYER_SECTIONS_WIDTH = (INTERIOR_WIDTH-INTERSECTION_PADDING)/2 - BORDER_THICK*2
    RIVAL_HEIGHT = 211



    # Rival selection
    rivalFrame = Frame(mainCanvas, bg=BG_VISUALS, width=PLAYER_SECTIONS_WIDTH, height=RIVAL_HEIGHT, highlightbackground=DETAILS_COLOR, highlightthickness=BORDER_THICK, highlightcolor=DETAILS_COLOR)
    rivalFrame.pack_propagate(False)
    rivalFrame.place(x=EXTERNAL_PADDING, y=totalHeight)


    rivalText = Label(rivalFrame, text="select rival", bg=BGCOLOR, fg=TEXT_COLOR, font=("Segoe UI", SUBTITLE_SIZE, "bold"))
    rivalText.pack()


    rivalSuperiorIndicator = Frame(rivalFrame, bg=BGCOLOR, height=2)
    rivalSuperiorIndicator.pack_propagate(False)
    rivalSuperiorIndicator.pack(fill="x")

    listFrame = Frame(rivalFrame, bg=BGCOLOR, height=165)
    listFrame.pack_propagate(False)
    listFrame.pack(fill="x", padx=30)


    def manageScrollIndicators(*args):
        scrollPosition = rivalList.yview()
        if scrollPosition[0]>0:
            rivalSuperiorIndicator.config(bg=ALTERNATIVE_COLOR_1)
        else:
            rivalSuperiorIndicator.config(bg=BGCOLOR)
        if scrollPosition[1]<1:
            rivalInferiorIndicator.config(bg=ALTERNATIVE_COLOR_2)
        else:
            rivalInferiorIndicator.config(bg=BGCOLOR)

    def mousewheelManager(event):
        if event.delta > 0:
            rivalList.yview_scroll(-1, "units")
        else:
            rivalList.yview_scroll(1, "units")
        

        return "break"

    global racers
    racers = []
    items = ["", "E:RR | None"] #There is a bug where you can select the empty item
    rivalList = Listbox(
        listFrame,
        font=("Segoe UI", SUBTITLE_SIZE),
        bg=BGCOLOR,
        fg=DETAILS_COLOR,
        selectbackground=BGCOLOR,
        selectforeground=MAINCOLOR,
        highlightthickness=0,
        relief="flat",
        height=4,
        yscrollcommand=manageScrollIndicators,
        exportselection=False # To fix the bug where the item gets unselected when double-clicking on the entry
    )
    for item in items:
        rivalList.insert("end", item)
    rivalList.select_set(1)
    rivalList.place(x=0, y=-20, relwidth=1, relheight=1.2)
    rivalList.bind("<MouseWheel>", mousewheelManager)

    rivalInferiorIndicator = Frame(rivalFrame, bg=BGCOLOR, height=2)
    rivalInferiorIndicator.pack_propagate(False)
    rivalInferiorIndicator.pack(fill="x")


    manageScrollIndicators()


    # Final steps

    NAME_HEIGHT = 100

    def checkLen(new_text):
        if len(new_text) < PLAYER_NAME_LEN:
            return True
        return False


    # Player name
    BUTTON_X = EXTERNAL_PADDING+PLAYER_SECTIONS_WIDTH+EXTERNAL_PADDING
    nameFrame = Frame(mainCanvas, bg=BG_VISUALS, width=PLAYER_SECTIONS_WIDTH, height=NAME_HEIGHT, highlightbackground=DETAILS_COLOR, highlightthickness=BORDER_THICK,highlightcolor=DETAILS_COLOR)
    nameFrame.pack_propagate(False)
    nameFrame.place(x=BUTTON_X, y=totalHeight)
    totalHeight = totalHeight + NAME_HEIGHT + INTERSECTION_PADDING + BORDER_THICK

        # Blocks large names
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

    underline = Frame(entryFrame, height=2, bg=DETAILS_COLOR)
    underline.pack(fill="x")

    def showUnderline(event):
        underline.config(bg=MAINCOLOR)
        nameEntry.config(fg=TEXT_COLOR)

    def hideUnderline(event):
        underline.config(bg=DETAILS_COLOR)
        nameEntry.config(fg=MAINCOLOR)


    nameEntry.bind("<FocusIn>", showUnderline)
    nameEntry.bind("<FocusOut>", hideUnderline)


    # Start button


    def startGame():
        parameters = {}
        spaceId = spaceList[-1].get()
        if spaceId==-1:
            print("ERROR: NO SPACE SELECTED") #TODO, something to reflec it
            return False
        else:
            parameters["space"] = spaceList[spaceId]["privateName"]

        mapId = mapsList[-1].get()
        if mapId==-1:
            print("ERROR: NO MAP SELECTED") #TODO, something to reflec it
            return False
        else:
            parameters["map"] = mapsList[mapId]["privateName"]
        
        rivalId = rivalList.curselection()
        print(rivalId)
        print(racers)
        if rivalId:
            rivalId = rivalId[0]
            if rivalId>1:
                parameters["rival"] = racers[rivalId-2]["name"]
            else:
                parameters["rival"] = None  
        else:
            parameters["rival"] = None  

        name = nameEntry.get()
        parameters["name"] = name
        for widget in main.winfo_children():
            widget.destroy()
        beginGame(main, parameters)
        createInterface(main)


    BUTTON_WIDTH = 200
    BUTTON_HEIGHT = 50

    global pixel_virtual
    pixel_virtual = tk.PhotoImage(width=1, height=1)
    startButton = Button(mainCanvas, bg=DETAILS_COLOR, fg=BGCOLOR, cursor="hand2", activebackground=MAINCOLOR_DARK,
                        text="START", relief="raised", border=5, font=("Segoe UI", SUBTITLE_SIZE, "bold"), image=pixel_virtual,
                        compound="c", width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command=startGame)
    startButton.place(x=BUTTON_X+ (PLAYER_SECTIONS_WIDTH-BUTTON_WIDTH)/2, y=totalHeight)
    totalHeight = totalHeight + BUTTON_HEIGHT + 2*INTERSECTION_PADDING+EXTERNAL_PADDING
    def onEnterButton(e):
        startButton.config(bg=MAINCOLOR)

    def onLeaveButton(e):
        startButton.config(bg=DETAILS_COLOR)

    startButton.bind("<Enter>", onEnterButton)
    startButton.bind("<Leave>", onLeaveButton)

    D.startCalculations()