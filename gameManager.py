from topologicalTerrain import *
from topologicalCar import topologicalCar
from topologicalCanvas import torus, KleinBottleV, projectivePlane, topologicalCanvas
from tkinter import Tk
from chronometer import finishLine
from inGameInterface import layout


def selectMap(TCanvas: topologicalCanvas, map:str)->terrainManager:
    """Returns the desired map.
    
    Args:
        TCanvas (topologicalCanvas): The topological canvas.
        map (str): The map that will be returned.
    Returns:
        The selectedMap
    """
    if map=="Pseudo-Circle":
        return topologicalPseudoCircle(TCanvas)

def selectSpace(interface:Tk, space:str, SIZE:float, visualHelp:bool =False)->topologicalCanvas:
    """Returns a topological space.
    Args:
        interface (Tk): The base parent.
        space (str). The name of the space. Options: "torus", "klein", "projective".
        SIZE (float): The size of the space.
        visualHelp (bool): If true it draws visual clues to help the player navegate.
    """
    windowSize = SIZE*1
    if space=="torus":
        Topos = torus(interface, dimX= SIZE, dimY= SIZE, windowH=windowSize, windowW=windowSize, visualHelp= visualHelp)
    elif space=="klein":
        Topos = KleinBottleV(interface, dimX= SIZE, dimY= SIZE, windowH=windowSize, windowW=windowSize, visualHelp= visualHelp)
    elif space=="projective":
        Topos = projectivePlane(interface, dimX= SIZE, dimY= SIZE, windowH=windowSize, windowW=windowSize, visualHelp= visualHelp)
    return Topos

def configureGame(interface:Tk, space: str, map:str):
    """Starts a race on the desired map and space.
    Args:
        interface (Tk): The parent class.
        space (str): The name of the space. Options: "torus", "klein", "projective".
        map (str): The name of the map. Options: "Pseudo-Circle".
    """
    SIZE = 700
    LAYOUT_SIZE = 80

    interface.geometry(str(SIZE)+"x"+str(SIZE+LAYOUT_SIZE)+"+"+str((interface.winfo_screenwidth()-SIZE)//2)+"+0")

    Topos = selectSpace(interface, space, SIZE)
    terrain = selectMap(Topos, map)
    car = topologicalCar(Topos, x0=20, y0=20, height=20, width=10, ground=terrain, acc=8, v0x=0, v0y=0)

    timer = finishLine(terrain.terrains[0], car)
    l = layout(interface)
    while(True):
        l.speed.updateNumber(int(np.linalg.norm(car.v)))
        l.timer.showTime(int(timer.time))
        l.laps.updateNumber(timer.laps)
        car.TCanvas.updateDelta()
        car.updateCar()
        timer.update()
        Topos.canvas.update()
        