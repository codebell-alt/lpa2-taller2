# Imagen base oficial de Python
FROM python:3.12-slim

# Instalar dependencias del sistema para ReportLab
RUN apt-get update && apt-get install -y \
    libfreetype6-dev \
    libjpeg62-turbo-dev \
    libpng-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Crear usuario no-root para seguridad
RUN useradd --create-home --shell /bin/bash app

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivos de requirements primero (mejor cache de Docker)
COPY ./app/requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir --upgrade pip==24.0 && \
    pip install --no-cache-dir -r requirements.txt

# Copiar el resto de la aplicación
COPY ./app .

# Cambiar ownership al usuario app
RUN chown -R app:app /app

# Cambiar a usuario no-root
USER app

# Exponer puerto
EXPOSE 3000

# Variables de entorno para Flask
ENV FLASK_APP=main.py
ENV FLASK_ENV=production

# Comando de arranque
CMD ["flask", "run", "--host=0.0.0.0", "--port=3000"]
