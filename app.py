from crypt import methods
import os
import sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

bookConnection = sqlite3.connect('books.db', check_same_thread=False)
bookConnection.row_factory = sqlite3.Row
app.config['JSON_SORT_KEYS'] = False
bookCursor = bookConnection.cursor()

bookCursor.execute('''CREATE TABLE IF NOT EXISTS Books (id INTEGER PRIMARY KEY, author TEXT, title TEXT, year_published INT)''')
bookConnection.commit()

@app.route('/api/books', methods=["POST"])
def addBook():
    author = request.json.get('author')
    title = request.json.get('title')
    yearPublished = request.json.get('yearPublished')

    bookCursor.execute('INSERT INTO Books (author, title, year_published) VALUES (?,?,?)', (author, title, yearPublished))
    bookConnection.commit()

    bookCursor.execute('SELECT * FROM Books ORDER BY id DESC LIMIT 1')
    for rows in bookCursor:
        newBookId = rows['id']
        newBookAuthor = rows['author']
        newBookTitle = rows['title']
        newBookYear = rows['year_published']

    return jsonify({'id':newBookId, 'author':newBookAuthor, 'title':newBookTitle, 'yearPublished':newBookYear}), 201

@app.route('/api/books', methods=["GET"])
def getBooks():
    bookList = []
    bookCursor.execute('SELECT * FROM Books ORDER BY title')
    for rows in bookCursor:
        newBookId = rows['id']
        newBookAuthor = rows['author']
        newBookTitle = rows['title']
        newBookYear = rows['year_published']

        currentBook = {
            'id':newBookId,
            'author':newBookAuthor,
            'title':newBookTitle,
            'yearPublished':newBookYear
        }

        bookList.append(currentBook)
    
    return jsonify({"books":bookList})

@app.route('/api/books', methods=["DELETE"])
def deleteBooks():
    bookList = []
    bookCursor.execute('DELETE FROM Books')
    bookConnection.commit()

    return jsonify(), 204

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
