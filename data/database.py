import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    try:
        import streamlit as st
        conn = psycopg2.connect(
            host=st.secrets["DB_HOST"],
            port=st.secrets["DB_PORT"],
            database=st.secrets["DB_NAME"],
            user=st.secrets["DB_USER"],
            password=st.secrets["DB_PASSWORD"]
        )
        return conn
    except Exception:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        return conn

def create_tables():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS exams (
                id SERIAL PRIMARY KEY,
                source VARCHAR(50) NOT NULL,
                exam_name TEXT NOT NULL,
                apply_last_date DATE,
                exam_date DATE,
                notification_url TEXT,
                scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        cursor.close()
        conn.close()
        print("Tables created successfully")

    except Exception as e:
        print(f"Error: {e}")

def cleanup_expired_exams():
    """
    Delete exams where the last date to apply has passed.
    Keeps database clean by removing outdated exam listings.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM exams
            WHERE apply_last_date < CURRENT_DATE
        """)

        deleted_count = cursor.rowcount
        conn.commit()
        cursor.close()
        conn.close()

        if deleted_count > 0:
            print(f"Cleaned up {deleted_count} expired exams from database")
        return deleted_count

    except Exception as e:
        print(f"Cleanup error: {e}")
        return 0

def get_applicable_exams():
    """
    Get all exams where the application deadline hasn't passed yet.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, source, exam_name, apply_last_date, exam_date, notification_url
            FROM exams
            WHERE apply_last_date >= CURRENT_DATE
            ORDER BY apply_last_date ASC
        """)

        applicable = cursor.fetchall()

        cursor.execute("""
            SELECT COUNT(*) FROM exams
            WHERE apply_last_date < CURRENT_DATE
        """)

        expired_count = cursor.fetchone()[0]
        cursor.close()
        conn.close()

        return {
            "applicable": applicable,
            "applicable_count": len(applicable),
            "expired_count": expired_count,
            "total_count": len(applicable) + expired_count
        }

    except Exception as e:
        print(f"Error fetching applicable exams: {e}")
        return {"applicable": [], "applicable_count": 0, "expired_count": 0, "total_count": 0}

if __name__ == "__main__":
    create_tables()


# import psycopg2
# import os
# from dotenv import load_dotenv
# from datetime import datetime

# load_dotenv()
# def get_connection():
#     conn = psycopg2.connect(
#         host=os.getenv("DB_HOST"),
#         port=os.getenv("DB_PORT"),
#         database=os.getenv("DB_NAME"),
#         user=os.getenv("DB_USER"),
#         password=os.getenv("DB_PASSWORD")
#     )
#     return conn

# def create_tables():
#     try:
#         conn = get_connection()
#         cursor = conn.cursor()

#         cursor.execute("""
#             CREATE TABLE IF NOT EXISTS exams (
#                 id SERIAL PRIMARY KEY,
#                 source VARCHAR(50) NOT NULL,
#                 exam_name TEXT NOT NULL,
#                 apply_last_date DATE,
#                 exam_date DATE,
#                 notification_url TEXT,
#                 scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#             )
#         """)

#         conn.commit()
#         cursor.close()
#         conn.close()
#         print("Tables created successfully")

#     except Exception as e:
#         print(f"Error: {e}")

# def cleanup_expired_exams():
#     """
#     Delete exams where the last date to apply has passed.
#     Keeps database clean by removing outdated exam listings.
#     """
#     try:
#         conn = get_connection()
#         cursor = conn.cursor()
        
#         # Delete exams where apply_last_date is in the past
#         cursor.execute("""
#             DELETE FROM exams
#             WHERE apply_last_date < CURRENT_DATE
#         """)
        
#         deleted_count = cursor.rowcount
#         conn.commit()
#         cursor.close()
#         conn.close()
        
#         if deleted_count > 0:
#             print(f"Cleaned up {deleted_count} expired exams from database")
#         return deleted_count
        
#     except Exception as e:
#         print(f"Cleanup error: {e}")
#         return 0

# def get_applicable_exams():
#     """
#     Get all exams where the application deadline hasn't passed yet.
#     Returns both applicable and expired exams with count summary.
#     """
#     try:
#         conn = get_connection()
#         cursor = conn.cursor()
        
#         # Get applicable exams (apply_last_date >= today)
#         cursor.execute("""
#             SELECT id, source, exam_name, apply_last_date, exam_date, notification_url
#             FROM exams
#             WHERE apply_last_date >= CURRENT_DATE
#             ORDER BY apply_last_date ASC
#         """)
        
#         applicable = cursor.fetchall()
        
#         # Get expired exams count
#         cursor.execute("""
#             SELECT COUNT(*) FROM exams
#             WHERE apply_last_date < CURRENT_DATE
#         """)
        
#         expired_count = cursor.fetchone()[0]
        
#         cursor.close()
#         conn.close()
        
#         return {
#             "applicable": applicable,
#             "applicable_count": len(applicable),
#             "expired_count": expired_count,
#             "total_count": len(applicable) + expired_count
#         }
        
#     except Exception as e:
#         print(f"Error fetching applicable exams: {e}")
#         return {"applicable": [], "applicable_count": 0, "expired_count": 0, "total_count": 0}

# if __name__ == "__main__":
#     create_tables()