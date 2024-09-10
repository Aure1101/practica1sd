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
productos_collection = db['Productos']


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

@app.get("/productos/")
async def get_product(pro_id):
    
    resultados = dict() # Tener todos los usuarios
    # Obtener de manera asincrona todos los usuarios
    productos = await productos_collection.find().to_list(None)

    # Iterar todos los elementos de la lista users
    for i, productos in enumerate(productos):
        # Diccionario por cada usuario
        resultados[i] = dict()
        resultados[i]["nombre"] = productos["nombre"]
        resultados[i]["descripcion"] = productos["descripcion"]
        resultados[i]["precio"] = productos["precio"]
        resultados[i]["stock"] = productos["stock"]

    return resultados

@app.get('/productos/')
async def get_product_id():
    productos = await productos_collection.find().tolist(None)
    for productos in Productos:
        productos=['_id']= str(productos['_id'])
    return productos

@app.post('/productos/')
async def create_product(pro:Productos):
    await productos_collection.insert_one(pro.dict())
    return {
        'message':'El usuario se a creado'
        }

@app.put('/productos/{pro_id}')
async def update_Producto(pro_id, pro: Productos):
    productos = await productos_collection.find().to_list(None)
    for _pro in productos:
        if str(_pro['_id'])== pro_id:
            await productos_collection.update_one(_pro, {'$set':pro.dict()})
            return {
                'message': f'Producto {pro_id} update Successfully'
            }
        
@app.delete('/productos/{pro_id}')
async def delate_productos(pro_id, pro:Productos):
    Productos= await productos_collection.find().to_list(None)
    for  _pro in Productos:
      if str(_pro['_id'])==pro_id:
       await productos_collection.delate_one(pro, {'$set': pro.dict()})
       return {
           'mesage': f'Producto{pro_id}'
       }

    raise HTTPException(status_code=404, detail=f'Producto {pro_id} not found')