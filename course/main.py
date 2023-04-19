#Importamos modulos
from fastapi import FastAPI #Modulo principal para una API en Python
from fastapi import Body    #Modulo para que un request no sea query
from fastapi import HTTPException
from fastapi import Path, Query, Request,Depends
from fastapi.responses import HTMLResponse  #Modulo que nos deja hacer codigo HTML
from fastapi.responses import JSONResponse  #Modulo que devuelve en formato JSON
from fastapi.security import HTTPBearer
from pydantic import BaseModel  #Modulo que con una clase crea un modelo con las variables
from pydantic import Field      #Rangos de campos en clases
from typing import Optional     #Para que un request sea opcional
from typing import List         #Lista
from jwt_manager import create_token #Crear token jwt
from jwt_manager import validate_token
from config.database import Motor, Sesion, Base
from models.movie import Movie as MovieModel

app = FastAPI()                     #Llamamos una API como app
app.title = "Mi primer FastAPI"     #Titulo del API
app.version = "29.07.22"            #Ponemos version de manera manual

Base.metadata.create_all(bind=Motor)

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != 'admin@gmail.com':
            raise HTTPException(status_code=403,detail='Credenciales son invalidas')

#Creamos una clase para ingresar con un usuario
class User(BaseModel):
    email: str
    password: str

#Creamos una clase como modelo de atributos de una pelicula
class Movie(BaseModel):
    title: str = Field(min_length=5,max_length=15)
    overview: str
    year: int = Field(le=2024)
    rating: float = Field(le=10)
    category: str

#Clase dentro de la otra clase con el esquema de datos 
    class Config:
        schema_extra={
            'example': {
                'title':'Movie',
                'overview':'Overview',
                'year':0,
                'rating':0.0,
                'category':'Category'
            }
        }

#Lista de diccionarios con dos peliculas y sus atributos
movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': 2009,
        'rating': 7.8,
        'category': 'Action'    
    },
    {
        'id': 2,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': 2009,
        'rating': 7.8,
        'category': 'Action'    
    }
]


#Get que retorna un codigo HTML gracias a HTMLResponse
@app.get('/', tags=['Home'], status_code=200)
def message():
    return HTMLResponse('<h1 style=color:teal>Hello world</h1>')

@app.post('/login', tags=['Authentication'])
def login(user: User):
    if user.email == 'admin@gmail.com' and user.password == 'admin':
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)
    else:
        return JSONResponse(status_code=404,content={'message':'El usuario es invalido'})

#Get que retorna la lista de diccionarios
@app.get('/movies',tags=['Movies'], response_model=List[Movie], status_code=200,dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    return JSONResponse(status_code=200, content=movies)

#Get que retorna un diccionario de la lista dependiendo de su id
@app.get('/movies/{id}', tags=['Movies'], response_model=Movie,status_code=200)
def get_id(id: int = Path(ge=1,le=2000)) -> Movie:
    for item in movies:
        if item['id'] == id:
            return JSONResponse(content=item)
    return JSONResponse(status_code=404, content={'message':'La pelicula no existe'})

#Get que retorna una lista de diccionarios con esa categoria
@app.get('/movies/',tags=['Movies'],response_model=List[Movie],status_code=200)
def get_movies_by_category(category:str = Query(min_length=5,max_length=15)) -> List[Movie]:
    category = category.capitalize()
    lista = [item for item in movies if item['category'] == category]
    return JSONResponse(content=lista)

#Post que añade un diccionario mas en la lista
@app.post('/movies',tags=['Movies'], response_model=dict,status_code=201)
def create_movies(movie: Movie) -> dict:
    db = Sesion()
    new_movie = MovieModel(**movie.dict())
    db.add(new_movie)
    db.commit()
    return JSONResponse(status_code=201, content={'message':'Se ha registrado la película'}) 

@app.put('/movies/{id}', tags=['Movies'], response_model=dict,status_code=200)
def update_movie(id:int, movie:Movie) -> dict:
    for item in movies:
        if item["id"] == id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
            return JSONResponse(status_code=200,content={'message':'Se ha modificado la película'})
        
@app.delete('/movies/{id}', tags=['Movies'], response_model=dict,status_code=200)
def delete_movie(id:int) -> dict:
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
            return JSONResponse(status_code=200, content={'message':'Se ha eliminado la película'})
        else:
            return JSONResponse(status_code=404, content={'message':'Pelicula no existente'})