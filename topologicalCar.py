from topologicalObjects import topologicalPolygon
from topologicalCanvas import topologicalCanvas
from topologicalTerrain import terrainManager
from numpy import pi
import numpy as np
from tkinter import StringVar
from Tmath import direcrion2D

import json

class topologicalCar():
    """
    A car that moves within a topological canvas

    Atributes:
        TCanvas (topologicalCanvas): The topological canvas where the car will be placed.
        body (topologicalPolygon): The rectangle that represents the car on the canvas.
        v (array): The velocity vector of the car.
        acc (float): The acceleration of the car.
        angle (float): The angle at which the car is looking.
        width (float): The width of the car.
        height (float): The height of the car.
        angVel (float): The speed at wich the car turns.
    """

    def __init__(self, TCanvas: topologicalCanvas, ground:terrainManager, x0:float, y0:float, height:float, width:float, color="blue", acc=1, v0x = 0, v0y=0,rotationSpeed = 1):
        
        """
        Initializes the car given tha basic parameters.

        Args:
            TCanvas (topologicalCanvas): The topological canvas where the car will be placed.
            x0 (float): The x coordinate where the car is placed.
            y0 (float): The x coordinate where the car is placed.
            height (float): The height of the car.
            width (float): The width of the car.
            acc (float): The acceleration of the car.
            v0x (float): The initial velocity at x axis.
            v0y (float): The initial velocity at y axis.
            rotationSpeed (float): The speed at wich the car turns.
        Returns:
            A topological car.
        """

        self.aeroCoef = 1
        self.wheight = 1
        self.wheelGreep = 1

        self.TCanvas = TCanvas
        self.body = topologicalPolygon(TCanvas, [np.array([x0-width/2,y0-height/2]), np.array([x0+width/2,y0-height/2]), np.array([x0+width/2,y0+height/2]), np.array([x0-width/2,y0+height/2])], fill=color, tags=["topologicalCar"])
        self.ground = ground
        
        self.v = np.array([v0x, v0y], float)
        self.a = acc
        self.angle = pi/2

        self.angVel = rotationSpeed

        self.width = width
        self.height = height

        self.following = True
        self.vars = {"v" : StringVar(value=""),"Position" : StringVar(value=""), "angle" : StringVar(value=""),"Grip reduction" : StringVar(value="")}

        self.trajectory = [] #TODO description
        
    
    def updateCar(self):
        """
        Manages the car updates on each frame. (It has to be called).
        """
        #self.aplyFriction()
        self.calcAcc()
        self.keyboardManagment()
        self.updatePosition()
        self.centerCamara()

        self.vars["v"].set(str(round(self.v[0],3))+" "+str(round(self.v[1],3))) 
        self.vars["Position"].set(str(self.body.position)) 
        self.vars["angle"].set(str(self.angle)) 
    
    def centerCamara(self):
        """Centers de camara on the car."""
        self.TCanvas.setCamaraPosition(self.body.position[0], self.body.position[1])

    def updatePosition(self):
        """
        Updates the car's topological position based on his speed.
        """

        delta = self.TCanvas.delta

        dx =self.v[0]*delta
        dy = self.v[1]*delta
        self.body.TMove(dx,dy)
    

    def calcAcc(self):
        """Computes the acceleration of the car and updates its speed."""


        power = 0
        if self.TCanvas.keyStates["w"]:
            power = 1
        if self.TCanvas.keyStates["s"]:
            power = -1
        
        power = power*self.a

        AIR_FRICTION = 0.5
        GRIP, GROUND_FRICTION = self.ground.getFriction(self.body.position)

        tangDirection = direcrion2D(self.angle)
        perpDirection = np.array((tangDirection[1], -tangDirection[0]))
        acc = tangDirection*power*10
        acc = acc - self.v*AIR_FRICTION
        speedCoef = np.exp(-np.linalg.norm(self.v)/250)
        acc = acc - np.sign(np.dot(self.v,tangDirection))*tangDirection*GROUND_FRICTION
        acc = acc - speedCoef*GRIP*np.dot(self.v,perpDirection)*perpDirection
        
        self.v = self.v + acc*self.TCanvas.delta
        
    def rotateCar(self, sign):
        """
        Rotates the car to the desired direction.

        Args:
            sign (sign): The direction of the rotation. Positive clockwise and negative counterclockwise.
        Returns:
            A topological car.
        """
        orientation = -sign

        if np.dot(self.v,direcrion2D(self.angle))<0:
            orientation = -orientation
        delta = self.TCanvas.delta
                                                    #TODO the 0.1 is complitly arbitrary
        turnCoef = (1-np.exp(-np.linalg.norm(self.v))**.1) #Don't allow the car to turn when its speed is low.
        angle = orientation*delta*self.angVel*turnCoef 
        self.angle = self.angle+angle
        self.body.TRotation(angle)

    def keyboardManagment(self):
        """
        Manages how the car interacts with the keyboard imputs.
        """
        
        if self.TCanvas.keyStates["a"]:
            self.rotateCar(1)
        if self.TCanvas.keyStates["d"]:
            self.rotateCar(-1)

    def updateTrajectory(self):
        if len(self.trajectory)==0:
            time = 0
        else:
            time = self.trajectory[-1]["t"]+self.TCanvas.delta
        self.trajectory.append({"x":self.body.position[0],
                                "y":self.body.position[1],
                                "angle": self.angle,
                                "t":time})

    def save(self, map:str, player:str):
        trajectoryFile = {"map": map, "player": player, "trajectory":self.trajectory}
        with open(map+player+".json", "w") as f:
            json.dump(trajectoryFile, f, indent=2)
