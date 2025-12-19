from tkinter import Canvas, Tk
import numpy as np


# If optimization is necessary, a modification that could help is to only draw to the external squares the mooving parts

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
            canvas (tkinter.Canvas): The canvas used to model de topological space.
            hOrientation (sign): The relation between the orientation of the left and bottom right.
            vOrientation (sign): The relation between the orientation of the top and bottom bottom.
            dimX (int): Witdh of the space.
            dimY (int): Height of the space.
            nElements (int): number of elements drawn on the original canvas.

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
                if c%2==0:
                    yloc = self.gluingFuncH(y)
                else:
                    yloc = y
                if r%2==0:
                    xloc = self.gluingFuncV(x)
                else:
                    xloc = x

                pointsMatrix[r][c][0] = xloc + c*self.dimX
                pointsMatrix[r][c][1] = yloc + r*self.dimY
        
        return pointsMatrix




class topologicalObject:
    """
    An object on the topological canvas.

    Attributes:
        TCanvas (topologicalCanvas): The topological canvas where the point will be drwan.
        Tid (str): The id of the element on the topological canvas. It is a string with the format "Tid"+int.
        x (float): The x coordinate of the original point (placed on the top left corner).
        y (float): The y coordinate of the original point (placed on the top left corner).
        objects (List[List[int]]): A matrix where the i,j element of the coordinates of the copy of the object placed at the canvas i,j.
    """
    def __init__(self, instances:list[list[int]], Tid, canvas: topologicalCanvas, x0=0, y0=0):
        
        self.x = x0
        self.y = y0
        self.Tid = Tid
        self.TCanvas = canvas
        self.objects = instances.copy()
    

    @classmethod
    def line(cls, TCanvas:topologicalCanvas, pInitial: np.array, pFinal: np.array, tags = [])-> int:
        """
        Creates a line on the topological space.

        That means that the line is reapeted on each of the copies of the original space.

        Args:
            pInitial (np.array): The initial point of the line on the original space.
            pFinal (np.array): The final point of the line on the original space.

        Returns:
            The ID of the line in the topological canvas.
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
        return topologicalObject(idMatrix,tags[-1], TCanvas, position[0], position[1])

    @classmethod
    def polygon(cls, TCanvas:topologicalCanvas, pointList: list[np.array], tags = [])-> int:
        """
        Creates a polygon on the topological space.

        That means that the polygon is reapeted on each of the copies of the original space.

        Args:
            pInitial (np.array): The initial point of the line on the original space.
            pFinal (np.array): The final point of the line on the original space.

        Returns:
            The ID of the line in the topological canvas.
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
        print(position)
        return cls(idMatrix,tags[-1], TCanvas, position[0], position[1])

    def move(self, dx, dy):
        """
        Moves all the copies of the object the amount specified.

        Args:
            dx (float): the displacement on the x direction.
            dy (float): the displacement on the x direction.

        Returns:
            None.
        """
        self.x = self.x + dx
        self.y = self.y + dy
        for r in range(6):
            for c in range(6):
                
                particularId = self.objects[r][c]
                self.TCanvas.canvas.move(particularId, dx, dy)
                dy = dy * self.TCanvas.hOrientation
            
            dx = dx*self.TCanvas.vOrientation
        print(self.x,self.y)

    def checkBounds(self):
        """
        Chech if the object is out of its localCanvas TODO (define local canvas) anv moves it back to tis canvas if is otherwise.

        Args:
            dx (float): the displacement on the x direction.
            dy (float): the displacement on the x direction.
        """
        if self.x<0:
            self.move(2*self.TCanvas.dimX, 0)
        elif self.x>2*self.TCanvas.dimX:
            self.move(-2*self.TCanvas.dimX, 0)
        if self.y<0:
            self.move(0, 2*self.TCanvas.dimY)
        elif self.y>2*self.TCanvas.dimY:
            self.move(0, -2*self.TCanvas.dimY)

    def TMove(self, dx:float, dy:float)->None:
        """
        Moves all the copies the object and teleports it to its local canvas if it moves out of it.

        Args:
            dx (float): the displacement on the x direction.
            dy (float): the displacement on the x direction.

        Returns:
            None.
        """
        self.move(dx, dy)
        self.checkBounds()



if __name__=="__main__":

    size = 100


    tk = Tk()
    Topos = topologicalCanvas(tk, hOrientation=1, vOrientation=-1, dimX= size, dimY= size, visualHelp= True)



    topologicalObject.line(Topos,[20,20],[50, 20])
    topologicalObject.polygon(Topos,[[30,30],[50, 30], [50,50]])

    tk.mainloop()
