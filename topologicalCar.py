from topologicalCanvas import topologicalCanvas, topologicalObject, topologicalPolygon
from numpy import pi
import numpy as np
from tkinter import Tk
from Tmath import direcrion2D, baseChange, baseChangeOrt, baseReturnOrt

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

    def __init__(self, TCanvas: topologicalCanvas, x0:float, y0:float, height:float, width:float, acc=1, v0x = 0, v0y=0,rotationSpeed = 0.05):
        
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
        
    
    def updateCar(self):
        """
        Manages the updates of the car on each frame. (It has to be called).
        """
        self.aplyFriction()
        self.keyboardManagment()
        self.updatePosition()
        self.updateCamara()
    
    def updateCamara(self):
        print(self.body.position, end=" ")
        self.TCanvas.setCamaraPosition(self.body.position[0], self.body.position[1])

    def updatePosition(self):
        """
        Updates the topological position of the car based on his speed and its speed.
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
        perpFriction = 2
        tangDirection = direcrion2D(self.angle)
        perpDirection = np.array((tangDirection[1], -tangDirection[0]))

        delta = self.TCanvas.delta

        vel = baseChangeOrt(tangDirection, perpDirection, self.v)
        vel[0] = -vel[0]*tangentFriction*delta
        vel[1] = -vel[1]*perpFriction*delta

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
        angle = 5*orientation*delta*self.angVel*np.log(np.linalg.norm(self.v)+1)
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



    topologicalPolygon(Topos,[[30,30],[50, 30], [50,50]])
    topologicalPolygon(Topos,[[0,0],[10, 0], [10,10], [0, 10]])
    print("Car1")
    car = topologicalCar(Topos, x0=20, y0=20, height=20, width=10, acc=50, v0x=0, v0y=0)

    
    while(True):
        car.TCanvas.updateDelta()
        
        car.updateCar()
        Topos.canvas.update()
