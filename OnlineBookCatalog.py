#  AUTHOR:  Michael O'Brien
#  CREATED:  14 September 2018
#  UPDATED:  21 September  2018
#  DESCRIPTION:  Online book catalog

#  Modules needed for application

from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

app.config.update(

    #  SECRET_KEY is used by 3rd party applications to secure things like cookies:  Should be strong and complex key
    SECRET_KEY = 'topsecret',
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Scuba2018!@localhost/catalog_db',
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    )

db = SQLAlchemy(app)

#  BASIC FLASK QUERY/ROUTING
@app.route('/index')
@app.route('/')
def hello_flask():
    return 'Hello Flask!'

#  QUERY STRINGS
@app.route('/new/')
def query_strings(greeting = 'Hello'):
    query_val = request.args.get('greeting', greeting)
    return '<h1> The greeting is:  {0} </h1>.'.format(query_val)


@app.route('/user')
@app.route('/user/<name>')
def no_query_strings(name='Michael'):
    return '<h1> Hello there {} </h1>.'.format(name)


@app.route('/temp')
def using_templates():
    return render_template('hello.html')


@app.route('/watch')
def movies():
    movie_list = ['Autopsy of Jane Doe',
                  'Neon Demon',
                  'Ghost in a Shell',
                  'Kong:  Skull Islannd',
                  'John Wick 2',
                  'Spiderman - Homecoming']
    return render_template('movies.html',
                           movies = movie_list,
                           name = 'Michael')


@app.route('/tables')
def movies_plus():
    movie_dict = {'Autopsy of Jane Doe' : 02.14,
                  'Neon Demon' : 3.20,
                  'Ghost in a Shell' : 1.50,
                  'Kong:  Skull Islannd' : 3.50,
                  'John Wick 2' : 02.52,
                  'Spiderman - Homecoming' : 1.48}
    return render_template('table_data.html',
                           movies = movie_dict,
                           name = 'Michael')


@app.route('/filters')
def filter_data():
    movie_dict = {'Autopsy of Jane Doe' : 02.14,
                  'Neon Demon' : 3.20,
                  'Ghost in a Shell' : 1.50,
                  'Kong:  Skull Islannd' : 3.50,
                  'John Wick 2' : 02.52,
                  'Spiderman - Homecoming' : 1.48}
    return render_template('filter_data.html',
                           movies = movie_dict,
                           name = None,
                           film = 'A Christmas Carol')


class Publication(db.Model):
    __tablename__ = 'publication'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), nullable = False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'The Publisher is {}'.format(self.name)


class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, index=True)
    author = db.Column(db.String(100))
    avg_rating = db.Column(db.Float)
    format = db.Column(db.String(50))
    image = db.Column(db.String(100), unique=True)
    num_pages = db.Column(db.Integer)
    pub_date = db.Column(db.DateTime, default=datetime.utcnow())

    # RELATIONSHIP
    pub_id = db.Column(db.Integer, db.ForeignKey('publication.id'))

    def __init__(self, title, author, avg_rating, book_format, image, num_pages, pub_id):
        self.title = title
        self.author = author
        self.avg_rating = avg_rating
        self.format = book_format
        self.image = image
        self.num_pages = num_pages
        self.pub_id = pub_id

    def __repr__(self):
        return '{} by {}'.format(self.title, self.author)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
