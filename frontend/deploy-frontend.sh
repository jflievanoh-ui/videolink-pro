#!/bin/bash
set -e

echo "🔹 Verificando pnpm..."
if ! command -v pnpm &> /dev/null
then
    echo "pnpm no está instalado. Instalando globalmente..."
    npm install -g pnpm
fi

# Limpiar lockfiles y node_modules antiguos
echo "🔹 Limpiando lockfiles y node_modules..."
rm -rf node_modules
rm -f package-lock.json
rm -f yarn.lock
rm -f pnpm-lock.yaml

# Instalar dependencias principales
echo "🔹 Instalando dependencias esenciales..."
pnpm add react react-dom react-router-dom
pnpm add -D @vitejs/plugin-react-swc vite

# Instalar el resto de dependencias
echo "🔹 Instalando el resto de dependencias del proyecto..."
pnpm install

# Build del proyecto
echo "🔹 Construyendo frontend con Vite..."
pnpm run build

echo "✅ Build completado. La carpeta 'dist' está lista para deploy en Render."
