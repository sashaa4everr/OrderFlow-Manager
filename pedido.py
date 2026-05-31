#Nuevamente se importan las librerias
import customtkinter as ctk
from tkinter import messagebox
import json
import os

# Tema de los colores, esto es para mantener una consistencia en el diseño de la aplicacion
BG = "#F7EFE6"
PANEL = "#E8CCBB"
ACCENT = "#D4A574"
TEXT = "#5A3F2B"

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

#esta clase es la que se encarga de mostrar la ventana de tomar pedido, esta ventana se abre al hacer click en el boton "Nuevo Pedido" del dashboard
#  esta clase tiene un "callback" que se llama cada vez que se guarda un nuevo pedido
#  esto es para que el dashboard pueda actualizar la tabla de pedidos sin tener que cerrar y abrir la ventana de nuevo, 
# ademas esta clase tiene una lista de productos predefinidos, cada producto tiene un nombre, una descripcion, y opciones para personalizar el pedido
# esta clase tambien tiene un metodo para guardar los pedidos en un archivo JSON y otro metodo para cargar los pedidos desde ese archivo JSON...
class PedidoApp(ctk.CTk):
    def __init__(self, parent=None, callback=None):
        super().__init__()
        self.title("Tomar Pedido - Burbu Shake")
        self.geometry("1000x700")
        self.resizable(False, False)
        self.configure(fg_color=BG)

        self.callback = callback  # Callback para notificar al dashboard
        self.archive = os.path.join(os.path.dirname(os.path.abspath(__file__)), "orders.json")
        self.orders = []

        self.products = [
            {"name": "Guanabanazo", "descriptionNormal": "Producto Sencillo", "hasPremium": True, "normalOptions": [{"label":"Onzas:", "options":["12 ONZ","16 ONZ"]}], "premiumOptions": []},
            {"name": "Maracumango", "descriptionNormal": "Producto Sencillo", "hasPremium": True, "normalOptions": [{"label":"Onzas:", "options":["12 ONZ","16 ONZ"]}], "premiumOptions": []},
            {"name": "Salpicón", "descriptionNormal": "Producto Sencillo", "hasPremium": True, "normalOptions": [{"label":"Onzas:", "options":["12 ONZ","16 ONZ"]}], "premiumOptions": []},
            {"name": "Waffle Burbuja", "descriptionNormal": "HELADO, FRUTA, TOPPING", "hasPremium": True, "normalOptions": [], "premiumOptions": []},
            {"name": "Merengones", "descriptionNormal": "Base MERENGON con crema", "hasPremium": False, "normalOptions": [], "premiumOptions": []},
        ]

        self.imgReferences = {}
        self.currentMode = "normal"

        self.create_layout()
        self.loadOrders()

    def validar_numero(self, valor):
        if valor == "":
            return True
    
        return valor.isdigit()

    def create_layout(self):
        # Sidebar
        sidebar = ctk.CTkFrame(self, fg_color=PANEL, width=220, corner_radius=18)
        sidebar.pack(side="left", fill="y", padx=20, pady=20)

        title = ctk.CTkLabel(sidebar, text="Pedidos", font=("Segoe UI", 20, "bold"), text_color=TEXT)
        title.pack(pady=(20,10))

        new_btn = ctk.CTkButton(sidebar, text="Nuevo Pedido", fg_color=ACCENT, hover_color="#c99f4d", text_color="white", corner_radius=12, command=lambda: self.show_frame("orders"))
        new_btn.pack(pady=10, padx=10)

        # Main area
        main = ctk.CTkFrame(self, fg_color=BG, corner_radius=18)
        main.pack(side="left", fill="both", expand=True, padx=(0,20), pady=20)

        # Header
        header = ctk.CTkFrame(main, fg_color="#FFFFFF", corner_radius=12)
        header.pack(fill="x", padx=20, pady=20)
        self.header_label = ctk.CTkLabel(header, text="Seleccione un producto", font=("Segoe UI", 18, "bold"), text_color=TEXT)
        self.header_label.pack(padx=20, pady=16, anchor="w")

        # Content frames
        content = ctk.CTkFrame(main, fg_color=BG)
        content.pack(fill="both", expand=True, padx=20, pady=(0,20))

        left = ctk.CTkFrame(content, fg_color="#F4E6DC", width=260, corner_radius=12)
        left.pack(side="left", fill="y", padx=(0,10), pady=10)
        left.pack_propagate(False)

        right = ctk.CTkFrame(content, fg_color="#F4E6DC", corner_radius=12)
        right.pack(side="left", fill="both", expand=True, padx=(10,0), pady=10)

        # Product buttons
        self.product_container = left
        for p in self.products:
            btn = ctk.CTkButton(left, text=p['name'], fg_color="#E8CCBB", text_color=TEXT, hover_color="#D4A574", corner_radius=10, command=lambda prod=p: self.show_product(prod))
            btn.pack(pady=8, padx=12, fill="x")

        # Right: info area
        self.info_frame = right
        self.info_placeholder = ctk.CTkLabel(self.info_frame, text="Detalles del producto", font=("Segoe UI", 14), text_color=TEXT)
        self.info_placeholder.pack(pady=40)

    def show_frame(self, name):
        if name == "orders":
            self.deiconify()

    def show_product(self, product):
        for w in self.info_frame.winfo_children():
            w.destroy()
        self.header_label.configure(text=product['name'])

        # Title
        ctk.CTkLabel(self.info_frame, text=product['name'], font=("Segoe UI", 16, "bold"), text_color=TEXT).pack(pady=(10,6))
        ctk.CTkLabel(self.info_frame, text=product['descriptionNormal'], font=("Segoe UI", 12), text_color=TEXT).pack(pady=(0,10))

        # Form
        form = ctk.CTkFrame(self.info_frame, fg_color="#FFFFFF", corner_radius=10)
        form.pack(padx=20, pady=10, fill="x")

        ctk.CTkLabel(form, text="Nombre del Cliente:", text_color=TEXT).grid(row=0, column=0, sticky="w", padx=10, pady=8)
        self.client_entry = ctk.CTkEntry(form)
        self.client_entry.grid(row=0, column=1, padx=10, pady=8)

        vcmd = (self.register(self.validar_numero), "%P")
        ctk.CTkLabel(form, text="Cantidad:", text_color=TEXT).grid(row=1, column=0, sticky="w", padx=10, pady=8)
        self.qty_entry = ctk.CTkEntry(form, validate="key", validatecommand=vcmd)
        self.qty_entry.grid(row=1, column=1, padx=10, pady=8)

        # Dropdowns
        self.dropdown_vars = {}
        options = product.get('normalOptions', [])
        for i, cfg in enumerate(options):
            ctk.CTkLabel(form, text=cfg['label'], text_color=TEXT).grid(row=2+i, column=0, sticky="w", padx=10, pady=6)
            var = ctk.StringVar(value=cfg['options'][0])
            om = ctk.CTkOptionMenu(form, values=cfg['options'], variable=var)
            om.grid(row=2+i, column=1, padx=10, pady=6)
            self.dropdown_vars[cfg['label']] = var

        save_btn = ctk.CTkButton(self.info_frame, text="Guardar Pedido", fg_color=ACCENT, text_color="white", corner_radius=12, command=lambda p=product: self.save_order(p))
        save_btn.pack(pady=12)

    def save_order(self, product):
        client = self.client_entry.get().strip() if hasattr(self, 'client_entry') else ''
        qty = self.qty_entry.get().strip() if hasattr(self, 'qty_entry') else ''
        if not client or not qty:
            messagebox.showwarning("Campos Incompletos", "Complete nombre y cantidad")
            return
        if not qty.isdigit():
            messagebox.showwarning("Cantidad inválida", "La cantidad debe ser numérica")
            return
        if int(qty) <= 0:
            messagebox.showwarning("Cantidad inválida","La cantidad debe ser mayor que cero")
            return
        selected = []
        for k,v in self.dropdown_vars.items():
            selected.append(f"{k} {v.get()}")
        optionSummary = " | ".join(selected) if selected else ""
        title = f"{product['name']} (Normal)"
        order = {"Title": title, "Description": product.get('descriptionNormal',''), "Image_Path": "", "Client": client, "Quantity": qty, "Option": optionSummary, "Complete": False}
        self.orders.append(order)
        self.saveJSON()
        messagebox.showinfo("Éxito", "Pedido registrado")
        # limpiar
        self.client_entry.delete(0, 'end')
        self.qty_entry.delete(0, 'end')
        # Notificar al dashboard si hay callback
        if self.callback:
            self.callback()
#No explique tanto la parte anterior porque son cosas que ya hemos visto en otras aplicaciones, entonces no lo vi necesario
#por otra parte, aca se explica el metodo save_order, este metodo se encarga de guardar el pedido en la lista de pedidos, y luego llama al metodo saveJSON para guardar esa lista en un archivo JSON, ademas este metodo tambien tiene una validacion para asegurarse de que el nombre del cliente y la cantidad no esten vacios, si alguno de esos campos esta vacio, se muestra un mensaje de advertencia y no se guarda el pedido, si todo esta correcto, se muestra un mensaje de exito y se limpian los campos de entrada para que el usuario pueda ingresar un nuevo pedido sin tener que borrar los campos manualmente
    def saveJSON(self):
        try:
            with open(self.archive, 'w', encoding='utf-8') as f:
                json.dump(self.orders, f, indent=4, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar orders.json:\n{e}")

    def loadOrders(self):
        if not os.path.exists(self.archive):
            with open(self.archive, 'w', encoding='utf-8') as f:
                json.dump([], f)
            self.orders = []
            return
        try:
            with open(self.archive, 'r', encoding='utf-8') as f:
                self.orders = json.load(f)
        except Exception:
            self.orders = []
#por ultimo, esta parte es para mostrar la tabla de pedidos en el dashboard.
if __name__ == '__main__':
    app = PedidoApp()
    app.mainloop()
