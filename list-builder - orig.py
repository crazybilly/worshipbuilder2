from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy


from creds import db_user, db_pass

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mariadb+pymysql://' + db_user + ':' + db_pass + '@192.168.2.75/barnchurch?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Recommended to disable for performance

db=SQLAlchemy(app)


class Sets(db.Model):
    __tablename__ = 'sets'
    set_id     = db.Column(db.Integer, primary_key=True)
    set_date   = db.Column(db.Date)

class Songs(db.Model):
    __tablename__ = 'songs'
    song_id    = db.Column(db.Integer, primary_key=True)
    song_name  = db.Column(db.String(255))

class SongsInSets(db.Model):
    __tablename__ = 'songs_in_sets'
    songs_in_sets_id = db.Column(db.Integer, primary_key=True)
    set_id     = db.Column(db.Integer)
    song_id    = db.Column(db.Integer)
    song_order = db.Column(db.Integer)




@app.route('/')
def get_songs():
    songs = db.session.query(Songs).order_by(Songs.song_name).all()
    sets = db.session.query(Sets).order_by(Sets.set_date.desc()).all()





    song_ul = '<ul>'

    for song in songs:
        song_ul += '<li id="' + str(song.song_id) + '">' + song.song_name + '</li>'

    song_ul += '</ul>'


    set_ul = '<select name="the_set">'

    for the_set in sets:
        set_ul += '<option value="' + str(the_set.set_id) + '">' + str(the_set.set_date) + '</option>'

    set_ul += '</select>'

    the_html = '<h2>Sets</h2>' + set_ul + '<h2>Songs</h2>' + song_ul
    #return the_html 


    return render_template('setbuilder.html', songs = songs, sets =sets)
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = True)
    app.add_url_rule('/', 'root', get_songs)