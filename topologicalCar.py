from topologicalObjects import topologicalPolygon, topologicalThickCurve
from topologicalCanvas import topologicalCanvas
from numpy import pi
import numpy as np
from tkinter import Tk, StringVar
from Tmath import direcrion2D, baseChange, baseChangeOrt, baseReturnOrt

from monitor import windowMonitor

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

    def __init__(self, TCanvas: topologicalCanvas, x0:float, y0:float, height:float, width:float, acc=1, v0x = 0, v0y=0,rotationSpeed = 1):
        
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

        self.TCanvas = TCanvas
        self.body = topologicalPolygon(TCanvas, [[x0-width/2,y0-height/2], [x0+width/2,y0-height/2], [x0+width/2,y0+height/2], [x0-width/2,y0+height/2]], tags=["topologicalCar"])
        self.v = np.array([v0x, v0y], float)
        self.a = acc
        self.angle = pi/2

        self.angVel = rotationSpeed

        self.width = width
        self.height = height

        self.following = True
        self.vars = {"v" : StringVar(value=""),"Position" : StringVar(value=""), "angle" : StringVar(value=""),"Grip reduction" : StringVar(value="")}
        
    
    def updateCar(self):
        """
        Manages the car updates on each frame. (It has to be called).
        """
        self.aplyFriction()
        self.keyboardManagment()
        self.updatePosition()
        self.updateCamara()

        self.vars["v"].set(str(round(self.v[0],3))+" "+str(round(self.v[1],3))) 
        self.vars["Position"].set(str(self.body.position)) 
        self.vars["angle"].set(str(self.angle)) 
    
    def updateCamara(self):
        
        self.TCanvas.setCamaraPosition(self.body.position[0], self.body.position[1])

    def updatePosition(self):
        """
        Updates the car's topological position based on his speed.
        """

        delta = self.TCanvas.delta

        dx =self.v[0]*delta
        dy = self.v[1]*delta
        self.body.TMove(dx,dy)
    

    def aplyFriction(self):
        """
        Aplies the friction to the car slowing it down based on its speed and direction.

        TODO consider diferent friction coeficient based on the terrain.
        """
        tangentFriction = 0.1
        perpFriction = 20
        tangDirection = direcrion2D(self.angle)
        perpDirection = np.array((tangDirection[1], -tangDirection[0]))

        delta = self.TCanvas.delta
                                                    #TODO the 100 is complitly arbitrary
        gripReduction = np.exp(-np.linalg.norm(self.v)/100) #Models the reduction of the wheel grip due to high speed.
        self.vars["Grip reduction"].set(str(round(gripReduction, 2)))
        
        vel = baseChangeOrt(tangDirection, perpDirection, self.v)
        vel[0] = -vel[0]*tangentFriction*delta
        vel[1] = -vel[1]*perpFriction*delta*gripReduction

        friction = baseReturnOrt(tangDirection, perpDirection, vel)

        self.v[0] = self.v[0] + friction[0]
        self.v[1] = self.v[1] + friction[1]
        

    def aplyAcceleration(self, sign):
        """
        Modifies the velocity of the car based on its acceleration.

        Args:
            sign (sign): Determines if it is puching forward or backwards.

        """

        delta = self.TCanvas.delta
        
        self.v[0] = self.v[0] + sign*delta*self.a*np.cos(self.angle)
        self.v[1] = self.v[1] + sign*delta*self.a*np.sin(self.angle)
        
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
        
        if self.TCanvas.keyStates["w"]:
            self.aplyAcceleration(1)
        if self.TCanvas.keyStates["s"]:
            self.aplyAcceleration(-1)
        if self.TCanvas.keyStates["a"]:
            self.rotateCar(1)
        if self.TCanvas.keyStates["d"]:
            self.rotateCar(-1)



if __name__=="__main__":
    size = 200

    tk = Tk()
    Topos = topologicalCanvas(tk, hOrientation=-1, vOrientation=-1, dimX= size, dimY= size, visualHelp= True)


    topologicalThickCurve(Topos, [np.array([100, 0]), np.array([100, 50]), np.array([100, 100]), np.array([100, 150]), np.array([100, 200])], [10, 20, 30, 40, 50], "black")
    

    topologicalPolygon(Topos,[[30,30],[50, 30], [50,50]])
    topologicalPolygon(Topos,[[0,0],[10, 0], [10,10], [0, 10]])
    print("Car1")
    car = topologicalCar(Topos, x0=20, y0=20, height=20, width=10, acc=50, v0x=0, v0y=0)


    cont = True
    
    while(True):
        car.TCanvas.updateDelta()
        
        car.updateCar()
        Topos.canvas.update()
        if cont:
            windowMonitor(tk, car.vars)
            cont = False