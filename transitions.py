from gameManager import configureGame
from tkinter import Tk



def beginGame(tk: Tk, config: dict):
    print(config)
    configureGame(tk, config["space"], config["map"], config["name"], config["rival"])