import os, uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from config.database import Motor, Base
from middlewares.error_handler import ErrorHandler
from routers.movie import movie_router
from routers.user import user_router

app = FastAPI()                     #Llamamos una API como app
app.title = "Mi primer FastAPI"     #Titulo del API
app.version = "29.07.22"            #Ponemos version de manera manual
app.add_middleware(ErrorHandler)
app.include_router(user_router)
app.include_router(movie_router)

Base.metadata.create_all(bind=Motor)

#Get que retorna un codigo HTML gracias a HTMLResponse
@app.get('/', tags=['Home'], status_code=200, response_class=HTMLResponse)
def message():
    return '''
    <head><title>Welcome back to my FastAPI Project</title></head>
    <body><center>
    <h1 style=color:teal>Welcome Back to my FastAPI Project</h1>
    <h2><a href=/docs>Documentación de la API</a></h2>
    </center></body>
    '''

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port = int(os.environ.get("PORT",8000)))
    