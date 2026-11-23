import { useEffect, useState } from 'react'
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, Cell, PieChart, Pie, Legend,
} from 'recharts'
import Layout from '../components/layout/Layout'
import Card from '../components/ui/Card'
import LoadingSpinner from '../components/ui/LoadingSpinner'
import ErrorMessage from '../components/ui/ErrorMessage'
import client from '../api/client'

const COLORS = {
  organik:    '#22c55e',
  plastik:    '#3b82f6',
  kertas:     '#eab308',
  logam:      '#6b7280',
  kaca:       '#06b6d4',
  elektronik: '#8b5cf6',
  b3:         '#ef4444',
  lainnya:    '#f97316',
}
const DEFAULT_COLOR = '#94a3b8'

const LABEL_MAP = {
  organik: 'Organik', plastik: 'Plastik', kertas: 'Kertas',
  logam: 'Logam', kaca: 'Kaca', elektronik: 'Elektronik',
  b3: 'B3', lainnya: 'Lainnya',
}

export default function StatisticsPage() {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    async function load() {
      try {
        const { data } = await client.get('/statistics')
        setStats(data)
      } catch {
        setError('Gagal memuat statistik.')
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  const chartData = (stats?.categories ?? []).map((c) => ({
    name: LABEL_MAP[c.category] ?? c.category,
    value: c.count,
    color: COLORS[c.category] ?? DEFAULT_COLOR,
  }))

  return (
    <Layout title="Statistik">
      {loading ? (
        <div className="flex justify-center py-20"><LoadingSpinner size="lg" /></div>
      ) : error ? (
        <ErrorMessage message={error} />
      ) : (
        <div className="space-y-5">
          {/* Summary cards */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <Card className="p-5 text-center">
              <p className="text-3xl font-bold text-primary-600">{stats?.total_analyses ?? 0}</p>
              <p className="text-sm text-gray-500 mt-1">Total Analisis</p>
            </Card>
            <Card className="p-5 text-center">
              <p className="text-3xl font-bold text-blue-500">{stats?.categories?.length ?? 0}</p>
              <p className="text-sm text-gray-500 mt-1">Kategori Ditemukan</p>
            </Card>
            <Card className="p-5 text-center">
              <p className="text-2xl font-bold text-emerald-600 truncate">
                {stats?.top_category_label ?? '—'}
              </p>
              <p className="text-sm text-gray-500 mt-1">
                Kategori Terbanyak
                {stats?.top_category_count
                  ? ` (${stats.top_category_count}x)`
                  : ''}
              </p>
            </Card>
          </div>

          {chartData.length === 0 ? (
            <Card className="p-10 text-center text-gray-400 text-sm">
              Belum ada data untuk ditampilkan. Mulai analisis sampah terlebih dahulu.
            </Card>
          ) : (
            <>
              {/* Bar chart */}
              <Card className="p-6">
                <h3 className="font-semibold text-gray-800 mb-4 text-sm">Jumlah Analisis per Kategori</h3>
                <ResponsiveContainer width="100%" height={260}>
                  <BarChart data={chartData} margin={{ top: 5, right: 10, left: -10, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                    <XAxis dataKey="name" tick={{ fontSize: 12 }} />
                    <YAxis allowDecimals={false} tick={{ fontSize: 12 }} />
                    <Tooltip
                      formatter={(val) => [val, 'Analisis']}
                      contentStyle={{ fontSize: 12, borderRadius: 8 }}
                    />
                    <Bar dataKey="value" radius={[4, 4, 0, 0]}>
                      {chartData.map((entry, idx) => (
                        <Cell key={idx} fill={entry.color} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </Card>

              {/* Pie chart */}
              <Card className="p-6">
                <h3 className="font-semibold text-gray-800 mb-4 text-sm">Distribusi Kategori Sampah</h3>
                <ResponsiveContainer width="100%" height={280}>
                  <PieChart>
                    <Pie
                      data={chartData}
                      dataKey="value"
                      nameKey="name"
                      cx="50%"
                      cy="50%"
                      outerRadius={100}
                      label={({ name, percent }) =>
                        `${name} ${(percent * 100).toFixed(0)}%`
                      }
                      labelLine={false}
                    >
                      {chartData.map((entry, idx) => (
                        <Cell key={idx} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip
                      formatter={(val) => [val, 'Analisis']}
                      contentStyle={{ fontSize: 12, borderRadius: 8 }}
                    />
                    <Legend wrapperStyle={{ fontSize: 12 }} />
                  </PieChart>
                </ResponsiveContainer>
              </Card>

              {/* Tabel */}
              <Card className="p-0 overflow-hidden">
                <div className="px-5 py-3 border-b border-gray-100">
                  <h3 className="font-semibold text-gray-800 text-sm">Rincian per Kategori</h3>
                </div>
                <table className="w-full text-sm">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="text-left px-5 py-2.5 text-xs font-semibold text-gray-500 uppercase">Kategori</th>
                      <th className="text-right px-5 py-2.5 text-xs font-semibold text-gray-500 uppercase">Jumlah</th>
                      <th className="text-right px-5 py-2.5 text-xs font-semibold text-gray-500 uppercase">Persentase</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-50">
                    {chartData.map((row) => (
                      <tr key={row.name} className="hover:bg-gray-50">
                        <td className="px-5 py-3 flex items-center gap-2">
                          <span
                            className="w-3 h-3 rounded-full flex-shrink-0"
                            style={{ backgroundColor: row.color }}
                          />
                          {row.name}
                        </td>
                        <td className="px-5 py-3 text-right font-medium">{row.value}</td>
                        <td className="px-5 py-3 text-right text-gray-500">
                          {stats?.total_analyses
                            ? `${((row.value / stats.total_analyses) * 100).toFixed(1)}%`
                            : '—'}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </Card>
            </>
          )}
        </div>
      )}
    </Layout>
  )
}
