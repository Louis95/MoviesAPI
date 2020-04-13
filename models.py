from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import Column, Integer, Date, String
import os

db = SQLAlchemy()



def set_up_db(app):
    app.config.from_object('config')
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)


class Movies(db.Model):
    __tablename__ = 'movies'
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    release_date = db.Column(db.String(), nullable=False)
    title = Column(String(180), nullable=False, unique=True)
    sets = db.relationship('Sets', backref='movies', lazy='dynamic')

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def show(self):
        return {
            'id': self.id,
            'release_date': self.release_date,
            'title': self.title
        }


class Actors(db.Model):
    __tablename__ = 'actors'
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    name = Column(String(180))
    age = Column(Integer)
    gender = Column(String(20))
    sets = db.relationship('Sets', backref='actors', lazy='dynamic')

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def show(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }

# pivot table for actor and movie
class Sets(db.Model):
    __tablename__ = 'sets'
    id = db.Column(db.Integer, primary_key=True)
    actor_id = db.Column(Integer, db.ForeignKey('actors.id'))
    movie_id = db.Column(Integer, db.ForeignKey('movies.id'))

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)

    def show(self):
        return {
            'id': self.id,
            'actor_id': self.actor_id,
            'movie_id': self.movie_id
        }

    def show_movie(self):
        return {
            'id': self.movie_id,
        }
