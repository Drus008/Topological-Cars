from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from tkinter import Tk, Canvas
from collections import deque
import numpy as np
import random


from topologicalCanvas import topologicalCanvas
from constants import *

def getLab(hexStr:str)->LabColor:
    """Given a color in hexadecimal format, returns its lab format.
    Args:
        hexStr (str): The color in hexadecimal format ("#XXXXXX").
    Returns:
        The color in LabColor format.
    """
    rgb = sRGBColor.new_from_rgb_hex(hexStr)
    return convert_color(rgb, LabColor)

def interpolateLab(color0:str, color1:str, t:float)->str:
    """Returns the color in between two other with a certain proportion.
    Args:
        color0 (str): The first color. It must be in hex format ("#XXXXXX").
        color1 (str): The second color. It must be in hex format ("#XXXXXX").
        t (float): A number between 0 and 1 that represents the proportion of color0 (color1 has the remaining 1-t).
    Returns:
        The mix of the two colors.
    """
    color0Lab = getLab(color0)
    color1Lab = getLab(color1)

    
    l = color0Lab.lab_l + (color1Lab.lab_l - color0Lab.lab_l) * t
    a = color0Lab.lab_a + (color1Lab.lab_a - color0Lab.lab_a) * t
    b = color0Lab.lab_b + (color1Lab.lab_b - color0Lab.lab_b) * t
    
    finalColor = LabColor(l, a, b)
    
    rgb = convert_color(finalColor, sRGBColor)
    
    r = max(0, min(255, int(rgb.rgb_r * 255)))
    g = max(0, min(255, int(rgb.rgb_g * 255)))
    b = max(0, min(255, int(rgb.rgb_b * 255)))
    
    return "#{:02x}{:02x}{:02x}".format(r, g, b)

GRADIENT_1 = [interpolateLab(BGCOLOR, ALTERNATIVE_COLOR_1, t) for t in np.linspace(0,1, 100)]
GRADIENT_2 = [interpolateLab(BGCOLOR, ALTERNATIVE_COLOR_2, t) for t in np.linspace(0,1, 100)]

class decoration:
    """A polygon with random sides and size that moves randomly across the canvas. It hides in the background unless specified.
    Attributes:
        parent (Canvas): The tk parent.
        color (int): The index of the visible color of the object.
        lastColor (int): Saves the index of the last color.
        nSides (int): The number of sides of the polygon.
        originalPosition (array): The starting position of the decoration. It tends to go there.
        position (array): Its actual position.
        speed (array): Its speed. (controlled by a semi-random walk)
        self.figura (int): The tkinter obkect drawn on the canvas.
    """
    
    def __init__(self, canvas:Canvas, position:(np.ndarray), vertex:list[np.ndarray], color: int=1):
        """Initializes a decoration.
        Args:
            canvas (Canvas): The parent of the decoration.
            position (array): The initial position.
            vertex (list[array]): A list of its vertices.
            color (int): The index of the color of the object when visible.
        """
        self.parent = canvas
        self.color = color
        self.lastColor = -1
        self.nSides = random.randint(3, 5)
        self.originalPosition = position
        self.position = position
        self.speed = np.zeros(2)
        self.vertex = vertex
        flatenedVertex = [list(v) for v in vertex]
        colors = [ALTERNATIVE_COLOR_1, ALTERNATIVE_COLOR_2]
        self.figure = canvas.create_polygon(*flatenedVertex, fill=colors[color-1])
    

    @classmethod
    def random(cls, canvas:Canvas, position:(np.ndarray), figuresSize:float=30, color:int=1):
        """Initializes a random decoration.
        Args:
            canvas (Canvas): The parent of the decoration.
            position (array): The initial position.
            figuresSize (float): The maximum length of a side.
            color (int): The index of the color of the object when visible.
        """
        nSides = random.randint(3, 5)
        vertex = []
        vertex.append(np.random.rand(2)*figuresSize+position)
        for i in range(nSides-1):
            correct = False
            while not correct:
                correct = True
                newSide = np.random.rand(2)*figuresSize+position
                if i>0:
                    if np.linalg.norm(newSide-vertex[i-2])<2*figuresSize/nSides:
                        correct = False
                        break
                for side in vertex:
                    if np.linalg.norm(newSide-side)<figuresSize/nSides:
                        correct = False
                        break
            vertex.append(newSide)
        return cls(canvas, position, vertex, color)

    def computeSpeed(self, delta:float)->np.ndarray:
        """Given the elapsed time, return its change in velocity.
        Args:
            delta (float): The time elapsed since the last computation.
        Returns:
            A vector with the velocity increment."""
        vNorm = abs(self.speed[0])+abs(self.speed[1])

        ORIGIN_REPULSION = 10
        ORIGIN_ATTRACTION = 0.1
        DISPERSION = 500

        if vNorm<0.02:
            dv = np.random.normal(scale=DISPERSION*delta, size=2)*ORIGIN_REPULSION
        else:
            d = self.position-self.originalPosition
            dv = np.random.normal(scale=DISPERSION*delta, size=2) - random.random()*d*ORIGIN_ATTRACTION
        return dv

    def applySpeed(self, dv:np.ndarray, delta:float)->None:
        """Given the time elapsed and the change in speed, it updates its position.
        Args:
            dv (array): The velocity increment.
            delta (float): The time elapsed.
            """

        self.speed = self.speed + dv

        dp = self.speed*delta
        self.position = self.position + dp
        self.parent.move(self.figure, *dp)

    def changeColor(self, c: float) -> None:
        """Reveals the object a certain amount controlled by c.
        Args:
            c (float): A float between 0 and 1 that controls the visibility of the decoration. 0 -> invisible, 1 -> Totally visible.
        """
        c = max(0.0, min(1.0, c))
        index = int(c*99)
        if index!=self.lastColor:
            if self.color==1:
                color = GRADIENT_1[index]
            else:
                color = GRADIENT_2[index]
            self.parent.itemconfigure(self.figure, fill=color)
    
    def cloneOriented(self, TCanvas:topologicalCanvas, row: int=0, col: int=0):
        """
        Creates a copy on the same canvas.
        """
        if row%2==0 and col%2==0:
            new_vertices = [ v.copy() for v in self.vertex]
            new_pos = self.position.copy()
        elif row%2==0 and col%2==1:
            new_vertices = [np.array([v[0], TCanvas.gluingFuncH(v[1])]) for v in self.vertex]
            new_pos = np.array([self.position[0], TCanvas.gluingFuncH(self.position[1])])
        elif row%2==1 and col%2==0:
            new_vertices = [np.array([TCanvas.gluingFuncV(v[0]), v[1]]) for v in self.vertex]
            new_pos = np.array([TCanvas.gluingFuncH(self.position[0]), self.position[1]])
        else:
            new_vertices = [np.array([TCanvas.gluingFuncV(v[0]), TCanvas.gluingFuncH(v[1])]) for v in self.vertex]
            new_pos = np.array([TCanvas.gluingFuncH(self.position[0]), TCanvas.gluingFuncV(self.position[1])])
        offset = np.array([TCanvas.dimX*col, TCanvas.dimY*row])
        new_vertices = new_vertices + offset
        new_pos = new_pos + offset
        
        new_dec = decoration(self.parent, new_pos, new_vertices, self.color)
                
        return new_dec


class decorationFamily:
    """The background animation.
    The idea is that it spawns random polygons that move randomly and hide in the background, appearing when specified.
    """
    # OPTIMIZE: This could manage all the variables with np instead of using the decoration class.
    def __init__(self, canvas: Canvas, number: int, decSize=30, minX=0, maxX=None, minY=0, maxY=None):
        canvas.update()
        if not maxX:
            maxX = canvas.winfo_width()
        if not maxY:
            maxY = canvas.winfo_height()
        self.decorations: list[decoration] = []
        self.parent = canvas
        self.animations = True
        
        self.mouseX = self.parent.winfo_pointerx()
        self.mouseY = self.parent.winfo_pointery()

        self.lastSpeeds = deque([], 10)

        for _ in range(number):
            correct = False
            while not correct:
                correct = True
                
                position = np.array([random.randint(minX, maxX), random.randint(minY, maxY)])
                color = random.randint(0,1)
                for dec in self.decorations:
                    if np.linalg.norm(dec.position-position)<min(maxX-minX,maxY-minY)/number:
                        correct = False
                        break
                self.decorations.append(decoration.random(canvas, position, color=color, figuresSize=decSize))
    
    def moveDecorations(self, delta:float)->None:
        """Moves each decoration.
        Args:
            delta (float): The time elapsed.
        """
        for dec in self.decorations:
            dv = dec.computeSpeed(delta)
            dec.applySpeed(dv, delta)

    def setColorBasedOnMouse(self) -> None:
        """Sets the visibility of the decorations based on the mouse speed."""
        newMouseX = self.parent.winfo_pointerx()
        newMouseY = self.parent.winfo_pointery()
        c = (abs(newMouseX-self.mouseX)+abs(newMouseY-self.mouseY))/200
        self.lastSpeeds.append(c)
        for dec in self.decorations:
            dec.changeColor(max(self.lastSpeeds))

        self.mouseX = newMouseX
        self.mouseY = newMouseY
        

    def startCalculations(self)->None:
        """Starts the animations"""
        if self.animations:
            self.setColorBasedOnMouse()
            self.moveDecorations(0.01)
            self.parent.after(10, self.startCalculations)

    def computeVelocity(self, delta:float)->list[np.ndarray]:
        """Computes the chage in velocity of each decoration.
        Args:
            delta (float): The time elapsed.
            
        Returns:
            A list with the velocity change of each decoration.
        """
        changes = []
        for dec in self.decorations:
            changes.append(dec.computeSpeed(delta))
        return changes
    
    def moveDecorionsPrecisely(self, delta:float, dvList:list[np.ndarray])->None:
        """Moves each decoration the specified amount.
        Args:
            delta (float): The time elapsed.
            dvList (list[array]): The amount of velocity change of each decoration.
        """
        for decId in range(len(self.decorations)):
            self.decorations[decId].applySpeed(dvList[decId], delta)

    def clone(self, TCanvas: topologicalCanvas, row: int, col: int):
        """Creates a clone following the geometry of a TCanvas.

        Args:
            TCanvas (topologicalCanvas): The TCanvas where the family will live.
            row (int): The corresponding cell row of the TCanvas.
            col (int): The corresponding cell column of the TCanvas.
        """

        newFamily = decorationFamily(self.parent, number=0)
        for item in self.decorations:
            clonedDec = item.cloneOriented(TCanvas,row, col)
            newFamily.decorations.append(clonedDec)
            
        return newFamily



class topologicalDecorationFamily:
    def __init__(self, TCanvas: topologicalCanvas, number: int, size = 100):
        self.TCanvas = TCanvas 
        self.instances: list[list[decorationFamily]] = []
        for r in range(6):
            row = []
            for c in range(6):
                if r==0 and c==0:
                    localFamily = decorationFamily(TCanvas.canvas, number, maxX=TCanvas.dimX, maxY=TCanvas.dimY, decSize=size)
                    row.append(localFamily)
                else:
                    row.append(localFamily.clone(TCanvas, r, c))
            self.instances.append(row)
    
    def moveDecorations(self, delta:float):
        displacement = self.instances[0][0].computeVelocity(delta)
        orientatorV = np.array([self.TCanvas.vOrientation,1])
        orientatorH = np.array([1, self.TCanvas.hOrientation])
        orientator = np.array([1,1])
        for r in range(6):
            for c in range(6):
                self.instances[r][c].moveDecorionsPrecisely(delta, displacement*orientator)
                orientator = orientator * orientatorH
            orientator = orientator * orientatorV    
    def startCalculations(self):
        self.moveDecorations(0.01)
        self.TCanvas.canvas.after(30, self.startCalculations)
                



if __name__=="__main__":
    tk = Tk()
    tk.geometry("750x750")
    canvas = Canvas(tk)
    canvas.pack(expand=True, fill="both")
    D = decorationFamily(canvas,100)
    D.startCalculations()
    D.setColorBasedOnMouse()
    tk.mainloop()