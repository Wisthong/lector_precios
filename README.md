# Lector de Precios - Distribuidora Universal
Una aplicación para consultar precios de productos mediante código de barras.

## Tabla de contenidos
1. [Descripción](#descripción)
2. [Requisitos](#requisitos)
3. [Instalación](#instalación)
4. [Uso](#uso)
5. [Contribuciones](#contribuciones)
6. [Licencia](#licencia)

## Descripción
Este proyecto es una herramienta de consulta de precios que permite buscar productos a partir de un código de barras. Los datos de los productos se leen desde un archivo en red y se muestran en una interfaz gráfica.

## Requisitos
- Python 3.x
- Tkinter (por lo general, ya está instalado con Python)
- Pillow (para manejar imágenes)
- Acceso a un archivo de productos (`CHECKER1.TXT`), el cual debe estar en un servidor de red.

Puedes instalar las dependencias con:
```bash
pip install -r requirements.txt
