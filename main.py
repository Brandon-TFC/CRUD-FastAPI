from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from jwt_manager import create_token
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from routers.movie import movie_router

app = FastAPI()
app.title = 'Aplicacion con FastApi Brandon Gutierrez' 
app.version = '0.0.1'

app.add_middleware(ErrorHandler)
app.include_router(movie_router)
Base.metadata.create_all(bind=engine)




class User(BaseModel):
    email:str
    password:str



movies =[
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Accion'  
    },
    {
        'id': 2,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Accion'  
    }
]

@app.get('/', tags=['home']) #Le cambiamos el default por el tag = home
def message():
    return HTMLResponse('<h1>Hello world</h1>')


@app.post('/login', tags=['auth'])
def login(user: User):
    if user.email == 'admin@gmail.com' and user.password == 'admin':
        token: str = create_token(user.dict())
    return JSONResponse(status_code=200, content=token)









#@app.delete('/movies/{movie_id}', tags=['movies'])
#def delete_movie(movie_id: int):
#    for movie in movies:
#        if movie['id'] == movie_id:
#            movies.remove(movie)
#
#            #Guardamos en el archivo json
#            with open('movies.json', 'w') as f:
#                json.dump(movies, f)
#
#            return {'message': 'Movie eliminada'}
#        raise HTTPException(status_code=404, detail='Movie no encontrada')





    