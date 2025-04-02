# Create a new file: c:\Users\abdoa\Downloads\flask-mysql-mvc (1)\drop_databases.py
import pymysql
import getpass

# Connect to MySQL server (without specifying a database)
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',  # Leave blank if you have no password
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

try:
    with connection.cursor() as cursor:
        # Drop the databases if they exist
        databases = ['flask_app_dev', 'flask_app_test', 'flask_app_prod']
        
        for db_name in databases:
            try:
                cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")
                print(f"Database '{db_name}' dropped successfully.")
            except pymysql.err.ProgrammingError as e:
                print(f"Error dropping '{db_name}': {e}")
finally:
    connection.close()
    print("Database cleanup completed.")
