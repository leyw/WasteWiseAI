import { useEffect, useState } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { ArrowLeft, AlertTriangle, CheckCircle2, Trash2 } from 'lucide-react'
import Layout from '../components/layout/Layout'
import Card from '../components/ui/Card'
import Badge from '../components/ui/Badge'
import LoadingSpinner from '../components/ui/LoadingSpinner'
import ErrorMessage from '../components/ui/ErrorMessage'
import client from '../api/client'

function RecommendationItem({ label, value }) {
  if (!value) return null
  return (
    <div className="border-b border-gray-100 last:border-0 py-3">
      <p className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">{label}</p>
      <p className="text-sm text-gray-700">{value}</p>
    </div>
  )
}

export default function HistoryDetailPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [item, setItem] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [deleting, setDeleting] = useState(false)

  useEffect(() => {
    async function load() {
      try {
        const { data } = await client.get(`/history/${id}`)
        setItem(data)
      } catch (err) {
        setError(
          err.response?.status === 404
            ? 'Riwayat tidak ditemukan.'
            : 'Gagal memuat detail riwayat.'
        )
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [id])

  async function handleDelete() {
    if (!confirm('Hapus riwayat ini secara permanen?')) return
    setDeleting(true)
    try {
      await client.delete(`/history/${id}`)
      navigate('/riwayat')
    } catch {
      alert('Gagal menghapus riwayat.')
      setDeleting(false)
    }
  }

  const rec = item?.recommendation ?? {}

  return (
    <Layout title="Detail Riwayat">
      {/* Back */}
      <div className="mb-4">
        <Link
          to="/riwayat"
          className="inline-flex items-center gap-1.5 text-sm text-gray-500 hover:text-gray-800 transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          Kembali ke Riwayat
        </Link>
      </div>

      {loading ? (
        <div className="flex justify-center py-20"><LoadingSpinner size="lg" /></div>
      ) : error ? (
        <ErrorMessage message={error} />
      ) : item ? (
        <div className="max-w-2xl space-y-5">
          {/* Mock warning */}
          {item.is_mock && (
            <div className="flex items-start gap-2 bg-amber-50 border border-amber-200 text-amber-800 rounded-lg px-4 py-3 text-sm">
              <AlertTriangle className="w-4 h-4 mt-0.5 flex-shrink-0 text-amber-500" />
              <div>
                <span className="font-semibold">Hasil Mock — Bukan Klasifikasi AI Nyata.</span>{' '}
                Jangan jadikan acuan pengelolaan sampah sesungguhnya.
              </div>
            </div>
          )}

          {/* Gambar + Identifikasi */}
          <Card className="p-6">
            {/* Gambar */}
            <div className="w-full max-h-60 rounded-xl bg-gray-100 overflow-hidden mb-5">
              <img
                src={`/${item.image_path}`}
                alt={item.filename}
                className="w-full h-full object-contain"
                onError={(e) => {
                  e.target.parentElement.classList.add('flex', 'items-center', 'justify-center')
                  e.target.style.display = 'none'
                  e.target.parentElement.innerHTML = '<span class="text-gray-400 text-sm">Gambar tidak tersedia</span>'
                }}
              />
            </div>

            {/* Header identifikasi */}
            <div className="flex items-start justify-between gap-3 mb-4">
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <CheckCircle2 className="w-4 h-4 text-primary-600" />
                  <span className="text-sm font-medium text-gray-500">Hasil Identifikasi</span>
                </div>
                <p className="text-xl font-bold text-gray-900">
                  {item.waste_name ?? 'Tidak diketahui'}
                </p>
              </div>
              <div className="flex flex-col items-end gap-1.5 flex-shrink-0">
                {item.category && <Badge label={item.category} type={item.category} />}
                {item.is_mock && <Badge label="Mock" type="mock" />}
              </div>
            </div>

            {/* Detail grid */}
            <div className="grid grid-cols-2 gap-3 text-sm mb-4">
              <div className="bg-gray-50 rounded-lg p-3">
                <p className="text-xs text-gray-500 mb-0.5">Material</p>
                <p className="font-medium text-gray-800">{item.material ?? '—'}</p>
              </div>
              <div className="bg-gray-50 rounded-lg p-3">
                <p className="text-xs text-gray-500 mb-0.5">Tingkat Keyakinan</p>
                <p className="font-medium text-gray-800">
                  {item.confidence != null ? `${Math.round(item.confidence * 100)}%` : '—'}
                </p>
              </div>
              <div className="bg-gray-50 rounded-lg p-3">
                <p className="text-xs text-gray-500 mb-0.5">File</p>
                <p className="font-medium text-gray-800 truncate">{item.filename}</p>
              </div>
              <div className="bg-gray-50 rounded-lg p-3">
                <p className="text-xs text-gray-500 mb-0.5">Waktu Analisis</p>
                <p className="font-medium text-gray-800 text-xs">
                  {item.created_at
                    ? new Date(item.created_at).toLocaleString('id-ID', {
                        dateStyle: 'long', timeStyle: 'short',
                      })
                    : '—'}
                </p>
              </div>
            </div>

            {item.description && (
              <p className="text-sm text-gray-600 leading-relaxed bg-gray-50 rounded-lg p-3">
                {item.description}
              </p>
            )}
          </Card>

          {/* Rekomendasi */}
          {Object.keys(rec).length > 0 && (
            <Card className="p-6">
              <h3 className="font-semibold text-gray-800 mb-3">Rekomendasi Pengelolaan</h3>
              <RecommendationItem label="Cara Memilah" value={rec.pemilahan} />
              <RecommendationItem label="Daur Ulang" value={rec.daur_ulang} />
              <RecommendationItem label="Persiapan Sebelum Dibuang" value={rec.persiapan} />
              <RecommendationItem label="Cara Pembuangan" value={rec.pembuangan} />
              <RecommendationItem label="Tips Pengurangan" value={rec.tips_pengurangan} />
            </Card>
          )}

          {/* Hapus */}
          <div className="flex justify-end">
            <button
              onClick={handleDelete}
              disabled={deleting}
              className="flex items-center gap-2 text-sm text-red-500 hover:text-red-700 border border-red-200 hover:border-red-400 px-4 py-2 rounded-lg transition-colors disabled:opacity-50"
            >
              {deleting ? <LoadingSpinner size="sm" /> : <Trash2 className="w-4 h-4" />}
              Hapus Riwayat
            </button>
          </div>
        </div>
      ) : null}
    </Layout>
  )
}
