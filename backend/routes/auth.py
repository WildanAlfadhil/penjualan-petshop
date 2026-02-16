from flask import Blueprint, request, jsonify, session
from database import execute_query
import hashlib

auth_bp = Blueprint('auth', __name__)


from functools import wraps

def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'role' not in session or session['role'] != 'admin':
            return jsonify({'success': False, 'message': 'Unauthorized: Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login endpoint"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'success': False, 'message': 'Username dan password harus diisi'}), 400
        
        # Hash the password
        hashed_password = hash_password(password)
        
        # Query user from database
        query = "SELECT id, username, full_name, email, role FROM users WHERE username = %s AND password = %s"
        users = execute_query(query, (username, hashed_password), fetch=True)
        
        if users and len(users) > 0:
            user = users[0]
            # Store user info in session
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['full_name'] = user['full_name']
            session['role'] = user['role']
            
            return jsonify({
                'success': True,
                'message': 'Login berhasil',
                'user': {
                    'id': user['id'],
                    'username': user['username'],
                    'full_name': user['full_name'],
                    'email': user['email'],
                    'role': user['role']
                }
            }), 200
        else:
            return jsonify({'success': False, 'message': 'Username atau password salah'}), 401
            
    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({'success': False, 'message': 'Terjadi kesalahan server'}), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Logout endpoint"""
    try:
        session.clear()
        return jsonify({'success': True, 'message': 'Logout berhasil'}), 200
    except Exception as e:
        print(f"Logout error: {e}")
        return jsonify({'success': False, 'message': 'Terjadi kesalahan server'}), 500

@auth_bp.route('/check', methods=['GET'])
def check_auth():
    """Check if user is authenticated"""
    if 'user_id' in session:
        return jsonify({
            'authenticated': True,
            'user': {
                'id': session['user_id'],
                'username': session['username'],
                'full_name': session['full_name'],
                'role': session['role']
            }
        }), 200
    else:
        return jsonify({'authenticated': False}), 401
