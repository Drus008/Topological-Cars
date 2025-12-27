from tkinter import Tk, Label, Frame

import tkinter as tk

from math import log10
from time import sleep

#2C2825

BGCOLOR = "#1E1C1A"
BGCOLOR_PAD = "#2C2825"
COLOR_CHARS = "white"
COLOR_PAD_OFF = "#564E48"

class character():

    def __init__(self,frame, char:str=""):
        self.parent = frame
        self.bg = BGCOLOR_PAD
        self.color = COLOR_CHARS
        self.offColor = COLOR_PAD_OFF
        self.character = char
        self.frame = Frame(frame, bg=self.bg, height=60, width=55, bd=5, relief="groove")
        self.frame.pack_propagate(False)

        self.label = Label(self.frame, text=self.character, bg=self.bg, fg=self.color, font=("Digital-7", 55, "bold"))
        self.label.pack(expand=True, fill="both")
        
    def hide(self):
        self.label.configure(bg=self.offColor, text="")

    def reveal(self):
        self.label.configure(bg=self.bg, text=self.character)

    def changeCharacter(self, char: str):
        self.label.configure(text=char)
    

class stringFlip():
    def __init__(self, parent, nChars: int, string: str):
        
        self.parent = parent
        self.frame = Frame(parent, bg=BGCOLOR)
        self.frame.grid_rowconfigure(0, weight=1)
        self.nChars = nChars
        self.charLabels: list[character] = []
        for digit in range(nChars):
            newChar = character(self.frame, "A")
            newChar.frame.grid(row=0,column=digit,sticky="nsew", padx=2)
            self.charLabels.append(newChar)
        self.updateWord(string)

    def updateWord(self, word:str):

        for i in range(1,self.nChars+1):
            if self.charLabels[-i].character!= word[-i]:
                self.charLabels[-i].changeCharacter(word[-i])

class counter(stringFlip):
    def __init__(self, parent, digits: int, number: int):
        self.number = number

        super().__init__(parent, digits, digits*"0"+str(number))

    def updateNumber(self, num:int):
        self.number = int(num)
        strNum = "0"* self.nChars + str(self.number)
        for nDigit in range(1,self.nChars+1):
            digit = strNum[-nDigit]
            if digit==1:
                digit = " "+digit
        
        self.updateWord(strNum)
    
    def count(self):
        self.updateNumber(self.number+1)
        self.frame.after(100, self.count)



class timeCounter():
    def __init__(self, parent):
        self.parent = parent
        self.frame = Frame(parent, bg=BGCOLOR)
        self.frame.grid_rowconfigure(0, weight=1)

        self.time = 0

        self.minute = counter(self.frame,1,0)        
        self.minute.frame.grid(row=0,column=0, padx=7, sticky="nsew")

        self.sec = counter(self.frame,2,0)
        self.sec.frame.grid(row=0,column=1, padx=7, sticky="nsew")

        self.showTime(self.time)
    
    def showTime(self, time: int):
        
        if time<600:
            seconds = time%60
            minutes = time//60
            self.minute.updateNumber(minutes)
            self.sec.updateNumber(seconds)
        elif self.time<600:
            self.minute.updateWord("E")
            self.sec.updateWord("RR")
        self.time = time
        

    def countTime(self):
        self.showTime(self.time+1)
        self.frame.after(100, self.countTime)


def counterTry(palabra:character, num: int):
    w = str(num)
    if num==1:
        w = " "+w
    palabra.changeCharacter(w)
    num = num +1
    if num<10:
        palabra.label.after(500, counterTry, palabra, num)


class layout():
    def __init__(self, window: Tk, ):
        self.baner = Frame(window, bg=BGCOLOR, height=80)
        self.baner.pack(side="bottom", fill="x")
        self.baner.pack_propagate(False)
        self.border = Frame(window, bg="black", height=5)
        self.border.pack(side="bottom", fill="x")


        self.speed = counter(self.baner, 3, 23)
        self.speed.frame.pack(side="left", fill="y", expand=True)

        self.timer = timeCounter(self.baner)
        self.timer.frame.pack(side="left",fill="y",expand=True)

        self.laps = counter(self.baner, 1, 0)
        self.laps.frame.pack(side="left",fill="y",expand=True)

        self.name = stringFlip(self.baner,3, "AAA")
        self.name.frame.pack(side="left",fill="y",expand=True)




class App(Tk):
    """
    Controlador principal de la ventana.
    """
    def __init__(self):
        super().__init__()
        
        self.title("Interfaz Modular Tkinter")
        self.geometry("600x600")
        
    
        

if __name__ == "__main__":
    app = App()
    lay = layout(app)
    #c = character(lay.baner, "A")
    #c.frame.pack(side="bottom", fill="y", expand=True)
    #c2 = counter(lay.baner, 3, 3)
    #c2.frame.pack(side="bottom", fill="y", expand=True)
    #counterTry(c, 0)
    #c3 = timeCounter(lay.baner)
    #c3.frame.pack(side="bottom",fill="y",expand=True)
    #c3.frame.after(2000, c3.countTime)
    #lay.baner.after(1000, lay.timer.countTime)
    app.mainloop()