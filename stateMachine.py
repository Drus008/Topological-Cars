from tkinter import Event

class keyStateMachine(dict):
    """
    A dict used as state machine designed to monitor wich keys are pressed
    
    Each keybord key has its dictionary key with a boolean asociated: true if the key is beeing presed and false otherwise.
    """
    def __init__(self):
        """
        It creates de state machine.
        """
        super().__init__({"w": False, "a":False, "s":False, "d":False})


    def keyPresed(self, key:Event):
        """
        Function to activate the key when its pressed
        
        Args:
            key (Event): The event of the pressed key.
        """
        key = key.keysym.lower()
        if key in self:
            self[key] = True
    
    def keyReleased(self, key:Event):
        """
        Function to activate the key when its released.
        
        Args:
            key (Event): The event of the released key.
        """
        key = key.keysym.lower()
        if key in self:
            self[key] = False