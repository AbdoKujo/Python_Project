from app import db
from flask import current_app
import pymysql
import logging

def get_db_connection():
    """Get a raw database connection"""
    try:
        connection = pymysql.connect(
            host=current_app.config['DB_HOST'],
            user=current_app.config['DB_USER'],
            password=current_app.config['DB_PASSWORD'],
            database=current_app.config['DB_NAME'],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except Exception as e:
        logging.error(f"Database connection error: {str(e)}")
        raise

def execute_query(query, params=None, fetch=True):
    """Execute a raw SQL query"""
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params or ())
            if fetch:
                return cursor.fetchall()
            connection.commit()
            return cursor.rowcount
    except Exception as e:
        connection.rollback()
        logging.error(f"Query execution error: {str(e)}")
        raise
    finally:
        connection.close()

def init_db():
    """Initialize the database"""
    db.create_all()
    logging.info("Database tables created")

