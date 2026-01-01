import numpy as np

from topologicalObjects import topologicalPolygon, topologicalThickCurve, topologicalCurve
from topologicalCanvas import topologicalCanvas
from constants import *


class topologicalRoad():
    def __init__(self, TCanvas: topologicalCanvas, pointsList: list[np.array], amplitude: float):
        self.TCanvas = TCanvas
        self.road = topologicalThickCurve(TCanvas, pointsList, [amplitude], fill=BGCOLOR_2)
        self.line1 = topologicalCurve(TCanvas, self.road.offset1, color=DETAILS_COLOR)
        self.line2 = topologicalCurve(TCanvas, self.road.offset2, color=DETAILS_COLOR)
        


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
        
    def detectTerrain(self, point:np.array)->str:
        """Given a point, it returns the TID of the terrain with highest zIndex that contains the point"""
        for terrain in self.terrains:
            if terrain.checkIfPointInside(point):
                return terrain.Tid
    
    def getFriction(self, point:np.array)->list[float]:
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
    precision = 25

    halfCircle1 = [radius*np.array([x*np.sin(np.pi*alfa/((precision)*2-4)),y*np.cos(np.pi*alfa/((precision)*2-4))]) for alfa in range(precision)]
    halfCircle2 = [np.array([x,y])-point for point in halfCircle1]
    road1 = topologicalRoad(TCanvas, halfCircle1, thickness)
    road2 = topologicalRoad(TCanvas, halfCircle2, thickness)


    terrain = terrainManager(TCanvas, 8, 8, 5)
    terrain.addTerrain(road1.road, 5, 10, 12)
    terrain.addTerrain(road2.road, 5, 10, 12)
    return terrain