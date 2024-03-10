from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Text, Optional
from datetime import datetime
from uuid import uuid4 as uuid
from fastapi.middleware.cors import CORSMiddleware

app =FastAPI()

# Permitir solicitudes desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

posts=[]

#postmodel
class Post(BaseModel):
    id: Optional[str]
    titulo: Text #ingresado desde typing 
    autor: Optional[str]
    created_at: datetime = datetime.now()
    genero: Optional[str]

@app.get('/posts')
def _posts ():
    return posts

#GUARDAR INFORMACION
"""
ingresan: los datos de la estructura
retorna: los datos asignados con ID realizada en el UUID
"""
@app.post('/posts')#se utiliza para guardar los elementos en el arreglo
def guardar_post(post: Post):
    #if post.id :# en caso de que el elemento no contenga informacion agregrá un uuid aleatorio
    post.id=str(uuid())    
    #print("2001")
    posts.append(post.dict())#agrega un elemento al final 
    return posts[-1]

#VERFICAR INFORMACION DEL UUID
"""
ingresa=una ID para realizar un busqueda en el arreglo
retorna=el ID si se encontró; sino envía un error 404
"""
@app.post('/posts/{post_id}')#para verificar cualquier ID
def comprobar_post(post_id: str):
    for post in posts:
        #print("ID del post:", post["id"])  # Imprimir el ID del post
        #print("Post ID proporcionado:", post_id) 
        if post["id"] == post_id:
                return post
    raise HTTPException(status_code=404,detail="post not found")

#ELIMINAR ELEMENTO
"""
ingresa=una ID del elemento a eliminar
retorna = post eliminado
"""
@app.delete("/posts/{post_id}")#eliminar ID seleccionada
def eliminar_post(post_id: str):
    for index, post in enumerate(posts):
        if post["id"]==post_id:
            posts.pop(index)
        return {"messagge":"post eliminado"}
    raise HTTPException(status_code=404,detail=" post not found")

#ACTUALIZAR ALGUN ELEMENTO CON BASE AL ID ENOCNTRADO
@app.put('/posts/{post_id}')
def actualizar_post(post_id: str,updatedPost: Post):
    for post in posts:
        if post["id"] == post_id:
            post["titulo"]= updatedPost.titulo
            post["autor"]= updatedPost.autor
            #post["created_at"]= updatedPost.created_at
            post["genero"]= updatedPost.genero
            return {"message":"post update"}
    raise HTTPException(status_code=404, detail="post not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)