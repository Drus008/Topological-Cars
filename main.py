from tkinter import Tk

from filesManager import checkFolders
from titleInterface import createInterface
from constants import DIMX, DIMY



tk = Tk()
xPos = str((tk.winfo_screenwidth()-DIMX)//2)
yPos = (tk.winfo_screenheight()-30-DIMY)//2
yPos = str(yPos) if yPos>0 else "0"
tk.geometry(str(DIMX)+"x"+str(DIMY)+"+"+xPos+"+"+yPos)

checkFolders()
createInterface(tk)
tk.mainloop()
