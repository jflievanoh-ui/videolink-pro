# Imagen base ligera con Python 3.11
FROM python:3.11-slim

# Setea el directorio de trabajo
WORKDIR /app

# Copiar requirements primero para aprovechar cache
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código al contenedor
COPY . .

# Render asigna automáticamente $PORT, lo respetamos
ENV PORT=10000

# Arrancar FastAPI con Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
