import numpy as np

from topologicalObjects import topologicalPolygon, topologicalThickCurve, topologicalCurve
from topologicalCanvas import topologicalCanvas
from constants import *


class topologicalRoad():
    def __init__(self, TCanvas: topologicalCanvas, pointsList: list[np.ndarray], amplitude: float, zIndex=0):
        self.TCanvas = TCanvas
        self.road = topologicalThickCurve(TCanvas, pointsList, [amplitude], fill=BGCOLOR_2, zIndex=zIndex)
        self.line1 = topologicalCurve(TCanvas, self.road.offset1, color=DETAILS_COLOR, zIndex=zIndex)
        self.line2 = topologicalCurve(TCanvas, self.road.offset2, color=DETAILS_COLOR, zIndex=zIndex)
        


class terrainManager:
    """A class to manage terrains."""
    def __init__(self, TCanvas: topologicalCanvas, backgroundFriction:float = 8, backgoundGrip: float = 10, backgroundTraction: float = 5):
        """Initializes the terrain manager.
        Args:
            TCanvas (topologicalCanvas): The topological canvas where the terrains live.
        """
        self.TCanvas = TCanvas
        self.terrains: list[topologicalPolygon] = []
        self.backgroundFriction = backgroundFriction
        self.backgoundGrip = backgoundGrip
        self.backgroundTraction = backgroundTraction
    
    def addTerrain(self, newTerrain: topologicalPolygon, friction: float, grip: float, traction: float):
        """Adds a terrain to the terrain manager.
        
        Args:
            newTerrain (topologicalPolygon): The shape of the terrain.
            friction (float): The friction of the terrain.
            grip (float): The grip of the terrain.
        """
        nTerrains = len(self.terrains)
        newTerrain.friction = friction
        newTerrain.grip = grip
        newTerrain.traction = traction
        #I don't know what would be the best way to add the parameter friction to this without creating a new class
        #(creating a new class would be problematic because newTerrain can be children of topologicalPolygon)
        for iTerrain in range(nTerrains):
            if self.terrains[iTerrain].zIndex<newTerrain.zIndex:
                self.terrains.insert(iTerrain,newTerrain)
                return
        self.terrains.append(newTerrain)
        
    def detectTerrain(self, point:np.ndarray)->str:
        """Given a point, it returns the TID of the terrain with highest zIndex that contains the point"""
        for terrain in self.terrains:
            if terrain.checkIfPointInside(point):
                return terrain.Tid
    
    def getFriction(self, point:np.ndarray)->list[float]:
        """Given a point, it returns the friction and grip of the terrain with highest zIndex that contains the point.
        Args:
            point (array): The coordinates of the point.
        Returns:
            A list with format [friction, grip].
        """
        for terrain in self.terrains:
            if terrain.checkIfPointInside(point):
                return terrain.friction, terrain.grip, terrain.traction
        return self.backgroundFriction, self.backgoundGrip, self.backgroundTraction


def topologicalPseudoCircle(TCanvas:topologicalCanvas)->terrainManager:
    """Returns the pseudocircle map"""
    x = TCanvas.dimX
    y = TCanvas.dimY
    thickness = 50
    radius = 1/2
    precision = 42

    halfCircle1 = [radius*np.array([x*np.sin(np.pi*alpha/((precision)*2-4)),y*np.cos(np.pi*alpha/((precision)*2-4))]) for alpha in range(precision)]
    halfCircle2 = [np.array([x,y])-point for point in halfCircle1]
    road1 = topologicalRoad(TCanvas, halfCircle1, thickness)
    road2 = topologicalRoad(TCanvas, halfCircle2, thickness)


    terrain = terrainManager(TCanvas, 8, 8, 5)
    terrain.addTerrain(road1.road, 5, 10, 12)
    terrain.addTerrain(road2.road, 5, 10, 12)
    return terrain

def ZHomology(TCanvas:topologicalCanvas) -> terrainManager:
    x = TCanvas.dimX
    y = TCanvas.dimY
    thickness = 50
    
    semiCirclePrecision = 20
    semiCircleRadius = x/6
    lin = np.linspace(0, 1, semiCirclePrecision)
    angles = lin*lin*(3-2*lin)
    s = 0.7
    angles = (lin*(1-s)+s*angles)*np.pi
    xCoords = semiCircleRadius*np.cos(angles)+x/2
    yCoords = -semiCircleRadius*np.sin(angles)+y
    semiCircle = np.column_stack((xCoords, yCoords))
    TsemiCircle = topologicalRoad(TCanvas, semiCircle, thickness)


    linePrecision = 10
    startPointLineL = np.array([x/3, y/2])
    endPointLineL = np.array([x/3, 0])
    lineL = np.linspace(startPointLineL, endPointLineL, linePrecision)
    TlineL = topologicalRoad(TCanvas, lineL, thickness)

    startPointLineR = np.array([2*x/3, y/2])
    endPointLineR = np.array([2*x/3, 0])
    lineR = np.linspace(startPointLineR, endPointLineR, 10)
    TlineR = topologicalRoad(TCanvas, lineR, thickness)

    sigmoidPrecision = 15
    sigmoid = lambda x: 1/(1+np.exp(-x))
    ySigmoid = np.linspace(y/2, y+1, sigmoidPrecision)
    xSigmoidR = sigmoid(np.linspace(-6, 6, sigmoidPrecision))*x/6+2*x/3
    sigmoidR = np.column_stack((xSigmoidR, ySigmoid))
    TSigmoidR = topologicalRoad(TCanvas, sigmoidR, thickness)

    xSigmoidL = x-xSigmoidR
    sigmoidL = np.column_stack((xSigmoidL, ySigmoid))
    TSigmoidL = topologicalRoad(TCanvas, sigmoidL, thickness)

    quarterCirclesPrecision = 17
    angles = -(1-(1-np.linspace(0, 1, quarterCirclesPrecision))**2)*np.pi/2
    xQuarterCircleL = np.cos(angles)*y/6
    xQuarterCircleR = x-xQuarterCircleL
    yQuarterCircleL = np.sin(angles)

    smallQuarterCircleRadius = y/3
    yQuarterCircleSmallL = -yQuarterCircleL*smallQuarterCircleRadius
    yQuarterCircleSmallR = yQuarterCircleSmallL

    quarterCircleSmallL = np.column_stack((xQuarterCircleL, yQuarterCircleSmallL))
    TquarterCircleSmallL = topologicalRoad(TCanvas, quarterCircleSmallL, thickness)
    quarterCircleSmallR = np.column_stack((xQuarterCircleR, yQuarterCircleSmallR))
    TquarterCircleSmallR = topologicalRoad(TCanvas, quarterCircleSmallR, thickness)

    bigQuarterCircleRadius = y-smallQuarterCircleRadius
    yQuarterCircleBigL = -yQuarterCircleL*bigQuarterCircleRadius
    yQuarterCircleBigR = yQuarterCircleBigL

    quarterCircleBigL = np.column_stack((xQuarterCircleL, yQuarterCircleBigL))
    TquarterCircleBigL = topologicalRoad(TCanvas, quarterCircleBigL, thickness)
    quarterCircleBigR = np.column_stack((xQuarterCircleR, yQuarterCircleBigR))
    TquarterCircleBigR = topologicalRoad(TCanvas, quarterCircleBigR, thickness)


    terrain = terrainManager(TCanvas, 60, 8, 5)
    terrain.addTerrain(TsemiCircle.road, 5, 10, 12)
    terrain.addTerrain(TlineL.road, 5, 10, 12)
    terrain.addTerrain(TlineR.road, 5, 10, 12)
    terrain.addTerrain(TSigmoidL.road, 5, 10, 12)
    terrain.addTerrain(TSigmoidR.road, 5, 10, 12)
    terrain.addTerrain(TquarterCircleBigL.road, 5, 10, 12)
    terrain.addTerrain(TquarterCircleBigR.road, 5, 10, 12)
    terrain.addTerrain(TquarterCircleSmallL.road, 5, 10, 12)
    terrain.addTerrain(TquarterCircleSmallR.road, 5, 10, 12)

    return terrain


if __name__=="__main__":
    from tkinter import Tk
    tk = Tk()
    TCanvas = topologicalCanvas(tk, 1, -1, dimX=750, dimY=750, visualHelp=True)
    ZHomology(TCanvas)
    

    tk.mainloop()


