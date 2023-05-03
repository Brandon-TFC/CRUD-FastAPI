import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base #Manipulacion de las tablas database



sqlit_file_name = "../database.sqlite"
base_dir = os.path.dirname(os.path.realpath(__file__))


database_url = f"sqlite:///{os.path.join(base_dir, sqlit_file_name)}"

#Motor de la base de datos
engine = create_engine(database_url, echo=True)

#Creacion de la seccion
Session = sessionmaker(bind=engine)

Base = declarative_base()