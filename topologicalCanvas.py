from tkinter import Canvas, Tk
import numpy as np


VISUAL_HELP = True

class topologicalCanvas():
    """
    Canvas with the extremes glooed.



    Attributes:
        canvas (tkinter.Canvas): The canvas used to model de topological space.
        glooingFuncV (callable): The glooing method between the top and bottom sides.
        glooingFuncH (callable): The glooing method between the left and right sides.
        dimX (int): Witdh of the space.
        dimY (int): Height of the space.
    """
    def _Id(x: float)->float:
        """
        Identity function

        Args:
            x (float): A number between 0 and 1 (inclusive).

        Returns:
            x
        """
        return x
    def __init__(self, tk:Tk, glooingFuncH: callable = _Id, glooingFuncV: callable =_Id,  dimX=300, dimY=300, visualHelp = False):
        """
        Initializes a topological canvas.

        Args:
            tk (tkinter.Tk): The Tk parent.
            glooingFuncH (callable): The glooing method between the top and bottom sides.
            glooingFuncV (callable): The glooing method between the left and bottom right.
            dimX (int): Witdh of the space.
            dimY (int): Height of the space.
            visualHelp (bool): If it is True, it shows some help to position yourself on the canvas.

        Returns:
            A topological canvas with the initialized values.
        """
        self.canvas: Canvas = Canvas(tk, width=dimX*4, height=dimY*4)

        if visualHelp:
            self.canvas.create_line(dimX, 0, dimX, dimY*4)
            self.canvas.create_line(2*dimX, 0, 2*dimX, dimY*4)
            self.canvas.create_line(3*dimX, 0, 3*dimX, dimY*4)
            self.canvas.create_line(0, dimY, dimX*4, dimY)
            self.canvas.create_line(0, 2*dimY, dimX*4, 2*dimY)
            self.canvas.create_line(0, 3*dimY, dimX*4, 3*dimY)
        
        self.canvas.pack()
        self.glooingFuncV = glooingFuncV
        self.glooingFuncH = glooingFuncH
        self.dimX = dimX
        self.dimY = dimY
        
    
    def create_line(self, pInitial: np.array, pFinal: np.array)-> None:
        """
        Creates a line on the topological space.

        That means that the line is reapeted on each of the copies of the original space.

        Args:
            pInitial (np.array): The initial point of the line on the original space.
            pFinal (np.array): The final point of the line on the original space.
        """
        for f in range(4):
            for c in range(4):
                funcH = self.glooingFuncH
                funcV = self.glooingFuncV
                if c%2==1:
                    funcH = topologicalCanvas._Id
                if f%2==1:
                    funcV = topologicalCanvas._Id

                p0x = funcV(pInitial[0]/self.dimX)*self.dimX
                p0y = funcH(pInitial[1]/self.dimY)*self.dimY
                p1x = funcV(pFinal[0]/self.dimX)*self.dimX
                p1y = funcH(pFinal[1]/self.dimY)*self.dimY

                self.canvas.create_line(p0x+c*self.dimX, p0y+f*self.dimY, p1x+c*self.dimX, p1y +f*self.dimY)


size = 200
def inv(x):
    return 1-x

tk = Tk()
Topos = topologicalCanvas(tk, glooingFuncH= topologicalCanvas._Id, glooingFuncV= inv, dimX= size, dimY= size, visualHelp= True)



Topos.create_line([20,20],[50, 20])

tk.mainloop()
