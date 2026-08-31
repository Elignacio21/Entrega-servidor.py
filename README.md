Explicación de diferencia :
GET : Es solo de lectura, se utiliza para leer los datos, sin que genere alguna modificación, solo consulta.
POST : Es para crear datos en el servidor
PATCH : Es para modificar datos parciales, ósea algunos atributos, no en su totalidad.
DELETE : Es para eliminar un recurso en especifico

Porque POST no es idempotente : No lo es porque puede crear recursos repetidos, ósea que si lo fuera cada vez que usas post se crearía 1 archivo y ya
