# Usa una imagen base de Python
FROM python:3.8

# Establece el directorio de trabajo en /app
WORKDIR C:/Users/juanf/OneDrive/Escritorio/technical_test/app

# Copia el archivo requirements.txt al directorio de trabajo
COPY requirements.txt .

# Instala las dependencias
RUN pip install -r requirements.txt

# Copia el resto de los archivos al directorio de trabajo
COPY . C:/Users/juanf/OneDrive/Escritorio/technical_test

# Expone el puerto 5000
EXPOSE 5000

# Ejecuta la aplicación cuando se inicie el contenedor
CMD ["python", "C:/Users/juanf/OneDrive/Escritorio/technical_test/app/app.py"]
