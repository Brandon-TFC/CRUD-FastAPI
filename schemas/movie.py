from pydantic import BaseModel, Field
from typing import Optional

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
