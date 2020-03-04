from flask import Flask
from flask import jsonify
from flask import request

from sqlalchemy import and_
from flask_sqlalchemy import SQLAlchemy

from config import DB_URI

from models import MoviesMovie
from models import MoviesComment
from models import MoviesMovierating

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
db = SQLAlchemy(app)


@app.route("/")
def hello():
    return "Welcome in sqlcodegen tutorial!"


@app.route("/movies")
def get_all_movies():
    movies = db.session.query(MoviesMovie).all()
    serialized_movies = [{"id": movie.id, "title": movie.title} for movie in movies]

    return jsonify(serialized_movies), 200


@app.route("/movies/filter")
def find_movies_by_title():
    title = request.args.get("title")

    movies = db.session.query(MoviesMovie).filter(MoviesMovie.title.contains(title)).all()
    serialized_movies = [{"id": movie.id, "title": movie.title} for movie in movies]

    return jsonify(serialized_movies), 200


@app.route("/movies/comments")
def get_all_movies_comments():
    comments = db.session.query(MoviesComment).filter(MoviesComment.text.isnot(None)).all()
    serialized_comments = [
        {"id": comment.id, "comment": comment.text, "movie_title": comment.movie.title} for comment in comments
    ]

    return jsonify(serialized_comments), 200


@app.route("/movies/ratings")
def get_all_movies_ratings():
    ratings = (
        db.session.query(MoviesMovierating)
        .filter(and_(MoviesMovierating.value.isnot(None), MoviesMovierating.source.isnot(None)))
        .all()
    )
    serialized_ratings = [
        {"id": rating.id, "source": rating.source, "value": rating.value, "movie_title": rating.movie.title}
        for rating in ratings
    ]

    return jsonify(serialized_ratings), 200


@app.route("/statistics")
def statistics():
    statistics = (
        db.session.query(MoviesMovie.title, db.func.count(MoviesComment.id), db.func.count(MoviesMovierating.id))
        .outerjoin(MoviesComment, MoviesMovie.id == MoviesComment.movie_id)
        .outerjoin(MoviesMovierating, MoviesMovie.id == MoviesMovierating.movie_id)
        .group_by(MoviesMovie.title)
        .all()
    )
    serialized_statistics = [
        {"movie_title": stat[0], "comments_count": stat[1], "ratings_count": stat[2]} for stat in statistics
    ]

    return jsonify(serialized_statistics), 200


if __name__ == "__main__":
    app.run()
