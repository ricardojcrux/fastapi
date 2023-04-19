import os                               #Modulo de datos del sistema
from sqlalchemy import create_engine    #Importamos dependencia del motor de la DB
from sqlalchemy.orm.session import sessionmaker         #
from sqlalchemy.ext.declarative import declarative_base

sqlite_db = '../database.sqlite'           #Nombre de la DB
db_dir = os.path.dirname(os.path.realpath(__file__))    #Trayendo la dirección del archivo

db_url = f'sqlite:///{os.path.join(db_dir,sqlite_db)}'  #Conectando la dirección de la DB con su nombre

Motor = create_engine(db_url, echo=True)    #Creación del motor de la DB
Sesion = sessionmaker(bind=Motor)           #Sesion enlazada con el motor de la DB
Base = declarative_base()                   #Funcion que nos sirve para manejar tablas de la DB