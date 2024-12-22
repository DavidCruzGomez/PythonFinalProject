# Usa una imagen base de Python
FROM python:3.10

# Autor del proyecto
LABEL authors="David Cruz Gómez"

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos de tu aplicación al contenedor
COPY . /app

# Instala las dependencias desde el archivo requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto en el que la aplicación va a correr
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["python", "main.py"]