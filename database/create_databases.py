import pymysql
import getpass

# Prompt for MySQL root password
password = getpass.getpass("Enter MySQL root password: ")

# Connect to MySQL server (without specifying a database)
connection = pymysql.connect(
    host='localhost',
    user='root',
    password=password,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

try:
    with connection.cursor() as cursor:
        # Create the databases
        databases = ['flask_app_dev', 'flask_app_test', 'flask_app_prod']
        
        for db_name in databases:
            try:
                cursor.execute(f"CREATE DATABASE {db_name}")
                print(f"Database '{db_name}' created successfully.")
            except pymysql.err.ProgrammingError:
                # Database already exists
                print(f"Database '{db_name}' already exists.")
                
finally:
    connection.close()
    print("Database creation completed.")