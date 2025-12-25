from topologicalCanvas import *
from topologicalCar import *
from topologicalObjects import *

from monitor import windowMonitor
from time import sleep

size = 200

tk = Tk()
Topos = topologicalCanvas(tk, hOrientation=-1, vOrientation=-1, dimX= size, dimY= size, visualHelp= True)

terrain = terrainManager(Topos)

road = topologicalThickCurve(Topos, [np.array([100, 0]), np.array([100, 50]), np.array([100, 100]), np.array([100, 150]), np.array([100, 200])], [10, 20, 30, 40, 50], "black")

terrain.addTerrain(road,1, 1)

triangel = topologicalPolygon(Topos,[np.array([30,30]),np.array([50, 30]), np.array([50,50])])
terrain.addTerrain(triangel, 10, 1)
topologicalPolygon(Topos,[np.array([0,0]),np.array([10, 0]), np.array([10,10]), np.array([0, 10])])
print("Car1")
car = topologicalCar(Topos, x0=20, y0=20, height=20, width=10, ground=terrain, acc=8, v0x=0, v0y=0)


cont = True

while(True):
    car.TCanvas.updateDelta()
    car.updateCar()
    Topos.canvas.update()
    if cont:
        windowMonitor(tk, car.vars)
        cont = False
    sleep(0.01)