from flask import Blueprint, request, jsonify, session
from database import execute_query
from routes.auth import admin_required

categories_bp = Blueprint('categories', __name__)

def check_auth():
    """Check if user is authenticated"""
    return 'user_id' in session

@categories_bp.route('', methods=['GET'])
def get_categories():
    """Get all categories"""
    if not check_auth():
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        query = "SELECT * FROM categories ORDER BY name ASC"
        categories = execute_query(query, fetch=True)
        return jsonify({'success': True, 'data': categories}), 200
        
    except Exception as e:
        print(f"Get categories error: {e}")
        return jsonify({'success': False, 'message': 'Terjadi kesalahan server'}), 500

@categories_bp.route('/<int:category_id>', methods=['GET'])
def get_category(category_id):
    """Get single category by ID"""
    if not check_auth():
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        query = "SELECT * FROM categories WHERE id = %s"
        categories = execute_query(query, (category_id,), fetch=True)
        
        if categories and len(categories) > 0:
            return jsonify({'success': True, 'data': categories[0]}), 200
        else:
            return jsonify({'success': False, 'message': 'Kategori tidak ditemukan'}), 404
            
    except Exception as e:
        print(f"Get category error: {e}")
        return jsonify({'success': False, 'message': 'Terjadi kesalahan server'}), 500

@categories_bp.route('', methods=['POST'])
@admin_required
def create_category():
    """Create new category"""
    if not check_auth():
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        
        query = "INSERT INTO categories (name, description) VALUES (%s, %s)"
        params = (data.get('name'), data.get('description', ''))
        
        category_id = execute_query(query, params)
        
        if category_id:
            return jsonify({
                'success': True,
                'message': 'Kategori berhasil ditambahkan',
                'id': category_id
            }), 201
        else:
            return jsonify({'success': False, 'message': 'Gagal menambahkan kategori'}), 500
            
    except Exception as e:
        print(f"Create category error: {e}")
        return jsonify({'success': False, 'message': 'Terjadi kesalahan server'}), 500

@categories_bp.route('/<int:category_id>', methods=['PUT'])
@admin_required
def update_category(category_id):
    """Update category"""
    if not check_auth():
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        
        query = "UPDATE categories SET name = %s, description = %s WHERE id = %s"
        params = (data.get('name'), data.get('description'), category_id)
        
        execute_query(query, params)
        
        return jsonify({
            'success': True,
            'message': 'Kategori berhasil diupdate'
        }), 200
            
    except Exception as e:
        print(f"Update category error: {e}")
        return jsonify({'success': False, 'message': 'Terjadi kesalahan server'}), 500

@categories_bp.route('/<int:category_id>', methods=['DELETE'])
@admin_required
def delete_category(category_id):
    """Delete category"""
    if not check_auth():
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        query = "DELETE FROM categories WHERE id = %s"
        execute_query(query, (category_id,))
        
        return jsonify({
            'success': True,
            'message': 'Kategori berhasil dihapus'
        }), 200
            
    except Exception as e:
        print(f"Delete category error: {e}")
        return jsonify({'success': False, 'message': 'Terjadi kesalahan server'}), 500
