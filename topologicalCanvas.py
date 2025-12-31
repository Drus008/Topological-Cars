from tkinter import Canvas, Tk
import numpy as np
import time

from stateMachine import keyStateMachine

# If optimization is necessary, a modification that could help is to only draw to the external squares the moving parts, and not the fixed ones

class topologicalCanvas():
    """
    Canvas with the sides glued.

    To get that effect a big canvas is created and divided into a matrix of 6x6 cells.
    The 2x2 cells of the center are the principal cells, where the action is supposed to happen.
    The other ones are there just to produce visual coherence.

    When we talk about a local property we are talking about the property of the object on the first cell (0,0).

    When we talk about a global property we are talking about the property of the object on the central cells (relative to them).

    When we talk about a normal property we are talking about the property of the object on the original canvas.

    Attributes:
        canvas (tkinter.Canvas): The canvas used to model the topological space.
        hOrientation (sign): The relation between the orientation of the left and right.
        vOrientation (sign): The relation between the orientation of the top and bottom.
        dimX (int): Width of the space.
        dimY (int): Height of the space.
        nElements (int): number of elements drawn on the original canvas.
        lastTime (time): The last time the canvas was updated.
        delta (float): The time elapsed between the last frame and the actual one.
        keyStates (keyStateMachine): A state machine to monitor which keys are pressed.
    """
    
    def gluingFuncH(self, y: float)->float:
        """
        Returns the number with the gluing relation applied.

        Args:
            y (float): The number to which the function will be applied.

        Returns:
           The number with the function applied.
        """
        if self.hOrientation==1:
            return y
        if self.hOrientation==-1:
            return self.dimY-y
    
    def gluingFuncV(self, x: float)->float:
        """
        Returns the number with the gluing relation applied.

        Args:
            x (float): The number to which the function will be applied.

        Returns:
           The number with the function applied.
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
            dimX (int): Width of the space.
            dimY (int): Height of the space.
            visualHelp (bool): If True it shows some visual help to make navigation easier.

        Returns:
            A topological canvas with the initialized values.
        """
        self.root = tk
        self.canvas: Canvas = Canvas(tk, width=windowW, height=windowH,
                                     scrollregion=(0,0,dimX*6,dimY*6))
        self.visualHelp = visualHelp
        if visualHelp:
            for i in range(6):
                self.canvas.create_line(i*dimX, 0, i*dimX, dimY*6)
                self.canvas.create_line(0, i*dimY, 6*dimY, i*dimY)
        
        self.canvas.pack(expand=True, fill="both")
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
        self.canvas.bind("<Configure>", self.changeOptions)

        self.canvas.config(takefocus=True)
        self.canvas.focus_set()
    
    
    def reflectedPoint(self, point:np.array)->np.array:
        """Given the coordinates of a point, returns its local coordinates."""
        newX=point[0]%self.dimX
        newY=point[1]%self.dimY
        #This could be optimized if needed
        if point[0]%(2*self.dimX)>self.dimX:
            newY = self.gluingFuncH(newY)
        if point[1]%(2*self.dimY)>self.dimY:
            newX = self.gluingFuncV(newX)
        return np.array([newX,newY])
        

    def topologicalPoint(self, x: float, y: float)->np.array:
        """
        Given the local coordinates of a point, returns the normal coordinates of the point on each cell.
        
        Args:
            x (float): the x local coordinate of the point.
            y (float): the y local coordinate of the point.

        Returns:
            A matrix where the element i,j are the normal coordinates of point on the i,j cell.
        """
        pointsMatrix = np.zeros((6,6,2))
        """ TODO It would be better if loc was calculated twice and placed on the corresponding indexes instead of calculating them every time """
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
    
    def updateDelta(self)->None:
        """
        It updates the time related variables.
        """
        newTime = time.perf_counter()
        self.delta = newTime - self.lastTime
        self.lastTime = newTime
    
    def getCamaraPosition(self)->np.array:
        """Returns the global position of the camera on the canvas"""
        fraccionx = self.canvas.xview()[0]
        fracciony = self.canvas.yview()[0]

        camarax = fraccionx * 6*self.dimX + self.windowX/2
        camaray = fracciony * 6*self.dimY + self.windowY/2

        camarax = camarax - self.dimX*2
        camaray = camaray - self.dimY*2
        print([camarax, camaray])
        return np.array([camarax, camaray])
    
    def setCamaraPosition(self, x:float, y:float)->np.array:
        """Sets the normal position of the camera to a specific global point"""
        camarax = x + self.dimX*2
        camaray = y + self.dimY*2
        fraccionx = (camarax - self.windowX/2)/(6*self.dimX)
        fracciony = (camaray - self.windowY/2)/(6*self.dimY)

        self.canvas.xview_moveto(fraccionx)
        self.canvas.yview_moveto(fracciony)

        return np.array([camarax, camaray])
    
    def changeOptions(self, event)->None:
        self.windowX = event.width
        self.windowY = event.height



class torus(topologicalCanvas):
    """
    A topological canvas that represents a Torus.
    """
    def __init__(self, tk, dimX=300, dimY=300, windowW= 400, windowH=400, visualHelp=False):
        super().__init__(tk, 1, 1, dimX, dimY, windowW=windowW, windowH=windowH, visualHelp=visualHelp)

class projectivePlane(topologicalCanvas):
    """
    A topological canvas that represents the projective plane.
    """
    def __init__(self, tk, dimX=300, dimY=300, windowW= 400, windowH=400, visualHelp=False):
        super().__init__(tk, -1, -1, dimX, dimY, windowW=windowW, windowH=windowH, visualHelp=visualHelp)

class KleinBottleH(topologicalCanvas):
    """
    A topological canvas that represents a Klein bottle (H).
    """
    def __init__(self, tk, dimX=300, dimY=300, windowW= 400, windowH=400, visualHelp=False):
        super().__init__(tk, 1, -1, dimX, dimY, windowW=windowW, windowH=windowH, visualHelp=visualHelp)

class KleinBottleV(topologicalCanvas):
    """
    A topological canvas that represents a Klein bottle (V).
    """
    def __init__(self, tk, dimX=300, dimY=300, windowW= 400, windowH=400, visualHelp=False):
        super().__init__(tk, -1, 1, dimX, dimY, windowW=windowW, windowH=windowH, visualHelp=visualHelp)

