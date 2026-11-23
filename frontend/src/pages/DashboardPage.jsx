import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { ScanLine, History, BarChart2, TrendingUp, Clock, Leaf } from 'lucide-react'
import Layout from '../components/layout/Layout'
import Card from '../components/ui/Card'
import Badge from '../components/ui/Badge'
import LoadingSpinner from '../components/ui/LoadingSpinner'
import { useAuth } from '../context/AuthContext'
import client from '../api/client'

function StatCard({ icon: Icon, label, value, color }) {
  return (
    <Card className="p-5 flex items-center gap-4">
      <div className={`w-12 h-12 rounded-xl flex items-center justify-center flex-shrink-0 ${color}`}>
        <Icon className="w-6 h-6 text-white" />
      </div>
      <div>
        <p className="text-sm text-gray-500">{label}</p>
        <p className="text-2xl font-bold text-gray-900">{value}</p>
      </div>
    </Card>
  )
}

export default function DashboardPage() {
  const { user } = useAuth()
  const [stats, setStats] = useState(null)
  const [recent, setRecent] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function load() {
      try {
        const [statsRes, histRes] = await Promise.all([
          client.get('/statistics'),
          client.get('/history?limit=5'),
        ])
        setStats(statsRes.data)
        setRecent(histRes.data)
      } catch {
        // Tampilkan dashboard kosong jika gagal
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  return (
    <Layout title="Dashboard">
      {/* Sambutan */}
      <div className="mb-6">
        <h2 className="text-xl font-semibold text-gray-900">
          Selamat datang, {user?.username}!
        </h2>
        <p className="text-sm text-gray-500 mt-1">
          Mulai analisis sampah atau lihat riwayat aktivitasmu.
        </p>
      </div>

      {loading ? (
        <div className="flex items-center justify-center py-20">
          <LoadingSpinner size="lg" />
        </div>
      ) : (
        <>
          {/* Stat cards */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
            <StatCard
              icon={BarChart2}
              label="Total Analisis"
              value={stats?.total_analyses ?? 0}
              color="bg-primary-600"
            />
            <StatCard
              icon={TrendingUp}
              label="Kategori Terbanyak"
              value={stats?.top_category_label ?? '—'}
              color="bg-blue-500"
            />
            <StatCard
              icon={Leaf}
              label="Kategori Unik"
              value={stats?.categories?.length ?? 0}
              color="bg-emerald-500"
            />
          </div>

          {/* CTA Analisis */}
          <Card className="p-6 mb-6 bg-gradient-to-r from-primary-600 to-emerald-500 border-0">
            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
              <div>
                <h3 className="text-white font-semibold text-lg">Mulai Analisis Sampah</h3>
                <p className="text-primary-100 text-sm mt-1">
                  Upload foto sampah dan dapatkan identifikasi serta rekomendasi pengelolaan.
                </p>
              </div>
              <Link
                to="/analisis"
                className="flex-shrink-0 flex items-center gap-2 bg-white text-primary-700 font-medium px-5 py-2.5 rounded-lg hover:bg-primary-50 transition-colors text-sm"
              >
                <ScanLine className="w-4 h-4" />
                Analisis Sekarang
              </Link>
            </div>
          </Card>

          {/* Riwayat terbaru */}
          <Card className="p-0 overflow-hidden">
            <div className="px-5 py-4 border-b border-gray-100 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Clock className="w-4 h-4 text-gray-400" />
                <span className="font-medium text-gray-800 text-sm">Aktivitas Terbaru</span>
              </div>
              <Link to="/riwayat" className="text-xs text-primary-600 hover:underline">
                Lihat semua
              </Link>
            </div>

            {recent.length === 0 ? (
              <div className="px-5 py-10 text-center text-gray-400 text-sm">
                Belum ada riwayat analisis.{' '}
                <Link to="/analisis" className="text-primary-600 hover:underline">
                  Mulai analisis pertama kamu!
                </Link>
              </div>
            ) : (
              <ul className="divide-y divide-gray-50">
                {recent.map((item) => (
                  <li key={item.id}>
                    <Link
                      to={`/riwayat/${item.id}`}
                      className="flex items-center gap-3 px-5 py-3.5 hover:bg-gray-50 transition-colors"
                    >
                      {/* Thumbnail */}
                      <div className="w-10 h-10 rounded-lg bg-gray-100 overflow-hidden flex-shrink-0">
                        <img
                          src={`/${item.image_path}`}
                          alt={item.filename}
                          className="w-full h-full object-cover"
                          onError={(e) => { e.target.style.display = 'none' }}
                        />
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-gray-800 truncate">
                          {item.waste_name ?? item.filename}
                        </p>
                        <p className="text-xs text-gray-400 mt-0.5">
                          {item.created_at
                            ? new Date(item.created_at).toLocaleString('id-ID', {
                                dateStyle: 'medium',
                                timeStyle: 'short',
                              })
                            : ''}
                        </p>
                      </div>
                      <div className="flex items-center gap-2 flex-shrink-0">
                        {item.category && (
                          <Badge label={item.category} type={item.category} />
                        )}
                        {item.is_mock && (
                          <Badge label="Mock" type="mock" />
                        )}
                      </div>
                    </Link>
                  </li>
                ))}
              </ul>
            )}
          </Card>
        </>
      )}
    </Layout>
  )
}
