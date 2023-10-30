import fastapi
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from pydantic import BaseModel

# Establece la conexión a la base de datos MySQL
conn = mysql.connector.connect(
    host="cxmgkzhk95kfgbq4.cbetxkdyhwsb.us-east-1.rds.amazonaws.com",
    user="ozsvheyeiz9rh52q",
    password="b2pg8um97obi3non",
    port="3306",
    database="w9t730hcg8tu8xon"
)

app = fastapi.FastAPI()

origins = [
    "http://localhost:8080",
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
        cursor = conn.cursor()
        cursor.execute('INSERT INTO contactos (email, nombre, telefono) VALUES (%s, %s, %s)',
                       (contacto.email, contacto.nombre, contacto.telefono))
        conn.commit()
        cursor.close()
        return contacto
    except Exception as e:
        return {"error": str(e)}

@app.get("/contactos")
async def obtener_contactos():
    """Obtiene todos los contactos."""
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM contactos;')
        response = []
        for row in cursor:
            contacto = {"email": row[0], "nombre": row[1], "telefono": row[2]}
            response.append(contacto)
        cursor.close()
        return response
    except Exception as e:
        return {"error": str(e)}

@app.get("/contactos/{email}")
async def obtener_contacto(email: str):
    """Obtiene un contacto por su email."""
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM contactos WHERE email = %s', (email,))
        contacto = None
        for row in cursor:
            contacto = {"email": row[0], "nombre": row[1], "telefono": row[2]}
        cursor.close()
        return contacto
    except Exception as e:
        return {"error": str(e)}

@app.put("/contactos/{email}")
async def actualizar_contacto(email: str, contacto: Contacto):
    """Actualiza un contacto."""
    try:
        cursor = conn.cursor()
        cursor.execute('UPDATE contactos SET nombre = %s, telefono = %s WHERE email = %s',
                       (contacto.nombre, contacto.telefono, email))
        conn.commit()
        cursor.close()
        return contacto
    except Exception as e:
        return {"error": str(e)}

@app.delete("/contactos/{email}")
async def eliminar_contacto(email: str):
    """Elimina un contacto."""
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM contactos WHERE email = %s', (email,))
        conn.commit()
        cursor.close()
        return {"mensaje": "Contacto eliminado"}
    except Exception as e:
        return {"error": str(e)}
