#!/bin/bash

# 1. Instalar PyInstaller y dependencias del sistema
echo "🔧 Instalando dependencias del sistema..."
sudo apt update
sudo apt install -y python3-pip python3-tk python3-pil.imagetk

# 2. Instalar PyInstaller si no está instalado
if ! command -v pyinstaller &> /dev/null; then
    echo "🚀 Instalando PyInstaller..."
    pip3 install pyinstaller
else
    echo "✅ PyInstaller ya está instalado."
fi

# 3. Empaquetar el ejecutable
echo "📦 Generando ejecutable..."
pyinstaller --onefile --noconsole \
  --add-data "logo.png:." \
  --add-data "lupa.png:." \
  index.py

echo "✅ Ejecutable creado en: dist/app"
