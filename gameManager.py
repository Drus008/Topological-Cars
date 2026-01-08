from tkinter import Tk

from topologicalCanvas import torus, KleinBottleH, projectivePlane, topologicalCanvas
from topologicalCar import topologicalCar
from chronometer import finishLine
from inGameInterface import layout
from topologicalTerrain import *




from constants import *

def selectMap(TCanvas: topologicalCanvas, map:str)->terrainManager:
    """Returns the desired map.
    
    Args:
        TCanvas (topologicalCanvas): The topological canvas.
        map (str): The map that will be returned.
    Returns:
        The selected map.
    """
    if map==MAP1_PRIVATE_NAME:
        return topologicalPseudoCircle(TCanvas)
    if map==MAP2_PRIVATE_NAME:
        return ZHomology(TCanvas)

def selectSpace(interface:Tk, space:str, SIZE:float, extraSIZE: float, visualHelp:bool =False)->topologicalCanvas:
    """Returns a topological space.
    Args:
        interface (Tk): The base parent.
        space (str): The name of the space. Options: "torus", "klein", "projective".
        SIZE (float): The size of the space.
        visualHelp (bool): If true it draws visual clues to help the player navigate.
    """
    windowSize = SIZE*1
    if space==TORUS_PRIVATE_NAME:
        Topos = torus(interface, dimX= SIZE, dimY= SIZE, windowH=windowSize-extraSIZE, windowW=windowSize, visualHelp= visualHelp)
    elif space==KLEIN_PRIVATE_NAME:
        Topos = KleinBottleH(interface, dimX= SIZE, dimY= SIZE, windowH=windowSize-extraSIZE, windowW=windowSize, visualHelp= visualHelp)
    elif space==RP2_PRIVATE_NAME:
        Topos = projectivePlane(interface, dimX= SIZE, dimY= SIZE, windowH=windowSize-extraSIZE, windowW=windowSize, visualHelp= visualHelp)
    return Topos


def configureGame(interface:Tk, space: str, mapName:str, playerName:str, rival:str):
    """Starts a race on the desired map and space.
    Args:
        interface (Tk): The parent class.
        space (str): The name of the space. Options: "torus", "klein", "projective".
        mapName (str): The name of the map. Options: "pseudo-circle".
        playerName (str): The name of the player.
        rival (str): The name of the rival.
    """

    
    SIZE = 750
    LAYOUT_SIZE = 80

    Topos = selectSpace(interface, space, SIZE, LAYOUT_SIZE)
    #d = topologicalDecorationFamily(Topos, 50) #Too slow to work
    #d.startCalculations()
    terrain = selectMap(Topos, mapName)
    car = topologicalCar(Topos, x0=20, y0=20, height=20, width=10, ground=terrain, v0x=0, v0y=0)

    timer = finishLine(terrain.terrains[0], car, spaceName=space, mapName=mapName, space=space, playerName=playerName, rivalName=rival)
    interface.protocol("VM_DELETE_WINDOW", timer.saveRecord)
    l = layout(interface)

    while(not Topos.keyStates["escape"]):
        l.speed.updateNumber(int(np.linalg.norm(car.v)))
        l.timer.showTime(int(timer.time))
        l.laps.updateNumber(timer.laps)
        car.TCanvas.updateDelta()
        car.updateCar()
        timer.update()
        
        print(Topos.delta)

        Topos.canvas.update()
    timer.saveRecord()
    l.destroy()
    Topos.destroy()
    interface.protocol("VM_DELETE_WINDOW", interface.destroy)




if __name__=="__main__":
    tk = Tk()
    configureGame(tk, TORUS_PRIVATE_NAME, MAP1_PRIVATE_NAME, "DRS", None)