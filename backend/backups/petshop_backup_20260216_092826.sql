-- Pet Shop Database Backup
-- Created: 2026-02-16 09:28:26

USE petshop;

-- Table: categories
DROP TABLE IF EXISTS `categories`;
CREATE TABLE `categories` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Data for table: categories
INSERT INTO `categories` (`id`, `name`, `description`, `created_at`, `updated_at`) VALUES (1, 'Makanan Hewan', 'Berbagai jenis makanan untuk hewan peliharaan', '2026-02-15 13:06:19', '2026-02-15 13:06:19');
INSERT INTO `categories` (`id`, `name`, `description`, `created_at`, `updated_at`) VALUES (2, 'Mainan', 'Mainan dan aksesori bermain untuk hewan', '2026-02-15 13:06:19', '2026-02-15 13:06:19');
INSERT INTO `categories` (`id`, `name`, `description`, `created_at`, `updated_at`) VALUES (3, 'Perawatan', 'Produk perawatan dan kebersihan hewan', '2026-02-15 13:06:19', '2026-02-15 13:06:19');
INSERT INTO `categories` (`id`, `name`, `description`, `created_at`, `updated_at`) VALUES (4, 'Kandang & Aksesoris', 'Kandang, tempat tidur, dan aksesoris lainnya', '2026-02-15 13:06:19', '2026-02-15 13:06:19');
INSERT INTO `categories` (`id`, `name`, `description`, `created_at`, `updated_at`) VALUES (5, 'Obat & Vitamin', 'Obat-obatan dan suplemen kesehatan hewan', '2026-02-15 13:06:19', '2026-02-15 13:06:19');

-- Table: customers
DROP TABLE IF EXISTS `customers`;
CREATE TABLE `customers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `address` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Data for table: customers
INSERT INTO `customers` (`id`, `name`, `email`, `phone`, `address`, `created_at`, `updated_at`) VALUES (1, 'Budi Santoso', 'budi@email.com', '081234567890', 'Jl. Merdeka No. 123, Jakarta', '2026-02-15 13:06:19', '2026-02-15 13:06:19');
INSERT INTO `customers` (`id`, `name`, `email`, `phone`, `address`, `created_at`, `updated_at`) VALUES (2, 'Siti Nurhaliza', 'siti@email.com', '081234567891', 'Jl. Sudirman No. 45, Bandung', '2026-02-15 13:06:19', '2026-02-15 13:06:19');
INSERT INTO `customers` (`id`, `name`, `email`, `phone`, `address`, `created_at`, `updated_at`) VALUES (3, 'Ahmad Dahlan', 'ahmad@email.com', '081234567892', 'Jl. Gatot Subroto No. 78, Surabaya', '2026-02-15 13:06:19', '2026-02-15 13:06:19');
INSERT INTO `customers` (`id`, `name`, `email`, `phone`, `address`, `created_at`, `updated_at`) VALUES (4, 'Dewi Lestari', 'dewi@email.com', '081234567893', 'Jl. Diponegoro No. 56, Yogyakarta', '2026-02-15 13:06:19', '2026-02-15 13:06:19');
INSERT INTO `customers` (`id`, `name`, `email`, `phone`, `address`, `created_at`, `updated_at`) VALUES (5, 'Rudi Hartono', 'rudi@email.com', '081234567894', 'Jl. Ahmad Yani No. 90, Semarang', '2026-02-15 13:06:19', '2026-02-15 13:06:19');

-- Table: products
DROP TABLE IF EXISTS `products`;
CREATE TABLE `products` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `category_id` int(11) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `price` decimal(10,2) NOT NULL,
  `stock` int(11) DEFAULT 0,
  `image_url` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `idx_products_category` (`category_id`),
  CONSTRAINT `products_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Data for table: products
INSERT INTO `products` (`id`, `name`, `category_id`, `description`, `price`, `stock`, `image_url`, `created_at`, `updated_at`) VALUES (1, 'Royal Canin Dog Food 10kg', 1, 'Makanan anjing premium dengan nutrisi lengkap', 450000.00, 25, 'https://via.placeholder.com/200', '2026-02-15 13:06:19', '2026-02-15 13:06:19');
INSERT INTO `products` (`id`, `name`, `category_id`, `description`, `price`, `stock`, `image_url`, `created_at`, `updated_at`) VALUES (2, 'Whiskas Cat Food 1.2kg', 1, 'Makanan kucing dengan rasa ikan tuna', 85000.00, 50, 'https://via.placeholder.com/200', '2026-02-15 13:06:19', '2026-02-15 13:06:19');
INSERT INTO `products` (`id`, `name`, `category_id`, `description`, `price`, `stock`, `image_url`, `created_at`, `updated_at`) VALUES (3, 'Pro Plan Kitten 1kg', 1, 'Makanan khusus anak kucing', 120000.00, 30, 'https://via.placeholder.com/200', '2026-02-15 13:06:19', '2026-02-15 13:06:19');
INSERT INTO `products` (`id`, `name`, `category_id`, `description`, `price`, `stock`, `image_url`, `created_at`, `updated_at`) VALUES (4, 'Pedigree Adult 1.5kg', 1, 'Makanan anjing dewasa', 95000.00, 40, 'https://via.placeholder.com/200', '2026-02-15 13:06:19', '2026-02-15 13:06:19');
INSERT INTO `products` (`id`, `name`, `category_id`, `description`, `price`, `stock`, `image_url`, `created_at`, `updated_at`) VALUES (5, 'Bola Mainan Anjing', 2, 'Bola karet untuk bermain anjing', 35000.00, 100, 'https://via.placeholder.com/200', '2026-02-15 13:06:19', '2026-02-15 13:06:19');
INSERT INTO `products` (`id`, `name`, `category_id`, `description`, `price`, `stock`, `image_url`, `created_at`, `updated_at`) VALUES (6, 'Cat Teaser Wand', 2, 'Mainan tongkat bulu untuk kucing', 45000.00, 75, 'https://via.placeholder.com/200', '2026-02-15 13:06:19', '2026-02-15 13:06:19');
INSERT INTO `products` (`id`, `name`, `category_id`, `description`, `price`, `stock`, `image_url`, `created_at`, `updated_at`) VALUES (7, 'Puzzle Feeder', 2, 'Mainan puzzle untuk melatih kecerdasan hewan', 125000.00, 20, 'https://via.placeholder.com/200', '2026-02-15 13:06:19', '2026-02-15 13:06:19');
INSERT INTO `products` (`id`, `name`, `category_id`, `description`, `price`, `stock`, `image_url`, `created_at`, `updated_at`) VALUES (8, 'Shampoo Anjing Anti Kutu', 3, 'Shampoo khusus anjing dengan formula anti kutu', 65000.00, 60, 'https://via.placeholder.com/200', '2026-02-15 13:06:19', '2026-02-15 13:06:19');
INSERT INTO `products` (`id`, `name`, `category_id`, `description`, `price`, `stock`, `image_url`, `created_at`, `updated_at`) VALUES (9, 'Cat Litter 5kg', 3, 'Pasir kucing gumpal dengan aroma lavender', 75000.00, 80, 'https://via.placeholder.com/200', '2026-02-15 13:06:19', '2026-02-15 13:06:19');
INSERT INTO `products` (`id`, `name`, `category_id`, `description`, `price`, `stock`, `image_url`, `created_at`, `updated_at`) VALUES (10, 'Pet Brush', 3, 'Sisir bulu hewan multifungsi', 55000.00, 45, 'https://via.placeholder.com/200', '2026-02-15 13:06:19', '2026-02-15 13:06:19');
INSERT INTO `products` (`id`, `name`, `category_id`, `description`, `price`, `stock`, `image_url`, `created_at`, `updated_at`) VALUES (11, 'Kandang Kucing Medium', 4, 'Kandang kucing ukuran medium dengan pintu', 350000.00, 15, 'https://via.placeholder.com/200', '2026-02-15 13:06:19', '2026-02-15 13:06:19');
INSERT INTO `products` (`id`, `name`, `category_id`, `description`, `price`, `stock`, `image_url`, `created_at`, `updated_at`) VALUES (12, 'Pet Bed Cushion', 4, 'Kasur empuk untuk hewan peliharaan', 180000.00, 35, 'https://via.placeholder.com/200', '2026-02-15 13:06:19', '2026-02-15 13:06:19');
INSERT INTO `products` (`id`, `name`, `category_id`, `description`, `price`, `stock`, `image_url`, `created_at`, `updated_at`) VALUES (13, 'Water Bowl Stainless', 4, 'Mangkuk air stainless steel anti karat', 45000.00, 90, 'https://via.placeholder.com/200', '2026-02-15 13:06:19', '2026-02-15 13:06:19');
INSERT INTO `products` (`id`, `name`, `category_id`, `description`, `price`, `stock`, `image_url`, `created_at`, `updated_at`) VALUES (14, 'Vitamin Anjing', 5, 'Multivitamin untuk kesehatan anjing', 95000.00, 40, 'https://via.placeholder.com/200', '2026-02-15 13:06:19', '2026-02-15 13:06:19');
INSERT INTO `products` (`id`, `name`, `category_id`, `description`, `price`, `stock`, `image_url`, `created_at`, `updated_at`) VALUES (15, 'Obat Cacing Kucing', 5, 'Obat cacing untuk kucing semua umur', 55000.00, 50, 'https://via.placeholder.com/200', '2026-02-15 13:06:19', '2026-02-15 13:06:19');

-- Table: transaction_details
DROP TABLE IF EXISTS `transaction_details`;
CREATE TABLE `transaction_details` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `transaction_id` int(11) NOT NULL,
  `product_id` int(11) DEFAULT NULL,
  `quantity` int(11) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `subtotal` decimal(12,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_transaction_details_transaction` (`transaction_id`),
  KEY `idx_transaction_details_product` (`product_id`),
  CONSTRAINT `transaction_details_ibfk_1` FOREIGN KEY (`transaction_id`) REFERENCES `transactions` (`id`) ON DELETE CASCADE,
  CONSTRAINT `transaction_details_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Data for table: transaction_details
INSERT INTO `transaction_details` (`id`, `transaction_id`, `product_id`, `quantity`, `price`, `subtotal`) VALUES (1, 1, 1, 1, 450000.00, 450000.00);
INSERT INTO `transaction_details` (`id`, `transaction_id`, `product_id`, `quantity`, `price`, `subtotal`) VALUES (2, 1, 5, 2, 35000.00, 70000.00);
INSERT INTO `transaction_details` (`id`, `transaction_id`, `product_id`, `quantity`, `price`, `subtotal`) VALUES (3, 1, 13, 1, 45000.00, 45000.00);
INSERT INTO `transaction_details` (`id`, `transaction_id`, `product_id`, `quantity`, `price`, `subtotal`) VALUES (4, 2, 2, 2, 85000.00, 170000.00);
INSERT INTO `transaction_details` (`id`, `transaction_id`, `product_id`, `quantity`, `price`, `subtotal`) VALUES (5, 2, 5, 1, 35000.00, 35000.00);
INSERT INTO `transaction_details` (`id`, `transaction_id`, `product_id`, `quantity`, `price`, `subtotal`) VALUES (6, 3, 1, 1, 450000.00, 450000.00);
INSERT INTO `transaction_details` (`id`, `transaction_id`, `product_id`, `quantity`, `price`, `subtotal`) VALUES (7, 4, 11, 1, 350000.00, 350000.00);
INSERT INTO `transaction_details` (`id`, `transaction_id`, `product_id`, `quantity`, `price`, `subtotal`) VALUES (8, 5, 9, 2, 75000.00, 150000.00);
INSERT INTO `transaction_details` (`id`, `transaction_id`, `product_id`, `quantity`, `price`, `subtotal`) VALUES (9, 5, 8, 1, 65000.00, 65000.00);
INSERT INTO `transaction_details` (`id`, `transaction_id`, `product_id`, `quantity`, `price`, `subtotal`) VALUES (10, 5, 10, 1, 55000.00, 55000.00);
INSERT INTO `transaction_details` (`id`, `transaction_id`, `product_id`, `quantity`, `price`, `subtotal`) VALUES (11, 6, 3, 2, 120000.00, 240000.00);
INSERT INTO `transaction_details` (`id`, `transaction_id`, `product_id`, `quantity`, `price`, `subtotal`) VALUES (12, 7, 12, 1, 180000.00, 180000.00);
INSERT INTO `transaction_details` (`id`, `transaction_id`, `product_id`, `quantity`, `price`, `subtotal`) VALUES (13, 8, 1, 1, 450000.00, 450000.00);
INSERT INTO `transaction_details` (`id`, `transaction_id`, `product_id`, `quantity`, `price`, `subtotal`) VALUES (14, 8, 14, 1, 95000.00, 95000.00);
INSERT INTO `transaction_details` (`id`, `transaction_id`, `product_id`, `quantity`, `price`, `subtotal`) VALUES (15, 9, 15, 2, 55000.00, 110000.00);
INSERT INTO `transaction_details` (`id`, `transaction_id`, `product_id`, `quantity`, `price`, `subtotal`) VALUES (16, 9, 13, 1, 45000.00, 45000.00);
INSERT INTO `transaction_details` (`id`, `transaction_id`, `product_id`, `quantity`, `price`, `subtotal`) VALUES (17, 10, 4, 2, 95000.00, 190000.00);
INSERT INTO `transaction_details` (`id`, `transaction_id`, `product_id`, `quantity`, `price`, `subtotal`) VALUES (18, 10, 6, 3, 45000.00, 135000.00);
INSERT INTO `transaction_details` (`id`, `transaction_id`, `product_id`, `quantity`, `price`, `subtotal`) VALUES (19, 10, 10, 1, 55000.00, 55000.00);

-- Table: transactions
DROP TABLE IF EXISTS `transactions`;
CREATE TABLE `transactions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `customer_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `transaction_date` datetime DEFAULT current_timestamp(),
  `total_amount` decimal(12,2) NOT NULL,
  `payment_method` enum('cash','credit_card','debit_card','e-wallet') DEFAULT 'cash',
  `status` enum('completed','pending','cancelled') DEFAULT 'completed',
  `notes` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `idx_transactions_customer` (`customer_id`),
  KEY `idx_transactions_date` (`transaction_date`),
  CONSTRAINT `transactions_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`) ON DELETE SET NULL,
  CONSTRAINT `transactions_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Data for table: transactions
INSERT INTO `transactions` (`id`, `customer_id`, `user_id`, `transaction_date`, `total_amount`, `payment_method`, `status`, `notes`, `created_at`, `updated_at`) VALUES (1, 1, 1, '2026-02-01 10:30:00', 535000.00, 'cash', 'completed', NULL, '2026-02-15 13:06:19', '2026-02-15 13:06:19');
INSERT INTO `transactions` (`id`, `customer_id`, `user_id`, `transaction_date`, `total_amount`, `payment_method`, `status`, `notes`, `created_at`, `updated_at`) VALUES (2, 2, 1, '2026-02-03 14:15:00', 205000.00, 'e-wallet', 'completed', NULL, '2026-02-15 13:06:19', '2026-02-15 13:06:19');
INSERT INTO `transactions` (`id`, `customer_id`, `user_id`, `transaction_date`, `total_amount`, `payment_method`, `status`, `notes`, `created_at`, `updated_at`) VALUES (3, 3, 2, '2026-02-05 09:45:00', 450000.00, 'credit_card', 'completed', NULL, '2026-02-15 13:06:19', '2026-02-15 13:06:19');
INSERT INTO `transactions` (`id`, `customer_id`, `user_id`, `transaction_date`, `total_amount`, `payment_method`, `status`, `notes`, `created_at`, `updated_at`) VALUES (4, 4, 1, '2026-02-07 16:20:00', 350000.00, 'debit_card', 'completed', NULL, '2026-02-15 13:06:19', '2026-02-15 13:06:19');
INSERT INTO `transactions` (`id`, `customer_id`, `user_id`, `transaction_date`, `total_amount`, `payment_method`, `status`, `notes`, `created_at`, `updated_at`) VALUES (5, 5, 2, '2026-02-08 11:00:00', 275000.00, 'cash', 'completed', NULL, '2026-02-15 13:06:19', '2026-02-15 13:06:19');
INSERT INTO `transactions` (`id`, `customer_id`, `user_id`, `transaction_date`, `total_amount`, `payment_method`, `status`, `notes`, `created_at`, `updated_at`) VALUES (6, 1, 1, '2026-02-10 13:30:00', 240000.00, 'e-wallet', 'completed', NULL, '2026-02-15 13:06:19', '2026-02-15 13:06:19');
INSERT INTO `transactions` (`id`, `customer_id`, `user_id`, `transaction_date`, `total_amount`, `payment_method`, `status`, `notes`, `created_at`, `updated_at`) VALUES (7, 2, 2, '2026-02-11 10:15:00', 180000.00, 'cash', 'completed', NULL, '2026-02-15 13:06:19', '2026-02-15 13:06:19');
INSERT INTO `transactions` (`id`, `customer_id`, `user_id`, `transaction_date`, `total_amount`, `payment_method`, `status`, `notes`, `created_at`, `updated_at`) VALUES (8, 3, 1, '2026-02-12 15:45:00', 520000.00, 'credit_card', 'completed', NULL, '2026-02-15 13:06:19', '2026-02-15 13:06:19');
INSERT INTO `transactions` (`id`, `customer_id`, `user_id`, `transaction_date`, `total_amount`, `payment_method`, `status`, `notes`, `created_at`, `updated_at`) VALUES (9, 4, 2, '2026-02-13 09:30:00', 150000.00, 'cash', 'completed', NULL, '2026-02-15 13:06:19', '2026-02-15 13:06:19');
INSERT INTO `transactions` (`id`, `customer_id`, `user_id`, `transaction_date`, `total_amount`, `payment_method`, `status`, `notes`, `created_at`, `updated_at`) VALUES (10, 5, 1, '2026-02-14 14:00:00', 395000.00, 'e-wallet', 'completed', NULL, '2026-02-15 13:06:19', '2026-02-15 13:06:19');

-- Table: users
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `role` enum('admin','staff') DEFAULT 'staff',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Data for table: users
INSERT INTO `users` (`id`, `username`, `password`, `full_name`, `email`, `role`, `created_at`, `updated_at`) VALUES (1, 'admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'Administrator', 'admin@petshop.com', 'admin', '2026-02-15 13:06:19', '2026-02-15 13:06:19');
INSERT INTO `users` (`id`, `username`, `password`, `full_name`, `email`, `role`, `created_at`, `updated_at`) VALUES (2, 'staff1', '10176e7b7b24d317acfcf8d2064cfd2f24e154f7b5a96603077d5ef813d6a6b6', 'Staff Member', 'staff@petshop.com', 'staff', '2026-02-15 13:06:19', '2026-02-16 08:39:04');

