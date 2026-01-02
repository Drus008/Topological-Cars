from numpy import pi
import numpy as np

from topologicalObjects import topologicalPolygon
from topologicalCanvas import topologicalCanvas
from topologicalTerrain import terrainManager
from Tmath import direction2D
from constants import *

class topologicalCar():
    """
    A car that moves within a topological canvas.

    Attributes:
        TCanvas (topologicalCanvas): The topological canvas where the car will be placed.
        body (topologicalPolygon): The rectangle that represents the car on the canvas.
        ground (terrainManager): The terrain on which the car will move.
        v (array): The velocity vector of the car.
        acc (float): The acceleration of the car.
        angle (float): The angle at which the car is looking.
        width (float): The width of the car.
        height (float): The height of the car.
        angVel (float): The speed at which the car turns.
    """

    def __init__(self, TCanvas: topologicalCanvas, ground:terrainManager, x0:float, y0:float, height:float, width:float, color=MAINCOLOR, acc=15, v0x = 0, v0y=0,rotationSpeed = 1):
        
        """
        Initializes the car given the basic parameters.

        Args:
            TCanvas (topologicalCanvas): The topological canvas where the car will be placed.
            ground (terrainManager): The terrain on which the car will move.
            x0 (float): The x coordinate where the car is placed.
            y0 (float): The y coordinate where the car is placed.
            height (float): The height of the car.
            width (float): The width of the car.
            color (str): The color of the car. It supports all the tkinter colors.
            acc (float): The acceleration of the car.
            v0x (float): The initial velocity on the x-axis.
            v0y (float): The initial velocity on the y-axis.
            rotationSpeed (float): The speed at which the car turns.
        Returns:
            A topological car.
        """

        self.TCanvas = TCanvas
        self.body = topologicalPolygon(TCanvas, [np.array([x0-width/2,y0-height/2]), np.array([x0+width/2,y0-height/2]), np.array([x0+width/2,y0+height/2]), np.array([x0-width/2,y0+height/2])], fill=color, tags=["topologicalCar"])
        self.ground = ground
        
        self.v = np.array([v0x, v0y], float)
        self.speed = 0
        self.a = acc
        self.angle = pi/2
        self.momentum = 0
        self.angVel = rotationSpeed

        self.width = width
        self.height = height
        
    
    def updateCar(self)->None:
        """
        Manages the car updates on each frame. (It has to be called).
        """
        self.calcAcc()
        self.keyboardManagment()
        self.updatePosition()
        self.centerCamera()
    
    def getPosition(self)->np.array:
        """Returns the position of the car."""
        return self.body.position
    
    def centerCamera(self)->None:
        """Centers the camera on the car."""
        self.TCanvas.setCamaraPosition(*self.getPosition())

    def updatePosition(self)->None:
        """
        Updates the car's global position based on its speed.
        """

        displacement =self.v*self.TCanvas.getDelta()
        self.body.TMove(*displacement)
    

    def calcAcc(self)->None:
        """Computes the acceleration of the car (based on terrain, friction, power...) and updates its speed and angle."""
        torque = 0
        dt = self.TCanvas.getDelta()
        if self.TCanvas.keyStates["s"]:
            torque = -0.1
        elif self.TCanvas.keyStates["w"]:
            self.momentum += dt
            torque = 1-np.exp(-self.momentum/5-0.2)
        else:
            if self.momentum>0:
                self.momentum -= dt*3
        
        
        AIR_FRICTION = 1
        GROUND_FRICTION, GRIP, TRACTION = self.ground.getFriction(self.body.position)

        tangDirection = direction2D(self.angle)
        perpDirection = np.array((tangDirection[1], -tangDirection[0]))
        acc = tangDirection*self.a*TRACTION*torque
        acc -=  self.v*AIR_FRICTION
        acc -=  (np.sign(np.dot(self.v,tangDirection)))*tangDirection*GROUND_FRICTION
        speedCoef = np.exp(-self.speed/250)
        acc -= speedCoef*GRIP*np.dot(self.v,perpDirection)*perpDirection
        
        self.v += acc*dt
        self.speed = np.linalg.norm(self.v)
        
    def rotateCar(self, sign)->None:
        """
        Rotates the car to the desired direction.

        Args:
            sign (sign): The direction of the rotation. Positive means clockwise and negative counterclockwise.
        """
        orientation = -sign

        if np.dot(self.v,direction2D(self.angle))<0:
            orientation = -orientation
        dt = self.TCanvas.getDelta()
                                                    #TODO the 0.1 is completely arbitrary
        turnCoef = (1-np.exp(-self.speed)**.1) #Don't allow the car to turn when its speed is low.
        angle = orientation*dt*self.angVel*turnCoef 
        self.angle += angle
        self.body.TRotation(angle)

    def keyboardManagment(self)->None:
        """
        Manages how the car interacts with the keyboard inputs.
        """
        if self.TCanvas.keyStates["a"]:
            self.rotateCar(1)
        if self.TCanvas.keyStates["d"]:
            self.rotateCar(-1)