#import json
from fastapi import FastAPI, HTTPException, Body, Path, Query, Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer


app = FastAPI()
app.title = 'Aplicacion con FastApi' 
app.version = '0.0.1'

class JTWBearer(HTTPBearer):
    async def __call__(self, request: Request):
         auth = await super().__call__(request)
         data = validate_token(auth.credentials)
         if data['email'] != 'admin@gmail.com':
             raise HTTPException(status_code=403, detail='Credenciales invalidas')


class User(BaseModel):
    email:str
    password:str



class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5, max_length=15)
    overview: str = Field(min_length=15, max_length=50)
    year: int = Field(default=2023, le=2023)
    rating: float = Field(ge=0.0, le=10.0)
    category: str = Field(min_length=5, max_length=20)

    class Config:
        schema_extra = {
            'example':{
                'id': 1,
                'title': 'Mi pelicula',
                'overview': 'Descripcion de la pelicula',
                'year': 203,
                'rating': 9.8,
                'category': 'Accion'

            }
        }


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


@app.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JTWBearer())])
def get_movies()-> List[Movie]:
    return JSONResponse(content=movies)


@app.get('/movies/{id}',tags=['movies'], response_model=Movie)
def get_movie(id: int= Path(ge=1, le=2000)) -> Movie:
    for item in movies:
        if item['id'] == id: 
            return JSONResponse(content=item)
        #Utilizamos la exception en caso de que no se encuentre el id ejecutado
    raise HTTPException(status_code=404, detail='Movie no encontrda')
    
    #return []
    
@app.get('/movie/', tags=['movies'], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15), year: int=Query(2023)) ->List[Movie]:
    # return[item for item in movies if item['category]==category]
    result = []
    for movie in movies:
        if movie['category'] == category and int(movie['year']) == year:
            result.append(movie)
    if result:
        return {'movies': result}
    else:
        raise HTTPException(status_code=404, detail="No se encontraron películas para la categoría y año especificados")

#Agregar un movie
@app.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    movies.append(dict(movie))
    return JSONResponse(status_code=201, content={'message': 'Se ha registrado la pelicula'})

#@app.post('/movies', tags=['movies'])
#def create_movie(movie: Movie):
#    movies.append(dict(movie))
#    return movies

#Modificar movie pidiendo el id 
@app.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict:
    for m in movies:
        if m['id'] == id:
             m['title'] = movie.title
             m['overview'] = movie.overview
             m['year'] = movie.year
             m['category'] = movie.category
             m['rating'] = movie.rating

            #Guardamos todos los updates que tenga en un archivo JSON
            #with open('movies.json', 'w') as f:
            #    json.dump(movies, f) #Escribir los updates en el archivo movies.json

        return {'message': 'Valores actualizados para la película con id {}'.format(id)}

    raise HTTPException(status_code=404, detail='Película no encontrada')

#@app.put('/movies/{id}', tags=['movies'])
#def update_movie(id: int, movie: Movie):
#    for m in movies:
#        if m['id'] == id:
#            if movie.title:
#                m['title'] = movie.title
#            if movie.overview:
#                m['overview'] = movie.overview
#            if movie.year:
#                m['year'] = movie.year
#            if movie.category:
#                m['category'] = movie.category
#            if movie.rating:
#                m['rating'] = movie.rating
#
#            #Guardamos todos los updates que tenga un en archivo JSON
#            #with open('movies.json', 'w') as f:
#            #    json.dump(movies, f) #Escirbir los updates en el archivo movies.json
#            return {'message': 'Movie: valores actualizados para la pelicula con id {}'.format(id)}
#    raise HTTPException(status_code=404, detail='Movie no encontrada')


#Eliminar movie por el meotod de id
@app.delete('/movies/{movie_id}', tags=['movies'], response_model=dict, status_code=200)
def delete_movie(movie_id: int) -> dict:
    for movie in movies: #iteramos en movie hasta encontrar el id
        if movie['id'] == movie_id:
            movies.remove(movie) #Una vez encontrado eliminamos la movie

            # Guardar en archivo JSON
            #with open('movies.json', 'w') as f:
            #    json.dump(movies, f)

            return {"message": "Movie eliminada."}

    raise HTTPException(status_code=404, detail="Movie no encontrada.")






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





    