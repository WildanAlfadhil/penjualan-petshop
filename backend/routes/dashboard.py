from flask import Blueprint, request, jsonify, session
from database import execute_query
from datetime import datetime, timedelta

dashboard_bp = Blueprint('dashboard', __name__)

def check_auth():
    """Check if user is authenticated"""
    return 'user_id' in session

@dashboard_bp.route('/stats', methods=['GET'])
def get_stats():
    """Get overall statistics"""
    if not check_auth():
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        # Total sales
        sales_query = "SELECT COALESCE(SUM(total_amount), 0) as total_sales FROM transactions WHERE status = 'completed'"
        sales_result = execute_query(sales_query, fetch=True)
        total_sales = sales_result[0]['total_sales'] if sales_result else 0
        
        # Total products
        products_query = "SELECT COUNT(*) as total_products FROM products"
        products_result = execute_query(products_query, fetch=True)
        total_products = products_result[0]['total_products'] if products_result else 0
        
        # Total customers
        customers_query = "SELECT COUNT(*) as total_customers FROM customers"
        customers_result = execute_query(customers_query, fetch=True)
        total_customers = customers_result[0]['total_customers'] if customers_result else 0
        
        # Total transactions
        trans_query = "SELECT COUNT(*) as total_transactions FROM transactions WHERE status = 'completed'"
        trans_result = execute_query(trans_query, fetch=True)
        total_transactions = trans_result[0]['total_transactions'] if trans_result else 0
        
        # Low stock products
        low_stock_query = "SELECT COUNT(*) as low_stock FROM products WHERE stock < 10"
        low_stock_result = execute_query(low_stock_query, fetch=True)
        low_stock = low_stock_result[0]['low_stock'] if low_stock_result else 0
        
        return jsonify({
            'success': True,
            'data': {
                'total_sales': float(total_sales),
                'total_products': total_products,
                'total_customers': total_customers,
                'total_transactions': total_transactions,
                'low_stock_products': low_stock
            }
        }), 200
        
    except Exception as e:
        print(f"Get stats error: {e}")
        return jsonify({'success': False, 'message': 'Terjadi kesalahan server'}), 500

@dashboard_bp.route('/sales-chart', methods=['GET'])
def get_sales_chart():
    """Get sales data for chart (last 7 days)"""
    if not check_auth():
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        query = """
            SELECT DATE(transaction_date) as date, 
                   COALESCE(SUM(total_amount), 0) as total
            FROM transactions
            WHERE status = 'completed' 
            AND transaction_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
            GROUP BY DATE(transaction_date)
            ORDER BY date ASC
        """
        
        results = execute_query(query, fetch=True)
        
        # Format data for chart
        labels = []
        data = []
        
        for row in results:
            labels.append(row['date'].strftime('%Y-%m-%d'))
            data.append(float(row['total']))
        
        return jsonify({
            'success': True,
            'data': {
                'labels': labels,
                'values': data
            }
        }), 200
        
    except Exception as e:
        print(f"Get sales chart error: {e}")
        return jsonify({'success': False, 'message': 'Terjadi kesalahan server'}), 500

@dashboard_bp.route('/category-chart', methods=['GET'])
def get_category_chart():
    """Get sales by category for pie chart"""
    if not check_auth():
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        query = """
            SELECT c.name as category, 
                   COALESCE(SUM(td.subtotal), 0) as total
            FROM categories c
            LEFT JOIN products p ON c.id = p.category_id
            LEFT JOIN transaction_details td ON p.id = td.product_id
            LEFT JOIN transactions t ON td.transaction_id = t.id
            WHERE t.status = 'completed' OR t.status IS NULL
            GROUP BY c.id, c.name
            ORDER BY total DESC
        """
        
        results = execute_query(query, fetch=True)
        
        # Format data for chart
        labels = []
        data = []
        
        for row in results:
            if row['total'] > 0:  # Only include categories with sales
                labels.append(row['category'])
                data.append(float(row['total']))
        
        return jsonify({
            'success': True,
            'data': {
                'labels': labels,
                'values': data
            }
        }), 200
        
    except Exception as e:
        print(f"Get category chart error: {e}")
        return jsonify({'success': False, 'message': 'Terjadi kesalahan server'}), 500

@dashboard_bp.route('/top-products', methods=['GET'])
def get_top_products():
    """Get top 5 selling products"""
    if not check_auth():
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        query = """
            SELECT p.name, 
                   COALESCE(SUM(td.quantity), 0) as total_sold,
                   COALESCE(SUM(td.subtotal), 0) as total_revenue
            FROM products p
            LEFT JOIN transaction_details td ON p.id = td.product_id
            LEFT JOIN transactions t ON td.transaction_id = t.id
            WHERE t.status = 'completed' OR t.status IS NULL
            GROUP BY p.id, p.name
            ORDER BY total_sold DESC
            LIMIT 5
        """
        
        results = execute_query(query, fetch=True)
        
        # Format data for chart
        labels = []
        data = []
        
        for row in results:
            labels.append(row['name'])
            data.append(row['total_sold'])
        
        return jsonify({
            'success': True,
            'data': {
                'labels': labels,
                'values': data
            }
        }), 200
        
    except Exception as e:
        print(f"Get top products error: {e}")
        return jsonify({'success': False, 'message': 'Terjadi kesalahan server'}), 500

@dashboard_bp.route('/recent-transactions', methods=['GET'])
def get_recent_transactions():
    """Get recent transactions"""
    if not check_auth():
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        query = """
            SELECT t.id, t.transaction_date, t.total_amount, 
                   t.payment_method, t.status,
                   c.name as customer_name
            FROM transactions t
            LEFT JOIN customers c ON t.customer_id = c.id
            ORDER BY t.transaction_date DESC
            LIMIT 10
        """
        
        transactions = execute_query(query, fetch=True)
        
        return jsonify({
            'success': True,
            'data': transactions
        }), 200
        
    except Exception as e:
        print(f"Get recent transactions error: {e}")
        return jsonify({'success': False, 'message': 'Terjadi kesalahan server'}), 500
