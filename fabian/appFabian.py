from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector

appFabian = FastAPI()

# Configuración de CORS para permitir todas las solicitudes desde cualquier origen
appFabian.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia esto a tu dominio real en producción
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="2292",
    database="info"
)

# Crear conexión a la base de datos SQLite
#conn = sqlite3.connect('datos.db')
#cursor = conn.cursor()

# Modelo de datos para un registro
class Registro(BaseModel):

    id: str
    fecha_diligenciamiento: str
    primer_nombre: str
    segundo_nombre: str
    primer_apellido: str
    segundo_apellido: str
    tipo_documento: str
    numero_documento: str
    nacionalidad: str
    ciudad_nacimiento: str
    fecha_nacimiento: str
    edad: int
    sexo: str
    identidad_genero_preg: str
    identidad_genero: str
    orientacion_sexual: str
    correo_electronico: str
    celular_llamadas: str
    whatsapp: str
    familiar_primer_nombre: str
    familiar_segundo_nombre: str
    familiar_primer_apellido: str
    familiar_segundo_apellido: str
    familiar_tipo_documento: str
    familiar_numero_documento: str
    familiar_correo_electronico: str
    familiar_celular_llamadas: str
    familiar_whatsapp: str
    grupo_etnico: str
    discapacidad: bool
    discapacidad_certificada: bool
    tipo_discapacidad: str
    segun_discapacidad: str
    grupo_atencion_diferencial: str
    grado_escolaridad: str
    ocupacion: str
    profesion: str
    pais_residencia: str
    departamento_residencia: str
    municipio_residencia: str
    zona_ubicacion: str
    zona_resto: str
    corregimiento_nombre: str
    barrio_nombre: str
    vereda_nombre: str
    direccion: str
    estrato_socioeconomico: int
    tipo_vivienda: str
    tenencia_vivienda: str
    servicios_basicos: str
    equipos_tecnologicos: str
    otros_equipos: str
    disponibilidad_formacion: str
    horario_formacion: str
    eje_final_formacion: str
    nivel_formacion: str
    modalidad_bootcamps: str
    requisitos_aceptados: bool
    origen: str
    codigo_departamento: str
    codigo_municipio: str
    campesino: bool
    motivaciones: str
    fecha_exp_cc: str
    puntaje: int
    estado_registro: str
    carga_documento: bool
    aprobacion_documento: bool
    cohorte: str
    segundos_prueba: int
    profesor: str
    fecha_prueba: str
    observaciones: str
    updated_at: str
    created_at: str



   # Ruta para buscar un registro por número de documento

class Usuario(BaseModel):
    username:str
    password:str

class Observaciones(BaseModel):
    numero_documento: str
    observaciones: str

# Ruta para el login de usuarios
@appFabian.post("/login")
def login(usuario: Usuario):
    cursor = mydb.cursor(dictionary=True)
    query = "SELECT * FROM usuarios WHERE username = %s AND password = %s"
    cursor.execute(query, (usuario.username, usuario.password))
    usuario_db = cursor.fetchone()  # Cambio aquí
    cursor.close()
    if usuario_db:  # Cambio aquí
        return {"message": "sesión iniciada"}
    else:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

@appFabian.post('/observaciones')
def agregar_observaciones(observaciones: Observaciones):
    cursor = mydb.cursor()
    query="UPDATE participantes SET observaciones = %s WHERE numero_documento = %s"
    cursor.execute(query,(observaciones.observaciones,observaciones.numero_documento))
    mydb.commit()
    cursor.close()
    return {"message":"Observaciones agregadas correctamente"}



@appFabian.get('/registros/{numero_documento}')
def buscar_registro(numero_documento: str):
    cursor = mydb.cursor(dictionary=True)
    query = "SELECT * FROM participantes WHERE numero_documento = %s"
    cursor.execute(query,(numero_documento,))
    registro=cursor.fetchone()
    cursor.close()
    if registro:
        return registro
    else:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
        return {"numero_documento": numero_documento, "nombre": "Nombre del usuario", "edad": 30}  # Solo un ejemplo, reemplaza con tu lógica


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(appFabian, host="0.0.0.0", port=8000)