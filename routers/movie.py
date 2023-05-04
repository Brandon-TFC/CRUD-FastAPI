from fastapi import APIRouter
from fastapi import Depends, Path, Query, HTTPException
from fastapi.responses import JSONResponse
from typing import List
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieServices
from schemas.movie import Movie

#Creacion de un router
movie_router = APIRouter()

@movie_router.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies()-> List[Movie]:
    db = Session()
    result = MovieServices(db).get_movies() #Mostrar todos los datos 
    return JSONResponse(content=jsonable_encoder(result))


@movie_router.get('/movies/{id}',tags=['movies'], response_model=Movie)
def get_movie(id: int= Path(ge=1, le=2000)) -> Movie:
    db = Session()
    result = MovieServices(db).get_movie(id)
    if not result:
        raise HTTPException(status_code=404, detail='Movie no encontrda')
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

    
        #Utilizamos la exception en caso de que no se encuentre el id ejecutado
   
    
    #return []
    
@movie_router.get('/movie/', tags=['movies'], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15), year: int=Query(2023)) ->List[Movie]:
    # return[item for item in movies if item['category]==category]
    result = []
    db = Session()
    result = MovieServices(db).get_movie_by_category(category)
    if not result:
        raise HTTPException(status_code=404, detail="No se encontraron películas para la categoría y año especificados")
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

    #for movie in movies:
    #    if movie['category'] == category and int(movie['year']) == year:
    #        result.movie_routerend(movie)
    #if result:
    #    return {'movies': result}
    #else:
    #    raise HTTPException(status_code=404, detail="No se encontraron películas para la categoría y año especificados")




#Agregar un movie
@movie_router.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:

    db = Session()
    MovieServices(db).create_movie(movie)
    #movies.movie_routerend(dict(movie))
    return JSONResponse(status_code=201, content={'message': 'Se ha registrado la pelicula'})

#@movie_router.post('/movies', tags=['movies'])
#def create_movie(movie: Movie):
#    movies.movie_routerend(dict(movie))
#    return movies

#Modificar movie pidiendo el id 
@movie_router.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict:
    db = Session()
    result = MovieServices(db).get_movie(id)
    if not result:
        raise HTTPException(status_code=404, detail='Película no encontrada')
    MovieServices(db).update_movie(id, movie)
    return {'message': 'Valores actualizados para la película con id {}'.format(id)}
    

            #Guardamos todos los updates que tenga en un archivo JSON
            #with open('movies.json', 'w') as f:
            #    json.dump(movies, f) #Escribir los updates en el archivo movies.json

    

#Eliminar movie por el meotod de id
@movie_router.delete('/movies/{movie_id}', tags=['movies'], response_model=dict, status_code=200)
def delete_movie(id: int) -> dict:
    db = Session()
    result: MovieModel = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        raise HTTPException(status_code=404, detail='Película no encontrada')
    MovieServices(db).delete_movie(id)
            # Guardar en archivo JSON
            #with open('movies.json', 'w') as f:
            #    json.dump(movies, f)

    return {"message": "Movie eliminada."}