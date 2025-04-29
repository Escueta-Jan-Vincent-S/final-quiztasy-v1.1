import mysql.connector
from mysql.connector import Error

def test_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='final_quiztasy_db',
            user='root',
            password='1234'
        )

        if connection.is_connected():
            print("✅ Successfully connected to the database!")
            db_info = connection.server_info
            print("MySQL Server version:", db_info)
    except Error as e:
        print("❌ Error while connecting to MySQL:", e)
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("🔌 MySQL connection is closed.")

if __name__ == "__main__":
    test_connection()
