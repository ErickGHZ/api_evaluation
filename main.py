import fastapi
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Establece la conexión a la base de datos MySQL
conn = mysql.connector.connect(
    host="cxmgkzhk95kfgbq4.cbetxkdyhwsb.us-east-1.rds.amazonaws.com",
    user="ozsvheyeiz9rh52q",
    password="myau9muxa9da64f7",    
    port="3306",
    database="w9t730hcg8tu8xon"
)

app = fastapi.FastAPI()

origins = [
    "http://localhost:8080",
    "https://heroku-mysql-frontend-ac0fa64dec05.herokuapp.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)   

class Contacto(BaseModel):
    email: str
    nombre: str
    telefono: str

@app.post("/contactos")
async def crear_contacto(contacto: Contacto):
    """Crea un nuevo contacto."""
    try:
        with conn.cursor() as cursor:
            cursor.execute('INSERT INTO contactos (email, nombre, telefono) VALUES (%s, %s, %s)',
                           (contacto.email, contacto.nombre, contacto.telefono))
        conn.commit()
        return contacto
    except mysql.connector.Error as e:
        return {"error": str(e)}

@app.get("/contactos")
async def obtener_contactos():
    """Obtiene todos los contactos."""
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM contactos;')
            response = [{"email": row[0], "nombre": row[1], "telefono": row[2]} for row in cursor]
        return response
    except mysql.connector.Error as e:
        return {"error": str(e)}

@app.get("/contactos/{email}")
async def obtener_contacto(email: str):
    """Obtiene un contacto por su email."""
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM contactos WHERE email = %s', (email,))
            contacto = [{"email": row[0], "nombre": row[1], "telefono": row[2]} for row in cursor]
        return contacto[0] if contacto else {"mensaje": "Contacto no encontrado"}
    except mysql.connector.Error as e:
        return {"error": str(e)}

@app.put("/contactos/{email}")
async def actualizar_contacto(email: str, contacto: Contacto):
    """Actualiza un contacto."""
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM contactos WHERE email = %s', (email,))
            if cursor.fetchone() is None:
                return {"error": "El contacto no existe"}
            
            cursor.execute('UPDATE contactos SET nombre = %s, telefono = %s WHERE email = %s',
                           (contacto.nombre, contacto.telefono, email))
        conn.commit()
        return contacto
    except mysql.connector.Error as e:
        return {"error": str(e)}

@app.delete("/contactos/{email}")
async def eliminar_contacto(email: str):
    """Elimina un contacto."""
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM contactos WHERE email = %s', (email,))
            if cursor.fetchone() is None:
                return {"error": "El contacto no existe"}
            
            cursor.execute('DELETE FROM contactos WHERE email = %s', (email,))
        conn.commit()
        return {"mensaje": "Contacto eliminado"}
    except mysql.connector.Error as e:
        return {"error": str(e)}
