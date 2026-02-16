import mysql.connector
from config import Config

def check_db():
    print("Checking database connection...")
    try:
        connection = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME,
            port=Config.DB_PORT
        )
        
        if connection.is_connected():
            print("✅ Connection Successful!")
            print(f"Connected to: {Config.DB_NAME} at {Config.DB_HOST}")
            
            cursor = connection.cursor(dictionary=True)
            
            # Check tables
            print("\nChecking tables...")
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            table_names = [list(t.values())[0] for t in tables]
            print(f"Tables found: {', '.join(table_names)}")
            
            required_tables = ['users', 'products', 'categories', 'transactions', 'transaction_details', 'customers']
            missing = [t for t in required_tables if t not in table_names]
            
            if missing:
                print(f"❌ MISSING TABLES: {missing}")
            else:
                print("✅ All required tables present.")
                
            # Check content
            print("\nChecking row counts:")
            for table in required_tables:
                if table in table_names:
                    cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
                    count = cursor.fetchall()[0]['count']
                    print(f"- {table}: {count} rows")
                    
            cursor.close()
            connection.close()
            
    except mysql.connector.Error as e:
        print(f"❌ DATABASE ERROR: {e}")
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    check_db()
