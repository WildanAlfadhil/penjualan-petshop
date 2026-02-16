from flask import Blueprint, request, jsonify, session
from database import execute_query, get_db_connection
import mysql.connector
from routes.auth import admin_required

transactions_bp = Blueprint('transactions', __name__)

def check_auth():
    """Check if user is authenticated"""
    return 'user_id' in session

@transactions_bp.route('', methods=['GET'])
def get_transactions():
    """Get all transactions with optional search"""
    if not check_auth():
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        search = request.args.get('search', '')
        
        query = """
            SELECT t.*, c.name as customer_name, u.full_name as user_name
            FROM transactions t
            LEFT JOIN customers c ON t.customer_id = c.id
            LEFT JOIN users u ON t.user_id = u.id
            WHERE 1=1
        """
        params = []
        
        if search:
            query += " AND (c.name LIKE %s OR t.payment_method LIKE %s)"
            params.append(f"%{search}%")
            params.append(f"%{search}%")
        
        query += " ORDER BY t.transaction_date DESC"
        
        transactions = execute_query(query, tuple(params), fetch=True)
        return jsonify({'success': True, 'data': transactions}), 200
        
    except Exception as e:
        print(f"Get transactions error: {e}")
        return jsonify({'success': False, 'message': 'Terjadi kesalahan server'}), 500

@transactions_bp.route('/<int:transaction_id>', methods=['GET'])
def get_transaction(transaction_id):
    """Get single transaction with details"""
    if not check_auth():
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        # Get transaction header
        query = """
            SELECT t.*, c.name as customer_name, u.full_name as user_name
            FROM transactions t
            LEFT JOIN customers c ON t.customer_id = c.id
            LEFT JOIN users u ON t.user_id = u.id
            WHERE t.id = %s
        """
        transactions = execute_query(query, (transaction_id,), fetch=True)
        
        if not transactions or len(transactions) == 0:
            return jsonify({'success': False, 'message': 'Transaksi tidak ditemukan'}), 404
        
        transaction = transactions[0]
        
        # Get transaction details
        detail_query = """
            SELECT td.*, p.name as product_name
            FROM transaction_details td
            LEFT JOIN products p ON td.product_id = p.id
            WHERE td.transaction_id = %s
        """
        details = execute_query(detail_query, (transaction_id,), fetch=True)
        transaction['details'] = details
        
        return jsonify({'success': True, 'data': transaction}), 200
            
    except Exception as e:
        print(f"Get transaction error: {e}")
        return jsonify({'success': False, 'message': 'Terjadi kesalahan server'}), 500

@transactions_bp.route('', methods=['POST'])
def create_transaction():
    """Create new transaction with details"""
    if not check_auth():
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    connection = get_db_connection()
    if not connection:
        return jsonify({'success': False, 'message': 'Database connection error'}), 500
    
    try:
        data = request.get_json()
        cursor = connection.cursor(dictionary=True)
        
        # Start transaction
        connection.start_transaction()
        
        # Insert transaction header
        trans_query = """
            INSERT INTO transactions (customer_id, user_id, total_amount, payment_method, status, notes)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        trans_params = (
            data.get('customer_id'),
            session['user_id'],
            data.get('total_amount'),
            data.get('payment_method', 'cash'),
            data.get('status', 'completed'),
            data.get('notes', '')
        )
        cursor.execute(trans_query, trans_params)
        transaction_id = cursor.lastrowid
        
        # Insert transaction details
        details = data.get('details', [])
        for detail in details:
            detail_query = """
                INSERT INTO transaction_details (transaction_id, product_id, quantity, price, subtotal)
                VALUES (%s, %s, %s, %s, %s)
            """
            detail_params = (
                transaction_id,
                detail['product_id'],
                detail['quantity'],
                detail['price'],
                detail['subtotal']
            )
            cursor.execute(detail_query, detail_params)
            
            # Update product stock
            stock_query = "UPDATE products SET stock = stock - %s WHERE id = %s"
            cursor.execute(stock_query, (detail['quantity'], detail['product_id']))
        
        # Commit transaction
        connection.commit()
        cursor.close()
        connection.close()
        
        return jsonify({
            'success': True,
            'message': 'Transaksi berhasil ditambahkan',
            'id': transaction_id
        }), 201
            
    except mysql.connector.Error as e:
        if connection:
            connection.rollback()
            connection.close()
        print(f"Create transaction error: {e}")
        return jsonify({'success': False, 'message': 'Terjadi kesalahan server'}), 500

@transactions_bp.route('/<int:transaction_id>', methods=['DELETE'])
@admin_required
def delete_transaction(transaction_id):
    """Delete transaction"""
    if not check_auth():
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        query = "DELETE FROM transactions WHERE id = %s"
        execute_query(query, (transaction_id,))
        
        return jsonify({
            'success': True,
            'message': 'Transaksi berhasil dihapus'
        }), 200
            
    except Exception as e:
        print(f"Delete transaction error: {e}")
        return jsonify({'success': False, 'message': 'Terjadi kesalahan server'}), 500

# Customer endpoints
@transactions_bp.route('/customers', methods=['GET'])
def get_customers():
    """Get all customers"""
    if not check_auth():
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        query = "SELECT * FROM customers ORDER BY name ASC"
        customers = execute_query(query, fetch=True)
        return jsonify({'success': True, 'data': customers}), 200
        
    except Exception as e:
        print(f"Get customers error: {e}")
        return jsonify({'success': False, 'message': 'Terjadi kesalahan server'}), 500

@transactions_bp.route('/customers', methods=['POST'])
def create_customer():
    """Create new customer"""
    if not check_auth():
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        
        query = """
            INSERT INTO customers (name, email, phone, address)
            VALUES (%s, %s, %s, %s)
        """
        params = (
            data.get('name'),
            data.get('email', ''),
            data.get('phone', ''),
            data.get('address', '')
        )
        
        customer_id = execute_query(query, params)
        
        if customer_id:
            return jsonify({
                'success': True,
                'message': 'Customer berhasil ditambahkan',
                'id': customer_id
            }), 201
        else:
            return jsonify({'success': False, 'message': 'Gagal menambahkan customer'}), 500
            
    except Exception as e:
        print(f"Create customer error: {e}")
        return jsonify({'success': False, 'message': 'Terjadi kesalahan server'}), 500
