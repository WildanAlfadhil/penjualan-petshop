import hashlib
from database import execute_query

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def reset_password():
    new_password = 'staff123'
    hashed_password = hash_password(new_password)
    
    # Update password for staff1
    query = "UPDATE users SET password = %s WHERE username = %s"
    # execute_query returns last_id for INSERT/UPDATE, we don't need it but we need to ensure commit
    # execute_query in database.py commits automatically if fetch=False
    execute_query(query, (hashed_password, 'staff1'), fetch=False)
    
    print(f"Password for 'staff1' has been reset to '{new_password}'")

if __name__ == "__main__":
    reset_password()
