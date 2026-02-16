# Pet Shop Management System

Aplikasi manajemen toko hewan peliharaan berbasis web dengan fitur lengkap untuk mengelola produk, kategori, transaksi, dan visualisasi data interaktif.

## 🚀 Fitur Utama

- **Autentikasi**: Login/Logout dengan validasi database
- **Dashboard Interaktif**: Visualisasi data dengan grafik (Line, Pie, Bar Chart)
- **Manajemen Produk**: CRUD lengkap dengan pencarian
- **Manajemen Kategori**: CRUD kategori produk
- **Manajemen Transaksi**: Pembuatan transaksi dengan multiple items
- **Backup Database**: Fitur backup otomatis database MySQL

## 🛠️ Tech Stack

### Frontend
- React.js 18
- Vite (Build tool)
- React Router (Routing)
- Axios (HTTP client)
- Chart.js & react-chartjs-2 (Visualisasi data)
- Tailwind CSS (Styling)

### Backend
- Python 3.x
- Flask (Web framework)
- MySQL Connector (Database)
- Flask-CORS (Cross-origin)

### Database
- MySQL 8.0+

## 📋 Prerequisites

Pastikan Anda telah menginstall:
- Python 3.8 atau lebih tinggi
- Node.js 16 atau lebih tinggi
- MySQL 8.0 atau lebih tinggi
- npm atau yarn

## 🔧 Installation & Setup

### 1. Database Setup

```bash
# Login ke MySQL
mysql -u root -p

# Import database schema
mysql -u root -p < database/petshop_schema.sql
```

### 2. Backend Setup

```bash
# Masuk ke direktori backend
cd backend

# Install dependencies
pip install -r requirements.txt

# Copy file environment (opsional)
copy .env.example .env

# Edit .env sesuai konfigurasi MySQL Anda
# DB_USER=root
# DB_PASSWORD=your_password
# DB_NAME=petshop

# Jalankan server Flask
python app.py
```

Server backend akan berjalan di `http://localhost:5000`

### 3. Frontend Setup

```bash
# Masuk ke direktori frontend
cd frontend

# Install dependencies
npm install

# Jalankan development server
npm run dev
```

Frontend akan berjalan di `http://localhost:5173`

## 👤 Default Login Credentials

```
Username: admin
Password: admin123
```

atau

```
Username: staff1
Password: staff123
```

## 📁 Struktur Proyek

```
tugas_akhir_basdat/
├── database/
│   └── petshop_schema.sql          # Database schema & sample data
├── backend/
│   ├── routes/
│   │   ├── auth.py                 # Authentication endpoints
│   │   ├── products.py             # Product CRUD endpoints
│   │   ├── categories.py           # Category CRUD endpoints
│   │   ├── transactions.py         # Transaction endpoints
│   │   ├── dashboard.py            # Dashboard data endpoints
│   │   └── backup.py               # Backup endpoints
│   ├── app.py                      # Main Flask application
│   ├── config.py                   # Configuration
│   ├── database.py                 # Database utilities
│   └── requirements.txt            # Python dependencies
└── frontend/
    ├── src/
    │   ├── components/
    │   │   └── Navbar.jsx          # Navigation component
    │   ├── pages/
    │   │   ├── Login.jsx           # Login page
    │   │   ├── Dashboard.jsx       # Dashboard with charts
    │   │   ├── Products.jsx        # Products management
    │   │   ├── Categories.jsx      # Categories management
    │   │   └── Transactions.jsx    # Transactions management
    │   ├── services/
    │   │   └── api.js              # API service layer
    │   ├── App.jsx                 # Main app component
    │   ├── main.jsx                # Entry point
    │   └── index.css               # Global styles
    ├── package.json
    └── vite.config.js
```

## 🎯 API Endpoints

### Authentication
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user
- `GET /api/auth/check` - Check authentication status

### Products
- `GET /api/products` - Get all products
- `GET /api/products/:id` - Get single product
- `POST /api/products` - Create product
- `PUT /api/products/:id` - Update product
- `DELETE /api/products/:id` - Delete product

### Categories
- `GET /api/categories` - Get all categories
- `POST /api/categories` - Create category
- `PUT /api/categories/:id` - Update category
- `DELETE /api/categories/:id` - Delete category

### Transactions
- `GET /api/transactions` - Get all transactions
- `POST /api/transactions` - Create transaction
- `DELETE /api/transactions/:id` - Delete transaction
- `GET /api/transactions/customers` - Get customers
- `POST /api/transactions/customers` - Create customer

### Dashboard
- `GET /api/dashboard/stats` - Get statistics
- `GET /api/dashboard/sales-chart` - Sales trend data
- `GET /api/dashboard/category-chart` - Category distribution
- `GET /api/dashboard/top-products` - Top selling products
- `GET /api/dashboard/recent-transactions` - Recent transactions

### Backup
- `POST /api/backup/create` - Create database backup
- `GET /api/backup/list` - List backup files

## 📊 Database Schema

### Tables
1. **users** - User authentication
2. **categories** - Product categories
3. **products** - Product inventory
4. **customers** - Customer information
5. **transactions** - Transaction headers
6. **transaction_details** - Transaction line items

## 🎨 Features Showcase

### Dashboard
- Total sales, products, customers, transactions statistics
- Sales trend line chart (7 days)
- Category distribution pie chart
- Top 5 products bar chart
- Recent transactions table

### Products Management
- Add, edit, delete products
- Search products by name
- Filter by category
- Stock level indicators

### Transactions
- Create multi-item transactions
- Add new customers on-the-fly
- Multiple payment methods
- Real-time total calculation

## 🔒 Security Features

- Password hashing (SHA256)
- Session-based authentication
- Protected API routes
- CORS configuration
- SQL injection prevention (parameterized queries)

## 🚀 Production Build

### Backend
```bash
# Set environment to production
# Update .env file with production settings
python app.py
```

### Frontend
```bash
cd frontend
npm run build
# Build output will be in dist/ folder
```

## 🐛 Troubleshooting

### Database Connection Error
- Pastikan MySQL server berjalan
- Periksa kredensial di file `.env` atau `config.py`
- Pastikan database `petshop` sudah dibuat

### CORS Error
- Pastikan backend berjalan di port 5000
- Pastikan frontend berjalan di port 5173
- Periksa konfigurasi CORS di `app.py`

### Module Not Found
```bash
# Backend
pip install -r requirements.txt

# Frontend
npm install
```

## 📝 License

This project is created for educational purposes.

## 👨‍💻 Author

Created as a final project for Advanced Database course.
