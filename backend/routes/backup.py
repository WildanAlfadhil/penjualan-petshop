from flask import Blueprint, jsonify, session, send_file
from database import get_db_connection
from routes.auth import admin_required
import os
from datetime import datetime

backup_bp = Blueprint('backup', __name__)

def check_auth():
    """Check if user is authenticated"""
    return 'user_id' in session

@backup_bp.route('/create', methods=['POST'])
@admin_required
def create_backup():
    """Create database backup"""
    if not check_auth():
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({'success': False, 'message': 'Database connection error'}), 500
        
        cursor = connection.cursor()
        
        # Create backup directory if not exists
        backup_dir = os.path.join(os.path.dirname(__file__), '..', 'backups')
        os.makedirs(backup_dir, exist_ok=True)
        
        # Generate backup filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = os.path.join(backup_dir, f'petshop_backup_{timestamp}.sql')
        
        # Get all tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(f"-- Pet Shop Database Backup\n")
            f.write(f"-- Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"USE petshop;\n\n")
            
            for table_tuple in tables:
                table = table_tuple[0]
                
                # Get table structure
                cursor.execute(f"SHOW CREATE TABLE `{table}`")
                create_table = cursor.fetchone()[1]
                f.write(f"-- Table: {table}\n")
                f.write(f"DROP TABLE IF EXISTS `{table}`;\n")
                f.write(f"{create_table};\n\n")
                
                # Get table data
                cursor.execute(f"SELECT * FROM `{table}`")
                rows = cursor.fetchall()
                
                if rows:
                    # Get column names
                    cursor.execute(f"SHOW COLUMNS FROM `{table}`")
                    columns = [col[0] for col in cursor.fetchall()]
                    
                    f.write(f"-- Data for table: {table}\n")
                    for row in rows:
                        values = []
                        for value in row:
                            if value is None:
                                values.append('NULL')
                            elif isinstance(value, str):
                                # Escape single quotes
                                escaped_value = value.replace("'", "''")
                                values.append(f"'{escaped_value}'")
                            elif isinstance(value, (datetime)):
                                values.append(f"'{value}'")
                            else:
                                values.append(str(value))
                        
                        values_str = ', '.join(values)
                        columns_str = ', '.join([f"`{col}`" for col in columns])
                        f.write(f"INSERT INTO `{table}` ({columns_str}) VALUES ({values_str});\n")
                    
                    f.write("\n")
        
        cursor.close()
        connection.close()
        
        return jsonify({
            'success': True,
            'message': 'Backup berhasil dibuat',
            'filename': f'petshop_backup_{timestamp}.sql'
        }), 200
        
    except Exception as e:
        print(f"Backup error: {e}")
        return jsonify({'success': False, 'message': f'Terjadi kesalahan: {str(e)}'}), 500

@backup_bp.route('/list', methods=['GET'])
def list_backups():
    """List all backup files"""
    if not check_auth():
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        backup_dir = os.path.join(os.path.dirname(__file__), '..', 'backups')
        
        if not os.path.exists(backup_dir):
            return jsonify({'success': True, 'data': []}), 200
        
        backups = []
        for filename in os.listdir(backup_dir):
            if filename.endswith('.sql'):
                filepath = os.path.join(backup_dir, filename)
                file_stats = os.stat(filepath)
                backups.append({
                    'filename': filename,
                    'size': file_stats.st_size,
                    'created_at': datetime.fromtimestamp(file_stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                })
        
        # Sort by creation time, newest first
        backups.sort(key=lambda x: x['created_at'], reverse=True)
        
        return jsonify({'success': True, 'data': backups}), 200
        
    except Exception as e:
        print(f"List backups error: {e}")
        return jsonify({'success': False, 'message': 'Terjadi kesalahan server'}), 500
