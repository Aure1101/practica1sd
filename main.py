# Crear API y manejar excepciones
from fastapi import FastAPI, HTTPException
#Para crear la estructura de los datos
from pydantic import BaseModel
#Conexion con MongoDB
from motor import motor_asyncio

#from bson.objectid import ObjectId

from datetime import date

# Configurar la coneccion con MongoDB
# Ubicacion de la coneccion de MongoDB
MONGO_URI = 'mongodb://localhost:27017'
# Ejecutar el cliente de bases de datos
client = motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client['sistemas_distribuidos']
users_collection = db['users']


# Objeto para interactuar con la API
app = FastAPI()


class Productos(BaseModel):
    nombre: str
    descripcion: str
    precio: float
    stock: int

class Categorias(BaseModel):
    nombre: str
    descripcion: str

class Pedidos(BaseModel):
    fecha: date
    total: float
    productos: list

class Clientes(BaseModel):
    nombre: str
    apellido: str
    correo_electronico: str