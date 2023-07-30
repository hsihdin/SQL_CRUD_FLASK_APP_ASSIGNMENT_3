from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

# Helper function to establish a connection to the database
def get_db_connection():
    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create the student table if it doesn't exist
def create_student_table():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS student (
            student_id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            dob TEXT NOT NULL,
            amount_due REAL
        )
    ''')
    conn.close()

# Route to create a new student record
@app.route('/students', methods=['POST'])
def create_student():
    student_id = request.form.get("student_id")
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    dob = request.form.get("dob")
    amount_due = float(request.form.get("amount_due"))

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO student (student_id, first_name, last_name, dob, amount_due)
            VALUES (?, ?, ?, ?, ?)
        ''', (student_id, first_name, last_name, dob, amount_due))
        conn.commit()
        conn.close()

        # Redirect to the success page
        return redirect(url_for('student_added_successfully'))
    except Exception as e:
        return "An error occurred", 500

# Route to show the success page after adding a student
@app.route('/students/success', methods=['GET'])
def student_added_successfully():
    return render_template('index.html', success_message="Student added successfully")

# Route to read a specific student record by student_id
@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM student WHERE student_id = ?', (student_id,))
        student = cursor.fetchone()
        conn.close()

        if student:
            return render_template('student_details.html', student=student)
        else:
            return "Student not found", 404
    except Exception as e:
        return "An error occurred", 500

# Route to show all student records
# Route to show all student records
@app.route('/students/list', methods=['GET'])
def list_students():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM student')
        students = cursor.fetchall()
        conn.close()

        return render_template('list_students.html', students=students)
    except Exception as e:
        error_message = "An error occurred: " + str(e)
        return render_template('error.html', error_message=error_message)



# Route for updating a student record

@app.route('/students/update/<int:student_id>/edit', methods=['GET', 'POST'])
def update_student(student_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        if request.method == 'POST':
            first_name = request.form.get("first_name")
            last_name = request.form.get("last_name")
            dob = request.form.get("dob")
            amount_due = float(request.form.get("amount_due"))

            cursor.execute('''
                UPDATE student
                SET first_name = ?, last_name = ?, dob = ?, amount_due = ?
                WHERE student_id = ?
            ''', (first_name, last_name, dob, amount_due, student_id))
            conn.commit()

            # Redirect to the student details page after update
            return redirect(url_for('list_students', success_message="Student record updated successfully"))

        cursor.execute('SELECT * FROM student WHERE student_id = ?', (student_id,))
        student = cursor.fetchone()
        conn.close()

        if student:
            return render_template('update_student.html', student=student)
        else:
            return "Student not found", 404

    except Exception as e:
        error_message = "An error occurred: " + str(e)
        return render_template('error.html', error_message=error_message)


# Route to delete a student record by student_id
@app.route('/students/delete/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Execute the DELETE operation
        cursor.execute('DELETE FROM student WHERE student_id = ?', (student_id,))

        # Check if any rows were affected
        if cursor.rowcount > 0:
            conn.commit()
            conn.close()
            return redirect(url_for('list_students', success_message="Student record deleted successfully"))
        else:
            conn.rollback()  # Rollback the transaction since no rows were deleted
            conn.close()
            return "Student record not found", 404

    except Exception as e:
        error_message = "An error occurred: " + str(e)
        return render_template('error.html', error_message=error_message)
# Route to serve the index.html file
@app.route('/')
def index():
    return render_template('index.html')

# Run the Flask app
if __name__ == '__main__':
    create_student_table()
    app.run(debug=True)
