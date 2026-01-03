from tkinter import Tk

from filesManager import checkFolders
from titleInterface import createInterface
from constants import DIMX, DIMY, GAME_NAME



tk = Tk()
xPos = str((tk.winfo_screenwidth()-DIMX)//2)
yPos = (tk.winfo_screenheight()-30-DIMY)//2
yPos = str(yPos) if yPos>0 else "0"
tk.geometry(str(DIMX)+"x"+str(DIMY)+"+"+xPos+"+"+yPos)
tk.resizable(False, False)
tk.title(GAME_NAME)
checkFolders()
createInterface(tk)
tk.mainloop()
