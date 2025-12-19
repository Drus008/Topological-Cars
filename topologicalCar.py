from topologicalCanvas import topologicalCanvas, topologicalObject
from tkinter import Tk
import time

class topologicalCar():
    """
    A car that moves within a topological canvas

    Atributes:
        vx (float): The speed of the car at the x axis.
        vy (float): The speed of the car at the y axis. (TODO maybe is better to use a np.array)
        body (topologicalObject): a poligon that draws the topological body of the car.
        width (float): the width of the car.
        height (float): the height of the car.

    Returns:
        None.
    """

    def __init__(self, canvas: topologicalCanvas, x0:float, y0:float, height:float, width:float, v0x = 0, v0y=0):
        
        
        self.body = topologicalObject.polygon(canvas, [[x0-width/2,y0-height/2], [x0+width/2,y0-height/2], [x0+width/2,y0+height/2], [x0-width/2,y0+height/2]], tags=["topologicalCar"])
        self.vx = v0x
        self.vy = v0y

        self.width = width
        self.height = height
    
        
    """
    Updates the topological position of the car based on his speed and its speed.

    Args:
        delta (float): the time elapsed bewteen the last frame.
    """
    def updatePosition(self, delta: float):
        dx =self.vx*delta
        dy = self.vy*delta
        self.body.TMove(dx,dy)
        



        
        
    
if __name__=="__main__":
    size = 100

    tk = Tk()
    Topos = topologicalCanvas(tk, hOrientation=1, vOrientation=-1, dimX= size, dimY= size, visualHelp= True)



    topologicalObject.line(Topos, [20,20],[50, 20])
    topologicalObject.polygon(Topos,[[30,30],[50, 30], [50,50]])
    topologicalObject.polygon(Topos,[[0,0],[10, 0], [10,10], [0, 10]])
    print("Car1")
    car = topologicalCar(Topos, 20, 20, 20, 10, 10,-30)
    prevTime = time.perf_counter()
    
    while(True):
        delta = time.perf_counter() - prevTime
        prevTime = time.perf_counter()
        car.updatePosition(delta)
        Topos.canvas.update()