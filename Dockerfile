# Usa una imagen de Python como base
FROM python:3.10

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python3 manage.py collectstatic --noinput

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
