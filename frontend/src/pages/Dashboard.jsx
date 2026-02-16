import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import { dashboardAPI } from '../services/api';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, BarElement, ArcElement, Title, Tooltip, Legend } from 'chart.js';
import { Line, Pie, Bar } from 'react-chartjs-2';

// Register ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

function Dashboard() {
  const [stats, setStats] = useState({});
  const [salesChart, setSalesChart] = useState({ labels: [], values: [] });
  const [categoryChart, setCategoryChart] = useState({ labels: [], values: [] });
  const [topProducts, setTopProducts] = useState({ labels: [], values: [] });
  const [recentTransactions, setRecentTransactions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      // Helper to catch individual errors and return default structure
      const fetchData = (promise) => promise.catch(err => {
        console.error('API call failed:', err);
        return { data: { data: [] } }; // Return empty data structure on error
      });

      const [statsRes, salesRes, categoryRes, topProductsRes, recentRes] = await Promise.all([
        fetchData(dashboardAPI.getStats()),
        fetchData(dashboardAPI.getSalesChart()),
        fetchData(dashboardAPI.getCategoryChart()),
        fetchData(dashboardAPI.getTopProducts()),
        fetchData(dashboardAPI.getRecentTransactions()),
      ]);

      // Handle stats separately as it returns an object, not array
      setStats(statsRes?.data?.data || {});
      setSalesChart(salesRes?.data?.data || { labels: [], values: [] });
      setCategoryChart(categoryRes?.data?.data || { labels: [], values: [] });
      setTopProducts(topProductsRes?.data?.data || { labels: [], values: [] });
      setRecentTransactions(recentRes?.data?.data || []);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const salesChartData = {
    labels: salesChart.labels,
    datasets: [
      {
        label: 'Penjualan (Rp)',
        data: salesChart.values,
        borderColor: 'rgb(14, 165, 233)',
        backgroundColor: 'rgba(14, 165, 233, 0.1)',
        tension: 0.4,
      },
    ],
  };

  const categoryChartData = {
    labels: categoryChart.labels,
    datasets: [
      {
        data: categoryChart.values,
        backgroundColor: [
          'rgba(14, 165, 233, 0.8)',
          'rgba(34, 197, 94, 0.8)',
          'rgba(251, 146, 60, 0.8)',
          'rgba(168, 85, 247, 0.8)',
          'rgba(236, 72, 153, 0.8)',
        ],
      },
    ],
  };

  const topProductsChartData = {
    labels: topProducts.labels,
    datasets: [
      {
        label: 'Jumlah Terjual',
        data: topProducts.values,
        backgroundColor: 'rgba(14, 165, 233, 0.8)',
      },
    ],
  };

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('id-ID', {
      style: 'currency',
      currency: 'IDR',
      minimumFractionDigits: 0,
    }).format(value);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <div className="flex items-center justify-center h-96">
          <div className="text-xl text-gray-600">Loading...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Dashboard</h1>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="card bg-gradient-to-br from-blue-500 to-blue-600 text-white">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-blue-100 text-sm">Total Penjualan</p>
                <p className="text-2xl font-bold mt-2">{formatCurrency(stats.total_sales || 0)}</p>
              </div>
              <div className="text-4xl opacity-50">💰</div>
            </div>
          </div>

          <div className="card bg-gradient-to-br from-green-500 to-green-600 text-white">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-green-100 text-sm">Total Produk</p>
                <p className="text-2xl font-bold mt-2">{stats.total_products || 0}</p>
              </div>
              <div className="text-4xl opacity-50">📦</div>
            </div>
          </div>

          <div className="card bg-gradient-to-br from-purple-500 to-purple-600 text-white">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-purple-100 text-sm">Total Customer</p>
                <p className="text-2xl font-bold mt-2">{stats.total_customers || 0}</p>
              </div>
              <div className="text-4xl opacity-50">👥</div>
            </div>
          </div>

          <div className="card bg-gradient-to-br from-orange-500 to-orange-600 text-white">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-orange-100 text-sm">Total Transaksi</p>
                <p className="text-2xl font-bold mt-2">{stats.total_transactions || 0}</p>
              </div>
              <div className="text-4xl opacity-50">🛒</div>
            </div>
          </div>
        </div>

        {/* Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <div className="card">
            <h2 className="text-xl font-semibold mb-4">Trend Penjualan (7 Hari Terakhir)</h2>
            <Line data={salesChartData} options={{ responsive: true, maintainAspectRatio: true }} />
          </div>

          <div className="card">
            <h2 className="text-xl font-semibold mb-4">Penjualan per Kategori</h2>
            <Pie data={categoryChartData} options={{ responsive: true, maintainAspectRatio: true }} />
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <div className="card">
            <h2 className="text-xl font-semibold mb-4">Top 5 Produk Terlaris</h2>
            <Bar data={topProductsChartData} options={{ responsive: true, maintainAspectRatio: true }} />
          </div>

          <div className="card">
            <h2 className="text-xl font-semibold mb-4">Transaksi Terbaru</h2>
            <div className="overflow-x-auto">
              <table className="min-w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-4 py-2 text-left text-xs font-medium text-gray-500">Tanggal</th>
                    <th className="px-4 py-2 text-left text-xs font-medium text-gray-500">Customer</th>
                    <th className="px-4 py-2 text-right text-xs font-medium text-gray-500">Total</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {recentTransactions.map((transaction) => (
                    <tr key={transaction.id} className="hover:bg-gray-50">
                      <td className="px-4 py-2 text-sm">
                        {new Date(transaction.transaction_date).toLocaleDateString('id-ID')}
                      </td>
                      <td className="px-4 py-2 text-sm">{transaction.customer_name}</td>
                      <td className="px-4 py-2 text-sm text-right font-medium">
                        {formatCurrency(transaction.total_amount)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
