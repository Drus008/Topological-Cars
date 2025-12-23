from topologicalCanvas import topologicalCanvas
import numpy as np
from tkinter import Tk
from Tmath import rotationMatrix


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
        
        rotatedVertices = (vertices -self.position)@rotation.T + self.position
        
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
    def __init__(self, TCanvas:topologicalCanvas, pointList: list[np.array], fill:str="black", tags = [])-> int:
        """
        Creates a polygon on the topological space.

        Args:
            TCanvas (topologicalCanvas): The topological canvas where the line will live.
            pointList (list[np.array]): A list of 2D arrays that represents the coodinates of edges of the polygon
            tags (list[str]): Tags assigned to the objecto of the canvas.

        Returns:
            The topological ID of the polygon.
        """

        self.color = fill

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
                color = fill
                if TCanvas.visualHelp and c==2 and r==2:
                    color="red"
                idRow.append(TCanvas.canvas.create_polygon(flattenedList, tags=tags, fill=color))
            idMatrix.append(idRow)
        position = vertices[0][0][0]
        for i in range(1,len(vertices)):
            position = position + vertices[i][0][0]
        position = position/len(vertices)
        super().__init__(idMatrix,tags[-1], TCanvas, position[0], position[1])

class topologicalThickCurve(topologicalPolygon):
    def __init__(self, TCanvas:topologicalCanvas, points:list[np.array], amplitude: list[float], fill: str="black", tags: list[str] = []):

        self.nPoints = len(points)

        if type(amplitude)==float:
            self.amplitude = []
            for _ in range(self.nPoints):
                self.amplitude.append(amplitude)
        else:
            self.aplitudes = amplitude

        self.center = points
        self.TCanvas = TCanvas
        self.color = fill
        
        ofsets = self.createOffset()
        self.ofset1 = ofsets[0]
        self.ofset2 = ofsets[1]

        self.interior = []
        vertices = self.ofset1 + self.ofset2[::-1]
        
        super().__init__(TCanvas, vertices, fill,tags)
    

    def createOffset(self): #TODO manage final point
        curve = self.center
        amplitudes = self.aplitudes
        ofset1 = []
        ofset2 = []
        for i in range(len(curve)-1):
            tangent = curve[i+1]-curve[i]
            orto = np.array([-tangent[1], tangent[0]])
            orto = 0.5*amplitudes[i]*orto/np.linalg.norm(orto)
            ofset1.append(curve[i]+orto)
            ofset2.append(curve[i]-orto)
        return [ofset1,ofset2]



if __name__=="__main__":

    size = 100

    tk = Tk()
    Topos = topologicalCanvas(tk, hOrientation=1, vOrientation=-1, dimX= size, dimY= size, visualHelp= True)

    topologicalLine(Topos,[20,20],[50, 20])
    topologicalPolygon(Topos,[[30,30],[50, 30], [50,50]])

    tk.mainloop()