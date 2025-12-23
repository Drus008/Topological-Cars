from tkinter import Canvas, Tk
from stateMachine import keyStateMachine
from Tmath import rotationMatrix
import numpy as np
import time

# If optimization is necessary, a modification that could help is to only draw to the external squares the mooving parts, and not the fix ones

class topologicalCanvas():
    """
    Canvas with the sides glued.

    Attributes:
        canvas (tkinter.Canvas): The canvas used to model de topological space.
        hOrientation (sign): The relation between the orientation of the left and bottom right.
        vOrientation (sign): The relation between the orientation of the top and bottom bottom.
        dimX (int): Witdh of the space.
        dimY (int): Height of the space.
        nElements (int): number of elements drawn on the original canvas.
        lastTime (time): The last time the canvas was updated.
        delta (float): The time elapsed between the las frame and the actual one.
        keyStates (keyStateMachine): A state machine to monitor wich keys are pressed.
    """
    
    def gluingFuncH(self, y: float)->float:
        """
        Returns the number with the gluing relation aplied.

        Args:
            y (float): The number to wich the function will be aplied.

        Returns:
           The number with the function aplied.
        """
        if self.hOrientation==1:
            return y
        if self.hOrientation==-1:
            return self.dimY-y
    
    def gluingFuncV(self, x: float)->float:
        """
        Returns the number with the gluing relation aplied.

        Args:
            y (float): The number to wich the function will be aplied.

        Returns:
           The number with the function aplied.
        """
        if self.vOrientation==1:
            return x
        if self.vOrientation==-1:
            return self.dimX-x

    def __init__(self, tk:Tk, hOrientation: int, vOrientation: int,  dimX=300, dimY=300, windowW= 400, windowH=400, visualHelp = False):
        """
        Initializes a topological canvas.

        Args:
            tk: The tkinter parent.
            hOrientation (sign): The relation between the orientation of the left and right sides.
            vOrientation (sign): The relation between the orientation of the top and bottom sides.
            dimX (int): Witdh of the space.
            dimY (int): Height of the space.
            visualHelp (bool): If True it shows some visual help to make navegation easier.

        Returns:
            A topological canvas with the initialized values.
        """
        self.canvas: Canvas = Canvas(tk, width=windowW, height=windowH,
                                     scrollregion=(0,0,dimX*6,dimY*6))
        self.visualHelp = visualHelp
        if visualHelp:
            for i in range(6):
                self.canvas.create_line(i*dimX, 0, i*dimX, dimY*6)
                self.canvas.create_line(0, i*dimY, 6*dimY, i*dimY)
        
        self.canvas.pack()
        self.vOrientation = vOrientation
        self.hOrientation = hOrientation
        self.dimX = dimX
        self.dimY = dimY

        self.windowX = windowH
        self.windowY = windowW

        self.nElements = 0

        self.lastTime = time.perf_counter()
        self.delta = 1

        self.keyStates = keyStateMachine()

        self.canvas.bind("<KeyPress>", self.keyStates.keyPresed)
        self.canvas.bind("<KeyRelease>", self.keyStates.keyReleased)

        self.canvas.config(takefocus=True)
        self.canvas.focus_set()
        
    def topologicalPoint(self, x: float, y: float)->np.array:
        """
        Given the coordinates of a point, returns the coordenates of each copy of the point in the topological canvas.
        
        Args:
            x (float): the x coordenate of the point.
            y (float): tht y coordenate of the point.

        Returns:
            A matrix where the element i,j are the cordinates of point on the i,j copy of the canvas.
        """
        pointsMatrix = np.zeros((6,6,2))
        """ TODO It would be better if loc was calculated twice and placed on the corresponding indexes insted of calculating them every time """
        for r in range(6):
            for c in range(6):
                if c%2==1:
                    yloc = self.gluingFuncH(y)
                else:
                    yloc = y
                if r%2==1:
                    xloc = self.gluingFuncV(x)
                else:
                    xloc = x

                pointsMatrix[r][c][0] = xloc + c*self.dimX
                pointsMatrix[r][c][1] = yloc + r*self.dimY
        
        return pointsMatrix
    
    def updateDelta(self):
        """
        It updates the time related variables.
        """
        newTime = time.perf_counter()
        self.delta = newTime - self.lastTime
        self.lastTime = newTime
    
    def getCamaraPosition(self)->np.array:

        fraccionx = self.canvas.xview()[0]
        fracciony = self.canvas.yview()[0]

        camarax = fraccionx * 6*self.dimX + self.windowX/2
        camaray = fracciony * 6*self.dimY + self.windowY/2

        camarax = camarax - self.dimX*2
        camaray = camaray - self.dimY*2

        return np.array([camarax, camaray])
    
    def setCamaraPosition(self, x:float, y:float)->np.array:

        camarax = x + self.dimX*2
        camaray = y + self.dimY*2
        fraccionx = (camarax - self.windowX/2)/(6*self.dimX)
        fracciony = (camaray - self.windowY/2)/(6*self.dimY)

        self.canvas.xview_moveto(fraccionx)
        self.canvas.yview_moveto(fracciony)

        return np.array([camarax, camaray])


class torus(topologicalCanvas):
    """
    A topological canvas that represents a Torus.
    """
    def __init__(self, tk, dimX=300, dimY=300, visualHelp=False):
        super().__init__(tk, 1, 1, dimX, dimY, visualHelp)

class projectivePlane(topologicalCanvas):
    """
    A topological canvas that represents the projectiva plane.
    """
    def __init__(self, tk, dimX=300, dimY=300, visualHelp=False):
        super().__init__(tk, -1, -1, dimX, dimY, visualHelp)

class KleinBottleH(topologicalCanvas):
    """
    A topological canvas that represents a Klein bottle (H).
    """
    def __init__(self, tk, dimX=300, dimY=300, visualHelp=False):
        super().__init__(tk, 1, -1, dimX, dimY, visualHelp)

class KleinBottleV(topologicalCanvas):
    """
    A topological canvas that represents a Klein bottle (V).
    """
    def __init__(self, tk, dimX=300, dimY=300, visualHelp=False):
        super().__init__(tk, -1, 1, dimX, dimY, visualHelp)



if __name__=="__main__":

    size = 100

    tk = Tk()
    Topos = topologicalCanvas(tk, hOrientation=1, vOrientation=-1, dimX= size, dimY= size, windowH=600, windowW= 600, visualHelp= True)

    from topologicalObjects import topologicalLine, topologicalPolygon

    topologicalLine(Topos,[20,20],[50, 20])
    topologicalPolygon(Topos,[[30,30],[50, 30], [50,50]])

    tk.mainloop()
