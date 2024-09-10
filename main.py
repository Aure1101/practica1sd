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
cat_collection = db['Categorias']
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

@app.get('/categorias')
async def get_categorias():
    categorias = await categorias_collection.find().to_list(None)
    for cat in categorias:
        cat['_id'] = str(cat['_id'])
    
    return categorias

@app.get('/categorias/{cat_id}')
async def get_categoria(cat_id):
    categorias = await categorias_collection.find().to_list(None)
    for cat in categorias:
        if cat_id == str(cat['_id']):
            cat['_id'] = str(cat['_id'])
            return cat
        
    raise HTTPException(status_code=404, message=f'Categoria {cat_id} not found')

@app.post('/categorias')
async def create_categoria(cat: Categorias):
    await categorias_collection.insert_one(cat.dict())
    return {
        'message': 'Categoria added successfully'
    }

@app.put('/categorias/{cat_id}')
async def update_categoria(cat_id, cat: Categorias):
    categorias = await categorias_collection.find().to_list(None)
    for _cat in categorias:
        if str(_cat['_id']) == cat_id:
            await categorias_collection.update_one(_cat, {'$set': cat.dict()})
            return {
                'message': f'Categoria {cat_id} updated Successfully'
            }
        
    raise HTTPException(status_code=404, detail=f'Categoria {cat_id} not found')

@app.delete('/categorias/{cat_id}')
async def delete_categoria(cat_id, cat: Categorias):
    categorias = await categorias_collection.find().to_list(None)
    for _cat in categorias:
        if str(_cat['_id']) == cat_id:
            await categorias_collection.delete_one(_cat, {'$set': cat.dict()})
            return {
                'message': f'Categoria {cat_id} deleted Successfully'
            }
        
    raise HTTPException(status_code=404, detail=f'Categoria {cat_id} not found')