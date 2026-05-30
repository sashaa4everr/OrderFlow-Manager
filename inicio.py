
#En esta seccion, se importa la libreria del tkinter para el tema visual 
import customtkinter as ctk
from PIL import Image, ImageDraw
import io
from dashboard import Dashboard

# aca se configura la apariencia, el "light" es por el tema
#claro, por otra parte, el class InterfazLogin es la clase principal
#  donde se encuentra toda la interfaz, los botones, los inputs, etc
#el def_init__ es el constructor de la clase, donde nos deja
# configurar la ventana, el titulo, el tamaño, etc
#Y el super().__init__() es para heredar las propiedades de la clase padre (ctk.CTk)
#  y luego se le agregan las propiedades especificas de esta ventana
ctk.set_appearance_mode("light")

class InterfazLogin(ctk.CTk):
    def __init__(self):
        super().__init__()


#el tema de las ventanas y los fondos

        # aca se configura la ventada derecha
        #"self" es para referenciar a la instancia actual de la clase
        #".geometry" y ".resizable" son para configurar el tamaño de la ventana y
        # si se puede redimensionar o no, estas propiedades son especiales de tkinter

        #debo de decir que  trato de ser lo mas especifica posible
        #debido a que estos temas no lo hemos visto
        self.title("welcome!")
        self.geometry("1000x650")
        self.resizable(False, False)
        
        # Color de fondo principal
        self.configure(fg_color="#ffffff")
        
        # aca se encuentra la parte donde creamos toda la interfaz, incluye
        #colores, botones, etc, se divide entre la parte del texto y los inputs
        self.crear_interfaz()
        
    def crear_interfaz(self):
        # Frame izquierdo (donde se pone la contrasena y eso)
        #".pack" es para colocar el frame en la ventana, "side" es para decir de que lado
        frame_izquierdo = ctk.CTkFrame(self, fg_color="#ffffff", corner_radius=0)
        frame_izquierdo.pack(side="left", fill="both", expand=True)
        
        # Frame derecho (bienvenida) 
        frame_derecho = ctk.CTkFrame(self, fg_color="#E8CCBB", corner_radius=0)
        frame_derecho.pack(side="right", fill="both", expand=True)
        
        # ===== PANEL IZQUIERDO =====
        # Contenedor principal, para centrar el contenido verticalmente, y se crea la funcion 
        #"izq_container" para colocar todo el contenido del panel izquierdo, como los inputs y los botones
        izq_container = ctk.CTkFrame(frame_izquierdo, fg_color="#ffffff")
        izq_container.pack(expand=True, padx=80)
        
        
        
        # Separador 1, esa linea q divide el titulo de los inputs
        # no tiene funcionalidad, pero se ve linda
        #se hace con la funcion "ctk.CTkFrame" 
        # podemos ver que ya se utilizo para algo distinto
        # pero, se ve como una linea al cambiar la altura, y el radio para que se vea redondeada
        sep1 = ctk.CTkFrame(izq_container, fg_color="#E8CCBB", height=3, corner_radius=2)
        sep1.pack(fill="x", pady=(0, 30), padx=20)
        
        # texto "usuario" es el texto que se encuentra encima del input
        #simplemente es el texto de usuario, y se le pone un color y fuente
        label_usuario = ctk.CTkLabel(
            izq_container,
            text="Usuario",
            font=("Segoe UI", 12, "bold"),
            text_color="#666666"
        )
        label_usuario.pack(anchor="w", padx=20, pady=(0, 8))
        
        # Campo de usuario, es ese cuadradito donde se ingresa lo del usuario
        #si han trabajado con html, se daran cuenta que usa propiedades muy similares
        #xomo widht, height, border color, etc...
        self.entrada_usuario = ctk.CTkEntry(
            izq_container,
            placeholder_text="Ingresa tu usuario",
            width=200,
            height=38,
            font=("Segoe UI", 11),
            fg_color="#F8F8F8",
            border_color="#E8CCBB",
            border_width=2,
            text_color="#333333"
        )
        self.entrada_usuario.pack(padx=20, pady=(0, 20))
        
        # Separador 2 (es mas que lo mismo del separador 1, osea la rayita)
        sep2 = ctk.CTkFrame(izq_container, fg_color="#E8CCBB", height=3, corner_radius=2)
        sep2.pack(fill="x", pady=(0, 30), padx=20)
        
        # Etiqueta contraseña, va mas de lo mismo que la del usuario...
        label_password = ctk.CTkLabel(
            izq_container,
            text="Contraseña",
            font=("Segoe UI", 12, "bold"),
            text_color="#666666"
        )
        label_password.pack(anchor="w", padx=20, pady=(0, 8))
        
        # Cuadrito de la contrasena, aca va mas de lo mismo nuevamente, tiene estos cambios, tho
        #1. tiene la nueva propiedad de "show" que es para que se ponga como puntitos, se puede cambiar por lo q sea realmente...
        #2. No explique porque se escribe "placeholder_text", en vez de input, esto se debe a que es una propiedad de la libreria especificamente
        self.entrada_password = ctk.CTkEntry(
            izq_container,
            placeholder_text="Ingresa tu contraseña",
            width=200,
            height=38,
            font=("Segoe UI", 11),
            show="●",
            fg_color="#F8F8F8",
            border_color="#E8CCBB",
            border_width=2,
            text_color="#333333"
        )
        self.entrada_password.pack(padx=20, pady=(0, 30))
        
        # Botones, no hay mucho que decir, cuando se le de click al boton se ejecuta el archivo "dashboard.py"
        #algo importante es el "command=self.procesar_datos" que es para ejecutar la funcion de procesar datos, esta funcion se encarga de validar los datos ingresados y abrir el dashboard si todo esta correcto
        btn_frame = ctk.CTkFrame(izq_container, fg_color="#ffffff")
        btn_frame.pack(pady=(20, 0))
        
        btn_enviar = ctk.CTkButton(
            btn_frame,
            text="ENVIAR",
            width=200,
            height=40,
            font=("Segoe UI", 13, "bold"),
            fg_color="#D4A574",
            text_color="white",
            hover_color="#C9956B",
            corner_radius=6,
            command=self.procesar_datos
        )
        btn_enviar.pack(pady=10)
        
        
        # ===== PANEL DERECHO =====

        #volvemos con el panel derecho, recuerden que aca esta todo el tema de la bienvenida y cosas mas que nada
        #decorativas, no hay mucho que decir, sin embargo lo importante si lo hablare 
        frame_contenido = ctk.CTkFrame(frame_derecho, fg_color="#E8CCBB")
        frame_contenido.pack(expand=True, fill="both", padx=50, pady=60)
        
        # Decoración superior 
        deco_top = ctk.CTkLabel(
            frame_contenido,
            text="✧",
            font=("Segoe UI", 40),
            text_color="#D4A574"
        )
        deco_top.pack(pady=(0, 10))
        
        # Título principal
        titulo = ctk.CTkLabel(
            frame_contenido,
            text="welcome!",
            font=("Segoe UI", 56, "bold"),
            text_color="#8B6F47"
        )
        titulo.pack(pady=(0, 30))
        
        # Línea decorativa
        linea = ctk.CTkFrame(frame_contenido, fg_color="#D4A574", height=2)
        linea.pack(fill="x", padx=50, pady=(0, 30))
        
        # Mensaje principal
        mensaje_principal = ctk.CTkLabel(
            frame_contenido,
            text="eficiente para organizar tus tareas y proyectos!",
            font=("Segoe UI", 14, "normal"),
            text_color="#A0826D",
            justify="center"
        )
        mensaje_principal.pack(pady=15)
        
        # Mensaje secundario
        mensaje_sec = ctk.CTkLabel(
            frame_contenido,
            text="¡Descubre cómo puede ayudarte a ser más productivo!",
            font=("Segoe UI", 12),
            text_color="#B8A190",
            justify="center"
        )
        mensaje_sec.pack(pady=(0, 30))
        
        # Características
        features_frame = ctk.CTkFrame(frame_contenido, fg_color="#D4A574", corner_radius=10)
        features_frame.pack(fill="both", expand=True, pady=20)
        
        features_text = ctk.CTkLabel(
            features_frame,
            text="...",
            font=("Segoe UI", 12),
            text_color="white",
            justify="center"
        )
        features_text.pack(expand=True)
    
    # esta funcion es para procesar los datos ingresados, es decir, validar que no esten vacios y luego abrir el dashboard si todo esta correcto
    def procesar_datos(self):
        """Procesa los datos ingresados"""
        usuario = self.entrada_usuario.get()
        password = self.entrada_password.get()
        

    #aca es donde se valida que los campos no esten vacios, si alguno de los campos esta vacio, se muestra un mensaje de error, y se detiene la ejecucion de la funcion
        if not usuario or not password:
            self.mostrar_resultado("⚠ Por favor completa\ntodos los campos")
            return

        self.abrir_dashboard(usuario)

    #se abre la ventana del dashboard, con "def_dashboard"
    def abrir_dashboard(self, usuario):
        self.withdraw()
        ventana_dashboard = Dashboard(self, usuario)
        ventana_dashboard.focus()

# esta funcion es para limpiar los campos de usuario y contraseña, se llama cuando se cierra el dashboard,
# esto es para que la proxima vez que se abra el login, los campos esten vacios
    def limpiar_campos(self):
        self.entrada_usuario.delete(0, "end")
        self.entrada_password.delete(0, "end")
    
    def mostrar_resultado(self, mensaje):
        popup = ctk.CTkToplevel(self)
        popup.title("Resultado")
        popup.geometry("300x180")
        popup.resizable(False, False)
        popup.attributes('-topmost', True)
        
        # aca basicamente se cambia el popup del "error" cuando hay espacios vacios
        popup.configure(fg_color="#ffffff")
        
        label = ctk.CTkLabel(
            popup,
            text=mensaje,
            font=("Segoe UI", 12),
            justify="center",
            wraplength=260,
            text_color="#333333"
        )
        label.pack(expand=True, padx=20, pady=20)
        
        btn = ctk.CTkButton(
            popup,
            text="Aceptar",
            command=popup.destroy,
            fg_color="#D4A574",
            hover_color="#C9956B",
            text_color="white",
            font=("Segoe UI", 11, "bold"),
            width=150
        )
        btn.pack(pady=10)

#ya por ultimo, esto es para ejecutar la aplicacion, se crea una instancia de la clase InterfazLogin y se llama al mainloop para que la ventana se mantenga abierta
if __name__ == "__main__":
    app = InterfazLogin()
    app.mainloop()
#hemos terminado el codigo del inicio, por fin!!