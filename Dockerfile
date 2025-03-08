# Dockerfile for Django with Python 3.10
FROM python:3.10-slim

# Instalar dependencias del sistema necesarias para psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /usr/src/app

# Copy and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Evita que Python genere archivos de bytecode (.pyc) en el contenedor.
ENV PYTHONDONTWRITEBYTECODE 1
# Desactiva el buffer en la salida de Python, asegurando que los logs se envíen directamente al terminal sin retrasos
ENV PYTHONUNBUFFERED 1

# Expose port 8000
EXPOSE 8000

# Run server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]