import numpy as np

from topologicalCanvas import topologicalCanvas
from Tmath import rotationMatrix, direction2D


class topologicalObject:
    """
    An object on the topological canvas.
    
    By topological object I refer to an object that is duplicated on every individual space with its respective orientation.
    
    Attributes:
        TCanvas (topologicalCanvas): The topological canvas where the point will be drawn.
        Tid (str): The id of the element on the topological canvas. It is a string with the format "Tid"+int.
        position (array): The position where the object is located.
        objects (List[List[int]]): A matrix where the i,j element is the id of the copy of the original object placed at the canvas i,j.
        zIndex: Used to manage some depth related aspects.
    """
    # OPTIMIZE Not drawing all the instances of an object would be a huge optimitzation.
    # Dividing objects in three categories will be the best:
    # Main objects: The objects that the camera follows. Only needs to draw 9 copies. (Ex: The player)
    # Static objects: Static objects that dont move. Only needs to draw 16 copies. (Ex: The roads)
    # Normal objects: Objects that has to be drawn all over the place. (Ex: The rival)
    def __init__(self, instances:list[list[int]], Tid, canvas: topologicalCanvas, x0=0, y0=0, zIndex = 0):
        """
        Creates an object on the topological space.

        Args:
            instances (list[list[int]]): The original id (tkinter) of the element drawn on each local canvas.
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
                if particularId:
                    self.TCanvas.canvas.move(particularId, dx, dy)
                dy = dy * self.TCanvas.hOrientation
            
            dx = dx*self.TCanvas.vOrientation
        

    def checkBounds(self)->None:
        """
        Check if the object is out of its global position and moves it back to its corresponding global space if needed.
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
        Moves all the copies of the object and teleports it to its global canvas if it moves out of it.

        Args:
            dx (float): the displacement on the x direction.
            dy (float): the displacement on the y direction.
        """
        self.move(dx, dy)
        self.checkBounds()

        
    def hide(self)->None:
        """Makes the object invisible"""
        for r in range(6):
            for c in range(6):
                self.TCanvas.canvas.itemconfig(self.objects[r][c], state = "hidden")
    
    def unhide(self)->None:
        """Makes the object visible"""
        for r in range(6):
            for c in range(6):
                self.TCanvas.canvas.itemconfig(self.objects[r][c], state = "normal")

    def Traise(self)->None:
        """Moves an object to the front"""
        for r in range(6):
            for c in range(6):
                self.TCanvas.canvas.tag_raise(self.objects[r][c])

    def computeDistanceToPoint(self, point:np.array)->float:
        """Compues the distance between a global point and the object"""
        points = self.TCanvas.topologicalPoint(*self.TCanvas.reflectedPoint(point))
        objectCoodinates = self.position + 2*np.array([self.TCanvas.dimX, self.TCanvas.dimY])
        distances = []
        for r in range(6):
            for c in range(6):
                distances.append(np.linalg.norm(points[r][c]-objectCoodinates))
        return min(distances)
        


class topologicalLine(topologicalObject):
    """
    Represents a line on a topological canvas.
    """
    def __init__(self, TCanvas:topologicalCanvas, pInitial: np.array, pFinal: np.array, color:str="black", tags: list[str] = [], zIndex = 0)-> int:
        """
        Creates a line on the topological space.

        Args:
            TCanvas (topologicalCanvas): The topological canvas where the line will live.
            pInitial (np.array): The initial point of the line on the original space.
            pFinal (np.array): The final point of the line on the original space.
            color (str): The color of the line.
            tags (list[str]): Tags assigned to the object of the canvas.

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
                idRow.append(TCanvas.canvas.create_line(initialPoints[r][c][0], initialPoints[r][c][1], finalPoints[r][c][0], finalPoints[r][c][1], fill=color, tags=tags))
            idMatrix.append(idRow)
        position = (initialPoints[0][0]+finalPoints[0][0])/2
        super().__init__(idMatrix,tags[-1], TCanvas, position[0], position[1], zIndex=zIndex)

class topologicalCurve():
    """
    Represents a curve on a topological canvas.
    """
    def __init__(self, TCanvas:topologicalCanvas, points: list[np.array], color:str = "black", tags: list[str] = [], zIndex = 0):
        """
        Creates a curve on the topological space.

        Args:
            TCanvas (topologicalCanvas): The topological canvas where the line will live.
            points (list[array]): List of points of the curve.
            color (str): The color of the line.
            tags (list[str]): Tags assigned to the object of the canvas.
        """
        tags.append("Tid"+str(TCanvas.nElements))
        TCanvas.nElements = TCanvas.nElements+1

        self.segments = []
        for p in range(len(points)-1):
            self.segments.append(topologicalLine(TCanvas, points[p], points[p+1], color, zIndex=zIndex))


class topologicalPolygon(topologicalObject):
    """
    Represents a polygon on a topological canvas.

    Attributes:
        color (str): The color of the interior of the polygon.
        localVertices (list[array]): A list of the local coordinates of the vertices of the polygon.

    """
    def __init__(self, TCanvas:topologicalCanvas, pointList: list[np.array], fill:str="black", tags = [], zIndex = 0)-> int:
        """
        Creates a polygon on the topological space.

        Args:
            TCanvas (topologicalCanvas): The topological canvas where the line will live.
            pointList (list[np.array]): A list of 2D arrays that represents the coordinates of edges of the polygon
            fill (str): The interior color of the polygon. It supports all the colors from tkinter.
            tags (list[str]): Tags assigned to the object of the canvas.
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
                    if self.objects[r][c]:
                        rotatedCopies[r][c].append(tPoint[r][c][0])
                        rotatedCopies[r][c].append(tPoint[r][c][1])
        for r in range(6):
            for c in range(6):
                if self.objects[r][c]:
                    objId = self.objects[r][c]
                    self.TCanvas.canvas.coords(objId, *rotatedCopies[r][c])

    @classmethod
    def rectangle(cls, TCanvas:topologicalCanvas, center: np.array, hight: float, width:float, angle: float, fill:str="black", tags=[], zIndex=0):
        """
        Creates a rectangle.

        Args:
            TCanvas (topologicalCanvas): The topological canvas where the rectangle will be drawn.
            center (array): The center of the rectangle.
            hight (float): The height of the rectangle.
            width (float): The width of the rectangle.
            angle (float): The angle that the rectangle will be facing.
            fill (str): The interior color of the polygon. It supports all the colors from tkinter.
            tags (list[str]): Tags assigned to the object of the canvas.
            zIndex (float): Its zIndex.
        """
        vector1 = direction2D(angle)
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
            center (array): The center of the rectangle.
            size (float): The size of each side of the square.
            angle (float): The angle that the rectangle will be facing.
            fill (str): The interior color of the polygon. It supports all the colors from tkinter.
            tags (list[str]): Tags assigned to the object of the canvas.
            zIndex (float): Its zIndex.
        """
        return cls.rectangle(TCanvas, center, size, size, angle, fill, tags, zIndex)

    def checkIfPointInside(self, point:np.array)->bool:
        """Given a point, it checks if the point is inside the local polygon.
        
        Args:
            point (np.array): The local coordinates of the point.
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
        """(Unused function)Creates a list of points that forms the boundary of the polygon."""
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
    Attributes:
        center (list[array]): A list of local points of the center line.
        amplitudes (list[float]): A list of the amplitude of the curve with respect to the corresponding center point.
        offset1 (list[array]): A list of one of the offsets of the curve.
        offset2 (list[array]): A list of the other of the offsets of the curve.
    """
    def __init__(self, TCanvas:topologicalCanvas, points:list[np.array], amplitude: list[float], fill: str="black", zIndex = 0, tags: list[str] = []):
        """
        It generates the thick line.
        
        Args:
            TCanvas (topologicalCanvas): The topological canvas where the thick curve will be drawn.
            points (list[array]): The list of points conforming the original curve.
            amplitude: list[float]: The amplitude of the curve at each point.
            fill (str): The interior color of the curve. It supports all the colors from tkinter.
            tags (list[str]): Tags assigned to the object of the canvas.
            zIndex (float): Its zIndex.
        """
        self.nPoints = len(points)
        
        if len(amplitude)==1:
            self.amplitudes = []
            for _ in range(self.nPoints):
                self.amplitudes.append(amplitude[0])
        else:
            self.amplitudes = amplitude

        self.center = points
        self.TCanvas = TCanvas
        self.color = fill
        
        offsets = self._createOffset()
        self.offset1 = offsets[0]
        self.offset2 = offsets[1]

        vertices = self.offset1 + self.offset2[::-1]
        
        super().__init__(TCanvas, vertices, fill,tags, zIndex=zIndex)
    

    def _createOffset(self)->None:
        """Given a curve (list of points), creates an offset to each side."""
        curve = self.center
        amplitudes = self.amplitudes
        offset1 = []
        offset2 = []
        for i in range(len(curve)-1):
            tangent = curve[i+1]-curve[i]
            orto = np.array([-tangent[1], tangent[0]])
            orto = 0.5*amplitudes[i]*orto/np.linalg.norm(orto)
            offset1.append(curve[i]+orto)
            offset2.append(curve[i]-orto)
        return [offset1,offset2]
    
    def getStart(self)->np.array:
        """Returns the start of the curve, precisely it returns the first point of each offset"""
        return np.array([self.offset1[0], self.offset2[0]])


# Useless class.
class objectsManager():
    def __init__(self, TCanvas: topologicalCanvas, objects: list[topologicalObject]):

        for obj in objects:
            if TCanvas!=obj.TCanvas:
                self.errorHandler("canvasIncompatibility")

        self.objects = objects.copy()
        self.TCanvas = TCanvas
    
    def addObject(self, obj: topologicalObject):
        if obj.TCanvas!=self.TCanvas:
            self.errorHandler("canvasIncompatibility")
        self.objects.append(obj)

    def addObjects(self, objects: list[topologicalObject])->None:
        for obj in objects:
            if obj.TCanvas!=self.TCanvas:
                self.errorHandler("canvasIncompatibility")
            self.objects.append(obj)
    

    def errorHandler(self, error:str)->None:
        if error=="canvasIncompatibility":
            raise ValueError("Error found when adding object due to canvas incompatibility")