from topologicalCanvas import topologicalCanvas
from topologicalObjects import topologicalPolygon, topologicalThickCurve
from Tmath import direcrion2D
import numpy as np



class terrainManager:
    """A class to manage terrains."""
    def __init__(self, TCanvas: topologicalCanvas):
        """Initializes the terrain manager.
        Args:
            TCanvas (topologicalCanvas): The topological canvas where the terrains live.
        """
        self.TCanvas = TCanvas
        self.terrains: list[topologicalPolygon] = []
    
    def addTerrain(self, newTerrain: topologicalPolygon, friction: float, grip: float):
        """Adds a terrain to the terrain manager.
        
        Args:
            newTerrain (topologicalPolygon): The shape of the terrain.
            fiction (float): The friction of the terrain.
            grip (float): The grip of the terrain.
        """
        nTerrains = len(self.terrains)
        newTerrain.friction = friction
        newTerrain.grip = grip
        #IDK what would be the best way to add the parameter friction to this without creating a new class
        #(creating a new class would be problematic becouse newTerrain can be childs of topologicalPolygon)
        for iTerrain in range(nTerrains):
            if self.terrains[iTerrain].zIndex<newTerrain.zIndex:
                self.terrains.insert(iTerrain,newTerrain)
                return
        self.terrains.append(newTerrain)
        
    def detectTerrain(self, point:np.array)->str:
        """Given a point it returns the TID of the terrain with biggest zIndex that contains the point"""
        for terrain in self.terrains:
            if terrain.checkIfPointInside(point):
                return terrain.Tid
    
    def getFriction(self, point:np.array)->list[float]:
        """Given a point it returns the friction and grip of the terrain with biggest zIndex that contains the point.
        Args:
            point (array): The coordinates of the point.
        Returns:
            A list wit format [friction, grip].
        """
        for terrain in self.terrains:
            if terrain.checkIfPointInside(point):
                return terrain.friction, terrain.grip
        return 10, 10
