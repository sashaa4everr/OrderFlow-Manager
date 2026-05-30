#se importan todas las librerias, al igual q el del inicio
import customtkinter as ctk
import json
import os
import subprocess
import sys
import threading

#basicamente, esta clase es la que se encarga de mostrar el dashboard
# es decir, lo que sale de las ganancias totales, ventas totales y los pedidos recientes
# ademas de un menu lateral para mirar entre las diferentes opciones
#algo importante es que reducimos algunas funciones cmo lo es lo de ventas totales, ya q este es apenas el BETA
#ctk.CTkToplevel es una clase del customtkinter que se utiliza para crear una ventana secundaria, en este caso el dashboard, que se abre desde la ventana principal del login y como q la tapa
class Dashboard(ctk.CTkToplevel):
    def __init__(self, parent, usuario: str):
        super().__init__(parent)
        self.parent = parent
        self.usuario = usuario
#
        self.title("Panel de control")
        self.geometry("1100x700")
        self.resizable(False, False)
        self.configure(fg_color="#F7EFE6")

        # Ruta del archivo de pedidos, tmb utilizamos un archivo json para guardar los pedidos, asi que necesitamos la ruta para cargar los pedidos en la tabla
        self.orders_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "orders.json")
        self.tabla = None  # Para referenciar la tabla de pedidos
