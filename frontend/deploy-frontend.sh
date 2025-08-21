#!/bin/bash
# Limpieza de lockfiles y node_modules
echo "🔹 Limpiando lockfiles y node_modules..."
rm -rf node_modules
rm -f package-lock.json
rm -f yarn.lock

# Instalar dependencias
echo "🔹 Instalando dependencias..."
npm install  # Cambia por `yarn install` si usas Yarn

# Instalar plugin de React SWC (asegura que esté presente)
echo "🔹 Asegurando @vitejs/plugin-react-swc..."
npm install --save-dev @vitejs/plugin-react-swc

# Build del proyecto
echo "🔹 Construyendo frontend con Vite..."
npm run build  # Cambia por `yarn build` si usas Yarn

echo "✅ Build completado. La carpeta 'dist' está lista para deploy en Render."
