from tkinter import Event

class keyStateMachine(dict):
    """
    A dict used as state machine designed to monitor which keys are pressed.
    
    Each keyboard key has its dictionary key with a boolean associated: true if the key is being pressed and false otherwise.
    """
    def __init__(self):
        """
        It creates the state machine.
        """
        super().__init__({"w": False, "a":False, "s":False, "d":False})


    def keyPresed(self, key:Event):
        """
        Function to activate the key when it is pressed.
        
        Args:
            key (Event): The event of the pressed key.
        """
        key = key.keysym.lower()
        if key in self:
            self[key] = True
    
    def keyReleased(self, key:Event):
        """
        Function to deactivate the key when it is released.
        
        Args:
            key (Event): The event of the released key.
        """
        key = key.keysym.lower()
        if key in self:
            self[key] = False