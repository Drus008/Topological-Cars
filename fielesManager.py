from pathlib import Path
from PIL import Image
import json
import sys

from constants import *


USER_DIR = Path.home() / "TopologicalRacing" / "Maps"

def checkFolders():
    """Checks if all the folders are created and creates them if aren't created"""
    for map in MAPS:
        for space in SPACES:
            direction = Path(USER_DIR / map / space)
            direction.mkdir(parents=True, exist_ok=True)


def getRecords(space: str, map: str)-> dict:
    """Gets the records of the players.
    Args:
        space (str): the private name of the space.
        map (str): the private name of the map.
    Returns:
        A dictionari of the form {"time":t, "name":n} with the time on the format min:sec with only one digit to the mins.
    """
    direction = USER_DIR / map / space
    JSONFiles = list(direction.glob('*.json'))
    rivals = []
    for fileDir in JSONFiles:
        with open(fileDir, "r", encoding="utf-8") as file:
            record = json.load(file)
            secInMin = 60
            timeStr = str(round(record["finalTime"])//secInMin) + ":" + str(round(record["finalTime"])%secInMin)
            rivals.append({"time":timeStr, "name": record["player"]})
    
    orderedRivals = sorted(rivals, key=lambda x: x["time"])
    return orderedRivals

def saveRecord(map:str, space:str, playerName:str, trajectory:dict):
        """Saves the record as a file named recordplayer.json on the respective file (map/space/)"""
        direction = USER_DIR / map / space
        trajectoryFile = {"map": map, "space":space, "player": playerName, "trajectory":trajectory, "finalTime": trajectory[-1]["t"]}
        with open(direction /("record"+playerName + ".json"), "w") as f:
            json.dump(trajectoryFile, f, indent=2)


def loadRecord(space:str, map:str, playerName:str):
    """Loads a record of a previous race into the clone."""
    direction = USER_DIR / map / space / ("record" + playerName + ".json")
    with open(direction, 'r', encoding='utf-8') as f:
        record = json.load(f)
    return record["trajectory"]


def loadImage(iconName: str)->Image.Image:
    """Loads an image."""
    imgShorPath = Path("resources/images/" + iconName + ".png")
    imgPath = resourcePath(imgShorPath)
    return Image.open(imgPath)


def resourcePath(relativePath):
    """Returns the absolute path. (works compiled and interpreted)"""
    try:
        basePath = Path(sys._MEIPASS)
    except Exception:
        basePath = Path(__file__).parent

    return basePath/relativePath

