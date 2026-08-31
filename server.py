import wsgiref.simple_server
import json


tareas = {}
prox_elemento = 1


def server(environ, start_response):
    global prox_elemento
    
    metodo = environ['REQUEST_METHOD']
    ruta = environ['PATH_INFO']
    
    
    if metodo == 'GET' and ruta == '/tasks':
        status = '200 OK'
        headers = [('Content-Type', 'application/json')]
        start_response(status, headers)
        lista_tareas = list(tareas.values())
        json_respuesta = json.dumps(lista_tareas)
        return [json_respuesta.encode('utf-8')]

    
    elif metodo == 'POST' and ruta == '/tasks':
        longitud = int(environ.get('CONTENT_LENGTH', 0))
        cuerpo = environ['wsgi.input'].read(longitud)
        
        datos = json.loads(cuerpo) if cuerpo else {}
        
        nueva_tarea = {
            "id": prox_elemento,
            "title": datos.get("title", ""),
            "done": datos.get("done", False)
        }
        
        tareas[prox_elemento] = nueva_tarea
        prox_elemento += 1
        
        status = '201 Created'
        headers = [('Content-Type', 'application/json')]
        start_response(status, headers)
        return [json.dumps(nueva_tarea).encode('utf-8')]

    elif ruta.startswith('/tasks/'):
        id_str = ruta.split('/')[-1]
        
        if not id_str.isdigit():
            status = '404 Not Found'
            headers = [('Content-Type', 'application/json')]
            start_response(status, headers)
            error = {"error": "El ID debe ser un numero entero"}
            return [json.dumps(error).encode('utf-8')]
        
        id_tarea = int(id_str)
        
        if id_tarea not in tareas:
            status = '404 Not Found'
            headers = [('Content-Type', 'application/json')]
            start_response(status, headers)
            error = {"error": "Tarea no encontrada"}
            return [json.dumps(error).encode('utf-8')]
            
        if metodo == 'GET':
            status = '200 OK'
            headers = [('Content-Type', 'application/json')]
            start_response(status, headers)
            tarea_encontrada = tareas[id_tarea]
            json_respuesta = json.dumps(tarea_encontrada)
            return [json_respuesta.encode('utf-8')]
            
        elif metodo == 'PATCH':
            longitud = int(environ.get('CONTENT_LENGTH', 0))
            cuerpo = environ['wsgi.input'].read(longitud)
            if cuerpo:
                datos_parciales = json.loads(cuerpo)
                for clave, valor in datos_parciales.items():
                    if clave in tareas[id_tarea]:
                        tareas[id_tarea][clave] = valor
            
            status = '200 OK'
            headers = [('Content-Type', 'application/json')]
            start_response(status, headers)
            json_respuesta = json.dumps(tareas[id_tarea])
            return [json_respuesta.encode('utf-8')]

        elif metodo == 'DELETE':
            del tareas[id_tarea]
            status = '200 OK'
            headers = [('Content-Type', 'application/json')]
            start_response(status, headers)
            json_respuesta = json.dumps({"mensaje": "Tarea eliminada correctamente"})
            return [json_respuesta.encode('utf-8')]
        else:
            status = '405 Method Not Allowed'
            headers = [('Content-Type', 'application/json')]
            start_response(status, headers)
            error = {"error": "Método no permitido para esta ruta"}
            return [json.dumps(error).encode('utf-8')]
            
    
    else:
        status = '404 Not Found'
        headers = [('Content-Type', 'application/json')]
        start_response(status, headers)
        error = {"error": "Ruta no encontrada o metodo incorrecto"}
        json_error = json.dumps(error)
        return [json_error.encode('utf-8')]


if __name__ == '__main__':
    puerto = 9292
    print(f"Servidor escuchando en http://localhost:{puerto} ...")
    wsgiref.simple_server.make_server('', puerto, server).serve_forever()[cite: 1]
