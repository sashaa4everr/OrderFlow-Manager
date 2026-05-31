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
        self.ventana_pedido_abierta = False
#
        self.title("Panel de control")
        self.geometry("1100x700")
        self.resizable(False, False)
        self.configure(fg_color="#F7EFE6")

        # Ruta del archivo de pedidos, tmb utilizamos un archivo json para guardar los pedidos, asi que necesitamos la ruta para cargar los pedidos en la tabla
        self.orders_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "orders.json")
        self.tabla = None  # Para referenciar la tabla de pedidos
        self.auto_refresh = True  # Bandera para actualizar automáticamente

        self.create_dashboard()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Iniciar la actualización automática de la tabla, mas adelante pondremos cosas nuevas con repecto a esto
        self.auto_actualizar_tabla()

#en este apartado, aparece la parte visual del dashboard, es decir, el menu lateral, el header, las tarjetas de ganancias y ventas totales, y el panel de pedidos recientes
    def create_dashboard(self):
        sidebar = ctk.CTkFrame(self, fg_color="#ffffff", width=220, corner_radius=20)
        sidebar.pack(side="left", fill="y", padx=(20, 10), pady=20)

        logo = ctk.CTkLabel(sidebar, text="Mi Tienda", font=("Segoe UI", 20, "bold"), text_color="#8B6F47")
        logo.pack(pady=(20, 20))

        self.botones = {}
        opciones = ["Inicio", "Nuevo pedido"]
        for opcion in opciones:
            boton = ctk.CTkButton(
                sidebar,
                text=opcion,
                width=180,
                height=45,
                fg_color="#E8CCBB",
                hover_color="#D4A574",
                text_color="#5A3F2B",
                font=("Segoe UI", 12, "bold"),
                corner_radius=10,
                command=lambda opt=opcion: self.cambiar_pantalla(opt)
            )
            boton.pack(pady=10)
            self.botones[opcion] = boton

        contenido = ctk.CTkFrame(self, fg_color="#F4E6DC", corner_radius=20)
        contenido.pack(side="left", fill="both", expand=True, padx=(0, 20), pady=20)
        self.contenido = contenido

        header = ctk.CTkFrame(contenido, fg_color="#ffffff", corner_radius=18)
        header.pack(fill="x", padx=20, pady=20)

        titulo = ctk.CTkLabel(
            header,
            text=f"Bienvenido, {self.usuario}",
            font=("Segoe UI", 24, "bold"),
            text_color="#8B6F47"
        )
        titulo.pack(anchor="w", padx=20, pady=20)

        cards_frame = ctk.CTkFrame(contenido, fg_color="#F4E6DC")
        cards_frame.pack(fill="x", padx=20, pady=(0, 15))


    #estas son las cositas que se ven ese cuadrado, que actualmente no funcionan en la BETA, sin embargo pensamos cambiarlo en un futuro
        self.crear_tarjeta(cards_frame, "Ganancias totales", "$", "+0%", 0)
        self.crear_tarjeta(cards_frame, "Ventas totales", "0", "+0%", 1)

        panel_pedidos = ctk.CTkFrame(contenido, fg_color="#E8CCBB", corner_radius=20)
        panel_pedidos.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        panel_titulo = ctk.CTkLabel(
            panel_pedidos,
            text="Pedidos recientes",
            font=("Segoe UI", 18, "bold"),
            text_color="#7D5D46"
        )
        panel_titulo.pack(anchor="nw", padx=20, pady=(20, 10))

        # Frame para la tabla (se puede actualizar)
        self.tabla_container = ctk.CTkFrame(panel_pedidos, fg_color="#E8CCBB")
        self.tabla_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Cargar los pedidos iniciales
        self.actualizar_tabla_pedidos()

        self.detalle_frame = ctk.CTkFrame(contenido, fg_color="#F7EFE6", corner_radius=18)
        self.detalle_frame.pack(fill="x", padx=20, pady=(0, 20))

        self.detalle_label = ctk.CTkLabel(
            self.detalle_frame,
            text="Selecciona una opción del menú para ver más detalles.",
            font=("Segoe UI", 14),
            text_color="#8B6F47"
        )
        self.detalle_label.pack(padx=20, pady=20)

    def crear_tarjeta(self, parent, titulo, valor, cambio, posicion):
        tarjeta = ctk.CTkFrame(parent, fg_color="#ffffff", corner_radius=18)
        tarjeta.grid(row=0, column=posicion, padx=15, pady=10, sticky="nsew")
        parent.grid_columnconfigure(posicion, weight=1)

        label_titulo = ctk.CTkLabel(
            tarjeta,
            text=titulo,
            font=("Segoe UI", 13),
            text_color="#7D5D46"
        )
        label_titulo.pack(anchor="w", padx=15, pady=(15, 5))

        label_valor = ctk.CTkLabel(
            tarjeta,
            text=valor,
            font=("Segoe UI", 24, "bold"),
            text_color="#8B6F47"
        )
        label_valor.pack(anchor="w", padx=15)

        label_cambio = ctk.CTkLabel(
            tarjeta,
            text=cambio,
            font=("Segoe UI", 12, "bold"),
            text_color="#3B7D3B"
        )
        label_cambio.pack(anchor="w", padx=15, pady=(10, 15))

    def cambiar_pantalla(self, opcion):
        if opcion == "Nuevo pedido":
            self.abrir_pedido()
        else:
            self.detalle_label.configure(text=f"Has seleccionado: {opcion}")

    def abrir_pedido(self):
        if self.ventana_pedido_abierta:
            return

        try:
            self.ventana_pedido_abierta = True
    
            ruta_pedido = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "pedido.py"
            )
    
            proceso = subprocess.Popen(
                [sys.executable, ruta_pedido]
            )
    
            def esperar_cierre():
                proceso.wait()
                self.ventana_pedido_abierta = False
    
            threading.Thread(
                target=esperar_cierre,
                daemon=True
            ).start()

        except Exception as e:
            self.ventana_pedido_abierta = False
            print("Error al abrir pedido:", e)

    def actualizar_tabla_pedidos(self):
        # Limpiar la tabla anterior
        for widget in self.tabla_container.winfo_children():
            widget.destroy()

        # Cargar pedidos del archivo JSON
        pedidos = self.cargar_pedidos()

        # Crear headers
        headers = ["Pedido", "Cliente", "Producto", "Cantidad"]
        header_frame = ctk.CTkFrame(self.tabla_container, fg_color="#E8CCBB")
        header_frame.pack(fill="x", pady=(0, 10))
        for texto in headers:
            label = ctk.CTkLabel(
                header_frame,
                text=texto,
                font=("Segoe UI", 12, "bold"),
                text_color="#7D5D46"
            )
            label.pack(side="left", expand=True)

        # Mostrar los últimos 3 pedidos mas recientes, la funcion de for i, pedido en enumerate, se refiere a que se van a mostrar los pedidos en orden inverso, es decir, el ultimo pedido que se hizo, va a ser el primero que se muestre en la tabla, y asi sucesivamente con los siguientes pedidos, esto es para que el usuario pueda ver los pedidos mas recientes sin tener que buscar entre todos los pedidos anteriores
        for i, pedido in enumerate(pedidos[-3:][::-1]):  # Últimos 3 pedidos en orden inverso
            fila_frame = ctk.CTkFrame(self.tabla_container, fg_color="#E8CDAD", height=45, corner_radius=12)
            fila_frame.pack(fill="x", pady=6)

            # Número de pedido, esto es para mostrar el numero de pedido, se muestra con un formato de 3 digitos
            label = ctk.CTkLabel(
                fila_frame,
                text=f"#{len(pedidos) - i:03d}",
                font=("Segoe UI", 12),
                text_color="#5A3F2B"
            )
            label.pack(side="left", expand=True)
#estos que saldran a continuacion, son para mostrar el diseno de esa tabla, cada uno esta dividido en 
#cada funcion.
            # Cliente
            label = ctk.CTkLabel(
                fila_frame,
                text=pedido.get("Client", "N/A"),
                font=("Segoe UI", 12),
                text_color="#5A3F2B"
            )
            label.pack(side="left", expand=True)

            # Producto
            label = ctk.CTkLabel(
                fila_frame,
                text=pedido.get("Title", "N/A"),
                font=("Segoe UI", 12),
                text_color="#5A3F2B"
            )
            label.pack(side="left", expand=True)

            # Cantidad
            label = ctk.CTkLabel(
                fila_frame,
                text=pedido.get("Quantity", "N/A"),
                font=("Segoe UI", 12),
                text_color="#5A3F2B"
            )
            label.pack(side="left", expand=True)
#en esta parte, Ese método intenta leer un archivo JSON con pedidos y devolverlos como lista
# Si el archivo no existe o hay un error, muestra un mensaje y devuelve una lista vacía.
    def cargar_pedidos(self):

        try:
            if os.path.exists(self.orders_file):
                with open(self.orders_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print("Error al cargar pedidos:")
        return []

    def auto_actualizar_tabla(self):

        if self.auto_refresh:
            self.actualizar_tabla_pedidos()
            self.after(1000, self.auto_actualizar_tabla)

    def on_close(self):
        self.auto_refresh = False
        self.parent.destroy()
        self.destroy()

