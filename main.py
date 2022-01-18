from flask import Flask, jsonify, request

from storage import all_movies, liked_movies, notliked_movies, didnotwatch_movies
from demographicfiltering import output
from contentfiltering import getreccomendations

# -----------------------1-------------
# all_movies = []

# with open('movies.csv') as f:
#   reader = csv.reader(f)
#   data = list(reader)
#   all_movies = data[1:]

# liked_movies = []
# disliked_movies = []
# didnotwatch_movies = []

app = Flask(__name__)


@app.route('/get-movie')
def get_movie():  # --------------2---------
    movie_data = {
        "title": all_movies[0][19],
        "poster_link": all_movies[0][27],
        "release_date": all_movies[0][13] or "N/A",
        "duration": all_movies[0][15],
        "rating": all_movies[0][20],
        "overview": all_movies[0][9]
    }
    return jsonify({
        'data': movie_data,  #changed here instead of movie_data[0]
        'status': 'success'
    })


@app.route('/liked-movie', methods=['POST'])
def liked_movies_route():
    movie = all_movies[0]
    # all_movies = all_movies[1:] ----------------3---------------
    liked_movies.append(movie)
    all_movies.pop(0)  # ---------4-------------

    return jsonify({
        'status': 'success'
    }), 201


@app.route('/unliked-movie', methods=['POST'])
def disliked_movies_route():
    movie = all_movies[0]
    # all_movies = all_movies[1:]
    notliked_movies.append(movie)  # -------------5------------
    all_movies.pop(0)
    return jsonify({
        'status': 'success'
    }), 201


@app.route('/did-not-watch', methods=['POST'])
def did_not_watch_view():
    movie = all_movies[0] # -------------------6--------------
    didnotwatch_movies.append(movie)
    all_movies.pop(0)
    return jsonify({
        'status': 'success'
    }), 201

@app.route("/popular-movies")
def popular_movies():
    movie_data = []
    for movie in output:
      print(movie)
      _d = {
            "title": movie[0],
            "poster_link": movie[1],
            "release_date": movie[2] or "N/A",
            "duration": movie[3],
            "rating": movie[4],
            "overview": movie[5]
        }
      movie_data.append(_d)
    return jsonify({
        "data": movie_data,
        "status": "success"
    }), 200

@app.route("/recommended-movies")
def recommended_movies():
    all_recommended = []
    for liked_movie in liked_movies:
        output = getreccomendations(liked_movie[19])
        for data in output:
            all_recommended.append(data)
    import itertools
    all_recommended.sort()
    all_recommended = list(all_recommended for all_recommended,_ in itertools.groupby(all_recommended))
    movie_data = []
    for recommended in all_recommended:
        _d = {
            "title": recommended[0],
            "poster_link": recommended[1],
            "release_date": recommended[2] or "N/A",
            "duration": recommended[3],
            "rating": recommended[4],
            "overview": recommended[5]
        }
        movie_data.append(_d)
    return jsonify({
        "data": movie_data,
        "status": "success"
    }), 200

if __name__ == '__main__':
    app.run()
