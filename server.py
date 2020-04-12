
"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver
To run locally:
    python server.py
Go to http://localhost:8111 in your browser.
A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""
import os
  # accessible as a variable in index.html:
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response
from flask import render_template
from flask import jsonify






tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)





#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@35.243.220.243/proj1part2
#
# For example, if you had username gravano and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://gravano:foobar@35.243.220.243/proj1part2"
#
DATABASEURI = "postgresql://ncc2137:3749@35.231.103.173/proj1part2"




# delete database array below later
database = [
  {
  "id": 0,
  "Name": "Tom Brady",
  "Team": "New England Patriots",
  "Bio": "Thomas Edward Patrick Brady Jr. (bord August 3, 1997) is an American footbal quarterback for the New England Patriots of the National Football League (NFL). He has won six Super Bowls, the most of any football player ever. Due to his various accomplishments and records, he is considered by fans and soprts analysts to be the G.O.A.T (greatest of all time).",
  "Rating": 97.7,
  "Height": "6-4",
  "Weight": "225 lbs",
  "Age": 41,
  "Experience": "20th season",
  "pic":"http://static.nfl.com/static/content/public/static/img/fantasy/transparent/200x200/BRA371156.png"

  },
  ]

Lookup_matches=[

]


#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#
engine.execute("""CREATE TABLE IF NOT EXISTS test (
  id serial,
  name text
);""")
engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")


@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """

  # DEBUG: this is debugging code to see what request looks like
  print(request.args)


  #
  # example of a database query
  #
  cursor = g.conn.execute("SELECT title FROM song")
  names = []
  for result in cursor:
    names.append(result['title'])  # can also be accessed using result[0]
  cursor.close()

  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be 
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  #     <div>{{data}}</div>
  #     
  #     # creates a <div> tag for each element in data
  #     # will print: 
  #     #
  #     #   <div>grace hopper</div>
  #     #   <div>alan turing</div>
  #     #   <div>ada lovelace</div>
  #     #
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #
  context = dict(data = names)


  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  return render_template("index.html", **context)

#
# This is an example of a different path.  You can see it at:
# 
#     localhost:8111/another
#
# Notice that the function name is another() rather than index()
# The functions for each app.route need to have different names
#
@app.route('/another')
def another():
  return render_template("another.html")


# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
  name = request.form['name']
  g.conn.execute('INSERT INTO test(name) VALUES (%s)', name)
  return redirect('/')


@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()


# Added code
@app.route('/Search')
def Search(database=database):
    return render_template('Search.html', database=database)

@app.route('/match', methods=['GET', 'POST'])
def match():
  global database
  global Lookup_matches
  Lookup_matches.clear()
  json_data = request.get_json()
  Lookup=json_data["Lookup"]
  x=0;
  while (x<len(database)):
    if Lookup.lower() in database[x]["Name"].lower():
      Lookup_matches.append(database[x]);
    elif Lookup.lower() in database[x]["Team"].lower():
      Lookup_matches.append(database[x]);
    elif Lookup.lower() in database[x]["Bio"].lower():
      Lookup_matches.append(database[x]);
    elif str(Lookup) in str(database[x]["Rating"]):
      Lookup_matches.append(database[x]);
    elif Lookup in database[x]["Height"]:
      Lookup_matches.append(database[x]);
    elif Lookup in database[x]["Weight"]:
      Lookup_matches.append(database[x]);
    elif str(Lookup) in str(database[x]["Age"]):
      Lookup_matches.append(database[x]);
    elif Lookup in database[x]["Experience"]:
      Lookup_matches.append(database[x]);
    x=x+1;
  return jsonify(Lookup_matches = Lookup_matches)


@app.route('/Home')
def Home():
    return render_template('Home.html')

@app.route('/Browse')
def Browse():
    return render_template('Browse.html')

@app.route('/Playlists')
def Playlists():
    return render_template('Playlists.html')

"""
GET FUNCTIONALITY - Kanak's code
"""

@app.route('/search_artist')
def search_artist_k():
    return render_template('Search_Artist_K.html')

@app.route('/search_song')
def search_song_k():
    return render_template('Search_Song_K.html')

@app.route('/search_album')
def search_album_k():
    return render_template('Search_Album_K.html')

@app.route('/search_playlist')
def search_playlist_k():
    return render_template('Search_Playlist_K.html')

@app.route('/search_user')
def search_user_k():
    return render_template('Search_User_K.html')

"""
Query Methods - Kanak's code
"""

@app.route('/get_artist_details', methods=['GET'])
def get_artist_details_k():
  artist_id = int(request.args['artist_id'])
  cursor = g.conn.execute("SELECT * FROM artist where artist_id={};".format(artist_id))
  artists = []
  for result in cursor:
    artists.append({
      'username': result['username'],
      'name': result['name'],
      'date_of_joining': result['date_of_joining'],
      'date_of_birth': result['date_of_birth']
    })
  cursor.close()

  return jsonify(Lookup_matches=artists)

@app.route('/get_song_details', methods=['GET'])
def get_song_details_k():
  song_id = request.args["song_id"]
  #Query
  #return

@app.route('/get_album_details', methods=['GET'])
def get_album_details_k():
  album_id = int(request.args["album_id"])
  cursor = g.conn.execute("select id, album_name, total_length, artist.name as artist_name, any_explicit from (select album.album_id as id, min(name) as album_name, sum(time) as total_length, bool_or(explicit) as any_explicit from songalbum, song, album where songalbum.song_id = song.song_id and album.album_id = songalbum.album_id and album.album_id = {} group by album.album_id) as foo, albumartist, artist where albumartist.album_id = foo.id and artist.artist_id = albumartist.artist_id;".format(album_id))
  albums = []
  for result in cursor:
    albums.append({
      'album_name': result['album_name'],
      'artist_name': result['artist_name'],
      'total_length': str(result['total_length']),
      'any_explicit': str(result['any_explicit'])
    })
  ## IF THERE ARE MULTIPLE ARTISTS THIS WILL RETURN MULTIPLE ROWS
  cursor.close()

  return jsonify(Lookup_matches=albums)

@app.route('/get_playlist_details', methods=['GET'])
def get_playlist_details_k():
  playlist_id = request.args["playlist_id"]
  #Query
  #return

@app.route('/get_user_details', methods=['GET'])
def get_user_details_k():
  user_id = request.args["user_id"]
  #Query
  #return

if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

    HOST, PORT = host, port
    print("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)

  run()
