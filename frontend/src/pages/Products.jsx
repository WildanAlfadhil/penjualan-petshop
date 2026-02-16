import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import { productsAPI, categoriesAPI } from '../services/api';

function Products() {
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [search, setSearch] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [editMode, setEditMode] = useState(false);
  const [currentProduct, setCurrentProduct] = useState({
    name: '',
    category_id: '',
    description: '',
    price: '',
    stock: '',
    image_url: 'https://via.placeholder.com/200',
  });
  const user = JSON.parse(localStorage.getItem('user') || '{}');

  useEffect(() => {
    fetchProducts();
    fetchCategories();
  }, []);

  const fetchProducts = async (searchTerm = '') => {
    try {
      const response = await productsAPI.getAll({ search: searchTerm });
      setProducts(response.data.data);
    } catch (error) {
      console.error('Error fetching products:', error);
    }
  };

  const fetchCategories = async () => {
    try {
      const response = await categoriesAPI.getAll();
      setCategories(response.data.data);
    } catch (error) {
      console.error('Error fetching categories:', error);
    }
  };

  const handleSearch = (e) => {
    const value = e.target.value;
    setSearch(value);
    fetchProducts(value);
  };

  const handleAdd = () => {
    setEditMode(false);
    setCurrentProduct({
      name: '',
      category_id: '',
      description: '',
      price: '',
      stock: '',
      image_url: 'https://via.placeholder.com/200',
    });
    setShowModal(true);
  };

  const handleEdit = (product) => {
    setEditMode(true);
    setCurrentProduct(product);
    setShowModal(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Apakah Anda yakin ingin menghapus produk ini?')) {
      try {
        await productsAPI.delete(id);
        fetchProducts(search);
        alert('Produk berhasil dihapus');
      } catch (error) {
        alert('Gagal menghapus produk');
      }
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editMode) {
        await productsAPI.update(currentProduct.id, currentProduct);
        alert('Produk berhasil diupdate');
      } else {
        await productsAPI.create(currentProduct);
        alert('Produk berhasil ditambahkan');
      }
      setShowModal(false);
      fetchProducts(search);
    } catch (error) {
      alert('Gagal menyimpan produk');
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
          <h1 className="text-3xl font-bold text-gray-900">Manajemen Produk</h1>
          {user.role === 'admin' && (
            <button onClick={handleAdd} className="btn-primary">
              + Tambah Produk
            </button>
          )}
        </div>

        <div className="card mb-6">
          <input
            type="text"
            placeholder="Cari produk..."
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
                <th>Nama Produk</th>
                <th>Kategori</th>
                <th>Harga</th>
                <th>Stok</th>
                <th>Aksi</th>
              </tr>
            </thead>
            <tbody>
              {products.map((product) => (
                <tr key={product.id}>
                  <td>{product.id}</td>
                  <td>{product.name}</td>
                  <td>{product.category_name}</td>
                  <td>{formatCurrency(product.price)}</td>
                  <td>
                    <span className={`px-2 py-1 rounded ${product.stock < 10 ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'}`}>
                      {product.stock}
                    </span>
                  </td>
                  <td>
                    {user.role === 'admin' && (
                      <>
                        <button onClick={() => handleEdit(product)} className="text-blue-600 hover:text-blue-800 mr-3">
                          Edit
                        </button>
                        <button onClick={() => handleDelete(product.id)} className="text-red-600 hover:text-red-800">
                          Hapus
                        </button>
                      </>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-8 max-w-md w-full">
            <h2 className="text-2xl font-bold mb-4">
              {editMode ? 'Edit Produk' : 'Tambah Produk'}
            </h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">Nama Produk</label>
                <input
                  type="text"
                  required
                  value={currentProduct.name}
                  onChange={(e) => setCurrentProduct({ ...currentProduct, name: e.target.value })}
                  className="input-field"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Kategori</label>
                <select
                  required
                  value={currentProduct.category_id}
                  onChange={(e) => setCurrentProduct({ ...currentProduct, category_id: e.target.value })}
                  className="input-field"
                >
                  <option value="">Pilih Kategori</option>
                  {categories.map((cat) => (
                    <option key={cat.id} value={cat.id}>{cat.name}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Deskripsi</label>
                <textarea
                  value={currentProduct.description}
                  onChange={(e) => setCurrentProduct({ ...currentProduct, description: e.target.value })}
                  className="input-field"
                  rows="3"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Harga</label>
                <input
                  type="number"
                  required
                  value={currentProduct.price}
                  onChange={(e) => setCurrentProduct({ ...currentProduct, price: e.target.value })}
                  className="input-field"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Stok</label>
                <input
                  type="number"
                  required
                  value={currentProduct.stock}
                  onChange={(e) => setCurrentProduct({ ...currentProduct, stock: e.target.value })}
                  className="input-field"
                />
              </div>
              <div className="flex space-x-3 mt-6">
                <button type="submit" className="btn-primary flex-1">
                  Simpan
                </button>
                <button type="button" onClick={() => setShowModal(false)} className="btn-secondary flex-1">
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

export default Products;
