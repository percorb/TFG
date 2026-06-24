import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk

from Lector_UI import setLetra, IniciarLectura, ContinuarLectura, PararLectura, getFila, getMuestra, getFin, getError, setError
from FuncionesRF import *

ctk.set_appearance_mode("system") # Para que tenga un modo oscuro o claro
ctk.set_default_color_theme("green") # Los botones serán verdes

app = ctk.CTk() # Para crear la ventana
app.geometry("400x400")

app.resizable(False, False) # Para no redimensionar la ventana
app.title("Interfaz del guante traductor")

Letra=None
ip=None
Seleccionado=False # Flag para saber si el usuario ha seleccionado una conexión con el Arduino
arduino = None # Para acceder al arduino


# Funciones de la interfaz de usuario
# Función para obtener el frame actualmente activo
def ObtenerFrameActual():
    for f in ListaFrames:
        if f.winfo_ismapped():
            return f

# ============================ #
# Funciones del menú principal #
# ============================ #
def Traduccion():
    frame_menu.pack_forget()
    frame_menu_traduccion.pack(fill="both",expand=True)
    
def Lectura():
    frame_menu.pack_forget()
    frame_lectura.pack(fill="both",expand=True)
    if arduino is not None:
        arduino.close()
    
def Salir():
    app.destroy()

def Volver(frame):
    global arduino
    if arduino is not None:
        arduino.close()
    cancel_wifi.set()
    frame.pack_forget()
    frame_menu.pack(fill="both",expand=True)
    
# ============================= #
# Funciones del menú de lectura #
# ============================= #
def GuardarLetra():
    global Letra
    letra = entry_texto.get().strip().upper()
    if not letra:
        Letra = False
        print("No hay ninguna letra colocada")
        info.configure(text="No hay letra seleccionada")
        return
    Letra = True
    setLetra(letra)
    info.configure(text=f"Letra seleccionada: {letra}")
    print(f"Letra enviada al sistema: {letra}")

def Leer():
    global Letra
    if not Letra:
        print("No hay ninguna letra seleccionada")
        return
    else:
        try:
            frame_lectura.pack_forget()
            frame_control_lectura.pack(fill="both",expand=True)
            IniciarLectura()
        except Exception as e:
            print(f"No se puede acceder al puerto serial")
            return

# ======================================== #
# Funciones del menú de control de lectura #
# ======================================== #

def salir_lectura():
    PararLectura()

    frame_control_lectura.pack_forget()
    frame_lectura.pack(fill="both", expand=True)
    
def ActualizarEstado():
    # Obtenemos los datos actuales
    muestra = getMuestra()
    fila = getFila()
    fin = getFin()
    error = getError()
    
    if error:
        if arduino is not None:
            arduino.close()
        frame_actual = ObtenerFrameActual()
        if frame_actual is not None:
            frame_actual.pack_forget()
        frame_error.pack(fill="both",expand=True)
        setError()
    # Para cerrar la lectura cuando este termina
    if fin and frame_control_lectura.winfo_ismapped():
        frame_control_lectura.pack_forget()
        frame_fin_lectura.pack(fill="both", expand=True)
        fin = False
    else:
        # Mandamos dichos datos a sus labels específicos
        label_muestra.configure(text=f"Muestras: {muestra}/50")
        label_fila.delete("1.0", "end")
        label_fila.insert("end", f"{fila}")
    app.after(500,ActualizarEstado) # Realiza este proceso cada 0.5 segundos

# =========================================== #
# Funciones del menú de control de traducción #
# =========================================== #

def ConexionLocal():
    global Seleccionado, arduino
    try:
        cancel_wifi.set() # Por si está intentando conectar via WiFi
        arduino = ConectarArduinoLocal()
        label_info.configure(text="Conexión local exitosa")
        Seleccionado=True
    except Exception as e:
        print("No se ha podido conectar por el puerto serial")
        label_info.configure(text="Conexión local fallida")
        Seleccionado=False

def ConexionWifi():
    cancel_wifi.clear()
    ip = entry_ip.get().strip()
    label_info.configure(text="Conectando...")
    
    ConectarArduinoWifiThread(ip,callback_ok,callback_fail)

def callback_ok(arduino_conn):
    global arduino, Seleccionado
    arduino = arduino_conn
    Seleccionado = True
    label_info.configure(text="Conexión WiFi OK")
    
def callback_fail():
    global Seleccionado
    Seleccionado = False
    label_info.configure(text="Conexión WiFi fallida")
    
    
# ================================ #
# Funciones del menú de traducción #
# ================================ #

def SeleccionarDataset():
    ruta = filedialog.askopenfilename(
        title="Selecciona un archivo .csv",
        filetypes=[("CSV files","*.csv")]
    )
    if ruta:
        print("Archivo seleccionado: ", ruta)
        return ruta
    else:
        print("No se seleccionó nada")
        return None
    
def IniciarTraduccion():
    cancel_wifi.set()
    global arduino
    if not Seleccionado or not arduino:
        label_info.configure(text="Selecciona una conexión")
        return
    else:
        # Cambio al frame de traducción
        frame_menu_traduccion.pack_forget()
        frame_traduccion.pack(fill="both",expand=True)
        try:
            ruta = SeleccionarDataset()
            X,y = PrepararDataset(ruta)
            scaler,X = EscalarDatos(X)
            rf = PrepararModelo(X,y)
            threading.Thread(
                target=PrediccionRealThread,
                args=(arduino, 10, rf, scaler, actualizar_ui),
                daemon=True
            ).start()
        except Exception as e:
            print(f"Error al iniciar la traducción: {e}")

def actualizar_ui(pred, top3):
    label_Prediccion.configure(text=f"Predicción: {pred}")

    label_probs.configure(
        text="Confianza: " + " | ".join(
            f"{c}: {p:.1%}" for c, p in top3
        )
    )

# ======================== #
# Frame del menú principal #
# ======================== #
frame_menu = ctk.CTkFrame(app)
frame_menu.pack(fill="both", expand=True)

# Título
titulo = ctk.CTkLabel(
    master=frame_menu,
    text="Guante Traductor",
    font=("Arial", 24, "bold")
)
titulo.place(relx=0.5, rely=0.1, anchor=tk.CENTER)    

# Botones
# - Traducción
traduccion = ctk.CTkButton(master=frame_menu,text="Traducción",command=Traduccion,width=200,height=40,font=("Arial", 18))
traduccion.place(relx=0.5,rely=0.3,anchor=tk.CENTER)
# - Lectura
lectura = ctk.CTkButton(master=frame_menu,text="Lectura",command=Lectura,width=200,height=40,font=("Arial", 18))
lectura.place(relx=0.5,rely=0.5,anchor=tk.CENTER)
# - Salir
salir = ctk.CTkButton(master=frame_menu,text="Salir",command=Salir,width=200,height=40,font=("Arial", 18))
salir.place(relx=0.5,rely=0.7,anchor=tk.CENTER)

# ================ #
# Frame de Lectura #
# ================ #
frame_lectura = ctk.CTkFrame(app)

# Título
titulo = ctk.CTkLabel(
    master=frame_lectura,
    text="Modo lectura",
    font=("Arial", 24, "bold")
)
titulo.place(relx=0.5, rely=0.1, anchor=tk.CENTER)  

# Input de texto
entry_texto = ctk.CTkEntry(
    master=frame_lectura,
    width=250,
    placeholder_text="Introduce el texto a traducir..."
)
entry_texto.place(relx=0.5,rely=0.35,anchor=tk.CENTER)

letra = entry_texto.get().strip().upper()
texto = f"Letra seleccionada: {letra}" if Letra else "No hay letra seleccionada"

# Informacion
info = ctk.CTkLabel(
    master=frame_lectura,
    text=texto,
    font=("Arial", 20, "bold")
)
info.place(relx=0.5, rely=0.23, anchor=tk.CENTER)  

# Botones
# Guardar letra
btn_save = ctk.CTkButton(
    frame_lectura,
    text="Guardar letra",
    command=GuardarLetra,
    width=200,
    height=40,
    font=("Arial", 18)
)
btn_save.place(relx=0.5,rely=0.5,anchor=tk.CENTER)

# Iniciar lectura
btn_iniciar = ctk.CTkButton(
    frame_lectura,
    text="Iniciar lectura de datos",
    command=Leer,
    width=200,
    height=40,
    font=("Arial", 18)
)
btn_iniciar.place(relx=0.5,rely=0.65,anchor=tk.CENTER)

# Volver al menú principal
btn_volver = ctk.CTkButton(
    frame_lectura,
    text="Volver",
    command=lambda: Volver(frame_lectura),
    width=200,
    height=40,
    font=("Arial", 18)
)
btn_volver.place(relx=0.5,rely=0.8,anchor=tk.CENTER)

# =========================== #
# Frame de control de lectura #
# =========================== #
frame_control_lectura = ctk.CTkFrame(app)

# Botones
btn_continuar = ctk.CTkButton(
    master=frame_control_lectura,
    text="Continuar",
    command=ContinuarLectura,
    width=200,
    height=40,
    font=("Arial", 18)
)
btn_continuar.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

btn_salir = ctk.CTkButton(
    master=frame_control_lectura,
    text="Salir",
    command=salir_lectura,
    width=200,
    height=40,
    font=("Arial", 18)
)
btn_salir.place(relx=0.5, rely=0.75, anchor=tk.CENTER)

# Labels
label_muestra = ctk.CTkLabel(
    master=frame_control_lectura,
    text="Muestras: 0/50",
    font=("Arial", 18, "bold")
)
label_muestra.place(relx=0.5, rely=0.1, anchor=tk.CENTER)  

label_fila = ctk.CTkTextbox(
    master=frame_control_lectura,
    font=("Arial", 14, "bold"),
    width=350, 
    height=120
)
label_fila.place(relx=0.5, rely=0.3, anchor=tk.CENTER)  

# ==================== #
# Frame fin de lectura #
# ==================== #

frame_fin_lectura = ctk.CTkFrame(app)

# Botones
btn_salir_fin = ctk.CTkButton(
    master=frame_fin_lectura,
    text="Salir",
    command=lambda: Volver(frame_fin_lectura),
    width=200,
    height=40,
    font=("Arial", 18)
)
btn_salir_fin.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Labels
label_fin = ctk.CTkLabel(
    master=frame_fin_lectura,
    text="¡Lectura finalizada!",
    font=("Arial", 18, "bold")
)
label_fin.place(relx=0.5, rely=0.25, anchor=tk.CENTER)  

# ============================ #
# Frame del menú de traducción #
# ============================ #
frame_menu_traduccion = ctk.CTkFrame(app)

# Título
titulo = ctk.CTkLabel(
    master=frame_menu_traduccion,
    text="Selecciona la conexión",
    font=("Arial", 24, "bold")
)
titulo.place(relx=0.5, rely=0.1, anchor=tk.CENTER)  

# Label de información
label_info = ctk.CTkLabel(
    master=frame_menu_traduccion,
    text="",
    font=("Arial", 18)
)
label_info.place(relx=0.5, rely=0.17, anchor=tk.CENTER) 

# Recibir ip si es necesario
entry_ip = ctk.CTkEntry(
    master=frame_menu_traduccion,
    width=250,
    placeholder_text="Introduce una dirección ip"
)
entry_ip.place(relx=0.5,rely=0.25,anchor=tk.CENTER)

ip_base = entry_ip.get().strip()

# Botones
btn_wifi = ctk.CTkButton(
    master=frame_menu_traduccion,
    text="Conexión WiFi",
    command=ConexionWifi,
    width=200,
    height=40,
    font=("Arial", 18)
)
btn_wifi.place(relx=0.5, rely=0.35, anchor=tk.CENTER)

btn_serial = ctk.CTkButton(
    master=frame_menu_traduccion,
    text="Conexión local",
    command=ConexionLocal,
    width=200,
    height=40,
    font=("Arial", 18)
)
btn_serial.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

btn_iniciar = ctk.CTkButton(
    master=frame_menu_traduccion,
    text="Iniciar",
    command=IniciarTraduccion,
    width=200,
    height=40,
    font=("Arial", 18)
)
btn_iniciar.place(relx=0.5, rely=0.65, anchor=tk.CENTER)

btn_salir = ctk.CTkButton(
    master=frame_menu_traduccion,
    text="Volver",
    command=lambda: Volver(frame_menu_traduccion),
    width=200,
    height=40,
    font=("Arial", 18)
)
btn_salir.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

# =================== #
# Frame de traducción #
# =================== #

frame_traduccion = ctk.CTkFrame(app)

# Botones
btn_salir = ctk.CTkButton(
    master=frame_traduccion,
    text="Volver",
    command=lambda: Volver(frame_traduccion),
    width=200,
    height=40,
    font=("Arial", 18)
)
btn_salir.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Labels
label_Prediccion = ctk.CTkLabel(
    master=frame_traduccion,
    text="Predicción: ",
    font=("Arial", 18, "bold")
)
label_Prediccion.place(relx=0.5, rely=0.1, anchor=tk.CENTER)  

label_probs = ctk.CTkLabel(
    master=frame_traduccion,
    text="Confianza: 0.00%",
    font=("Arial", 18, "bold")
)
label_probs.place(relx=0.5, rely=0.2, anchor=tk.CENTER)  

label_candidatos = ctk.CTkLabel(
    master=frame_traduccion,
    text="A | B | C",
    font=("Arial", 18, "bold")
)
label_candidatos.place(relx=0.5, rely=0.3, anchor=tk.CENTER)  

# ============== #
# Frame de error #
# ============== #

frame_error = ctk.CTkFrame(app)

# Botones
btn_salir = ctk.CTkButton(
    master=frame_error,
    text="Volver",
    command=lambda: Volver(frame_error),
    width=200,
    height=40,
    font=("Arial", 18)
)
btn_salir.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Labels
label_error = ctk.CTkLabel(
    master=frame_error,
    text="Hay un problema con los sensores.\nReinicia el Arduino, si sigue fallando, revisa\nlos cables.",
    font=("Arial", 18, "bold")
)
label_error.place(relx=0.5, rely=0.1, anchor=tk.CENTER)  


# Lista con todos los frames
ListaFrames = [frame_control_lectura, frame_lectura, frame_fin_lectura, frame_menu, frame_menu_traduccion, frame_traduccion]

ActualizarEstado()
app.mainloop()