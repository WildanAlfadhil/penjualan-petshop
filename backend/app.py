from flask import Flask, session
from flask_cors import CORS
from config import Config
import os

# Import routes
from routes.auth import auth_bp
from routes.products import products_bp
from routes.categories import categories_bp
from routes.transactions import transactions_bp
from routes.dashboard import dashboard_bp
from routes.backup import backup_bp

app = Flask(__name__)
app.config.from_object(Config)

# Configure CORS to allow credentials
CORS(app, supports_credentials=True, origins=['http://localhost:5173', 'http://localhost:5174', 'http://localhost:5175', 'http://localhost:3000', 'http://127.0.0.1:5173', 'http://127.0.0.1:5174', 'http://127.0.0.1:5175', 'http://127.0.0.1:3000'])

# Configure session
app.secret_key = Config.SECRET_KEY

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(products_bp, url_prefix='/api/products')
app.register_blueprint(categories_bp, url_prefix='/api/categories')
app.register_blueprint(transactions_bp, url_prefix='/api/transactions')
app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
app.register_blueprint(backup_bp, url_prefix='/api/backup')

@app.route('/')
def index():
    return {
        'message': 'Pet Shop API',
        'version': '1.0.0',
        'endpoints': {
            'auth': '/api/auth',
            'products': '/api/products',
            'categories': '/api/categories',
            'transactions': '/api/transactions',
            'dashboard': '/api/dashboard',
            'backup': '/api/backup'
        }
    }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
