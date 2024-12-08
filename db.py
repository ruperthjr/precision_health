import os
import sqlite3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# SQLite connection setup
DATABASE_PATH = os.getenv('SQLITE_DB_PATH', 'precision_health.db')


def get_db_connection():
    """
    Establish a connection to the SQLite database.
    Returns:
        connection: SQLite connection object.
    """
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row  # To return dictionary-like rows
    return connection


def create_tables():
    """
    Create all necessary tables for the application if they don't exist.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Creating Users Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                age INTEGER,
                gender TEXT,
                height REAL,
                weight REAL,
                medical_conditions TEXT,
                health_goals TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Creating Activity Logs Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                activity_description TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')

        # Creating Plans Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                lifestyle_plan TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')

        # Creating Workouts Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS workouts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                workout_plan TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')

        # Creating Consultations Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS consultations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                question TEXT,
                response TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')

        # Creating Doctor Visits Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS doctor_visits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                visit_reason TEXT,
                appointment_date TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')

        # Creating Recommendations Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recommendations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                health_recommendation TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')

        conn.commit()


def save_user_activity(user_id, activity_description):
    """
    Logs user activity into the database for analytics purposes.

    Args:
        user_id (int): The ID of the user performing the activity.
        activity_description (str): A brief description of the user's activity.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO user_activities (user_id, activity_description)
                VALUES (?, ?)
            ''', (user_id, activity_description))
            conn.commit()
    except Exception as e:
        print(f"Error saving user activity: {e}")


def create_user(name, email, password, age, gender, height, weight, medical_conditions, health_goals):
    """
    Creates a new user in the database.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (name, email, password, age, gender, height, weight, medical_conditions, health_goals)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, email, password, age, gender, height, weight, medical_conditions, health_goals))
        conn.commit()


def get_user_by_email(email):
    """
    Fetches user details by email.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        return cursor.fetchone()


def update_user_info(user_email, updated_info):
    """
    Updates user information in the database.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            # Build dynamic SET clause for SQL query
            set_clause = ', '.join([f"{key} = ?" for key in updated_info.keys()])
            values = list(updated_info.values())
            cursor.execute(f'''
                UPDATE users
                SET {set_clause}
                WHERE email = ?
            ''', values + [user_email])
            
            conn.commit()
            return True
    except Exception as e:
        print(f"Error updating user info: {e}")
        return False


def create_plan(user_id, lifestyle_plan):
    """
    Creates a lifestyle plan for a user.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO user_plans (user_id, lifestyle_plan)
            VALUES (?, ?)
        ''', (user_id, lifestyle_plan))
        conn.commit()


def get_latest_plan(user_id):
    """
    Fetches the latest lifestyle plan for a user.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM user_plans WHERE user_id = ? ORDER BY created_at DESC LIMIT 1', (user_id,))
        return cursor.fetchone()


def create_workout(user_id, workout_plan):
    """
    Creates a workout plan for a user.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO workouts (user_id, workout_plan)
            VALUES (?, ?)
        ''', (user_id, workout_plan))
        conn.commit()


def get_latest_workout(user_id):
    """
    Fetches the latest workout plan for a user.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM workouts WHERE user_id = ? ORDER BY created_at DESC LIMIT 1', (user_id,))
        return cursor.fetchone()


def create_consultation_log(user_id, question, response):
    """
    Logs a user consultation.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO consultations (user_id, question, response)
            VALUES (?, ?, ?)
        ''', (user_id, question, response))
        conn.commit()


def get_consultation_log(user_id):
    """
    Fetches all consultations for a user.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM consultations WHERE user_id = ?', (user_id,))
        return cursor.fetchall()


def schedule_doctor_visit(user_id, visit_reason, appointment_date):
    """
    Schedules a doctor visit for a user.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO doctor_visits (user_id, visit_reason, appointment_date)
            VALUES (?, ?, ?)
        ''', (user_id, visit_reason, appointment_date))
        conn.commit()


def get_doctor_visits(user_id):
    """
    Fetches all doctor visits for a user.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM doctor_visits WHERE user_id = ? ORDER BY appointment_date', (user_id,))
        return cursor.fetchall()


def create_health_recommendation(user_id, recommend):
    """
    Creates a health recommendation for a user.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO recommendations (user_id, health_recommendation)
            VALUES (?, ?)
        ''', (user_id, recommend))
        conn.commit()


def get_health_recommendation_db(user_id):
    """
    Fetches the latest health recommendation for a user.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM recommendations WHERE user_id = ? ORDER BY created_at DESC LIMIT 1', (user_id,))
        return cursor.fetchone()
    
    

def get_user_health_data(user_id):
    """
    Fetches health-related data for the given user.

    Args:
        user_id (int): The ID of the user.

    Returns:
        dict: A dictionary containing the user's health-related data, including
              medical conditions, health goals, height, weight, etc.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT medical_conditions, health_goals, height, weight, age, gender, medications
                FROM users
                WHERE id = ?
            ''', (user_id,))
            result = cursor.fetchone()
            if result:
                return {
                    "medical_conditions": result["medical_conditions"],
                    "health_goals": result["health_goals"],
                    "height": result["height"],
                    "weight": result["weight"],
                    "age": result["age"],
                    "gender": result["gender"],
                    "medications": result["medications"] if result["medications"] else []  # Ensure it's a list
                }
            return {}
    except Exception as e:
        print(f"Error fetching user health data: {e}")
        return {}
    


# Initialize the database
create_tables()
