from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

#NOTAS
"""
Quiza sea necesario COMENTAR la linea 41 de app.py
post.id=str(uui())
"""

#PRUEBAS PARA AGREGAR
def test_guardar_post():
    # Datos de prueba para enviar en la solicitud POST
    data = {
        "id":"string",
        "titulo": "Nuevo libro",
        "autor": "Autor",
        "genero": "Ficción"
        }
    
    # Enviar solicitud POST a /posts
    response = client.post("/posts", json=data)
    
    # Verificar el código de estado de la respuesta
    #assert response.status_code == 200
    print("2002")
    
    # Verificar que la respuesta contiene los datos esperados
    assert response.json()["id"] == "string"
    assert response.json()["titulo"] == "Nuevo libro"
    assert response.json()["autor"] == "Autor"
    assert response.json()["genero"] == "Ficción"
    print("2003")

def test_guardar_post2():
    data = {
        "id": "string2",
        "titulo": "Otro libro",
        "autor": "Otro Autor",
        "genero": "Fantasía"
    }

    # Enviar solicitud POST a /posts
    response = client.post("/posts", json=data)
    
    # Verificar el código de estado de la respuesta
    assert response.status_code == 200
    
    # Verificar que la respuesta contiene los datos esperados
    assert response.json()["id"] == "string2"
    assert response.json()["titulo"] == "Otro libro"
    assert response.json()["autor"] == "Otro Autor"
    assert response.json()["genero"] == "Terror"

#PRUEBA PARA ELIMINAR
def test_eliminar_post():
    # Agregar un libro para luego eliminarlo
    data = {
        "id": "1234",
        "titulo": "Libro a eliminar",
        "autor": "Autor a eliminar",
        "genero": "Género a eliminar"
    }
    # Agregar el libro
    response = client.post("/posts", json=data)
    assert response.status_code == 200

    # Obtener el ID del libro agregado
    id = response.json()["id"]

    # Enviar solicitud DELETE para eliminar el libro
    response = client.delete(f"/posts/{id}")

    # Verificar que el libro haya sido eliminado correctamente
    assert response.status_code == 200

#COMPROBACION DE EXISTENCIA

def test_comprobar_post_existente():
    # Agregar un post para luego verificar su existencia
    data = {
        "id": "post_existente",
        "titulo": "Título del post",
        "autor": "Autor del post",
        "genero": "Género del post"
    }
    # Agregar el post
    client.post("/posts", json=data)

    # Enviar solicitud GET para verificar el post
    response = client.post("/posts")
    
    # Verificar que se recibe un código de estado 200 y los datos del post son correctos
    assert response.status_code == 200
    assert response.json()["id"] == "post_existente"
    assert response.json()["titulo"] == "Título del post"
    assert response.json()["autor"] == "Autor del post"
    assert response.json()["genero"] == "Género del post"

def test_comprobar_post_no_existente():


    # Enviar solicitud GET para verificar un post que no existe
    response = client.post("/posts/post_no_existente")
    
    # Verificar que se recibe un código de estado 404 y el mensaje de error apropiado
    assert response.status_code == 404
    assert response.json()["detail"] == "post no se encontró"

#COMPROBACION DE ACTUALIZACION

def test_actualizar_post_existente():
    # Agregar un post para luego actualizarlo
    data = {
        "id": "post_para_actualizar",
        "titulo": "Título original",
        "autor": "Autor original",
        "genero": "Género original"
    }
    # Agregar el post
    client.post("/posts", json=data)

    # Datos actualizados para el post
    data_actualizado = {
        "id": "post_para_actualizar",
        "titulo": "Título actualizado",
        "autor": "Autor actualizado",
        "genero": "Género actualizado"
    }

    # Enviar solicitud PUT para actualizar el post
    response = client.put("/posts/post_para_actualizar", json=data_actualizado)
    
    # Verificar que se recibe un código de estado 200 y el mensaje de éxito
    assert response.status_code == 200
    assert response.json()["message"] == "post update"

def test_actualizar_post_no_existente():
    # Datos actualizados para el post
    data_actualizado = {
        "titulo": "Título actualizado",
        "autor": "Autor actualizado",
        "genero": "Género actualizado"
    }

    # Enviar solicitud PUT para actualizar un post que no existe
    response = client.put("/posts/post_no_existente", json=data_actualizado)
    
    # Verificar que se recibe un código de estado 404 y el mensaje de error apropiado
    assert response.status_code == 404
    assert response.json()["detail"] == "post not found"




