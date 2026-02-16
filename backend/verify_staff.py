import hashlib
from database import execute_query

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def check_users():
    users = execute_query("SELECT id, username, password, role FROM users", fetch=True)
    with open("users.txt", "w") as f:
        f.write("Users in database:\n")
        if not users:
            f.write("No users found.\n")
            return
            
        for user in users:
            f.write(f"ID: {user['id']}, Username: {user['username']}, Role: {user['role']}\n")
            f.write(f"Stored Hash: {user['password']}\n")
            
            # Check common passwords
            common_passwords = ['staff', 'staff1', 'staff123', '123456', 'password', 'admin123']
            found = False
            for pwd in common_passwords:
                if hash_password(pwd) == user['password']:
                    f.write(f"  [MATCH] Password is: '{pwd}'\n")
                    found = True
                    break
            if not found:
                 f.write("  [NO MATCH] Password not found in common list\n")

if __name__ == "__main__":
    check_users()

