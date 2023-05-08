from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = 'qa.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS questions (id INTEGER PRIMARY KEY, title TEXT, question TEXT, date_created TEXT)')
        c.execute('CREATE TABLE IF NOT EXISTS answers (id INTEGER PRIMARY KEY, answer TEXT, question_id INTEGER, date_created TEXT)')
        conn.commit()

@app.route('/')
def home():
    with sqlite3.connect(DATABASE) as conn:
        c = conn.cursor()
        c.execute('SELECT id, title FROM questions')
        questions = c.fetchall()
    return render_template('home.html', questions=questions)

@app.route('/question/<int:id>')
def question(id):
    with sqlite3.connect(DATABASE) as conn:
        c = conn.cursor()
        c.execute('SELECT title, question FROM questions WHERE id = ?', (id,))
        question = c.fetchone()
        c.execute('SELECT answer FROM answers WHERE question_id = ?', (id,))
        answers = c.fetchall()
    return render_template('question.html', question=question, answers=answers)

@app.route('/add_question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        title = request.form['title']
        question = request.form['question']
        with sqlite3.connect(DATABASE) as conn:
            c = conn.cursor()
            c.execute('INSERT INTO questions (title, question, date_created) VALUES (?, ?, datetime("now"))', (title, question,))
            conn.commit()
        return redirect(url_for('home'))
    return render_template('add_question.html')

@app.route('/add_answer/<int:id>', methods=['GET', 'POST'])
def add_answer(id):
    if request.method == 'POST':
        answer = request.form['answer']
        with sqlite3.connect(DATABASE) as conn:
            c = conn.cursor()
            c.execute('INSERT INTO answers (answer, question_id, date_created) VALUES (?, ?, datetime("now"))', (answer, id,))
            conn.commit()
        return redirect(url_for('question', id=id))
    return render_template('add_answer.html')
