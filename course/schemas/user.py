from pydantic import BaseModel

#Creamos una clase para ingresar con un usuario
class User(BaseModel):
    email: str = 'admin@gmail.com'
    password: str = 'admin'