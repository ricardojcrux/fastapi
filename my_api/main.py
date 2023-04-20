from fastapi import FastAPI, Path
from fastapi.responses import JSONResponse
from scheme import Student
import json 

ric = FastAPI()
ric.title = 'API de Estudiantes'
ric.version = '1.0'

with open('data.json') as info:
    data = json.load(info)

datos = dict(data)

@ric.get('/',tags=['Student'])
def data():
    return datos

@ric.get('/student/{id}', tags=['Student'])
def consulta(id: int = Path(ge=1,le=100)):
    lista = datos['Estudiantes']
    for student in lista:
        if student['id'] == id:
            return student
    return JSONResponse(content=[],status_code=404)

@ric.post('/student/',tags=['Student'])
def new_student(student:Student):
    lista = datos['Estudiantes']
    lista.append(student)
    datos['Estudiantes'] = lista
    return {'message':'Se ha registrado al estudiante'}

@ric.delete('/student/{id}', tags=['Student'])
def bye_student(id: int = Path(ge=1,le=100)):
    lista = datos['Estudiantes']
    for student in lista:
        if student['id'] == id:
            lista.remove(student)
            return {'message':'Se ha eliminado al estudiante'}