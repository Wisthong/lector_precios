import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from datetime import datetime

# Rutas y colores institucionales
# ARCHIVO = "/mnt/checker/CHECKER1.TXT"
ARCHIVO = r"\\192.168.40.250\trm_universal\CHECKER1.TXT"
COLOR_AZUL = "#1e429f"
COLOR_AMARILLO = "#fabc0b"
COLOR_BLANCO = "#ffffff"
COLOR_FONDO = "#f5f8ff"

FONT_REGULAR = ("Arial", 16)
FONT_LG = ("Arial", 24, "bold")
FONT_XL = ("Arial", 28, "bold")

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
    # Llamar directamente a la función de búsqueda sin necesidad de presionar Enter
    buscar_producto()
    
def buscar_producto(event=None):
    codigo = entry_codigo.get().strip()
    producto = productos.get(codigo)
    if producto:
        item, nombre, precio = producto
        label_nombre_val.config(text=nombre)
        label_item_val.config(text=item)
        label_precio_val.config(text=f"${precio:,.0f}")
        # Programar limpieza después de 10 segundos
        root.after(10000, limpiar_campos)
    else:
        label_nombre_val.config(text="Producto no encontrado")
        label_item_val.config(text="")
        label_precio_val.config(text="")
        root.after(5000, limpiar_campos)  # Limpieza más rápida para "no encontrado"
    entry_codigo.delete(0, tk.END)

# Evento para escanear código de barras
def on_scan_codigo(event):
    # Asumiendo que el escáner de código de barras ya llena entry_codigo
    simular_enter()  # Llamar a la función para simular la pulsación de Enter

def limpiar_campos():
    label_nombre_val.config(text="")
    label_item_val.config(text="")
    label_precio_val.config(text="")

root = tk.Tk()
root.title("Lector de Precios - Distribuidora Universal")
root.geometry("600x600")
root.configure(bg=COLOR_FONDO)

# ENCABEZADO
frame_header = tk.Frame(root, bg=COLOR_AZUL, height=100)
frame_header.pack(fill=tk.X)

try:
    logo_img = Image.open("logo.png")
    # logo_img = logo_img.resize((100, 60), Image.Resampling.LANCZOS)
    logo_img = logo_img.resize((300, 180), Image.Resampling.LANCZOS)
    logo_photo = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(frame_header, image=logo_photo, bg=COLOR_AZUL)
    logo_label.image = logo_photo
    logo_label.pack(pady=10)
except Exception as e:
    print("Error cargando imagen:", e)

# BUSCADOR
frame_search = tk.Frame(root, bg=COLOR_FONDO)
frame_search.pack(pady=20)

# icon_label = tk.Label(frame_search, text="🔍", font=("Arial", 18), bg=COLOR_FONDO)
# icon_label.pack(side=tk.LEFT, padx=5)

# Cargar la imagen
lupa_img = Image.open("lupa.png")
lupa_img = lupa_img.resize((24, 24), Image.Resampling.LANCZOS)
lupa_photo = ImageTk.PhotoImage(lupa_img)

# Crear la etiqueta con la imagen
icon_label = tk.Label(frame_search, image=lupa_photo, bg=COLOR_FONDO)
icon_label.image = lupa_photo  # Mantener una referencia para evitar que la imagen sea eliminada por el recolector de basura
icon_label.pack(side=tk.LEFT, padx=5)

entry_codigo = tk.Entry(frame_search, font=FONT_LG, width=25, justify="center")
entry_codigo.pack(side=tk.LEFT, padx=10)
entry_codigo.focus()
entry_codigo.bind("<Return>", buscar_producto)

def on_codigo_input(event):
    if entry_codigo.get():
        # Cancelar cualquier búsqueda anterior programada
        if hasattr(root, "after_id"):
            root.after_cancel(root.after_id)
        # Esperar 300ms tras el último carácter antes de buscar
        root.after_id = root.after(300, simular_enter)

# entry_codigo.bind("<KeyRelease>", on_codigo_input)

# RESULTADOS
frame_resultado = tk.Frame(root, bg=COLOR_BLANCO, bd=2, relief="groove")
frame_resultado.pack(padx=40, pady=20, fill=tk.X, expand=True)

def etiqueta(t, row):
    label = tk.Label(frame_resultado, text=t, font=FONT_LG, fg=COLOR_BLANCO, bg=COLOR_AMARILLO, anchor="w")
    label.grid(row=row, column=0, sticky="w", padx=10, pady=10)
    return tk.Label(frame_resultado, text="", font=FONT_XL, bg=COLOR_BLANCO, anchor="w")

label_nombre_val = etiqueta("Descripción:", 0)
label_nombre_val.grid(row=0, column=1, sticky="w", padx=10)

label_item_val = etiqueta("Ítem:", 1)
label_item_val.grid(row=1, column=1, sticky="w", padx=10)

# Precio - en columna aparte (columna 2)
frame_precio_destacado = tk.Frame(frame_resultado, bg=COLOR_BLANCO, padx=10, pady=5)
frame_precio_destacado.grid(row=0, column=2, rowspan=3, sticky="e", padx=20, pady=10)

label_precio_texto = tk.Label(
    frame_precio_destacado,
    text="Precio:",
    font=FONT_LG,
    fg=COLOR_BLANCO,
    bg=COLOR_AMARILLO
)
label_precio_texto.pack(anchor="w")

label_precio_val = tk.Label(
    frame_precio_destacado,
    text="",
    font=("Arial", 48, "bold"),
    bg=COLOR_BLANCO
)
label_precio_val.pack()


# label_precio_val = etiqueta("Precio:", 2)
# label_precio_val.grid(row=2, column=1, sticky="w", padx=10)


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