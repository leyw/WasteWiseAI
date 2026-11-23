import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { History, Trash2, ChevronRight, AlertTriangle } from 'lucide-react'
import Layout from '../components/layout/Layout'
import Card from '../components/ui/Card'
import Badge from '../components/ui/Badge'
import LoadingSpinner from '../components/ui/LoadingSpinner'
import ErrorMessage from '../components/ui/ErrorMessage'
import client from '../api/client'

const CATEGORIES = ['', 'organik', 'plastik', 'kertas', 'logam', 'kaca', 'elektronik', 'b3', 'lainnya']
const CATEGORY_LABELS = {
  '': 'Semua Kategori',
  organik: 'Organik', plastik: 'Plastik', kertas: 'Kertas',
  logam: 'Logam', kaca: 'Kaca', elektronik: 'Elektronik',
  b3: 'B3', lainnya: 'Lainnya',
}

export default function HistoryPage() {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [category, setCategory] = useState('')
  const [deletingId, setDeletingId] = useState(null)

  async function load(cat = '') {
    setLoading(true)
    setError('')
    try {
      const params = cat ? `?category=${cat}` : ''
      const { data } = await client.get(`/history${params}`)
      setItems(data)
    } catch {
      setError('Gagal memuat riwayat.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  function handleCategoryChange(cat) {
    setCategory(cat)
    load(cat)
  }

  async function handleDelete(id) {
    if (!confirm('Hapus riwayat ini?')) return
    setDeletingId(id)
    try {
      await client.delete(`/history/${id}`)
      setItems((prev) => prev.filter((i) => i.id !== id))
    } catch {
      alert('Gagal menghapus riwayat.')
    } finally {
      setDeletingId(null)
    }
  }

  return (
    <Layout title="Riwayat Analisis">
      {/* Filter */}
      <div className="flex flex-wrap gap-2 mb-5">
        {CATEGORIES.map((cat) => (
          <button
            key={cat}
            onClick={() => handleCategoryChange(cat)}
            className={`text-xs px-3 py-1.5 rounded-full font-medium transition-colors ${
              category === cat
                ? 'bg-primary-600 text-white'
                : 'bg-white text-gray-600 border border-gray-200 hover:border-primary-300'
            }`}
          >
            {CATEGORY_LABELS[cat]}
          </button>
        ))}
      </div>

      {loading ? (
        <div className="flex justify-center py-20"><LoadingSpinner size="lg" /></div>
      ) : error ? (
        <ErrorMessage message={error} />
      ) : items.length === 0 ? (
        <Card className="p-10 text-center text-gray-400 text-sm">
          Belum ada riwayat analisis.{' '}
          <Link to="/analisis" className="text-primary-600 hover:underline">
            Mulai analisis sekarang!
          </Link>
        </Card>
      ) : (
        <Card className="p-0 overflow-hidden">
          <ul className="divide-y divide-gray-100">
            {items.map((item) => (
              <li key={item.id} className="flex items-center gap-3 px-4 py-3.5 hover:bg-gray-50 transition-colors">
                {/* Thumbnail */}
                <div className="w-11 h-11 rounded-lg bg-gray-100 overflow-hidden flex-shrink-0">
                  <img
                    src={`/${item.image_path}`}
                    alt={item.filename}
                    className="w-full h-full object-cover"
                    onError={(e) => { e.target.style.display = 'none' }}
                  />
                </div>

                {/* Info */}
                <Link to={`/riwayat/${item.id}`} className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-gray-800 truncate">
                    {item.waste_name ?? item.filename}
                  </p>
                  <p className="text-xs text-gray-400 mt-0.5">
                    {item.created_at
                      ? new Date(item.created_at).toLocaleString('id-ID', {
                          dateStyle: 'medium', timeStyle: 'short',
                        })
                      : ''}
                  </p>
                </Link>

                {/* Badges */}
                <div className="flex items-center gap-1.5 flex-shrink-0">
                  {item.category && <Badge label={item.category} type={item.category} />}
                  {item.is_mock && <Badge label="Mock" type="mock" />}
                </div>

                {/* Actions */}
                <div className="flex items-center gap-1 flex-shrink-0">
                  <Link
                    to={`/riwayat/${item.id}`}
                    className="p-1.5 text-gray-400 hover:text-primary-600 transition-colors"
                    title="Lihat detail"
                  >
                    <ChevronRight className="w-4 h-4" />
                  </Link>
                  <button
                    onClick={() => handleDelete(item.id)}
                    disabled={deletingId === item.id}
                    className="p-1.5 text-gray-400 hover:text-red-500 transition-colors disabled:opacity-40"
                    title="Hapus"
                  >
                    {deletingId === item.id
                      ? <LoadingSpinner size="sm" />
                      : <Trash2 className="w-4 h-4" />}
                  </button>
                </div>
              </li>
            ))}
          </ul>
        </Card>
      )}
    </Layout>
  )
}
