import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import { transactionsAPI, productsAPI } from '../services/api';

function Transactions() {
  const [transactions, setTransactions] = useState([]);
  const [customers, setCustomers] = useState([]);
  const [products, setProducts] = useState([]);
  const [search, setSearch] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [showCustomerModal, setShowCustomerModal] = useState(false);
  const [newCustomer, setNewCustomer] = useState({ name: '', email: '', phone: '', address: '' });
  const [currentTransaction, setCurrentTransaction] = useState({
    customer_id: '',
    payment_method: 'cash',
    notes: '',
    details: [],
  });
  const [selectedProduct, setSelectedProduct] = useState('');
  const [quantity, setQuantity] = useState(1);
  const user = JSON.parse(localStorage.getItem('user') || '{}');

  useEffect(() => {
    fetchTransactions();
    fetchCustomers();
    fetchProducts();
  }, []);

  const fetchTransactions = async (searchTerm = '') => {
    try {
      const response = await transactionsAPI.getAll({ search: searchTerm });
      setTransactions(response.data.data);
    } catch (error) {
      console.error('Error fetching transactions:', error);
    }
  };

  const fetchCustomers = async () => {
    try {
      const response = await transactionsAPI.getCustomers();
      setCustomers(response.data.data);
    } catch (error) {
      console.error('Error fetching customers:', error);
    }
  };

  const fetchProducts = async () => {
    try {
      const response = await productsAPI.getAll();
      setProducts(response.data.data);
    } catch (error) {
      console.error('Error fetching products:', error);
    }
  };

  const handleSearch = (e) => {
    const value = e.target.value;
    setSearch(value);
    fetchTransactions(value);
  };

  const handleAddCustomer = async (e) => {
    e.preventDefault();
    try {
      await transactionsAPI.createCustomer(newCustomer);
      fetchCustomers();
      setShowCustomerModal(false);
      setNewCustomer({ name: '', email: '', phone: '', address: '' });
      alert('Customer berhasil ditambahkan');
    } catch (error) {
      alert('Gagal menambahkan customer');
    }
  };

  const handleAddProduct = () => {
    if (!selectedProduct || quantity <= 0) {
      alert('Pilih produk dan masukkan jumlah yang valid');
      return;
    }

    const product = products.find(p => p.id === parseInt(selectedProduct));
    if (!product) return;

    const existingItem = currentTransaction.details.find(d => d.product_id === product.id);
    if (existingItem) {
      alert('Produk sudah ada dalam transaksi');
      return;
    }

    const subtotal = product.price * quantity;
    const newDetail = {
      product_id: product.id,
      product_name: product.name,
      quantity: quantity,
      price: product.price,
      subtotal: subtotal,
    };

    setCurrentTransaction({
      ...currentTransaction,
      details: [...currentTransaction.details, newDetail],
    });

    setSelectedProduct('');
    setQuantity(1);
  };

  const handleRemoveProduct = (index) => {
    const newDetails = currentTransaction.details.filter((_, i) => i !== index);
    setCurrentTransaction({ ...currentTransaction, details: newDetails });
  };

  const calculateTotal = () => {
    return currentTransaction.details.reduce((sum, item) => sum + item.subtotal, 0);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (currentTransaction.details.length === 0) {
      alert('Tambahkan minimal satu produk');
      return;
    }

    try {
      const transactionData = {
        ...currentTransaction,
        total_amount: calculateTotal(),
      };
      await transactionsAPI.create(transactionData);
      alert('Transaksi berhasil ditambahkan');
      setShowModal(false);
      setCurrentTransaction({
        customer_id: '',
        payment_method: 'cash',
        notes: '',
        details: [],
      });
      fetchTransactions(search);
    } catch (error) {
      alert('Gagal menyimpan transaksi');
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Apakah Anda yakin ingin menghapus transaksi ini?')) {
      try {
        await transactionsAPI.delete(id);
        fetchTransactions(search);
        alert('Transaksi berhasil dihapus');
      } catch (error) {
        alert('Gagal menghapus transaksi');
      }
    }
  };

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('id-ID', {
      style: 'currency',
      currency: 'IDR',
      minimumFractionDigits: 0,
    }).format(value);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold text-gray-900">Manajemen Transaksi</h1>
          <button onClick={() => setShowModal(true)} className="btn-primary">
            + Transaksi Baru
          </button>
        </div>

        <div className="card mb-6">
          <input
            type="text"
            placeholder="Cari transaksi..."
            value={search}
            onChange={handleSearch}
            className="input-field"
          />
        </div>

        <div className="table-container">
          <table className="table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Tanggal</th>
                <th>Customer</th>
                <th>Total</th>
                <th>Metode Pembayaran</th>
                <th>Status</th>
                <th>Aksi</th>
              </tr>
            </thead>
            <tbody>
              {transactions.map((transaction) => (
                <tr key={transaction.id}>
                  <td>{transaction.id}</td>
                  <td>{new Date(transaction.transaction_date).toLocaleDateString('id-ID')}</td>
                  <td>{transaction.customer_name}</td>
                  <td>{formatCurrency(transaction.total_amount)}</td>
                  <td className="capitalize">{transaction.payment_method}</td>
                  <td>
                    <span className={`px-2 py-1 rounded text-xs ${
                      transaction.status === 'completed' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                    }`}>
                      {transaction.status}
                    </span>
                  </td>
                  <td>
                    {user.role === 'admin' && (
                      <button onClick={() => handleDelete(transaction.id)} className="text-red-600 hover:text-red-800">
                        Hapus
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Transaction Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 overflow-y-auto">
          <div className="bg-white rounded-lg p-8 max-w-4xl w-full m-4">
            <h2 className="text-2xl font-bold mb-4">Transaksi Baru</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-1">Customer</label>
                  <div className="flex space-x-2">
                    <select
                      required
                      value={currentTransaction.customer_id}
                      onChange={(e) => setCurrentTransaction({ ...currentTransaction, customer_id: e.target.value })}
                      className="input-field flex-1"
                    >
                      <option value="">Pilih Customer</option>
                      {customers.map((customer) => (
                        <option key={customer.id} value={customer.id}>{customer.name}</option>
                      ))}
                    </select>
                    <button
                      type="button"
                      onClick={() => setShowCustomerModal(true)}
                      className="btn-secondary whitespace-nowrap"
                    >
                      + Baru
                    </button>
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1">Metode Pembayaran</label>
                  <select
                    value={currentTransaction.payment_method}
                    onChange={(e) => setCurrentTransaction({ ...currentTransaction, payment_method: e.target.value })}
                    className="input-field"
                  >
                    <option value="cash">Cash</option>
                    <option value="credit_card">Credit Card</option>
                    <option value="debit_card">Debit Card</option>
                    <option value="e-wallet">E-Wallet</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Catatan</label>
                <textarea
                  value={currentTransaction.notes}
                  onChange={(e) => setCurrentTransaction({ ...currentTransaction, notes: e.target.value })}
                  className="input-field"
                  rows="2"
                />
              </div>

              <div className="border-t pt-4">
                <h3 className="font-semibold mb-3">Produk</h3>
                <div className="flex space-x-2 mb-4">
                  <select
                    value={selectedProduct}
                    onChange={(e) => setSelectedProduct(e.target.value)}
                    className="input-field flex-1"
                  >
                    <option value="">Pilih Produk</option>
                    {products.map((product) => (
                      <option key={product.id} value={product.id}>
                        {product.name} - {formatCurrency(product.price)} (Stok: {product.stock})
                      </option>
                    ))}
                  </select>
                  <input
                    type="number"
                    min="1"
                    value={quantity}
                    onChange={(e) => setQuantity(parseInt(e.target.value))}
                    className="input-field w-24"
                    placeholder="Qty"
                  />
                  <button type="button" onClick={handleAddProduct} className="btn-secondary">
                    Tambah
                  </button>
                </div>

                <table className="min-w-full border">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-4 py-2 text-left text-xs">Produk</th>
                      <th className="px-4 py-2 text-right text-xs">Harga</th>
                      <th className="px-4 py-2 text-right text-xs">Qty</th>
                      <th className="px-4 py-2 text-right text-xs">Subtotal</th>
                      <th className="px-4 py-2 text-xs">Aksi</th>
                    </tr>
                  </thead>
                  <tbody>
                    {currentTransaction.details.map((item, index) => (
                      <tr key={index} className="border-t">
                        <td className="px-4 py-2 text-sm">{item.product_name}</td>
                        <td className="px-4 py-2 text-sm text-right">{formatCurrency(item.price)}</td>
                        <td className="px-4 py-2 text-sm text-right">{item.quantity}</td>
                        <td className="px-4 py-2 text-sm text-right">{formatCurrency(item.subtotal)}</td>
                        <td className="px-4 py-2 text-center">
                          <button
                            type="button"
                            onClick={() => handleRemoveProduct(index)}
                            className="text-red-600 hover:text-red-800 text-sm"
                          >
                            Hapus
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                  <tfoot className="bg-gray-50 font-bold">
                    <tr>
                      <td colSpan="3" className="px-4 py-2 text-right">Total:</td>
                      <td className="px-4 py-2 text-right">{formatCurrency(calculateTotal())}</td>
                      <td></td>
                    </tr>
                  </tfoot>
                </table>
              </div>

              <div className="flex space-x-3 mt-6">
                <button type="submit" className="btn-primary flex-1">
                  Simpan Transaksi
                </button>
                <button type="button" onClick={() => setShowModal(false)} className="btn-secondary flex-1">
                  Batal
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Customer Modal */}
      {showCustomerModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-8 max-w-md w-full">
            <h2 className="text-2xl font-bold mb-4">Tambah Customer</h2>
            <form onSubmit={handleAddCustomer} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">Nama</label>
                <input
                  type="text"
                  required
                  value={newCustomer.name}
                  onChange={(e) => setNewCustomer({ ...newCustomer, name: e.target.value })}
                  className="input-field"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Email</label>
                <input
                  type="email"
                  value={newCustomer.email}
                  onChange={(e) => setNewCustomer({ ...newCustomer, email: e.target.value })}
                  className="input-field"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Telepon</label>
                <input
                  type="text"
                  value={newCustomer.phone}
                  onChange={(e) => setNewCustomer({ ...newCustomer, phone: e.target.value })}
                  className="input-field"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Alamat</label>
                <textarea
                  value={newCustomer.address}
                  onChange={(e) => setNewCustomer({ ...newCustomer, address: e.target.value })}
                  className="input-field"
                  rows="2"
                />
              </div>
              <div className="flex space-x-3 mt-6">
                <button type="submit" className="btn-primary flex-1">
                  Simpan
                </button>
                <button type="button" onClick={() => setShowCustomerModal(false)} className="btn-secondary flex-1">
                  Batal
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default Transactions;
