from flask import Flask, render_template, request, redirect, url_for, jsonify
#from flask_sqlalchemy import SQLAlchemy
import db, os, datetime
from models import Movie
from db import insert

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
#db = SQLAlchemy(app)

#class Pelicula(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    titulo = db.Column(db.String(80), unique=True, nullable=False)
if not os.path.isfile('movies.db'):
    db.connect()

@app.route('/')
def home():
    return render_template('home.html')
    #return render_template('home.html', peliculas=movies.query.all())

@app.route('/catalog', methods=['GET'])
def getRequest():
    content_type = request.headers.get('Content-Type')
    mvs = [b.serialize() for b in db.view()]
    if (content_type == 'application/json'):
        json = request.json
        for b in mvs:
            if b['id'] == int(json['id']):
                return jsonify({
                    # 'error': '',
                    'res': b,
                    'status': '200',
                    'msg': 'Success getting all movies in library!👍😀'
                })
        return jsonify({
            'error': f"Error ⛔❌! Book with id '{json['id']}' not found!",
            'res': '',
            'status': '404'
        })
    else:
        return render_template('catalog.html', peliculas=mvs)


@app.route('/search', methods=['GET'])
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

@app.route('/new_movie', methods=['GET', 'POST'])
def newMovie():
    if request.method == 'POST':
        title = request.form['title']
        available = request.form['available'] == 'True'
        date = datetime.datetime.now()
        mv = Movie(db.getNewId(), available, title, date)
        db.insert(mv)
        return render_template('success.html')
    else:
        return render_template('new_movie.html')

@app.route('/update_movie', methods=['GET','POST'])
def updateMovie(id):
    if request.method == 'PUT':
        title = request.form['title']
        available = request.form['available'] == 'True'
        date = datetime.datetime.now()
        mv = Movie(db.getNewId(), available, title, date)
        db.update(mv)
        return render_template('success_update.html')
    else:
        return render_template('update_movie.html')
    
@app.route('/delete_movie', methods=['GET', 'DELETE'])
def deleteMovie(id):
    if request.method == 'POST':
        req_args = request.view_args
        bks = [b for b in db if b.id == id]
        if req_args:
            for b in bks:
                if b['id'] == int(req_args['id']):
                    db.delete(b['id'])
                    updated_bks = [b.serialize() for b in db.view()]
        return render_template('success_delete.html')
    else:
        return render_template('delete.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
