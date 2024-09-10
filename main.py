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
clientes_collection = db['Clientes']


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

@app.get('/clientes/')
async def get_clientes():
    cl = dict()
    clientes = await clientes_collection.find().to_list(None)

    for i, cliente in enumerate(clientes):
        cl[i] = dict()
        cl[i]["nombre"] = cliente["nombre"]
        cl[i]["apellido"] = cliente["apellido"]
        cl[i]["correo_electronico"] = cliente["correo_electronico"]
    return cl

@app.get('/clientes/')
async def get_cliente_id():
    clientes = await clientes_collection.find().to_list(None)
    for cliente in clientes:
        clientes=['_id'] = str(cliente['_id'])

@app.post('/clientes/')
async def create_cliente(cliente: Clientes):
    await clientes_collection.insert_one(cliente.dict())
    return{
        'message': "Cliente added succesfully"
    }

@app.put('/clientes/{cli_id}')
async def update_cliente(cli_id, cli: Clientes):
    clientes = await clientes_collection.find().to_list(None)
    for _cli in clientes:
        if str(_cli['_id']) == cli_id:
            await clientes_collection.update_one(_cli, {'$set': cli.dict()})
            return{
                'message': f'Cliente {cli_id} updated successfully'
            }

@app.delete('/clientes/{cli_id}')
async def delete_cliente(cli_id, cli: Clientes):
    clientes = await clientes_collection.find().to_list(None)
    for _cli in clientes:
        if str(_cli['_id']) == cli_id:
            await clientes_collection.delete_one(_cli, {'$set': cli.dict()})
            return {
                'message': 'The client has been eliminated'
            }
        raise HTTPException(status_code=404, detail=f'Client: {cli_id} not found')