from tkinter import Event

class keyStateMachine(dict):
    """
    A dictionary used as a state machine designed to monitor which keys are pressed.

    Each keyboard key has its dictionary key with a boolean associated: True if the key is being pressed and False otherwise.
    """
    def __init__(self):
        """
        Creates the state machine.
        """
        super().__init__({"w": False, "a":False, "s":False, "d":False, "escape": False})


    def keyPresed(self, key:Event):
        """
        Activates the key when it is pressed.

        Args:
            key (Event): The event of the pressed key.
        """
        key = key.keysym.lower()
        if key in self:
            self[key] = True
    
    def keyReleased(self, key:Event):
        """
        Deactivates the key when it is released.

        Args:
            key (Event): The event of the released key.
        """
        key = key.keysym.lower()
        if key in self:
            self[key] = False