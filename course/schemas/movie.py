from pydantic import BaseModel, Field
from typing import Optional

#Creamos una clase como modelo de atributos de una pelicula
class Movie(BaseModel):
    title: str = Field(min_length=5,max_length=50)
    overview: str = Field(min_length=5, max_length=200)
    year: int = Field(le=2024)
    rating: float = Field(le=10)
    category: str = Field(min_length=3,max_length=30)

#Clase dentro de la otra clase con el esquema de datos 
    class Config:
        schema_extra={
            'example': {
                'title':'Pelicula',
                'overview':'Acá va la resena de la película',
                'year':2023,
                'rating':0.0,
                'category':'Categoria'
            }
        }