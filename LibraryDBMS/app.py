from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# Secret key for session management
app.secret_key = 'pra'

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'  # MySQL server location
app.config['MYSQL_USER'] = 'root'  # MySQL username
app.config['MYSQL_PASSWORD'] = 'tamil_2005'  # MySQL password
app.config['MYSQL_DB'] = 'library_management1'  # Name of the database

# Initialize MySQL
mysql = MySQL(app)

# Home Route
@app.route('/')
def home():
    return render_template('home.html')

# Book Routes
@app.route('/book_list', methods=['GET'])
def book_list():
    search_query = request.args.get('search', '')
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM books WHERE title LIKE %s", ('%' + search_query + '%',))
    books = cur.fetchall()
    cur.close()
    return render_template('book_list.html', books=books, search_query=search_query)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        year = request.form['year']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO books (title, author, year) VALUES (%s, %s, %s)", (title, author, year))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('book_list'))
    return render_template('add_book.html')

@app.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM books WHERE id = %s", (book_id,))
    book = cur.fetchone()

    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        year = request.form['year']

        cur.execute("UPDATE books SET title = %s, author = %s, year = %s WHERE id = %s",
                    (title, author, year, book_id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('book_list'))

    cur.close()
    return render_template('edit_book.html', book=book)

@app.route('/delete_book/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM books WHERE id = %s", (book_id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('book_list'))
# Run the application
if __name__ == '__main__':
    app.run(debug=True)
