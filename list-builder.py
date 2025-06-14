import os
import re
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

root_path = os.path.realpath(__file__)[:-len(os.path.basename(__file__))]
static_path = root_path + 'static\\'


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
    song_in_sets_id = db.Column(db.Integer, primary_key=True)
    set_id     = db.Column(db.Integer)
    song_id    = db.Column(db.Integer)
    song_order = db.Column(db.Integer)


class LiturgicalSundays(db.Model):
    __tablename__ = 'liturgical_sundays'
    liturgical_key  = db.Column(db.Integer, primary_key = True)
    sunday_dt       = db.Column(db.Date)
    sunday_title    = db.Column(db.String(255))
    sunday_url      = db.Column(db.String(255))
    liturgical_year = db.Column(db.String(255))




# --- FUNCTIONS ----------------------------

def songs_in_set_query(the_set_id):
    songs_in_set = (db.session.query(SongsInSets, Songs)
        .where(SongsInSets.set_id == the_set_id)
        .filter(SongsInSets.song_id == Songs.song_id)
        .order_by(SongsInSets.song_order)
        .all())
    
    return songs_in_set


def get_songs_by_set(the_set_id):
    songs_in_set = songs_in_set_query(the_set_id = the_set_id)

    the_results = list() 

    for x in songs_in_set:
        the_results.append(x[1])

    return(the_results)
    

def save_a_set(the_set_id, the_song_ids, db = db):

    # delete all of the sets rows
    this_sets_current_songs = db.session.query(SongsInSets).filter_by(set_id = the_set_id).all()
    print('deleting all songs in set ' + str(the_set_id))
    for s in this_sets_current_songs:
        db.session.delete(s)
    db.session.commit()


    # insert rows for the_song_ids

    the_new_rows = list()

    for i in range(len(the_song_ids)) :
        newsonginset = SongsInSets(set_id = the_set_id, song_id = the_song_ids[i], song_order = i + 1)
        the_new_rows.append(newsonginset)

    print('adding new songs to set ' + str(the_set_id))

    db.session.add_all(the_new_rows)
    db.session.commit()
       
    return(1)




# -- ROUTES ---------------------------------------------------------


@app.route('/sets/<int:selected_set>')
@app.route('/')
def get_songs(selected_set=None):
    songs = db.session.query(Songs).order_by(Songs.song_name).all()
    sets = db.session.query(Sets).order_by(Sets.set_date.desc()).all()

    if selected_set is None :
        selected_set = sets[0].set_id

    songs_in_this_set = get_songs_by_set(selected_set)

    return render_template('setbuilder.html', songs = songs, sets =sets, songs_in_this_set = songs_in_this_set, selected_set = selected_set)




@app.route('/changeset', methods=['POST'])
def changeset():
    the_selected_set = request.form['set_selector']
    the_selected_set = int(the_selected_set)
    print('changing set to ' + str(the_selected_set))
    return redirect(url_for('get_songs', selected_set=the_selected_set))





@app.route('/editsong/<the_song_id>')
def editsong(the_song_id):
    if the_song_id == '99999999':  
        the_song = list()
        blank_song = {"song_id" : '', "song_name" : '', "song_key" : '', "song_lyrics" : ''}
        print('youre making a new song')
        the_song.append(blank_song)
    else:
        the_song = db.session.query(Songs).where(Songs.song_id == the_song_id).all()
        print('getting existing song' + str(the_song_id))

    possible_keys = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    print(the_song)
    print(type(the_song))
    print(len(the_song))

    return render_template('editsong.html', the_song = the_song, possible_keys = possible_keys)




    
@app.route('/newset', methods=['POST'])
def newset():

    newset_date = request.form['newset_date']

    db.session.add(Sets(set_date = newset_date))
    db.session.commit()

    return redirect(url_for('get_songs'))






@app.route('/save_sets', methods=['POST'])
def save_sets():

    data = request.get_json()
    the_set_order = data.get('dropzone')
    the_selected_set = data.get('the_selected_set')
    print('selected set is ' + str(the_selected_set))

    save_a_set(the_set_id=the_selected_set, the_song_ids=the_set_order, db = db)

    return redirect(url_for('get_songs'))


@app.route('/publish_set/<int:the_set_id>')
def publish_set(the_set_id):

    # build contents query
    songs_in_set = get_songs_by_set(the_set_id=the_set_id)

    the_set_date = db.session.query(Sets).where(Sets.set_id == the_set_id).one()
    the_set_date = the_set_date.set_date 
    print(type(the_set_date))

    liturgical_sunday = (db.session.query(LiturgicalSundays)
        .where(LiturgicalSundays.sunday_dt == the_set_date)
    ).one()

    slide_style_path = url_for('static', filename = 'slide-style.css')

    '''
    # no clue why this isn't working right. Is this going to break in production???
    md_header_path = url_for('static', filename = 'md-header.md')
    md_communion_path = static_path + 'md-communion.md'
    '''

    with open('static/md-header.md', 'r', encoding = 'utf-8') as file:
        md_header = file.read()
    with open('static/md-communion.md', 'r', encoding = 'utf-8') as file:
        md_communion= file.read()

    the_rmd = '---\ntitle: "' + liturgical_sunday.sunday_title + '"'
    the_rmd = the_rmd + '\noutput:\n  slidy_presentation:\n    css: slide-style.css\n'
    the_rmd = the_rmd + md_header 

    for song in songs_in_set :
        the_rmd = the_rmd + '\n' + song.song_lyrics + '\n<span class="songkey">' + song.song_key + '</span>\n\n\n'

    the_rmd = the_rmd + md_communion + '\n'
    the_rmd = the_rmd + '[lectionary](' + liturgical_sunday.sunday_url + ')'


    final_md_path = 'output/fullset.rmd'

    with open(final_md_path, 'w', encoding='utf-8') as file:
        file.write(the_rmd)


    final_md_path_full = "'" + root_path + final_md_path + "'"
    final_md_path_full = re.sub(r'\\', '/',  final_md_path_full)

    rmarkdown_command = '"rmarkdown::render(' + final_md_path_full + ')"'
    rscript_command = 'Rscript -e ' + rmarkdown_command

    os.system(rscript_command)
    
    # copy to location (or maybe don't! just point the big link at the actual file? )
    # add link to UI


    return redirect(url_for('get_songs', selected_set=the_set_id))




if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = True)
    app.add_url_rule('/', 'root', get_songs)