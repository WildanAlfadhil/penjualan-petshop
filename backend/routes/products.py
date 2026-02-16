from flask import Blueprint, request, jsonify, session
from database import execute_query
from routes.auth import admin_required

products_bp = Blueprint('products', __name__)

def check_auth():
    """Check if user is authenticated"""
    return 'user_id' in session

@products_bp.route('', methods=['GET'])
def get_products():
    """Get all products with optional search and filter"""
    if not check_auth():
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        search = request.args.get('search', '')
        category_id = request.args.get('category_id', '')
        
        query = """
            SELECT p.*, c.name as category_name 
            FROM products p 
            LEFT JOIN categories c ON p.category_id = c.id 
            WHERE 1=1
        """
        params = []
        
        if search:
            query += " AND p.name LIKE %s"
            params.append(f"%{search}%")
        
        if category_id:
            query += " AND p.category_id = %s"
            params.append(category_id)
        
        query += " ORDER BY p.created_at DESC"
        
        products = execute_query(query, tuple(params), fetch=True)
        return jsonify({'success': True, 'data': products}), 200
        
    except Exception as e:
        print(f"Get products error: {e}")
        return jsonify({'success': False, 'message': 'Terjadi kesalahan server'}), 500

@products_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get single product by ID"""
    if not check_auth():
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        query = """
            SELECT p.*, c.name as category_name 
            FROM products p 
            LEFT JOIN categories c ON p.category_id = c.id 
            WHERE p.id = %s
        """
        products = execute_query(query, (product_id,), fetch=True)
        
        if products and len(products) > 0:
            return jsonify({'success': True, 'data': products[0]}), 200
        else:
            return jsonify({'success': False, 'message': 'Produk tidak ditemukan'}), 404
            
    except Exception as e:
        print(f"Get product error: {e}")
        return jsonify({'success': False, 'message': 'Terjadi kesalahan server'}), 500

@products_bp.route('', methods=['POST'])
@admin_required
def create_product():
    """Create new product"""
    if not check_auth():
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        
        query = """
            INSERT INTO products (name, category_id, description, price, stock, image_url)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (
            data.get('name'),
            data.get('category_id'),
            data.get('description', ''),
            data.get('price'),
            data.get('stock', 0),
            data.get('image_url', 'https://via.placeholder.com/200')
        )
        
        product_id = execute_query(query, params)
        
        if product_id:
            return jsonify({
                'success': True,
                'message': 'Produk berhasil ditambahkan',
                'id': product_id
            }), 201
        else:
            return jsonify({'success': False, 'message': 'Gagal menambahkan produk'}), 500
            
    except Exception as e:
        print(f"Create product error: {e}")
        return jsonify({'success': False, 'message': 'Terjadi kesalahan server'}), 500

@products_bp.route('/<int:product_id>', methods=['PUT'])
@admin_required
def update_product(product_id):
    """Update product"""
    if not check_auth():
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        
        query = """
            UPDATE products 
            SET name = %s, category_id = %s, description = %s, 
                price = %s, stock = %s, image_url = %s
            WHERE id = %s
        """
        params = (
            data.get('name'),
            data.get('category_id'),
            data.get('description'),
            data.get('price'),
            data.get('stock'),
            data.get('image_url'),
            product_id
        )
        
        execute_query(query, params)
        
        return jsonify({
            'success': True,
            'message': 'Produk berhasil diupdate'
        }), 200
            
    except Exception as e:
        print(f"Update product error: {e}")
        return jsonify({'success': False, 'message': 'Terjadi kesalahan server'}), 500

@products_bp.route('/<int:product_id>', methods=['DELETE'])
@admin_required
def delete_product(product_id):
    """Delete product"""
    if not check_auth():
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        query = "DELETE FROM products WHERE id = %s"
        execute_query(query, (product_id,))
        
        return jsonify({
            'success': True,
            'message': 'Produk berhasil dihapus'
        }), 200
            
    except Exception as e:
        print(f"Delete product error: {e}")
        return jsonify({'success': False, 'message': 'Terjadi kesalahan server'}), 500
