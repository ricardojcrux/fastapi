from pydantic import BaseModel, Field
from typing import Optional

class Student(BaseModel):
    id: Optional[int] = Field(ge=1)
    name: str
    level: str 
    country: str
    birth_year: int = Field(le=2023)

    class Config:
        schema={
            'example':{
                'id':0,
                'name':'Nombre Apellido',
                'level':'Numero Grado',
                'country':'Pais',
                'birth_year': 2000
            }
        }