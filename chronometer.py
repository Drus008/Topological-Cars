from topologicalObjects import topologicalThickCurve, topologicalPolygon
from topologicalCar import topologicalCar
import numpy as np
from time import time
from tkinter import Label
import json


class finishLine():
    """A class that manages all the race-like features.
    Atributes:
        TCanvas (topologicalCanvas): The topological canvas where the finishLine will live.
        car (topologicalCar): The car that will be racing.
        size (float): The heigth of the finish line.
        interface (Label): The label where the time will be shown. #TODO this has to be done apart.
        TOTAL_LAPS (int): The total number of laps that has to be done to finish the race.
        laps (int): The number of laps done by the car.
        active (bool): Represents if the finish line is active, i.e. if the car crosses the line it counts as a laps. This atribute is ment to prevent that corossing the finish line and going backwards counts as one lap.
        counting (bool): Represents if the timer is counting,
        startTime (float): Is the time when the race began (the car corossed the line for the first time).
        time (float): The time past from the begin of the race.
        newTrajectory (list[dict]): The record of the trajectory of the car once it starts the race.
        self.rival (rival): The replay of the loaded rival.

     """

    def __init__(self, curve:topologicalThickCurve, car: topologicalCar, size = 20):
        """Crates the finish line.
        Args:
            curve (topologicalThickCurve): The curve where the finish line will be placed (at the start).
            car (topologicalCar): The car that will be recorded.
            size (float): The height of th finish line. 
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
        
        self.interface = Label(
            self.TCanvas.root, text="",
            font=("Helvetica", 40, "bold"),
            bg="black", fg="red" )
        self.interface.place(relx=0.5, rely=0.9, anchor="n")
        
        self._createVisuals()

        self.newTrajectory = []
        self.rival = rival.cloneCar(car, self)        


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
    
    def checkLaps(self):
        """Chcks if the has has complited a lap and keeps track of how many has completed."""
        position = self.car.body.position

        if self.active:
            if self.hitbox.checkIfPointInside(position):
                if self.laps==0:
                    self.startTime = time()
                    print("STARTING RACE")
                    self.counting = True
                    self.rival.start()
                elif self.laps==self.TOTAL_LAPS:
                    print("RACE FINISHED", self.time)
                    self.saveRecord("1", "1") # TODO This has to be done later on, cuz here it lags
                    self.active=False
                    self.counting = False
                    self.rival.stop()
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
        """Updates the values on the interface #TODO this has to be moved out"""
        if self.counting:
            self.interface.config(text=str(round(self.time,1)))

    def updateRecord(self):
        """Updates the record of the playable car."""
        if self.counting:
            self.newTrajectory.append({"x":self.car.body.position[0],
                                "y":self.car.body.position[1],
                                "angle": self.car.angle,
                                "t":self.time})

    def update(self):
        """Updates all the necesary thing"""
        if self.counting:
            self.time = time() - self.startTime
        self.rival.update()
        self.updateRecord()
        self.checkLaps()
        self.updateChronometer()

    def saveRecord(self, map:str, player:str):
        """Saves the record as a file named mapplayer.json"""
        trajectoryFile = {"map": map, "player": player, "trajectory":self.newTrajectory}
        with open(map+player+".json", "w") as f:
            json.dump(trajectoryFile, f, indent=2)


class rival(topologicalPolygon):
    """Emulates a car following a given trajectory.
    Atrubutes:
        timer (finishLine): The finishLine that manages the records.
        trajectory (list[dict]): A list of times, position and angle of the car.
        step (int): The index of the trajectory list that the clone is at right now.
    """

    @classmethod
    def cloneCar(cls, car:topologicalCar, timer:finishLine):
        """Clones a given car ang sets it up to race."""

        rival = super().rectangle(car.TCanvas, car.body.position, car.height, car.width, timer.angle, fill="red")
        rival.timer = timer

        rival.trajectory = []
        rival.angle = timer.angle
        rival.step = 0
        rival.hide()
        rival.loadRecord("11")
        return rival
    
    def start(self):
        """Starts the run."""
        self.unhide()

    def stop(self):
        """Stops the run."""
        self.hide()

    def loadRecord(self, name: str):
        """Loads a record of a previous race in to the clone."""
        with open(name+'.json', 'r', encoding='utf-8') as f:
            self.record = json.load(f)["trajectory"]

    def update(self):
        """Updates the clone's position and angle based on the time elapsed an the loaded trajectory."""
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
