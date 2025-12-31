from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from tkinter import Tk, Canvas
from collections import deque
import numpy as np
import random




from constants import *

def getLab(hex_str)->LabColor:
    rgb = sRGBColor.new_from_rgb_hex(hex_str)
    return convert_color(rgb, LabColor)

def interpolateLab(color0:str, color1:str, t:float)->str:
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

class decoration:
    
    def __init__(self, canvas:Canvas, position, size=30, color=ALTERNATIVE_COLOR_1):
        self.parent = canvas
        self.color = color
        self.direction = np.zeros(2)
        
        self.nSides = random.randint(3, 5)
        self.originalPositon = position
        self.position = position
        self.speed = np.zeros(2)
        
        vertex = self.createSides(size)
        self.figure = canvas.create_polygon(*vertex, fill=color)

    def createSides(self, size):
        sides = []
        sides.append(np.random.rand(2)*size+self.position)
        points = [sides[0][0], sides[0][1]]
        for i in range(self.nSides-1):
            correct = False
            while not correct:
                correct = True
                newSide = np.random.rand(2)*size+self.position
                if i>0:
                    if np.linalg.norm(newSide-sides[i-2])<2*size/self.nSides:
                        correct = False
                        break
                for side in sides:
                    if np.linalg.norm(newSide-side)<size/self.nSides:
                        correct = False
                        break
            sides.append(newSide)
            points = points + list(newSide)
        return points

    def computeSpeed(self, delta):
        vNorm = np.linalg.norm(self.speed)

        ORIGIN_REPULSION = 10
        FRICTION = 0.1
        ORIGIN_ATRACTION = 0.1
        DISPERSION = 500

        if vNorm<0.02:
            dv = np.random.normal(scale=DISPERSION*delta, size=2)*ORIGIN_REPULSION
        else:
            d = self.position-self.originalPositon
            dv = np.random.normal(scale=DISPERSION*delta, size=2) - random.random()*d*ORIGIN_ATRACTION # - self.speed*FRICTION 

        return dv

    def aplySpeed(self, dv, delta):

        self.speed = self.speed + dv

        dp = self.speed*delta
        self.position = self.position + dp
        if np.linalg.norm(self.position)>4000:
            print("OUT")
        self.parent.move(self.figure, *dp)
        
    
    def changeColor(self, c):

        self.parent.itemconfigure(self.figure, fill=interpolateLab(BGCOLOR, self.color, c))


class decorationFamily:
    def __init__(self, canvas: Canvas, number: int):
        canvas.update()
        self.decorations: list[decoration] = []
        self.parent = canvas
        self.animations = True
        
        self.mouseX = self.parent.winfo_pointerx()
        self.mouseY = self.parent.winfo_pointery()

        self.lastSpeeds = deque([], 10)

        dimX = canvas.winfo_width()
        dimY = canvas.winfo_height()

        colors = [ALTERNATIVE_COLOR_1, ALTERNATIVE_COLOR_2]
        for _ in range(number):
            correct = False
            while not correct:
                correct = True
                
                position = np.array([random.randint(0, dimX), random.randint(0, dimY)])
                color = colors[round(random.random())]
                for dec in self.decorations:
                    if np.linalg.norm(dec.position-position)<min(dimX,dimY)/number:
                        correct = False
                        break
                self.decorations.append(decoration(canvas, position, color=color))
    
    def moveDecorations(self, delta:float):
        for dec in self.decorations:
            dv = dec.computeSpeed(delta)
            dec.aplySpeed(dv, delta)
    
    def setColor(self):
        newMouseX = self.parent.winfo_pointerx()
        newMouseY = self.parent.winfo_pointery()
        c = np.linalg.norm(np.array([newMouseX-self.mouseX, newMouseY-self.mouseY]))/1400
        self.lastSpeeds.append(c)
        for dec in self.decorations:
            dec.changeColor(max(self.lastSpeeds))

        self.mouseX = newMouseX
        self.mouseY = newMouseY
        

    def startCalculations(self):
        if self.animations:
            self.setColor()
            self.moveDecorations(0.01)
            self.parent.after(10, self.startCalculations)


if __name__=="__main__":
    tk = Tk()
    tk.geometry("750x750")
    canvas = Canvas(tk)
    canvas.pack(expand=True, fill="both")
    D = decorationFamily(canvas,100)
    D.startCalculations()
    D.setColor()
    tk.mainloop()