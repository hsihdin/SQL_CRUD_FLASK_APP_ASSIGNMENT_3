from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
db = SQLAlchemy(app)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    amount_due = db.Column(db.Float, default=0.0)

    def __init__(self, first_name, last_name, dob, amount_due):
        self.first_name = first_name
        self.last_name = last_name
        self.dob = dob
        self.amount_due = amount_due


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        dob_str = request.form['dob']
        dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
        amount_due = float(request.form['amountDue'])

        new_student = Student(first_name=first_name, last_name=last_name, dob=dob, amount_due=amount_due)
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        students = Student.query.all()
        return render_template('index.html', students=students)


@app.route('/update/<int:student_id>', methods=['GET', 'POST'])
def update_student(student_id):
    student = Student.query.get_or_404(student_id)
    if request.method == 'POST':
        student.first_name = request.form['firstName']
        student.last_name = request.form['lastName']
        dob_str = request.form['dob']
        student.dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
        student.amount_due = float(request.form['amountDue'])
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('update_student.html', student=student)


@app.route('/delete/<int:student_id>', methods=['GET', 'POST'])
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    if request.method == 'POST':
        db.session.delete(student)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('delete_student.html', student=student)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
