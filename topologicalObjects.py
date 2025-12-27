from topologicalCanvas import topologicalCanvas
import numpy as np
from Tmath import rotationMatrix, direcrion2D


class topologicalObject:
    """
    An object on the topological canvas.
    
    By topological object I refear to an object that is duplicated on every individual space with its respective orientation.
    
    Attributes:
        TCanvas (topologicalCanvas): The topological canvas where the point will be drwan.
        Tid (str): The id of the element on the topological canvas. It is a string with the format "Tid"+int.
        position (array): The position where the object will be placed.
        objects (List[List[int]]): A matrix where the i,j element is the id of the copy of the original object placed at the canvas i,j.
        zIndex: Used to manage som deepth related aspects.
    """
    def __init__(self, instances:list[list[int]], Tid, canvas: topologicalCanvas, x0=0, y0=0, zIndex = 0):
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
        self.zIndex = zIndex
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
        Chech if the object is out of its global position and moves it back to its corresponding global space if needed otherwise.
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
        Moves all the copies the object and teleports it to its global canvas if it moves out of it.

        Args:
            dx (float): the displacement on the x direction.
            dy (float): the displacement on the x direction.
        """
        self.move(dx, dy)
        self.checkBounds()

        
    def hide(self):
        """Makes the object invisible"""
        for r in range(6):
            for c in range(6):
                self.TCanvas.canvas.itemconfig(self.objects[r][c], state = "hidden")
    
    def unhide(self):
        """Makes the object visible"""
        for r in range(6):
            for c in range(6):
                self.TCanvas.canvas.itemconfig(self.objects[r][c], state = "normal")


        


class topologicalLine(topologicalObject):
    """
    Represents a line on a topological canvas.
    """
    def __init__(self, TCanvas:topologicalCanvas, pInitial: np.array, pFinal: np.array, tags: list[str] = [], zIndex = 0)-> int:
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
        super().__init__(idMatrix,tags[-1], TCanvas, position[0], position[1], zIndex=zIndex)


class topologicalPolygon(topologicalObject):
    """
    Represents a polygon on a topological canvas.

    Atributes:
        color (str): The color of the interior of the polygon.
        localVerices (list[array]): A list of the local coordinates of the vertices of the polygon.

    """
    def __init__(self, TCanvas:topologicalCanvas, pointList: list[np.array], fill:str="black", tags = [], zIndex = 0)-> int:
        """
        Creates a polygon on the topological space.

        Args:
            TCanvas (topologicalCanvas): The topological canvas where the line will live.
            pointList (list[np.array]): A list of 2D arrays that represents the coodinates of edges of the polygon
            fill (str): The interior color of the polygon. It suports all the collors from tkinter.
            tags (list[str]): Tags assigned to the objecto of the canvas.
            zIndex (float): Its zIndex.

        Returns:
            The topological ID of the polygon.
        """

        self.color = fill

        tags.append("Tid"+str(TCanvas.nElements))
        TCanvas.nElements = TCanvas.nElements+1

        self.localVertices = pointList.copy()

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
        
        super().__init__(idMatrix,tags[-1], TCanvas, position[0], position[1], zIndex=zIndex)

    def TRotation(self, rads: float)->None:
        """
        It rotates the object a certain angle (relative).
        
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

    @classmethod
    def rectangle(cls, TCanvas:topologicalCanvas, center: np.array, hight: float, width:float, angle: float, fill:str="black", tags=[], zIndex=0):
        """
        Creates a rectangle.

        Args:
            TCanvas (topologicalCanvas): The topological canvas where the rectangle will be drawn.
            Center (array): The center of the recangle.
            hight (float): The hight of the rectangle.
            width (float): The width of the rectangle.
            angle (float): The angle that the rectangle will be facing.
            fill (str): The interior color of the polygon. It suports all the collors from tkinter.
            tags (list[str]): Tags assigned to the objecto of the canvas.
            zIndex (float): Its zIndex.
        """
        vector1 = direcrion2D(angle)
        vector2 = np.array([vector1[1], -vector1[0]])
        vertex1 = center+(width*vector2 - hight*vector1)/2
        vertex2 = center+(width*vector2 + hight*vector1)/2
        vertex3 = center+(-width*vector2 + hight*vector1)/2
        vertex4 = center+(-width*vector2 - hight*vector1)/2

        return cls(TCanvas, [vertex1, vertex2, vertex3, vertex4], fill, tags, zIndex)
    
    @classmethod
    def square(cls, TCanvas:topologicalCanvas, center: np.array, size:float, angle: float, fill:str="black", tags=[], zIndex=0):
        """
        Creates a square.

        Args:
            TCanvas (topologicalCanvas): The topological canvas where the rectangle will be drawn.
            Center (array): The center of the recangle.
            size (float): The size of each side of the square.
            angle (float): The angle that the rectangle will be facing.
            fill (str): The interior color of the polygon. It suports all the collors from tkinter.
            tags (list[str]): Tags assigned to the objecto of the canvas.
            zIndex (float): Its zIndex.
        """
        return cls.rectangle(TCanvas, center, size, size, angle, fill, tags, zIndex)

    def checkIfPointInside(self, point:np.array)->bool:
        """Given a point, it checks if the point is inside the local polygon.
        
        Args:
            (array): The local coordinates of the point.
        Returns:
            True if the point is inside the local polygon and false otherwise.
        """

        localPoint = self.TCanvas.reflectedPoint(point)
        cutsCounter = 0
        for i in range(len(self.localVertices)):
            prevPoint = self.localVertices[i-1]
            nextPoint = self.localVertices[i]
            if prevPoint[1]>localPoint[1] or nextPoint[1]>localPoint[1]:
                if (prevPoint[0]-localPoint[0])*(nextPoint[0]-localPoint[0])<0:
                    cutsCounter = cutsCounter +1
        if cutsCounter%2==1:
            return True

        return False


    # Useless function right now
    def createLocalBoundry(self, vertices: list[np.array]):
        """(Unused function)Creates a list of points that forms the boundry of the polygon."""
        PRECISION = 1
        
        numbPoints = len(vertices)
        allPointNear = False
        points = vertices.copy()
        
        iterations = 0
        #This code could be faster by avoiding to check the already checked segments
        while not allPointNear:
            iterations = iterations+1
            if iterations%100==0:
                print(iterations, end=", ")
            newPoints = []
            allPointNear=True

            numbPoints = len(points)
            for nPoint in range(numbPoints):
                actualPoint = points[nPoint]
                prevPoint = points[nPoint-1]
                vector = prevPoint-actualPoint
                prevDist = np.linalg.norm(vector)
                newPoints.append(prevPoint)
                if prevDist>PRECISION:
                    newPoint = actualPoint+vector/2
                    newPoints.append(newPoint)
                    allPointNear=False
            points = newPoints
        self.localBoundry = points




class topologicalThickCurve(topologicalPolygon):
    """It represents a thick curve on the topological canvas.
    Atributes:
        center (list[array]): A list of local points of the center line.
        amplitudes (list[float]): A list of the amplitude of the curve with respect to the correspoinding center point.
        offset1 (list[array]): A list of one of the offsets of the curve.
        offset2 (list[array]): A list of the other of the offsets of the curve.
    """
    def __init__(self, TCanvas:topologicalCanvas, points:list[np.array], amplitude: list[float], fill: str="black", zIndex = 0, tags: list[str] = []):
        """
        It generates the thick line.
        
        Args:
            TCanvas (topologicalCanvas): The topological canvas where the thick curve will be drown.
            points (list[array]): The list of points conforming the original curve.
            amplitude: list[float]: The amplitud of the curve at each point.
            fill (str): The interior color of the curve. It suports all the collors from tkinter.
            tags (list[str]): Tags assigned to the objecto of the canvas.
            zIndex (float): Its zIndex.
            
        """
        self.nPoints = len(points)
        
        if len(amplitude)==1:
            print("YES")
            self.amplitudes = []
            for _ in range(self.nPoints):
                self.amplitudes.append(amplitude[0])
        else:
            self.amplitudes = amplitude

        self.center = points
        self.TCanvas = TCanvas
        self.color = fill
        
        ofsets = self._createOffset()
        self.ofset1 = ofsets[0]
        self.ofset2 = ofsets[1]

        vertices = self.ofset1 + self.ofset2[::-1]
        
        super().__init__(TCanvas, vertices, fill,tags, zIndex=zIndex)
    

    def _createOffset(self):
        """Given a curve (list of point), creates an offset to each side."""
        curve = self.center
        amplitudes = self.amplitudes
        ofset1 = []
        ofset2 = []
        for i in range(len(curve)-1):
            tangent = curve[i+1]-curve[i]
            orto = np.array([-tangent[1], tangent[0]])
            orto = 0.5*amplitudes[i]*orto/np.linalg.norm(orto)
            ofset1.append(curve[i]+orto)
            ofset2.append(curve[i]-orto)
        return [ofset1,ofset2]
    
    def getStart(self)->np.array:
        """Returns the start of the curve, precisely it returns the first point of each ofset"""
        return np.array([self.ofset1[0], self.ofset2[0]])


# Usless class.
class objectsManager():
    def __init__(self, TCanvas: topologicalCanvas, objects: list[topologicalObject]):

        for obj in objects:
            if TCanvas!=obj.TCanvas:
                self.errorHandeler("canvasIncompatibility")

        self.objects = objects.copy()
        self.TCanvas = TCanvas
    
    def addObject(self, obj: topologicalObject):
        if obj.TCanvas!=self.TCanvas:
            self.errorHandeler("canvasIncompatibility")
        self.objects.append(obj)

    def addObjects(self, objects: list[topologicalObject]):
        for obj in objects:
            if obj.TCanvas!=self.TCanvas:
                self.errorHandeler("canvasIncompatibility")
            self.objects.append(obj)
    

    def errorHandeler(self, error:str):
        if error=="canvasIncompatibility":
            raise ValueError("Error found when adding object due to canvas incomatibility")


