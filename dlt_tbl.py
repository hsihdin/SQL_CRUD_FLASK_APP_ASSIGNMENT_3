import sqlite3

def select_all_students():
    try:
        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM student')
        students = cursor.fetchall()
        conn.close()
        return students
    except Exception as e:
        print("Error:", e)
        return []

if __name__ == '__main__':
    # Example usage:
    students = select_all_students()
    for student in students:
        print(student)


