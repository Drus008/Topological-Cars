from tkinter import Tk, Label, Frame


BGCOLOR = "#1E1C1A"
BGCOLOR_PAD = "#2C2825"
COLOR_CHARS = "white"
COLOR_PAD_OFF = "#564E48"

class charPanel():
    """A widget that shows a panel with a char.
    Atributes:
        parent: The tkInter parent.
        bg (str): The background color of the panel.
        color (str): The font color.
        offColor (str): The panel color when its off.
        character (str): The character beeing show on the panel.
        frame (Frame): The frame that contains the character.
        label (Label): The tkInter label with the character.
    """
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
        
    def hide(self)->None:
        """Hides the character."""
        self.label.configure(bg=self.offColor, text="")

    def reveal(self)->None:
        """Reveals the character."""
        self.label.configure(bg=self.bg, text=self.character)

    def changeCharacter(self, char: str)->None:
        """Changes the character on the panel.
        Args:
            char (str): The character that will be placed on the panel."""
        self.label.configure(text=char)
    

class charPanelColection():
    """A widget that displays a colection of charPanels.
    Atributes:
        parent: The tkInter parent.
        frame: The frame that contains the charPanels.
        nCars (int): The number of chars in the colection.
        charLabelsList (list[charPanel]): A list with the charPanles.
        word (str): The word shown on the
    """
    def __init__(self, parent, nChars: int, string: str):
        self.parent = parent
        self.frame = Frame(parent, bg=BGCOLOR)
        self.frame.grid_rowconfigure(0, weight=1)
        self.nChars = nChars
        self.charLabelsList: list[charPanel] = []
        for digit in range(nChars):
            newChar = charPanel(self.frame, "A")
            newChar.frame.grid(row=0,column=digit,sticky="nsew", padx=2)
            self.charLabelsList.append(newChar)
        self.string = " "*nChars+ string
        self.updateWord(self.string)

    def updateWord(self, word: str)->None:
        """Updates the word shown on the panels.

        If the word is larger than the panel it shows the last characters.
        If the word is smaller than the panel it shows the word at the left and fills the remanig characters with spaces.

        """
        self.string = " "*self.nChars+ word
        for i in range(1,self.nChars+1):
            if self.charLabelsList[-i].character!= word[-i]:
                self.charLabelsList[-i].changeCharacter(word[-i])

class counterPanel(charPanelColection):
    """A charPanelColection intended to display numbers.

    It shows 0s on the empty chars.

    Atributes:
        number (int): The number shown.
    """
    def __init__(self, parent, digits: int, number: int):
        self.number = number

        super().__init__(parent, digits, digits*"0"+str(number))

    
    def updateNumber(self, num:int)->None:
        """Updates the number shown.
        Args:
            num (int): The number that will be shown."""
        self.number = int(num)
        strNum = "0"* self.nChars + str(self.number)
        for nDigit in range(1,self.nChars+1):
            digit = strNum[-nDigit]
            if digit=="1":
                digit = " "+digit
            self.charLabelsList[-nDigit].changeCharacter(digit)



class timeCounter():
    """A widget to display a minute and a second.
    Atributes:
        parent: The tkInter parent.
        frame (Frame): The frame that contains the panels.
        time (int): The number of seconds repesented on the panels.
        minute (counterPanel): the counter panel that displays the minutes (1 digit).
        sec (counterPanel): The counter panel that displays the seconds (2 digits).
    """
    def __init__(self, parent):
        self.parent = parent
        self.frame = Frame(parent, bg=BGCOLOR)
        self.frame.grid_rowconfigure(0, weight=1)

        self.time = 0

        self.minute = counterPanel(self.frame,1,0)        
        self.minute.frame.grid(row=0,column=0, padx=7, sticky="nsew")

        self.sec = counterPanel(self.frame,2,0)
        self.sec.frame.grid(row=0,column=1, padx=7, sticky="nsew")

        self.showTime(self.time)
    
    def showTime(self, time: int)->None:
        """Shows the time on the displays.

        If the time given is grater than 9min 59s then it displays "ERR".

        Args:
            time (int): The time that will be shown.
        """
        if time<600:
            seconds = time%60
            minutes = time//60
            self.minute.updateNumber(minutes)
            self.sec.updateNumber(seconds)
        elif self.time<600:
            self.minute.updateWord("E")
            self.sec.updateWord("RR")
        self.time = time
        


class layout():
    """The main layout that shows the speed, the time, the number of laps, and the name of the player.

    Attributes:
        banner: The frame that contains the panels.
        border: The border of the panel.
        speed (counterPanel): The panel intended to show the speed (3 digits).
        timer (timeCounter): The panel intended to show the time.
        laps (counterPanel): The panel intended to show the number of laps (1 digit).
    """
    def __init__(self, window: Tk):
        self.banner = Frame(window, bg=BGCOLOR, height=80)
        self.banner.pack(side="bottom", fill="x")
        self.banner.pack_propagate(False)
        self.border = Frame(window, bg="black", height=5)
        self.border.pack(side="bottom", fill="x")

        self.speed = counterPanel(self.banner, 3, 23)
        self.speed.frame.pack(side="left", fill="y", expand=True)

        self.timer = timeCounter(self.banner)
        self.timer.frame.pack(side="left", fill="y", expand=True)

        self.laps = counterPanel(self.banner, 1, 0)
        self.laps.frame.pack(side="left", fill="y", expand=True)

    def destroy(self) -> None:
        self.banner.destroy()
        self.border.destroy()
    





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