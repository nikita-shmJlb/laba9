from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.now)


with app.app_context():
    db.create_all()

@app.route('/')
def index():
    books = Book.query.order_by(Book.date_added.desc()).all()
    return render_template('index.html', books=books)

@app.route('/add', methods=['POST'])
def add_book():
    author = request.form.get('author')
    name = request.form.get('name')
    if author and name:
        new_book = Book(author=author, name=name)
        db.session.add(new_book)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:book_id>')
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=False)