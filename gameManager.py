from topologicalTerrain import *
from topologicalCar import topologicalCar
from topologicalCanvas import torus, KleinBottleV, projectivePlane
from tkinter import Tk
from chronometer import finishLine



def topologicalPseudoCircle(TCanvas:topologicalCanvas):
    x = TCanvas.dimX
    y = TCanvas.dimY
    thickness = 50
    radius = 1/2
    precision = 100

    halfCircle1 = [radius*np.array([x*np.sin(np.pi*alfa/((precision)*2-4)),y*np.cos(np.pi*alfa/((precision)*2-4))]) for alfa in range(precision)]
    halfCircle2 = [np.array([x,y])-point for point in halfCircle1]
    road1 = topologicalThickCurve(TCanvas, halfCircle1, [thickness])
    road2 =topologicalThickCurve(TCanvas, halfCircle2, [thickness])

    terrain = terrainManager(TCanvas)
    terrain.addTerrain(road1, 10, 10)
    terrain.addTerrain(road2, 10, 10)
    return terrain

def selectMap(TCanvas: topologicalCanvas, map:str)->terrainManager:
    if map=="Pseudo-Circle":
        return topologicalPseudoCircle(TCanvas)


def configureGame(interface:Tk, space: str, map:str):
    SIZE = 300

    if space=="torus":
        Topos = torus(interface, dimX= SIZE, dimY= SIZE, windowH=SIZE, windowW=SIZE, visualHelp= False)
    elif space=="klein":
        Topos = KleinBottleV(interface, dimX= SIZE, dimY= SIZE, windowH=SIZE, windowW=SIZE, visualHelp= False)
    elif space=="projective":
        Topos = projectivePlane(interface, dimX= SIZE, dimY= SIZE, windowH=SIZE, windowW=SIZE, visualHelp= False)
    
    terrain = selectMap(Topos, map)
    
    car = topologicalCar(Topos, x0=20, y0=20, height=20, width=10, ground=terrain, acc=8, v0x=0, v0y=0)

    finishLine(terrain.terrains[0])

    while(True):
        car.TCanvas.updateDelta()
        car.updateCar()
        Topos.canvas.update()
        