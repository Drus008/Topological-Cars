from tkinter import Canvas, Tk
from stateMachine import keyStateMachine
from Tmath import rotationMatrix
import numpy as np
import time

# If optimization is necessary, a modification that could help is to only draw to the external squares the mooving parts, and not the fix ones

class topologicalCanvas():
    """
    Canvas with the sides glued.

    Attributes:
        canvas (tkinter.Canvas): The canvas used to model de topological space.
        hOrientation (sign): The relation between the orientation of the left and bottom right.
        vOrientation (sign): The relation between the orientation of the top and bottom bottom.
        dimX (int): Witdh of the space.
        dimY (int): Height of the space.
        nElements (int): number of elements drawn on the original canvas.
        lastTime (time): The last time the canvas was updated.
        delta (float): The time elapsed between the las frame and the actual one.
        keyStates (keyStateMachine): A state machine to monitor wich keys are pressed.
    """
    
    def gluingFuncH(self, y: float)->float:
        """
        Returns the number with the gluing relation aplied.

        Args:
            y (float): The number to wich the function will be aplied.

        Returns:
           The number with the function aplied.
        """
        if self.hOrientation==1:
            return y
        if self.hOrientation==-1:
            return self.dimY-y
    
    def gluingFuncV(self, x: float)->float:
        """
        Returns the number with the gluing relation aplied.

        Args:
            y (float): The number to wich the function will be aplied.

        Returns:
           The number with the function aplied.
        """
        if self.vOrientation==1:
            return x
        if self.vOrientation==-1:
            return self.dimX-x

    def __init__(self, tk:Tk, hOrientation: int, vOrientation: int,  dimX=300, dimY=300, visualHelp = False):
        """
        Initializes a topological canvas.

        Args:
            tk: The tkinter parent.
            hOrientation (sign): The relation between the orientation of the left and right sides.
            vOrientation (sign): The relation between the orientation of the top and bottom sides.
            dimX (int): Witdh of the space.
            dimY (int): Height of the space.
            visualHelp (bool): If True it shows some visual help to make navegation easier.

        Returns:
            A topological canvas with the initialized values.
        """
        self.canvas: Canvas = Canvas(tk, width=dimX*6, height=dimY*6)
        self.visualHelp = visualHelp
        if visualHelp:
            for i in range(6):
                self.canvas.create_line(i*dimX, 0, i*dimX, dimY*6)
                self.canvas.create_line(0, i*dimY, 6*dimY, i*dimY)
        
        self.canvas.pack()
        self.vOrientation = vOrientation
        self.hOrientation = hOrientation
        self.dimX = dimX
        self.dimY = dimY
        self.nElements = 0

        self.lastTime = time.perf_counter()
        self.delta = 1

        self.keyStates = keyStateMachine()

        self.canvas.bind("<KeyPress>", self.keyStates.keyPresed)
        self.canvas.bind("<KeyRelease>", self.keyStates.keyReleased)

        self.canvas.config(takefocus=True)
        self.canvas.focus_set()
        
    def topologicalPoint(self, x: float, y: float)->np.array:
        """
        Given the coordinates of a point, returns the coordenates of each copy of the point in the topological canvas.
        
        Args:
            x (float): the x coordenate of the point.
            y (float): tht y coordenate of the point.

        Returns:
            A matrix where the element i,j are the cordinates of point on the i,j copy of the canvas.
        """
        pointsMatrix = np.zeros((6,6,2))
        """ TODO It would be better if loc was calculated twice and placed on the corresponding indexes insted of calculating them every time """
        for r in range(6):
            for c in range(6):
                if c%2==1:
                    yloc = self.gluingFuncH(y)
                else:
                    yloc = y
                if r%2==1:
                    xloc = self.gluingFuncV(x)
                else:
                    xloc = x

                pointsMatrix[r][c][0] = xloc + c*self.dimX
                pointsMatrix[r][c][1] = yloc + r*self.dimY
        
        return pointsMatrix
    
    def updateDelta(self):
        """
        It updates the time related variables.
        """
        newTime = time.perf_counter()
        self.delta = newTime - self.lastTime
        self.lastTime = newTime


class torus(topologicalCanvas):
    """
    A topological canvas that represents a Torus.
    """
    def __init__(self, tk, dimX=300, dimY=300, visualHelp=False):
        super().__init__(tk, 1, 1, dimX, dimY, visualHelp)

class projectivePlane(topologicalCanvas):
    """
    A topological canvas that represents the projectiva plane.
    """
    def __init__(self, tk, dimX=300, dimY=300, visualHelp=False):
        super().__init__(tk, -1, -1, dimX, dimY, visualHelp)

class KleinBottleH(topologicalCanvas):
    """
    A topological canvas that represents a Klein bottle (H).
    """
    def __init__(self, tk, dimX=300, dimY=300, visualHelp=False):
        super().__init__(tk, 1, -1, dimX, dimY, visualHelp)

class KleinBottleV(topologicalCanvas):
    """
    A topological canvas that represents a Klein bottle (V).
    """
    def __init__(self, tk, dimX=300, dimY=300, visualHelp=False):
        super().__init__(tk, -1, 1, dimX, dimY, visualHelp)

class topologicalObject:
    """
    An object on the topological canvas.
    
    By topological object I refear to an object that is duplicated on every individual space with its respective orientation.
    
    Attributes:
        TCanvas (topologicalCanvas): The topological canvas where the point will be drwan.
        Tid (str): The id of the element on the topological canvas. It is a string with the format "Tid"+int.
        position (array): The position where the object will be placed.
        objects (List[List[int]]): A matrix where the i,j element is the id of the copy of the original object placed at the canvas i,j.
    """
    def __init__(self, instances:list[list[int]], Tid, canvas: topologicalCanvas, x0=0, y0=0):
        """
        Creates a object on the topological space.

        Args:
            instances (list[list[int]]): The original id (tkinter) of the element drawed on each local canvas.
            Tid: The topological ID of the object.
            canvas (topologicalCanvas): The topological canvas where the object will live.
        """
        self.position = np.array([x0, y0])
        self.Tid = Tid
        self.TCanvas = canvas
        self.objects = instances.copy()
    

    def move(self, dx, dy)->None:
        """
        Moves all the copies of the object the amount specified.

        Args:
            dx (float): the displacement on the x direction.
            dy (float): the displacement on the y direction.
        """
        self.position = self.position + np.array([dx,dy])
        for r in range(6):
            for c in range(6):
                
                particularId = self.objects[r][c]
                self.TCanvas.canvas.move(particularId, dx, dy)
                dy = dy * self.TCanvas.hOrientation
            
            dx = dx*self.TCanvas.vOrientation
        

    def checkBounds(self)->None:
        """
        Chech if the object is out of its localCanvas TODO (define local canvas) anv moves it back to tis canvas if is otherwise.
        """
        x = self.position[0]
        if x<0:
            self.move(2*self.TCanvas.dimX, 0)
        elif x>2*self.TCanvas.dimX:
            self.move(-2*self.TCanvas.dimX, 0)

        y=self.position[1]
        if y<0:
            self.move(0, 2*self.TCanvas.dimY)
        elif y>2*self.TCanvas.dimY:
            self.move(0, -2*self.TCanvas.dimY)

    def TMove(self, dx:float, dy:float)->None:
        """
        Moves all the copies the object and teleports it to its local canvas if it moves out of it.

        Args:
            dx (float): the displacement on the x direction.
            dy (float): the displacement on the x direction.
        """
        self.move(dx, dy)
        self.checkBounds()
    
    def TRotation(self, rads: float)->None:
        """
        It rotates the object a certain angle.
        
        Args:
            rads (float): The angle of rotation.
        """
        rotation = rotationMatrix(rads)
        
        vertices = np.array(self.TCanvas.canvas.coords(self.objects[0][0])).reshape(-1, 2)
        print(vertices[0])
        rotatedVertices = (vertices -self.position)@rotation.T + self.position
        print(rotatedVertices[0])
        rotatedCopies = []
        for r in range(6):
            rList = []
            for c in range(6):
                rList.append([])
            rotatedCopies.append(rList)
        
        for point in rotatedVertices:
            tPoint = self.TCanvas.topologicalPoint(point[0], point[1])
            for r in range(6):
                for c in range(6):
                    rotatedCopies[r][c].append(tPoint[r][c][0])
                    rotatedCopies[r][c].append(tPoint[r][c][1])
        print(rotatedCopies[0][0][0],rotatedCopies[0][0][1])
        for r in range(6):
            for c in range(6):
                objId = self.objects[r][c]
                self.TCanvas.canvas.coords(objId, *rotatedCopies[r][c])


        


class topologicalLine(topologicalObject):
    """
    Represents a line on a topological canvas.
    """
    def __init__(self, TCanvas:topologicalCanvas, pInitial: np.array, pFinal: np.array, tags: list[str] = [])-> int:
        """
        Creates a line on the topological space.

        Args:
            TCanvas (topologicalCanvas): The topological canvas where the line will live.
            pInitial (np.array): The initial point of the line on the original space.
            pFinal (np.array): The final point of the line on the original space.
            tags (list[str]): Tags assigned to the objecto of the canvas.

        Returns:
            The topological ID of the line.
        """
        tags.append("Tid"+str(TCanvas.nElements))
        TCanvas.nElements = TCanvas.nElements+1

        initialPoints = TCanvas.topologicalPoint(pInitial[0],pInitial[1])
        finalPoints = TCanvas.topologicalPoint(pFinal[0],pFinal[1])

        idMatrix = []

        for r in range(6):
            idRow = []
            for c in range(6):
                idRow.append(TCanvas.canvas.create_line(initialPoints[r][c][0], initialPoints[r][c][1], finalPoints[r][c][0], finalPoints[r][c][1], tags=tags))
            idMatrix.append(idRow)
        position = (initialPoints[0][0]+finalPoints[0][0])/2
        super().__init__(idMatrix,tags[-1], TCanvas, position[0], position[1])


class topologicalPolygon(topologicalObject):
    """
    Represents a polygon on a topological canvas.
    """
    def __init__(self, TCanvas:topologicalCanvas, pointList: list[np.array], tags = [])-> int:
        """
        Creates a polygon on the topological space.

        Args:
            TCanvas (topologicalCanvas): The topological canvas where the line will live.
            pointList (list[np.array]): A list of 2D arrays that represents the coodinates of edges of the polygon
            tags (list[str]): Tags assigned to the objecto of the canvas.

        Returns:
            The topological ID of the polygon.
        """
        tags.append("Tid"+str(TCanvas.nElements))
        TCanvas.nElements = TCanvas.nElements+1

        vertices = []
        for point in pointList:
            vertices.append(TCanvas.topologicalPoint(point[0], point[1]))

        idMatrix = []

        for r in range(6):
            idRow = []
            for c in range(6):
                flattenedList = []
                for matrix in vertices:
                    flattenedList = flattenedList + [matrix[r][c][0],matrix[r][c][1]]
                color = "black"
                if TCanvas.visualHelp and c==2 and r==2:
                    color="red"
                idRow.append(TCanvas.canvas.create_polygon(flattenedList, tags=tags, fill=color))
            idMatrix.append(idRow)
        position = vertices[0][0][0]
        for i in range(1,len(vertices)):
            position = position + vertices[i][0][0]
        position = position/len(vertices)
        super().__init__(idMatrix,tags[-1], TCanvas, position[0], position[1])

if __name__=="__main__":

    size = 100


    tk = Tk()
    Topos = topologicalCanvas(tk, hOrientation=1, vOrientation=-1, dimX= size, dimY= size, visualHelp= True)



    topologicalLine(Topos,[20,20],[50, 20])
    topologicalPolygon(Topos,[[30,30],[50, 30], [50,50]])

    tk.mainloop()
