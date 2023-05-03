from fastapi import APIRouter, Path, Query, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse  #Modulo que nos deja hacer codigo HTML
from pydantic import BaseModel, Field  #Modulo que con una clase crea un modelo con las variables
from typing import Optional, List   #Para que un request sea opcional
from typing import List         #Lista
from config.database import Motor, Sesion, Base
from models.movie import Movie as MovieModel
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService
from schemas.movie import Movie

movie_router = APIRouter()

#Get que retorna la lista de diccionarios
@movie_router.get('/movies',tags=['Movies'], response_model=List[Movie], status_code=200,dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Sesion()
    result = MovieService(db).get_movies()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

#Get que retorna un diccionario de la lista dependiendo de su id
@movie_router.get('/movies/{id}', tags=['Movies'], response_model=Movie,status_code=200)
def get_id(id: int = Path(ge=1)) -> Movie:
    db = Sesion()
    result = MovieService(db).get_movie(id)
    if not result:
         return JSONResponse(status_code=404, content={'message':f'La pelicula con el id: {id} no existe'})
    return JSONResponse(content=jsonable_encoder(result))

#Get que retorna una lista de diccionarios con esa categoria
@movie_router.get('/movies/',tags=['Movies'],response_model=List[Movie],status_code=200)
def get_movies_by_category(category:str = Query(min_length=1)) -> List[Movie]:
    category = category.capitalize()
    db = Sesion()
    result = MovieService(db).get_movies_by_category(category)
    if result == []:
        return JSONResponse(status_code=404, content={'message':f'No existen peliculas con la categoria {category}'})
    return JSONResponse(content=jsonable_encoder(result))

#Post que añade un diccionario mas en la lista
@movie_router.post('/movies',tags=['Movies'], response_model=dict,status_code=201)
def create_movies(movie: Movie) -> dict:
    db = Sesion()
    MovieService(db).create_movie(movie)
    return JSONResponse(status_code=201, content={'message':'Se ha registrado la película'}) 

@movie_router.put('/movies/{id}', tags=['Movies'], response_model=dict,status_code=200)
def update_movie(id:int, movie:Movie) -> dict:
    db = Sesion()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={'message':f'La pelicula con el id: {id} no existe'})
    MovieService(db).update_movie(id,movie)
    return JSONResponse(status_code=200,content={'message':f'Se ha modificado la película con id: {id}'})
        
@movie_router.delete('/movies/{id}', tags=['Movies'], response_model=dict,status_code=200)
def delete_movie(id:int) -> dict:
    db = Sesion()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={'message':f'La pelicula con el id: {id} no existe'})
    MovieService(db).delete_movie(id)
    return JSONResponse(status_code=200,content={'message':f'Se ha eliminado la película con id: {id}'})   