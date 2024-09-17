# Crear API y manejar excepciones
from fastapi import FastAPI, HTTPException  # Importa FastAPI y HTTPException para crear la API y manejar errores

# Para crear la estructura de los datos
from pydantic import BaseModel  # Pydantic permite crear modelos de datos para validación

# Conexión con MongoDB
from motor import motor_asyncio  # Motor proporciona una conexión asíncrona a MongoDB

#from bson.objectid import ObjectId  # Comentado: para manejar ObjectId en MongoDB

from datetime import date  # Para manejar fechas en el modelo de pedidos

# Configurar la conexión con MongoDB
MONGO_URI = 'mongodb://localhost:27017'  # Define la URI para conectarse a MongoDB
client = motor_asyncio.AsyncIOMotorClient(MONGO_URI)  # Crea el cliente de MongoDB
db = client['sistemas_distribuidos']  # Selecciona la base de datos 'sistemas_distribuidos'

# Colecciones de la base de datos
cat_collection = db['Categorias']  # Colección de categorías
users_collection = db['users']  # Colección de usuarios
clientes_collection = db['Clientes']  # Colección de clientes
productos_collection = db['Productos']  # Colección de productos
pedidos_collection = db['Pedidos']  # Colección de pedidos

# Objeto para interactuar con la API
app = FastAPI()  # Inicializa la API usando FastAPI

# Modelos de datos utilizando Pydantic para validar la estructura de entrada
class Productos(BaseModel):  # Modelo para los productos
    nombre: str
    descripcion: str
    precio: float
    stock: int

class Categorias(BaseModel):  # Modelo para las categorías
    nombre: str
    descripcion: str

class Pedidos(BaseModel):  # Modelo para los pedidos
    fecha: date
    total: float
    productos: list

class Clientes(BaseModel):  # Modelo para los clientes
    nombre: str
    apellido: str
    correo_electronico: str

# Rutas de la API

# Obtener todos los clientes
@app.get('/clientes/')
async def get_clientes():
    cl = dict()  # Crear un diccionario para almacenar los clientes
    clientes = await clientes_collection.find().to_list(None)  # Obtener la lista de clientes

    for i, cliente in enumerate(clientes):  # Iterar sobre los clientes
        cl[i] = dict()  # Crear un diccionario para cada cliente
        cl[i]["nombre"] = cliente["nombre"]  # Guardar nombre
        cl[i]["apellido"] = cliente["apellido"]  # Guardar apellido
        cl[i]["correo_electronico"] = cliente["correo_electronico"]  # Guardar correo electrónico
    return cl  # Retorna la lista de clientes

# Obtener cliente por ID
@app.get('/clientes/')
async def get_cliente_id():
    clientes = await clientes_collection.find().to_list(None)  # Obtener todos los clientes
    for cliente in clientes:
        clientes['_id'] = str(cliente['_id'])  # Convertir el _id a string

# Crear un nuevo cliente
@app.post('/clientes/')
async def create_cliente(cliente: Clientes):
    await clientes_collection.insert_one(cliente.dict())  # Insertar el cliente en la base de datos
    return{
        'message': "Cliente added successfully"  # Mensaje de éxito
    }

# Actualizar cliente por ID
@app.put('/clientes/{cli_id}')
async def update_cliente(cli_id, cli: Clientes):
    clientes = await clientes_collection.find().to_list(None)  # Obtener todos los clientes
    for _cli in clientes:
        if str(_cli['_id']) == cli_id:  # Verificar si coincide el ID
            await clientes_collection.update_one(_cli, {'$set': cli.dict()})  # Actualizar el cliente
            return{
                'message': f'Cliente {cli_id} updated successfully'  # Mensaje de éxito
            }

# Eliminar cliente por ID
@app.delete('/clientes/{cli_id}')
async def delete_cliente(cli_id, cli: Clientes):
    clientes = await clientes_collection.find().to_list(None)  # Obtener todos los clientes
    for _cli in clientes:
        if str(_cli['_id']) == cli_id:  # Verificar si coincide el ID
            await clientes_collection.delete_one(_cli, {'$set': cli.dict()})  # Eliminar el cliente
            return {
                'message': 'The client has been eliminated'  # Mensaje de éxito
            }
        raise HTTPException(status_code=404, detail=f'Client: {cli_id} not found')  # Error si no se encuentra

# Obtener todas las categorías
@app.get('/categorias')
async def get_categorias():
    categorias = await categorias_collection.find().to_list(None)  # Obtener todas las categorías
    for cat in categorias:
        cat['_id'] = str(cat['_id'])  # Convertir _id a string
    
    return categorias  # Retorna las categorías

# Obtener categoría por ID
@app.get('/categorias/{cat_id}')
async def get_categoria(cat_id):
    categorias = await categorias_collection.find().to_list(None)  # Obtener todas las categorías
    for cat in categorias:
        if cat_id == str(cat['_id']):  # Verificar si coincide el ID
            cat['_id'] = str(cat['_id'])  # Convertir _id a string
            return cat
        
    raise HTTPException(status_code=404, message=f'Categoria {cat_id} not found')  # Error si no se encuentra

# Crear nueva categoría
@app.post('/categorias')
async def create_categoria(cat: Categorias):
    await categorias_collection.insert_one(cat.dict())  # Insertar la categoría
    return {
        'message': 'Categoria added successfully'  # Mensaje de éxito
    }

# Actualizar categoría por ID
@app.put('/categorias/{cat_id}')
async def update_categoria(cat_id, cat: Categorias):
    categorias = await categorias_collection.find().to_list(None)  # Obtener todas las categorías
    for _cat in categorias:
        if str(_cat['_id']) == cat_id:  # Verificar si coincide el ID
            await categorias_collection.update_one(_cat, {'$set': cat.dict()})  # Actualizar categoría
            return {
                'message': f'Categoria {cat_id} updated Successfully'  # Mensaje de éxito
            }
        
    raise HTTPException(status_code=404, detail=f'Categoria {cat_id} not found')  # Error si no se encuentra

# Eliminar categoría por ID
@app.delete('/categorias/{cat_id}')
async def delete_categoria(cat_id, cat: Categorias):
    categorias = await categorias_collection.find().to_list(None)  # Obtener todas las categorías
    for _cat in categorias:
        if str(_cat['_id']) == cat_id:  # Verificar si coincide el ID
            await categorias_collection.delete_one(_cat, {'$set': cat.dict()})  # Eliminar categoría
            return {
                'message': f'Categoria {cat_id} deleted Successfully'  # Mensaje de éxito
            }
        
    raise HTTPException(status_code=404, detail=f'Categoria {cat_id} not found')  # Error si no se encuentra

# Definición de una ruta GET para obtener todos los productos
@app.get('/productos/')
async def get_product_id():
    # Obtener todos los productos de la colección 'productos_collection'
    productos = await productos_collection.find().to_list(None)
    
    # Convertir los IDs de los productos a cadenas de texto
    for producto in productos:
        producto['_id'] = str(producto['_id'])

    # Retornar la lista de productos
    return productos

# Definición de una ruta GET para obtener un producto específico por su ID
@app.get('/productos/{prod_id}')
async def get_categoria(prod_id):
    # Obtener todos los productos de la colección
    productos = await productos_collection.find().to_list(None)
    
    # Buscar el producto con el ID especificado
    for prod in productos:
        if prod_id == str(prod['_id']):
            prod['_id'] = str(prod['_id'])
            return prod
    
    # Lanzar una excepción HTTP 404 si el producto no se encuentra
    raise HTTPException(status_code=404, message=f'Producto {prod_id} not found')

# Definición de una ruta POST para crear un nuevo producto
@app.post('/productos/')
async def create_product(pro: Productos):
    # Insertar el nuevo producto en la base de datos
    await productos_collection.insert_one(pro.dict())
    
    # Retornar un mensaje de éxito
    return {
        'message': 'El producto se ha creado'
    }

# Definición de una ruta PUT para actualizar un producto existente
@app.put('/productos/{pro_id}')
async def update_Producto(pro_id, pro: Productos):
    # Obtener todos los productos de la colección
    productos = await productos_collection.find().to_list(None)
    
    # Buscar el producto con el ID especificado
    for _pro in productos:
        if str(_pro['_id']) == pro_id:
            # Actualizar el producto en la base de datos
            await productos_collection.update_one(_pro, {'$set': pro.dict()})
            return {
                'message': f'Producto {pro_id} actualizado con éxito'
            }

# Definición de una ruta DELETE para eliminar un producto
@app.delete('/productos/{pro_id}')
async def delete_productos(pro_id, pro: Productos):
    # Obtener todos los productos de la colección
    productos = await productos_collection.find().to_list(None)
    
    # Buscar el producto con el ID especificado
    for _pro in productos:
        if str(_pro['_id']) == pro_id:
            # Eliminar el producto de la base de datos
            await productos_collection.delete_one(pro, {'$set': pro.dict()})
            return {
                'message': f'Producto {pro_id} eliminado'
            }

    # Lanzar una excepción HTTP 404 si el producto no se encuentra
    raise HTTPException(status_code=404, detail=f'Producto {pro_id} not found')

# Definición de una ruta GET para obtener pedidos
@app.get('/pedidos/')
async def get_pedidos():
    # Obtener una lista de pedidos de la colección 'pedidos_collection'
    pedidos = await pedidos_collection.find().to_list(length=1)
    
    # Convertir los IDs de los pedidos a cadenas de texto
    for pedido in pedidos:
        pedido['_id'] = str(pedido['_id'])
    
    # Retornar la lista de pedidos
    return pedidos

# Definición de una ruta GET para obtener un pedido específico por su ID
@app.get('/user/{id}')
async def get_categoria(id: str):
    # Verificar si existe un pedido con el ID especificado
    if pedidos_collection.find_one({"_id": ObjectId(id)}) is not None:
        pedido = await pedidos_collection.find_one({"_id": ObjectId(id)})
        pedido['_id'] = str(pedido['_id'])
        return pedido

    # Retornar un error HTTP 404 si no se encuentra el pedido
    return HTTPException(status_code=404, detail=f"Error")

# Definición de una ruta POST para crear un nuevo pedido
@app.post('/pedidos/')
async def create_user(pedido: Pedidos):
    # Insertar el nuevo pedido en la base de datos
    await pedidos_collection.insert_one(pedido.model_dump())
    
    # Retornar un mensaje de éxito
    return {
        'message': 'El pedido se ha creado'
    }

# Definición de una ruta DELETE para eliminar un pedido por su ID
@app.delete("/delete/pedido/{id}")
async def delete_student(id: str):
    # Intentar eliminar el pedido con el ID especificado
    delete_result = await pedidos_collection.delete_one({"_id": ObjectId(id)})

    # Verificar si el pedido fue eliminado con éxito
    if delete_result.deleted_count == 1:
        return Response("Se eliminó")

    # Lanzar una excepción HTTP 404 si el pedido no se encuentra
    raise HTTPException(status_code=404, detail=f"Error")

# Definición de una ruta PUT para actualizar un pedido por su ID
@app.put("/update/pedido/{id}")
async def update_pedido(id: str, pedido: Pedidos):
    # Preparar los datos del pedido para la actualización
    pedido = {
        k: v for k, v in pedido.model_dump(by_alias=True).items() if v is not None
    }
    pedido['fecha'] = str(pedido['fecha'])

    # Actualizar el pedido si se proporcionaron campos válidos
    if len(pedido) >= 1:
        update_result = await pedidos_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": pedido},
        )

    # Si el pedido se actualizó con éxito, retornar los datos actualizados
    if update_result is not None:
        update_result['_id'] = str(update_result['_id'])
        return update_result

    # Lanzar una excepción HTTP 404 si no se encuentra el pedido
    raise HTTPException(status_code=404, detail=f"Error")
