from datetime import date
from fastapi import FastAPI, HTTPException, Response
from bson import ObjectId
from typing import List

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
MONGO_URI = 'mongodb://localhost:27017'

from motor import motor_asyncio
# Ejecutar cliente de DB
client = motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client['Tienda']
pedidos_collection = db['Pedidos']

class Pedidos(BaseModel):
    fecha: date
    total: float
    productos: list


app = FastAPI()

@app.get('/pedidos/')
async def get_pedidos():
    pedidos = await pedidos_collection.find().to_list(length=1)
    for pedido in pedidos:
        pedido['_id'] = str(pedido['_id'])
    return pedidos

@app.get('/user/{id}')
async def get_categoria(id: str):
    if pedidos_collection.find_one({"_id": ObjectId(id)}) is not None:
        pedido = await pedidos_collection.find_one({"_id": ObjectId(id)})
        pedido['_id'] = str(pedido['_id'])
        return pedido

    return HTTPException(status_code=404, detail=f"Error")

@app.post('/pedidos/')
async def create_user(pedido: Pedidos):
    await pedidos_collection.insert_one(pedido.model_dump())
    return {
        'message': 'El usuario se creó'
    }

@app.delete("/delete/pedido/{id}")
async def delete_student(id: str):

    delete_result = await pedidos_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response("Se eliminó")

    raise HTTPException(status_code=404, detail=f"Error")

@app.put("/update/pedido/{id}")
async def update_pedido(id: str, pedido: Pedidos):
    pedido = {
        k: v for k, v in pedido.model_dump(by_alias=True).items() if v is not None
    }
    pedido['fecha'] = str(pedido['fecha'])

    if len(pedido) >= 1:
        update_result = await pedidos_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": pedido},
        )
    
    if update_result is not None:
        update_result['_id'] = str(update_result['_id'])
        return update_result
    
   
    raise HTTPException(status_code=404, detail=f"Error")
    
