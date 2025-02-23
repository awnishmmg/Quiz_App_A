import sqlite3
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

# Database connection
def getConnection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def initialise_db():
    with getConnection() as conn:
        print('-----------Database Initialised--------------')
        
        # Create the 'admin' table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS admin (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        
        # Create the 'users' table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fullname TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL,
                qualification TEXT NOT NULL,
                dob TEXT NOT NULL,
                token TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT '1'
            )
        ''')

        # create the Subject 
        conn.execute('''
                CREATE TABLE IF NOT EXISTS subject (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                difficulty_level TEXT NOT NULL CHECK(difficulty_level IN ('easy', 'medium', 'hard')))
            ''')
        # create the chapter
        conn.execute('''
            CREATE TABLE IF NOT EXISTS chapter(
                id INTEGER primary key autoincrement,
                name text not null,
                description text not null,
                subject_id integer null
                )
        ''')


       

        # create the Quiz
        conn.execute('''
            CREATE TABLE IF NOT EXISTS quiz(
                id INTEGER primary key autoincrement,
                name text not null,
                description text not null,
                chapter_id integer null,
                start_date text null,
                end_date text null,
                status text null,
                time_duration text null,
                remarks text null     
                )
        ''')

        #create the questions
        conn.execute('''
            CREATE TABLE IF NOT EXISTS questions(
                id INTEGER primary key autoincrement,
                quiz_id integer not null,
                question text not null,
                option_1 text null,
                option_2 text null,
                option_3 text null,
                option_4 text null,
                correct_option integer not null,
                correct_mark integer not null DEFAULT '1',
                wrong_mark integer not null default '0'     
                )
        ''')

        #create the scores 
        conn.execute('''
            CREATE TABLE IF NOT EXISTS scores(
                id INTEGER primary key autoincrement,
                quiz_id integer not null,
                question_id integer not null,
                user_id integer not null,
                attempted_option integer null,
                scored_mark text not null default '0'     
                )
        ''')

def create_admin(admin_email,admin_password):
    """ Check if admin exists, if not create one """
    conn = getConnection()
    cursor = conn.cursor()

    # Check if admin exists
    cursor.execute("SELECT * FROM admin WHERE email = ?", (admin_email,))
    admin = cursor.fetchone()

    if not admin:
        hashed_password = bcrypt.generate_password_hash(admin_password).decode('utf-8')
        cursor.execute("INSERT INTO admin (email, password) VALUES (?, ?)",
                       (admin_email, hashed_password))
        conn.commit()
        print("✅ Admin user created!")
    else:
        print("ℹ️ Admin already exists.")
    conn.close()


def validateAdmin(email):
    conn = getConnection()
    cursor = conn.cursor()

    isAdmin = False

    if "admin" in email.lower():  # Check if "admin" is in the email
        cursor.execute("SELECT * FROM admin WHERE email = ?", (email,))
        isAdmin = True
    else:
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    
    user = cursor.fetchone()
    conn.close()
    return [user,isAdmin]


def create_user(data):
        
        # Get data from the user
        conn = getConnection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (fullname, email, password, qualification, dob,token,status) VALUES (?, ?, ?, ?, ?,?,?)",
                (data['fullname'], data['email'], data['password'], data['qualification'], data['dob'],'',1)
            )
            conn.commit()
        except Exception as e:
            print(f"Error: {str(e)}")
            return False
        finally:
            conn.close()
            return True

def get_users_list():
        
        # Get data from the user
        conn = getConnection()
        cursor = conn.cursor()
        # Fetch all users
        cursor.execute("SELECT id, fullname, email, qualification, dob FROM users ORDER BY id DESC")
        users = cursor.fetchall()
        conn.close()

        return users

def get_user_details(user_id):
    conn = getConnection()
    cursor = conn.cursor()

    # Fetch user details
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    return user

def getuser_count():
     conn = getConnection()
     cursor = conn.cursor()

     #Get User Count
     cursor.execute("SELECT count(*) as user_count from users")
     row = cursor.fetchone()
     user_count = row[0]
     conn.close()

     return user_count


def delete_user(user_id):
    conn = getConnection()
    cursor = conn.cursor()

    try:
        #connection cursor
        cursor.execute("Delete from users where id=?",(user_id,))
        conn.commit()
    except Exception as e:
        print(f"Error: {str(e)}")
        return False
    finally:
        conn.close()
        return True

def update_user_details(user_id,updated_user):
    conn = getConnection()
    cursor = conn.cursor()

    sql = ''' update users set fullname=?,email=?,
                         qualification=?,dob=? where id=?
                         '''
    try: #cursor Object has been created.
        cursor.execute(sql,(updated_user['fullname'],updated_user['email'],updated_user['qualification'],
                         updated_user['dob'],user_id)
                        )
        print(sql)
        conn.commit()
        return False
    except Exception as e:
        print(f'Exception : {str(e)}')
        return False
    finally: 
        conn.close()
        return True

def model_subject_add(subject):
    conn = getConnection()
    cursor = conn.cursor()

    sql = '''
        Insert into subject(name,description,difficulty_level) values(?,?,?)
    '''
    cursor.execute(sql,(subject['name'],subject['description'],subject['difficulty_level']))
    
    try:
         print(sql)
         conn.commit()
    except Exception as e:
         print(f'Exception Error {str(e)}')
         return False
    finally:
         conn.close()
         return True
     
def model_get_subjects():
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute('select * from subject order by id desc')
    subjects = cursor.fetchall()
    return subjects

def model_get_subject_count():
     conn = getConnection()
     cursor = conn.cursor()

     #Get User Count
     cursor.execute("SELECT count(*) as subject_count from subject")
     row = cursor.fetchone()
     subject_count = row[0]
     conn.close()

     return subject_count

def model_delete_subject(subject_id):
    conn = getConnection()
    cursor = conn.cursor()

    cursor.execute('delete from subject where id=?',(subject_id,))
    try:
        conn.commit()
    except Exception as e:
        print(f'Exception Error {str(e)}')
        return True
    finally:
        conn.close()
        return True
    
def model_get_subjects_details(subject_id):
     conn = getConnection()
     cursor = conn.cursor()

     cursor.execute('select * from subject where id=?',(subject_id,))
     subject = cursor.fetchone()
     conn.close()
     return subject

def model_subject_updated(subject_id,subject):
    conn = getConnection()
    cursor = conn.cursor()

    cursor.execute('update subject set name=?,description=?,difficulty_level=? where id=?',(
         subject['name'],subject['description'],subject['difficulty_level'],subject_id
    ))

    try:
         conn.commit()
    except Exception as e:
         print(f'Exception Error {str(e)}')
         return False
    finally:
         conn.close()
         return True
    
#----------------------------------------Chapter Models-----------------------
def modal_chapter_create(chapter):
     conn = getConnection()
     cursor = conn.cursor()
     cursor.execute('''
        Insert into chapter(name,description,subject_id) values(?,?,?)
    ''',(chapter['name'],chapter['description'],chapter['subject_id']))

     try:
          conn.commit()
     except Exception as e:
          print(f'Exception Error {str(e)}')
          return False
     finally:
          conn.close()
          return True
     
def modal_chapter_getAll():
     conn = getConnection()
     cursor = conn.cursor()
     cursor.execute('''
        select * from chapter order by id desc
    ''')
     
     chapters = cursor.fetchall()
     return chapters

def model_delete_chapter(chapter_id):
    conn = getConnection()
    cursor = conn.cursor()

    cursor.execute('delete from chapter where id=?',(chapter_id,))
    try:
        conn.commit()
    except Exception as e:
        print(f'Exception Error {str(e)}')
        return True
    finally:
        conn.close()
        return True
    
def model_get_chapter_details(chapter_id):
     conn = getConnection()
     cursor = conn.cursor()

     cursor.execute('select * from chapter where id=?',(chapter_id,))
     chapter = cursor.fetchone()
     return chapter


def model_chapter_updated(chapter_id,chapter):
    conn = getConnection()
    cursor = conn.cursor()

    cursor.execute('update chapter set name=?,description=?,subject_id=? where id=?',(
         chapter['name'],chapter['description'],chapter['subject_id'],chapter_id
    ))

    try:
         conn.commit()
    except Exception as e:
         print(f'Exception Error {str(e)}')
         return False
    finally:
         conn.close()
         return True


def model_get_chapter_count():
     conn = getConnection()
     cursor = conn.cursor()

     #Get User Count
     cursor.execute("SELECT count(*) as chapter_count from subject")
     row = cursor.fetchone()
     chapter_count = row[0]
     conn.close()

     return chapter_count

#----------------------------------------Quiz Models-----------------------

def model_quiz_create(quiz):
    conn = getConnection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO quiz (name, description, chapter_id, start_date, end_date, status, time_duration, remarks)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        quiz['name'], quiz['description'], quiz['chapter_id'], 
        quiz['start_date'], quiz['end_date'], quiz['status'], 
        quiz['time_duration'], quiz['remarks']
    ))

    try:
        conn.commit()
    except Exception as e:
        print(f'Exception Error {str(e)}')
        return False
    finally:
        conn.close()
        return True
    

def model_quiz_getAll():
    conn = getConnection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM quiz ORDER BY id DESC
    ''')
    
    quizzes = cursor.fetchall()
    conn.close()
    
    return quizzes


def model_delete_quiz(quiz_id):
    conn = getConnection()
    cursor = conn.cursor()

    cursor.execute('DELETE FROM quiz WHERE id=?', (quiz_id,))
    
    try:
        conn.commit()
    except Exception as e:
        print(f'Exception Error {str(e)}')
        return False
    finally:
        conn.close()
        return True
    

def model_get_quiz_details(quiz_id):
    conn = getConnection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM quiz WHERE id=?', (quiz_id,))
    quiz = cursor.fetchone()
    conn.close()

    return quiz


def model_quiz_update(quiz_id, quiz):
    conn = getConnection()
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE quiz SET name=?, description=?, chapter_id=?, 
        start_date=?, end_date=?, status=?, time_duration=?, remarks=?
        WHERE id=?
    ''', (
        quiz['name'], quiz['description'], quiz['chapter_id'], 
        quiz['start_date'], quiz['end_date'], quiz['status'], 
        quiz['time_duration'], quiz['remarks'], quiz_id
    ))

    try:
        conn.commit()
    except Exception as e:
        print(f'Exception Error {str(e)}')
        return False
    finally:
        conn.close()
        return True


def model_get_quiz_count():
    conn = getConnection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) AS quiz_count FROM quiz")
    row = cursor.fetchone()
    quiz_count = row[0] if row else 0
    conn.close()

    return quiz_count

# ---------------------------------- Question Model Methods --------------------------------------------

def model_question_create(question):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO questions (quiz_id, question, option_1, option_2, option_3, option_4, correct_option, correct_mark, wrong_mark) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        question['quiz_id'], question['question'], question['option_1'], question['option_2'], 
        question['option_3'], question['option_4'], question['correct_option'], 
        question['correct_mark'], question['wrong_mark']
    ))

    try:
        conn.commit()
    except Exception as e:
        print(f'Exception Error {str(e)}')
        return False
    finally:
        conn.close()
        return True


def model_question_getAll():
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM questions ORDER BY id DESC
    ''')
    questions = cursor.fetchall()
    conn.close()
    return questions


def model_get_question_details(question_id):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM questions WHERE id=?', (question_id,))
    question = cursor.fetchone()
    conn.close()
    return question


def model_question_update(question_id, question):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE questions 
        SET quiz_id=?, question=?, option_1=?, option_2=?, option_3=?, option_4=?, correct_option=?, correct_mark=?, wrong_mark=?
        WHERE id=?
    ''', (
        question['quiz_id'], question['question'], question['option_1'], question['option_2'], 
        question['option_3'], question['option_4'], question['correct_option'], 
        question['correct_mark'], question['wrong_mark'], question_id
    ))

    try:
        conn.commit()
    except Exception as e:
        print(f'Exception Error {str(e)}')
        return False
    finally:
        conn.close()
        return True


def model_question_delete(question_id):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM questions WHERE id=?', (question_id,))
    
    try:
        conn.commit()
    except Exception as e:
        print(f'Exception Error {str(e)}')
        return False
    finally:
        conn.close()
        return True

def model_get_question_count():
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM questions')
    count = cursor.fetchone()[0]  # Fetch the count value
    conn.close()
    return count