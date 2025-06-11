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
    song_key   = db.Column(db.String(255))
    song_lyrics= db.Column(db.String(255))

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



    return render_template('setbuilder.html', songs = songs, sets =sets)


@app.route('/editsong/<the_song_id>')
def editsong(the_song_id):
    if the_song_id == '99999999':  
        the_song = list()
        blank_song = {"song_id" : '', "song_name" : '', "song_key" : '', "song_lyrics" : ''}
        print('youre making a new song')
        print(blank_song)
        the_song.append(blank_song)
    else:
        the_song = db.session.query(Songs).where(Songs.song_id == the_song_id).all()
        print('getting existing song')
        print(the_song_id)

    possible_keys = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    print(the_song)
    print(type(the_song))
    print(len(the_song))

    return render_template('editsong.html', the_song = the_song, possible_keys = possible_keys)

    

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = True)
    app.add_url_rule('/', 'root', get_songs)