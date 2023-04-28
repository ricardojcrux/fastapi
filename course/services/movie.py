from models.movie import Movie as MovieModel
from schemas.movie import Movie

class MovieService():

    def __init__(self,db) -> None:
        self.db = db

    def get_movies(self):
        result = self.db.query(MovieModel).all()
        return result
    
    def get_movies(self,id):
        result = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        return result
    
    def get_movies_by_category(self,category):
        result = self.db.query(MovieModel).filter(MovieModel.category == category).all()
        return result
    
    def create_movies(self, movie: Movie):
        new_movie = Movie(**movie.dict())
        self.db.add(new_movie)
        self.db.commit()
        return
