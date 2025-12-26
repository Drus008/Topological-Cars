from topologicalObjects import topologicalThickCurve, topologicalPolygon
from topologicalCar import topologicalCar
import numpy as np
from time import time
from tkinter import Label


class finishLine():
    def __init__(self, curve:topologicalThickCurve, car: topologicalCar, size = 20):

        self.TOTAL_LAPS = 3
        self.laps = 0
        self.active = False
        self.counting = False
        
        
        self.TCanvas = curve.TCanvas
        self.car = car
        self.size = size
        self.curve = curve

        self.startTime = None

        self.interface = Label(
            self.TCanvas.root, 
            text="",
            font=("Helvetica", 40, "bold"),
            bg="black",
            fg="red",
        )
        self.interface.place(relx=0.5, rely=0.9, anchor="n")
        self.createVisuals()


    def createVisuals(self):
        squareSide = self.size/3
        nSquare = 0

        amplitude = self.curve.amplitudes[0]
        while(nSquare*squareSide<amplitude):
            nSquare = nSquare+1
            
        amplitude = nSquare*squareSide
        center = self.curve.center[0]
        direction = self.curve.center[1]-self.curve.center[0]
        angle = np.arctan2(direction[1], direction[0])
        
        self.hitbox = topologicalPolygon.rectangle(self.TCanvas, center, self.size, amplitude, angle)
        vec1 = self.hitbox.localVertices[1]-self.hitbox.localVertices[0]
        vec1 = squareSide*vec1/np.linalg.norm(vec1)
        vec2 = self.hitbox.localVertices[-1]-self.hitbox.localVertices[0]
        vec2 = squareSide*vec2/np.linalg.norm(vec2)
        squarePosition0 = self.hitbox.localVertices[0]+(vec1+vec2)/2
        for r in range(3):
            for c in range(nSquare):
                squarePosition = squarePosition0 + c*vec2+r*vec1
                if (r+c)%2==1:
                    color = "black"
                else:
                    color = "white"
                topologicalPolygon.square(self.TCanvas,squarePosition,squareSide,angle, fill=color)
    
    def checkLaps(self):
        position = self.car.body.position
        if self.active:
            if self.hitbox.checkIfPointInside(position):
                
                if self.laps==0:
                    self.startTime = time()
                    print("STARTING RACE")
                    self.counting = True
                elif self.laps==self.TOTAL_LAPS:
                    print("RACE FINISHED", time()-self.startTime)
                    self.active=False
                    self.counting = False
                self.laps = self.laps + 1
                print("LAPS:", self.laps)
                self.active = False
                    
        else:
            localCar = self.TCanvas.reflectedPoint(position)
            xDistance = abs(self.hitbox.position[0]-localCar[0])
            yDistance = abs(self.hitbox.position[1]-localCar[1])
            if xDistance>self.TCanvas.dimX/2 or yDistance>self.TCanvas.dimY/2:
                self.active=True

    def updateChronometer(self):
        if self.counting:
            self.interface.config(text=str(round(time()-self.startTime,1)))

    def update(self):
        self.checkLaps()
        self.updateChronometer()