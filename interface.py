import tkinter as tk
from tkinter import ttk
import time

#Made by AI just to have it.
# TODO It has to be ramade entierly

class InputView(ttk.Frame):
    """
    Esta clase maneja exclusivamente la interfaz de entrada de datos.
    Es un módulo independiente que se puede reutilizar o modificar sin romper el resto.
    """
    def __init__(self, parent, submit_callback):
        super().__init__(parent)
        self.submit_callback = submit_callback
        self.pack(fill='both', expand=True, padx=20, pady=20)
        
        self._create_widgets()

    def _create_widgets(self):
        # Configuración de grid para que se vea ordenado
        self.columnconfigure(1, weight=1)

        # Selector 1
        ttk.Label(self, text="Space:").grid(row=0, column=0, sticky='w', pady=5)
        self.combo_a = ttk.Combobox(self, values=["Torus", "Klein Bottle", "Projective Plane"], state="readonly")
        self.combo_a.current(0)
        self.combo_a.grid(row=0, column=1, sticky='ew', pady=5)

        # Selector 2
        ttk.Label(self, text="Map:").grid(row=1, column=0, sticky='w', pady=5)
        self.combo_b = ttk.Combobox(self, values=["Alfa", "Beta", "Gamma"], state="readonly")
        self.combo_b.current(0)
        self.combo_b.grid(row=1, column=1, sticky='ew', pady=5)

        ttk.Label(self, text="Oponent:").grid(row=2, column=0, sticky='w', pady=5)
        self.combo_b = ttk.Combobox(self, values=["Antonio", "Carlos", "Gemma"], state="readonly")
        self.combo_b.current(0)
        self.combo_b.grid(row=2, column=1, sticky='ew', pady=5)

        # Caja de Texto
        ttk.Label(self, text="Player name:").grid(row=3, column=0, sticky='w', pady=5)
        self.entry_text = ttk.Entry(self)
        self.entry_text.grid(row=3, column=1, sticky='ew', pady=5)

        # Botón de Acción
        self.btn_submit = ttk.Button(self, text="Start", command=self._on_submit)
        self.btn_submit.grid(row=4, column=0, columnspan=2, pady=20)

    def _on_submit(self):
        """Recopila los datos y llama a la función del controlador principal"""
        data = {
            "space": self.combo_a.get(),
            "map": self.combo_b.get(),
            "player": self.entry_text.get()
        }
        # Ejecutamos el callback pasando los datos limpios
        self.submit_callback(data)


class MainApp(tk.Tk):
    """
    El Controlador Principal. Hereda de tk.Tk.
    Gestiona la ventana y la transición entre vistas.
    """
    def __init__(self):
        super().__init__()
        self.title("Aplicación Modular Tkinter")
        self.geometry("400x300")
        
        # Contenedor principal
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)

        # Iniciamos mostrando la vista de entrada
        self.show_input_view()

    def show_input_view(self):
        """Limpia el contenedor y carga el formulario"""
        self._clear_container()
        # Instanciamos la vista y le pasamos nuestra función de procesamiento
        InputView(self.container, submit_callback=self.ejecutar_logica)

    def ejecutar_logica(self, data):
        """
        Esta función se ejecuta al pulsar el botón.
        1. Oculta/Destruye la vista anterior.
        2. Ejecuta la lógica deseada.
        """
        print(f"Datos recibidos: {data}") # Debug en consola
        
        # PASO 1: Esconder todo (limpiar el contenedor)
        self._clear_container()

        # PASO 2: Feedback visual (opcional pero recomendado)
        lbl_info = ttk.Label(self.container, text="Procesando datos...\nMira la consola.", justify="center")
        lbl_info.pack(expand=True)
        
        # Forzamos la actualización de la GUI para que se vea el cambio antes de procesar
        self.update() 

        # PASO 3: Ejecutar la función de lógica de negocio
        self._business_logic(data)

    def _business_logic(self, data):
        """Aquí va tu código pesado o lógica real"""
        # Simulamos un proceso
        time.sleep(1) 
        print("Lógica ejecutada exitosamente.")
        
        # Opcional: Mostrar resultado final o botón para volver
        for widget in self.container.winfo_children():
            widget.destroy()
            
        ttk.Label(self.container, text="¡Hecho!", font=("Arial", 14, "bold")).pack(pady=20)
        ttk.Button(self.container, text="Reiniciar", command=self.show_input_view).pack()

    def _clear_container(self):
        """Método utilitario para limpiar la pantalla actual"""
        for widget in self.container.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()