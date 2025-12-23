import tkinter as tk

# Made by IA
class windowMonitor(tk.Toplevel):
    def __init__(self, parent, diccionario_variables):
        super().__init__(parent)
        self.title("Monitor")
        self.geometry("250x150")

        self.dict = diccionario_variables

        # Genera etiquetas automáticamente según las variables que le pases
        for nombre, variable in self.dict.items():
            frame = tk.Frame(self)
            frame.pack(pady=5, fill="x", padx=20)
            tk.Label(frame, text=f"{nombre}:", width=10, anchor="w").pack(side="left")
            tk.Label(frame, textvariable=variable, font=("Arial", 12, "bold")).pack(side="right")