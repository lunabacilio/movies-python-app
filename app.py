from flask import Flask, render_template, request, jsonify

import db, os, datetime
from models import Movie
#from db import insert
from db import delete

app = Flask(__name__)

if not os.path.isfile('movies.db'):
    db.connect()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/catalog', methods=['GET']) #Put all data together
def getRequest():
    mvs = [b.serialize() for b in db.view()]
    return render_template('catalog.html', movies=mvs)


@app.route('/search', methods=['GET']) #Read data
def getRequestId():
    id = request.args.get('id')
    mvs = [b.serialize() for b in db.view()]
    if id:
        for b in mvs:
            if b['id'] == int(id):
                return render_template('search.html', pelicula=b)
            else:
                return render_template('error.html')
        return render_template('search.html', pelicula=None)
    else:
        return render_template('search.html', pelicula=None)

@app.route('/new_movie', methods=['GET', 'POST']) # Create data
def newMovie():
    if request.method == 'POST':
        title = request.form['name']
        available = request.form['available'] == 'True'
        date = datetime.datetime.now()
        mv = Movie(db.getNewId(), available, title, date)
        db.insert(mv)
        return render_template('success.html')
    else:
        return render_template('new_movie.html')

@app.route('/update_movie', methods=['GET','POST']) #Update data
def updateMovie():
    if request.method == 'POST':
        movie_id = request.form.get('movie_id')
        available = request.form.get('available')
        name = request.form.get('name')
        date = datetime.datetime.now()
        mv = Movie(movie_id, available, name, date)
        db.update(mv)
        return render_template('success_update.html')
    else:
        return render_template('update_movie.html')
    
@app.route('/delete_movie', methods=['GET', 'POST']) # Delete data
def delete_form():
    if request.method == 'POST':
        movie_id = request.form.get('movie_id')
        db.delete(movie_id)
        return render_template('success_delete.html')
    else:
        return render_template('delete.html')
    
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
