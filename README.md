# Practica1sd

## Implementacion de la API
Operaciones de la API:
- GET:
Este método se utiliza para recuperar información de un recurso sin modificarlo, puede realizar la misma solicitud varias veces y no cambia el estado del recurso.

- POST:
Este método envía datos al servidor para crear un nuevo recurso, hacer la misma solicitud varias veces podría crear múltiples recursos.

- PUT:
Se para actualizar un recurso completo y si el recurso no existe se puede crear uno nuevo.

- DELETE:
Elimina un recurso identificado por una clave y hacer la misma solicitud varias veces tendrá el mismo resultado.

## Colecciones
Las colecciones en nuestra base de datos incluyen:
- Productos
- Categorías
- Pedidos
- Clientes
 
De manera mas descriptiva estas incluyen:

Productos
- id (ObjectId): identificador ´unico del producto
- nombre (String): nombre del producto
- descripci´on (String): descripci´on del producto
- precio (Number): precio del producto
- stock (Number): cantidad de unidades en stock

Categorias
- id (ObjectId): identificador unico de la categorıa
- nombre (String): nombre de la categorıa
- descripci´on (String): descripcion de la categorıa

Pedidos
- id (ObjectId): identificador ´unico del pedido
- fecha (Date): fecha en que se realiz´o el pedido
- total (Number): total del pedido
- productos (Array): arreglo de productos incluidos en el pedido

Clientes
- id (ObjectId): identificador ´unico del cliente
- nombre (String): nombre del cliente
- apellido (String): apellido del cliente
- correo electr´onico (String): correo electr´onico del cliente

  ![image](https://github.com/user-attachments/assets/5245ca15-ba54-4c9f-a3dd-ec8671d3d5f2)

