from datetime import datetime
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os



db_path = os.path.join(os.getcwd(), 'test.db')


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id
    
@app.route('/', methods=['GET', 'POST'])
def index():
    #return render_template('index.html')
    if request.method == 'POST':
        task_content = request.form['content']

        print(f"Task content: {task_content}")  # Add this line for debugging
        new_task = Todo(content=task_content)

        print(f"Task content: {new_task}")  # Add this line for debugging

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        #return render_template('index.html')
        except:
            return 'There was an issue adding your task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)
        #return render_template('index.html')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('update.html', task=task)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

if __name__ == '__main__':
    with app.app_context():  # Ensure this is within the app context
        db.create_all()  # This will create the database tables
        print("Database tables created")
        if os.path.exists('test.db'):
            print("Database file 'test.db' created successfully")
        else:
            print("Failed to create database file 'test.db'")
        app.run(debug=True)