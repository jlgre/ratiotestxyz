from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Testimonial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    author = db.Column(db.String(50))

    def __repr__(self):
        return '<Task %r>' %self.id

@app.route('/', methods=['POST','GET'])
def index():
    message='waiting...'
    if request.method == 'POST':
        ss=request.form['summand']
        ratio(ss)
    else:
        return render_template('index.html')

'''
@app.route('/delete/<int:id>')
def delete(id):
    taskDel = Todo.query.get_or_404(id)
    try:
        db.session.delete(taskDel)
        db.session.commit()
        return redirect('/')
    except:
        return 'delete failed'


@app.route('/update/<int:id>', methods=['POST','GET'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content=request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            'update failed'
    else:
        return render_template('update.html', task=task)
'''
if __name__ == "__main__":
    app.run(debug=True)
