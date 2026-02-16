-- Pet Shop Database Schema
-- Drop database if exists and create new one
DROP DATABASE IF EXISTS petshop;
CREATE DATABASE petshop;
USE petshop;

-- Users table for authentication
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    role ENUM('admin', 'staff') DEFAULT 'staff',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Categories table
CREATE TABLE categories (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Products table
CREATE TABLE products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(200) NOT NULL,
    category_id INT,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock INT DEFAULT 0,
    image_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
);

-- Customers table
CREATE TABLE customers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(20),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Transactions table
CREATE TABLE transactions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT,
    user_id INT,
    transaction_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(12, 2) NOT NULL,
    payment_method ENUM('cash', 'credit_card', 'debit_card', 'e-wallet') DEFAULT 'cash',
    status ENUM('completed', 'pending', 'cancelled') DEFAULT 'completed',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE SET NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- Transaction details table
CREATE TABLE transaction_details (
    id INT PRIMARY KEY AUTO_INCREMENT,
    transaction_id INT NOT NULL,
    product_id INT,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(12, 2) NOT NULL,
    FOREIGN KEY (transaction_id) REFERENCES transactions(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE SET NULL
);

-- Insert default admin user (password: admin123)
-- Password is hashed using SHA256
INSERT INTO users (username, password, full_name, email, role) VALUES
('admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'Administrator', 'admin@petshop.com', 'admin'),
('staff1', '10176e7b233a758ce491629856f6c58bf1350a58a698946ded259a4f66a70e7e', 'Staff Member', 'staff@petshop.com', 'staff');

-- Insert sample categories
INSERT INTO categories (name, description) VALUES
('Makanan Hewan', 'Berbagai jenis makanan untuk hewan peliharaan'),
('Mainan', 'Mainan dan aksesori bermain untuk hewan'),
('Perawatan', 'Produk perawatan dan kebersihan hewan'),
('Kandang & Aksesoris', 'Kandang, tempat tidur, dan aksesoris lainnya'),
('Obat & Vitamin', 'Obat-obatan dan suplemen kesehatan hewan');

-- Insert sample products
INSERT INTO products (name, category_id, description, price, stock, image_url) VALUES
('Royal Canin Dog Food 10kg', 1, 'Makanan anjing premium dengan nutrisi lengkap', 450000, 25, 'https://via.placeholder.com/200'),
('Whiskas Cat Food 1.2kg', 1, 'Makanan kucing dengan rasa ikan tuna', 85000, 50, 'https://via.placeholder.com/200'),
('Pro Plan Kitten 1kg', 1, 'Makanan khusus anak kucing', 120000, 30, 'https://via.placeholder.com/200'),
('Pedigree Adult 1.5kg', 1, 'Makanan anjing dewasa', 95000, 40, 'https://via.placeholder.com/200'),
('Bola Mainan Anjing', 2, 'Bola karet untuk bermain anjing', 35000, 100, 'https://via.placeholder.com/200'),
('Cat Teaser Wand', 2, 'Mainan tongkat bulu untuk kucing', 45000, 75, 'https://via.placeholder.com/200'),
('Puzzle Feeder', 2, 'Mainan puzzle untuk melatih kecerdasan hewan', 125000, 20, 'https://via.placeholder.com/200'),
('Shampoo Anjing Anti Kutu', 3, 'Shampoo khusus anjing dengan formula anti kutu', 65000, 60, 'https://via.placeholder.com/200'),
('Cat Litter 5kg', 3, 'Pasir kucing gumpal dengan aroma lavender', 75000, 80, 'https://via.placeholder.com/200'),
('Pet Brush', 3, 'Sisir bulu hewan multifungsi', 55000, 45, 'https://via.placeholder.com/200'),
('Kandang Kucing Medium', 4, 'Kandang kucing ukuran medium dengan pintu', 350000, 15, 'https://via.placeholder.com/200'),
('Pet Bed Cushion', 4, 'Kasur empuk untuk hewan peliharaan', 180000, 35, 'https://via.placeholder.com/200'),
('Water Bowl Stainless', 4, 'Mangkuk air stainless steel anti karat', 45000, 90, 'https://via.placeholder.com/200'),
('Vitamin Anjing', 5, 'Multivitamin untuk kesehatan anjing', 95000, 40, 'https://via.placeholder.com/200'),
('Obat Cacing Kucing', 5, 'Obat cacing untuk kucing semua umur', 55000, 50, 'https://via.placeholder.com/200');

-- Insert sample customers
INSERT INTO customers (name, email, phone, address) VALUES
('Budi Santoso', 'budi@email.com', '081234567890', 'Jl. Merdeka No. 123, Jakarta'),
('Siti Nurhaliza', 'siti@email.com', '081234567891', 'Jl. Sudirman No. 45, Bandung'),
('Ahmad Dahlan', 'ahmad@email.com', '081234567892', 'Jl. Gatot Subroto No. 78, Surabaya'),
('Dewi Lestari', 'dewi@email.com', '081234567893', 'Jl. Diponegoro No. 56, Yogyakarta'),
('Rudi Hartono', 'rudi@email.com', '081234567894', 'Jl. Ahmad Yani No. 90, Semarang');

-- Insert sample transactions
INSERT INTO transactions (customer_id, user_id, transaction_date, total_amount, payment_method, status) VALUES
(1, 1, '2026-02-01 10:30:00', 535000, 'cash', 'completed'),
(2, 1, '2026-02-03 14:15:00', 205000, 'e-wallet', 'completed'),
(3, 2, '2026-02-05 09:45:00', 450000, 'credit_card', 'completed'),
(4, 1, '2026-02-07 16:20:00', 350000, 'debit_card', 'completed'),
(5, 2, '2026-02-08 11:00:00', 275000, 'cash', 'completed'),
(1, 1, '2026-02-10 13:30:00', 240000, 'e-wallet', 'completed'),
(2, 2, '2026-02-11 10:15:00', 180000, 'cash', 'completed'),
(3, 1, '2026-02-12 15:45:00', 520000, 'credit_card', 'completed'),
(4, 2, '2026-02-13 09:30:00', 150000, 'cash', 'completed'),
(5, 1, '2026-02-14 14:00:00', 395000, 'e-wallet', 'completed');

-- Insert sample transaction details
-- Transaction 1
INSERT INTO transaction_details (transaction_id, product_id, quantity, price, subtotal) VALUES
(1, 1, 1, 450000, 450000),
(1, 5, 2, 35000, 70000),
(1, 13, 1, 45000, 45000);

-- Transaction 2
INSERT INTO transaction_details (transaction_id, product_id, quantity, price, subtotal) VALUES
(2, 2, 2, 85000, 170000),
(2, 5, 1, 35000, 35000);

-- Transaction 3
INSERT INTO transaction_details (transaction_id, product_id, quantity, price, subtotal) VALUES
(3, 1, 1, 450000, 450000);

-- Transaction 4
INSERT INTO transaction_details (transaction_id, product_id, quantity, price, subtotal) VALUES
(4, 11, 1, 350000, 350000);

-- Transaction 5
INSERT INTO transaction_details (transaction_id, product_id, quantity, price, subtotal) VALUES
(5, 9, 2, 75000, 150000),
(5, 8, 1, 65000, 65000),
(5, 10, 1, 55000, 55000);

-- Transaction 6
INSERT INTO transaction_details (transaction_id, product_id, quantity, price, subtotal) VALUES
(6, 3, 2, 120000, 240000);

-- Transaction 7
INSERT INTO transaction_details (transaction_id, product_id, quantity, price, subtotal) VALUES
(7, 12, 1, 180000, 180000);

-- Transaction 8
INSERT INTO transaction_details (transaction_id, product_id, quantity, price, subtotal) VALUES
(8, 1, 1, 450000, 450000),
(8, 14, 1, 95000, 95000);

-- Transaction 9
INSERT INTO transaction_details (transaction_id, product_id, quantity, price, subtotal) VALUES
(9, 15, 2, 55000, 110000),
(9, 13, 1, 45000, 45000);

-- Transaction 10
INSERT INTO transaction_details (transaction_id, product_id, quantity, price, subtotal) VALUES
(10, 4, 2, 95000, 190000),
(10, 6, 3, 45000, 135000),
(10, 10, 1, 55000, 55000);

-- Create indexes for better performance
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_transactions_customer ON transactions(customer_id);
CREATE INDEX idx_transactions_date ON transactions(transaction_date);
CREATE INDEX idx_transaction_details_transaction ON transaction_details(transaction_id);
CREATE INDEX idx_transaction_details_product ON transaction_details(product_id);
