# Usa una versión más compatible de Python
FROM python:3.9.0-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo requirements.txt al contenedor y actualiza pip
COPY requirements.txt .
RUN python -m pip install --upgrade pip

# Instala dependencias del sistema y luego las de Python
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copia el resto del código de la aplicación
COPY . .

# Exponer el puerto en el que correrá Flask
EXPOSE 9090

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]
