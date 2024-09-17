FROM python:3.12-slim-bookworm

# Instalacion de paquetes necesarios para UV
RUN apt-get update && apt-get install -y curl ca-certificates

#Descargar UV en el contenedor
ADD https://astral.sh/uv/install.sh /uv-installer.sh

#Ejecutar instalador y Eliinar Archivos Innecesarios
RUN sh /uv-installer.sh && rm /uv-installer.sh

#Agregar uv a comandos path
ENV PATH="/root/cargo/bin:$PATH"

#Copiar la aplicacion de fastapi al container
ADD . /app


RUN uv sync --frozen

RUN uv run fastapi dev main.py