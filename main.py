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
clientes_collection = db['Clientes']
productos_collection = db['Productos']
pedidos_collection = db['Pedidos']

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
        clientes['_id'] = str(cliente['_id'])

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

@app.get('/productos/')
async def get_product_id():
    productos = await productos_collection.find().tolist(None)
    for producto in productos:
        producto['_id']= str(producto['_id'])

    return productos

@app.get('/productos/{prod_id}')
async def get_categoria(prod_id):
    productos = await productos_collection.find().tolist(None)
    for prod in productos:
        if prod_id == str(prod['_id']):
            prod['_id'] = str(prod['_id'])
            return prod
        
    raise HTTPException(status_code=404, message=f'Producto {prod_id} not found')


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
    productos= await productos_collection.find().to_list(None)
    for  _pro in productos:
      if str(_pro['_id'])==pro_id:
       await productos_collection.delate_one(pro, {'$set': pro.dict()})
       return {
           'mesage': f'Producto{pro_id}'
       }

    raise HTTPException(status_code=404, detail=f'Producto {pro_id} not found')


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
    
