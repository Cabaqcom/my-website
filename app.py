from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# 仮のデータベース（リストで保存）
questions = []

@app.route('/')
def index():
    return render_template('index.html', questions=questions)

@app.route('/ask', methods=['GET', 'POST'])
def ask():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        question = {
            'id': len(questions) + 1,
            'title': title,
            'content': content,
            'answers': [],
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        questions.append(question)
        return redirect(url_for('index'))
    return render_template('ask.html')

@app.route('/question/<int:question_id>', methods=['GET', 'POST'])
def question_detail(question_id):
    question = next((q for q in questions if q['id'] == question_id), None)
    if request.method == 'POST':
        answer = request.form['answer']
        question['answers'].append({
            'content': answer,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M')
        })
        return redirect(url_for('question_detail', question_id=question_id))
    return render_template('question.html', question=question)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
