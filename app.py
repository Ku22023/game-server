# Importing flask module in the project is mandatory
#Render template is used to load in HTML files
from flask import Flask, render_template, request, redirect, flash, url_for
import random
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

def get_db_connection():
    conn = sqlite3.connect('login.db')
    conn.row_factory = sqlite3.Row
    return conn
    
def init_db():
    conn = get_db_connection() 
    with app.open_resource('schema.sql') as f:
        conn.executescript (f.read().decode('utf8'))
    conn.close()


@app.route('/add_game', methods=('GET', 'POST'))
def add_game():
    conn = get_db_connection()
    games = conn.execute('SELECT * FROM games').fetchone()

    if request.method == 'POST':
        id = request.form['id']
        title = request.form['title']
        platform = request.form['platform']
        genre = request.form['genre']
        year = request.form['year']
        sales = request.form['sales']


        if not id or not title or not platform or not genre or not year or not sales: 
            flash('All fields are required!')
        else:
            conn.execute('INSERT INTO games (id, title, platform, genre, year, sales) VALUES (id = ? title = ?, platform = ?, genre = ?, year = ?, sales = ?)',
                (id, title, platform, genre, year, sales))
            conn.commit()
            conn.close()
            return render_template('add_games.html')
            
    return render_template('add_games.html')

@app.route('/login', methods=('POST', 'GET'))
def login():
    if request.method == 'POST':
        user_name = request.form['userName']
        password = request.form['password']

        if not user_name or not password: 
            flash('All Fields required')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO users (username, password) VALUES (?,?)', (user_name, password))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template("login.html")

@app.route('/view_games', methods=('POST', 'GET'))
def view_games():
    conn = get_db_connection()
    sql = "SELECT * FROM games"
    games = conn.execute(sql).fetchall()
    conn.close()
    return render_template('view_games.html', games=games)

@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit_game(id):
    conn = get_db_connection()
    games = conn.execute('SELECT * FROM games WHERE id=?', (id,)).fetchone()

    if request.method == 'POST':
        title = request.form['title']
        platform = request.form['platform']
        genre = request.form['genre']
        year = request.form['year']
        sales = request.form['sales']


        if not id or not title or not platform or not genre or not year or not sales: 
            flash('All fields are required!')
        else:
            conn.execute('UPDATE games SET title = ?, platform = ?, genre = ?, year = ?, sales = ? WHERE id = ?', 
                (title, platform, genre, year, sales, id))
            conn.commit()
            conn.close()
            return redirect(url_for('view_games'))
            
    return render_template('edit_user.html', games=games)

@app.route('/delete/<int:id>', methods=('POST',))
def delete_game(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('User deleted successfully!')
    return redirect(url_for('view_games.html'))

if __name__ == '__main__':
    app.run(debug=True,port=7496)