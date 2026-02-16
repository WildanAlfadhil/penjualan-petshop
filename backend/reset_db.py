import mysql.connector
from config import Config
import os

def reset_database():
    print("Connecting to MySQL server...")
    try:
        # Connect without database first to drop/create it
        connection = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            port=Config.DB_PORT
        )
        cursor = connection.cursor()
        
        # Read schema file
        schema_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'petshop_schema.sql')
        print(f"Reading schema from {schema_path}...")
        
        with open(schema_path, 'r') as f:
            schema_sql = f.read()
            
        print("Executing schema...")
        # Execute schema commands
        for result in cursor.execute(schema_sql, multi=True):
            pass
            
        connection.commit()
        cursor.close()
        connection.close()
        print("Database reset successfully! Password hashes updated.")
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    reset_database()
