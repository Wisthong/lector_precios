import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from datetime import datetime

# Rutas y colores institucionales
ARCHIVO = "/mnt/checker/CHECKER1.TXT"
# ARCHIVO = r"\\192.168.40.250\trm_universal\CHECKER1.TXT"
COLOR_AZUL = "#1e429f"
COLOR_AMARILLO = "#fabc0b"
COLOR_BLANCO = "#ffffff"
COLOR_FONDO = "#f5f8ff"

root = tk.Tk()
root.title("Lector de Precios - Distribuidora Universal")

# Detectar resolución de pantalla
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Configuración adaptativa
if screen_width == 800 and screen_height == 480:
    root.geometry("800x480")
    FONT_REGULAR = ("Arial", 12)
    FONT_LG = ("Arial", 18, "bold")
    FONT_XL = ("Arial", 22, "bold")
    LOGO_SIZE = (150, 90)
    ENTRY_WIDTH = 18
    PRECIO_FONT = ("Arial", 28, "bold")
else:
    root.geometry("600x600")
    FONT_REGULAR = ("Arial", 16)
    FONT_LG = ("Arial", 24, "bold")
    FONT_XL = ("Arial", 28, "bold")
    LOGO_SIZE = (300, 180)
    ENTRY_WIDTH = 25
    PRECIO_FONT = ("Arial", 48, "bold")

root.configure(bg=COLOR_FONDO)

def cargar_productos():
    productos = {}
    if not os.path.exists(ARCHIVO):
        return productos

    with open(ARCHIVO, "r", encoding="utf-8", errors="ignore") as f:
        for linea in f:
            partes = linea.strip().split(",")
            if len(partes) < 4:
                continue
            codigo = partes[0].strip()
            item = partes[1].strip()
            nombre = partes[2].strip()
            try:
                precio = int(partes[3].strip())
            except ValueError:
                precio = 0
            productos[codigo] = (item, nombre, precio)
    return productos

def simular_enter():
    buscar_producto()

def buscar_producto(event=None):
    codigo = entry_codigo.get().strip()
    producto = productos.get(codigo)
    if producto:
        item, nombre, precio = producto
        label_nombre_val.config(text=nombre)
        label_item_val.config(text=item)
        label_precio_val.config(text=f"${precio:,.0f}")
        root.after(10000, limpiar_campos)
    else:
        label_nombre_val.config(text="Producto no encontrado")
        label_item_val.config(text="")
        label_precio_val.config(text="")
        root.after(5000, limpiar_campos)
    entry_codigo.delete(0, tk.END)

def on_scan_codigo(event):
    simular_enter()

def limpiar_campos():
    label_nombre_val.config(text="")
    label_item_val.config(text="")
    label_precio_val.config(text="")

# ENCABEZADO
frame_header = tk.Frame(root, bg=COLOR_AZUL, height=100)
frame_header.pack(fill=tk.X)

try:
    logo_img = Image.open("logo.png")
    logo_img = logo_img.resize(LOGO_SIZE, Image.Resampling.LANCZOS)
    logo_photo = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(frame_header, image=logo_photo, bg=COLOR_AZUL)
    logo_label.image = logo_photo
    logo_label.pack(pady=10)
except Exception as e:
    print("Error cargando imagen:", e)

# BUSCADOR
frame_search = tk.Frame(root, bg=COLOR_FONDO)
frame_search.pack(pady=10)

try:
    lupa_img = Image.open("lupa.png")
    lupa_img = lupa_img.resize((24, 24), Image.Resampling.LANCZOS)
    lupa_photo = ImageTk.PhotoImage(lupa_img)
    icon_label = tk.Label(frame_search, image=lupa_photo, bg=COLOR_FONDO)
    icon_label.image = lupa_photo
    icon_label.pack(side=tk.LEFT, padx=5)
except Exception as e:
    print("Error cargando imagen lupa:", e)

entry_codigo = tk.Entry(frame_search, font=FONT_LG, width=ENTRY_WIDTH, justify="center")
entry_codigo.pack(side=tk.LEFT, padx=10)
entry_codigo.focus()
entry_codigo.bind("<Return>", buscar_producto)

# RESULTADOS
frame_resultado = tk.Frame(root, bg=COLOR_BLANCO, bd=2, relief="groove")
frame_resultado.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

def etiqueta(t, row):
    label = tk.Label(frame_resultado, text=t, font=FONT_LG, fg=COLOR_BLANCO, bg=COLOR_AMARILLO, anchor="w")
    label.grid(row=row, column=0, sticky="w", padx=10, pady=10)
    return tk.Label(frame_resultado, text="", font=FONT_XL, bg=COLOR_BLANCO, anchor="w")

label_nombre_val = etiqueta("Descripción:", 0)
label_nombre_val.grid(row=0, column=1, sticky="w", padx=10)

label_item_val = etiqueta("Ítem:", 1)
label_item_val.grid(row=1, column=1, sticky="w", padx=10)

# Precio debajo del ítem (fila 2, columna 1)
label_precio_titulo = tk.Label(frame_resultado, text="Precio:", font=FONT_LG, fg=COLOR_BLANCO, bg=COLOR_AMARILLO, anchor="w")
label_precio_titulo.grid(row=2, column=0, sticky="w", padx=10, pady=10)

label_precio_val = tk.Label(frame_resultado, text="", font=PRECIO_FONT, bg=COLOR_BLANCO, anchor="w")
label_precio_val.grid(row=2, column=1, sticky="w", padx=10)

# FOOTER
frame_footer = tk.Frame(root, bg=COLOR_AZUL)
frame_footer.pack(fill=tk.X, side=tk.BOTTOM)

anio = datetime.now().year
label_footer_left = tk.Label(frame_footer, text=f"© {anio} Desarrollador: Wisthong Martinez", font=("Arial", 10), fg=COLOR_BLANCO, bg=COLOR_AZUL)
label_footer_right = tk.Label(frame_footer, text=f"© {anio} Diseño: Luis Rojas", font=("Arial", 10), fg=COLOR_BLANCO, bg=COLOR_AZUL)
label_footer_left.pack(side=tk.LEFT, padx=10, pady=5)
label_footer_right.pack(side=tk.RIGHT, padx=10, pady=5)

# CARGA INICIAL Y ACTUALIZACIÓN
productos = cargar_productos()

def recargar_productos():
    global productos
    productos = cargar_productos()
    root.after(60000, recargar_productos)

recargar_productos()
root.mainloop()
