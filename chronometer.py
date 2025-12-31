
from time import time
import numpy as np

from topologicalObjects import topologicalThickCurve, topologicalPolygon
from fielesManager import saveRecord, loadRecord
from topologicalCar import topologicalCar
from Tmath import direcrion2D
from constants import *

class finishLine():
    """A class that manages all the race-like features.
    Attributes:
        TCanvas (topologicalCanvas): The topological canvas where the finishLine will live.
        car (topologicalCar): The car that will be racing.
        size (float): The height of the finish line.
        TOTAL_LAPS (int): The total number of laps that have to be completed to finish the race.
        laps (int): The number of laps done by the car.
        active (bool): Represents if the finish line is active, i.e. if the car crosses the line it counts as a lap. This attribute is meant to prevent crossing the finish line and going backwards from counting as one lap.
        counting (bool): Represents if the timer is counting.
        startTime (float): The time when the race began (the car crossed the line for the first time).
        time (float): The time passed from the beginning of the race.
        newTrajectory (list[dict]): The record of the trajectory of the car once it starts the race.
        rival (rival): The replay of the loaded rival.
        hitbox (topologicalPolygon): The hitbox of the finish line.
     """

    def __init__(self, curve:topologicalThickCurve, car: topologicalCar, spaceName:str, mapName: str, space: str, playerName:str, rivalName:str=None, size = 20):
        """Creates the finish line.
        Args:
            curve (topologicalThickCurve): The curve where the finish line will be placed (at the start).
            car (topologicalCar): The car that will be recorded.
            size (float): The height of the finish line. 
        """

        self.TCanvas = curve.TCanvas
        self.car = car
        self.size = size
        self.curve = curve

        self.TOTAL_LAPS = 3
        self.laps = 0
        self.active = True
        self.counting = False
        self.startTime = None
        self.time = 0
        
        self.playerName = playerName
        self.mapName = mapName
        self.spaceName = spaceName

        self._createVisuals()

        self.placeCarBehindFinishLine()

        self.newTrajectory = []
        if rivalName:
            self.rival = rival.cloneCar(car, self, rivalName, space, mapName)
        else:
            self.rival = None

    def _createVisuals(self):
        """Creates the visual representation of the finish line."""
        squareSide = self.size/3
        nSquare = 0

        amplitude = self.curve.amplitudes[0]
        while(nSquare*squareSide<amplitude):
            nSquare = nSquare+1
            
        amplitude = nSquare*squareSide
        center = self.curve.center[0]
        direction = self.curve.center[1]-self.curve.center[0]
        angle = np.arctan2(direction[1], direction[0])
        self.angle = angle
        
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
    
    def placeCarBehindFinishLine(self, distance: int = 30):
        """Places de car just behind th finish line"""
        displacement = self.hitbox.position - self.car.body.position
        displacement = displacement - distance*direcrion2D(self.angle)
        self.car.body.move(*displacement)
        self.car.body.TRotation(self.angle-self.car.angle)
        self.car.angle = self.angle
        self.car.body.Traise()

    def checkLaps(self):
        """Checks if the car has completed a lap and keeps track of how many laps have been completed."""
        position = self.car.body.position
        if self.active:
            if self.hitbox.checkIfPointInside(position):
                if self.laps==0:
                    self.startTime = time()
                    print("STARTING RACE")
                    self.counting = True
                    if self.rival:
                        self.rival.start()
                elif self.laps==self.TOTAL_LAPS:
                    print("RACE FINISHED", self.time)
                    saveRecord(self.mapName, self.spaceName, self.playerName, self.newTrajectory) # TODO This has to be done later on, because here it lags
                    self.active=False
                    self.counting = False
                    if self.rival:
                        self.rival.stop()
                self.laps = self.laps + 1
                self.active = False
        else:
            distance = self.hitbox.computeDistanceToPoint(self.car.getPosition())
            if distance>self.TCanvas.dimX/3:
                self.active=True


    def updateRecord(self):
        """Updates the record of the playable car."""
        if self.counting:
            self.newTrajectory.append({"x":self.car.body.position[0],
                                "y":self.car.body.position[1],
                                "angle": self.car.angle,
                                "t":self.time})

    def update(self):
        """Updates all the necessary things."""
        if self.counting:
            self.time = time() - self.startTime
        if self.rival:
            self.rival.update()
        self.updateRecord()
        self.checkLaps()



class rival(topologicalPolygon):
    """Emulates a car following a given trajectory.
    Attributes:
        timer (finishLine): The finishLine that manages the records.
        trajectory (list[dict]): A list of times, positions and angles of the car.
        step (int): The index of the trajectory list that the clone is at right now.
    """

    @classmethod
    def cloneCar(cls, car:topologicalCar, timer:finishLine, rivalName:str, space:str, map:str):
        """Clones a given car and sets it up to race."""

        rival = super().rectangle(car.TCanvas, car.body.position, car.height, car.width, timer.angle, fill="red")
        rival.timer = timer

        rival.trajectory = []
        rival.angle = timer.angle
        rival.step = 0
        rival.hide()
        rival.record = loadRecord(space, map, rivalName)
        return rival
    
    def start(self):
        """Starts the run."""
        self.unhide()

    def stop(self):
        """Stops the run."""
        self.hide()

    def update(self):
        """Updates the clone's position and angle based on the time elapsed and the loaded trajectory."""
        if self.timer.counting:
            for t in range(self.step,len(self.record)):
                if self.record[t]["t"]>self.timer.time:
                    self.step = t
                    displacement = np.array([self.record[t]["x"]-self.position[0],self.record[t]["y"]-self.position[1]])
                    self.move(displacement[0], displacement[1])
                    dAngle = self.record[t]["angle"]-self.angle
                    self.TRotation(dAngle)
                    self.angle = self.record[t]["angle"]
                    
                    break
