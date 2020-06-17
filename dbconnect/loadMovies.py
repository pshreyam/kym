from base64 import b64encode
from . import connect_to_db


def loadMovies(table_name):
    """ 
    Loads Movies From Different Tables.
    """
    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)
    sql = f"SELECT * FROM {table_name}"
    cursor.execute(sql)
    movies = cursor.fetchall()
    conn.close()
    for movie in movies:
        movie['image'] = b64encode(movie.get('image','')).decode("utf-8")
    return movies

def getUserSelectMovies(user_id):
    """
    Gets Movies Liked By Users.
    """
    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)
    sql = f"""SELECT * FROM userselectmovies, imdb WHERE `imdb`.`id` = `userselectmovies`.`movie_id` AND `userselectmovies`.`user_id` = {user_id}"""
    cursor.execute(sql)
    movies = cursor.fetchall()
    conn.close()
    for movie in movies:
        movie['image'] = b64encode(movie.get('image','')).decode("utf-8")
    return movies

def getUserContent(user):
    """
    Gets Content For Users Based Upon Their Gender And Nationality.
    (Not Final Algo Implementation)(Temporary) 
    """
    content = {}
    nationality = user.get('nationality','').lower() 
    gender = user.get('gender','')

    content['userSelect'] = getUserSelectMovies(user.get('id'))
    content['userSelect_title'] = 'Movies liked'
    content['userSelect_category'] = 'imdb'

    if nationality == 'nepalese' or nationality == 'nepali':
        content['primary'] = loadMovies('nepali')[:5]
        content['primary_category'] = 'Nepali'
    elif nationality == 'indian':
        content['primary'] = loadMovies('hindi')[:5]
        content['primary_category'] = 'Hindi'
    else:
        content['primary'] = loadMovies('imdb')[:5]
        content['primary_category'] = 'Imdb'

    if gender == 'M':
        content['secondary'] = loadMovies('action')[:5]
        content['secondary_category'] = 'Action'
    else:
        content['secondary'] = loadMovies('musical')[:5]
        content['secondary_category'] = 'Musical'

    if (nationality == 'nepali' or nationality == 'nepalese' or nationality=='indian'):
        content['default'] = loadMovies('imdb')[:5]
        content['default_category'] = 'Imdb'

    return content


def selectMovies(user_id, movie_id):
    """
    Like Movie For Users From Imdb.
    """
    if not user_id:
        return 'There was some problem adding the movie!' ,'error'
    conn = connect_to_db()
    cursor = conn.cursor()
    sql = f"""SELECT * FROM userselectmovies 
            WHERE movie_id = {movie_id} AND user_id = {user_id}"""
    cursor.execute(sql)
    existing = cursor.fetchone()
    if existing:
        conn.commit()
        conn.close()
        return 'Movie already added to dashboard!', 'info'
    sql = f"INSERT INTO userselectmovies(movie_id,user_id) VALUES({movie_id},{user_id})"
    cursor.execute(sql)
    conn.commit()
    conn.close()
    return 'Successfully added to dashboard!' ,'success'


def search_movie(category, title):
    if not title:
        return None
    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)
    sql = f"SELECT * FROM {category} WHERE title LIKE '%{title}%'"
    cursor.execute(sql)
    movies = cursor.fetchall()
    conn.close()
    for movie in movies:
        movie['image'] = b64encode(movie.get('image','')).decode("utf-8")
    return movies
