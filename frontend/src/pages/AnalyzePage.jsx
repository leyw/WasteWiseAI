import { useState, useRef, useCallback } from 'react'
import { Upload, X, ScanLine, AlertTriangle, CheckCircle2, ImagePlus } from 'lucide-react'
import Layout from '../components/layout/Layout'
import Card from '../components/ui/Card'
import Badge from '../components/ui/Badge'
import LoadingSpinner from '../components/ui/LoadingSpinner'
import ErrorMessage from '../components/ui/ErrorMessage'
import client from '../api/client'

const MAX_MB = 5
const ALLOWED = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp']

function MockWarning() {
  return (
    <div className="flex items-start gap-2 bg-amber-50 border border-amber-200 text-amber-800 rounded-lg px-4 py-3 text-sm">
      <AlertTriangle className="w-4 h-4 mt-0.5 flex-shrink-0 text-amber-500" />
      <div>
        <span className="font-semibold">Hasil Mock — Bukan Klasifikasi AI Nyata.</span>{' '}
        Hasil ini dihasilkan oleh data contoh karena API Vision belum dikonfigurasi.
        Jangan jadikan acuan pengelolaan sampah sesungguhnya.
      </div>
    </div>
  )
}

function RecommendationItem({ label, value }) {
  if (!value) return null
  return (
    <div className="border-b border-gray-100 last:border-0 py-3">
      <p className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">{label}</p>
      <p className="text-sm text-gray-700">{value}</p>
    </div>
  )
}

export default function AnalyzePage() {
  const [file, setFile] = useState(null)
  const [preview, setPreview] = useState(null)
  const [validationError, setValidationError] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const fileInputRef = useRef(null)

  const validateAndSetFile = useCallback((f) => {
    setValidationError('')
    setResult(null)
    setError('')

    if (!ALLOWED.includes(f.type)) {
      setValidationError('Format tidak didukung. Gunakan JPG, PNG, atau WEBP.')
      return
    }
    if (f.size > MAX_MB * 1024 * 1024) {
      setValidationError(`Ukuran file melebihi batas ${MAX_MB} MB.`)
      return
    }
    setFile(f)
    setPreview(URL.createObjectURL(f))
  }, [])

  function handleFileChange(e) {
    if (e.target.files?.[0]) validateAndSetFile(e.target.files[0])
  }

  function handleDrop(e) {
    e.preventDefault()
    if (e.dataTransfer.files?.[0]) validateAndSetFile(e.dataTransfer.files[0])
  }

  function handleRemove() {
    setFile(null)
    setPreview(null)
    setResult(null)
    setError('')
    setValidationError('')
    if (fileInputRef.current) fileInputRef.current.value = ''
  }

  async function handleAnalyze() {
    if (!file) return
    setLoading(true)
    setError('')
    setResult(null)
    try {
      const form = new FormData()
      form.append('file', file)
      const { data } = await client.post('/analyze', form, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      setResult(data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Analisis gagal. Silakan coba lagi.')
    } finally {
      setLoading(false)
    }
  }

  const rec = result?.recommendation ?? {}

  return (
    <Layout title="Analisis Sampah">
      <div className="max-w-2xl mx-auto space-y-5">

        {/* Upload area */}
        <Card className="p-6">
          <h3 className="font-semibold text-gray-800 mb-4 flex items-center gap-2">
            <ImagePlus className="w-4 h-4 text-primary-600" />
            Upload Gambar Sampah
          </h3>

          {!preview ? (
            /* Drop zone */
            <div
              onDrop={handleDrop}
              onDragOver={(e) => e.preventDefault()}
              className="border-2 border-dashed border-gray-300 hover:border-primary-400 rounded-xl p-10 text-center cursor-pointer transition-colors"
              onClick={() => fileInputRef.current?.click()}
            >
              <Upload className="w-10 h-10 text-gray-300 mx-auto mb-3" />
              <p className="text-sm font-medium text-gray-600">
                Klik atau seret gambar ke sini
              </p>
              <p className="text-xs text-gray-400 mt-1">
                JPG, PNG, WEBP — maks. {MAX_MB} MB
              </p>
              <input
                ref={fileInputRef}
                type="file"
                accept="image/jpeg,image/png,image/webp"
                className="hidden"
                onChange={handleFileChange}
              />
            </div>
          ) : (
            /* Preview */
            <div className="relative">
              <img
                src={preview}
                alt="Preview"
                className="w-full max-h-72 object-contain rounded-xl bg-gray-100"
              />
              <button
                onClick={handleRemove}
                className="absolute top-2 right-2 bg-white rounded-full p-1.5 shadow text-gray-500 hover:text-red-500 transition-colors"
                title="Hapus gambar"
              >
                <X className="w-4 h-4" />
              </button>
              <p className="text-xs text-gray-500 mt-2 truncate">{file.name}</p>
            </div>
          )}

          {validationError && (
            <ErrorMessage message={validationError} className="mt-3" />
          )}

          <button
            onClick={handleAnalyze}
            disabled={!file || loading}
            className="btn-primary w-full mt-4 flex items-center justify-center gap-2"
          >
            {loading ? (
              <>
                <LoadingSpinner size="sm" />
                Menganalisis...
              </>
            ) : (
              <>
                <ScanLine className="w-4 h-4" />
                Analisis Sampah
              </>
            )}
          </button>
        </Card>

        {/* Error */}
        <ErrorMessage message={error} />

        {/* Hasil analisis */}
        {result && (
          <div className="space-y-4">
            {result.is_mock && <MockWarning />}

            {/* Identifikasi */}
            <Card className="p-6">
              <div className="flex items-start justify-between gap-3 mb-4">
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <CheckCircle2 className="w-4 h-4 text-primary-600" />
                    <h3 className="font-semibold text-gray-800">Hasil Identifikasi</h3>
                  </div>
                  <p className="text-xl font-bold text-gray-900">
                    {result.waste_name ?? 'Tidak diketahui'}
                  </p>
                </div>
                <div className="flex flex-col items-end gap-1.5 flex-shrink-0">
                  {result.category && (
                    <Badge label={result.category} type={result.category} />
                  )}
                  {result.is_mock && <Badge label="Mock" type="mock" />}
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3 text-sm mb-4">
                <div className="bg-gray-50 rounded-lg p-3">
                  <p className="text-xs text-gray-500 mb-0.5">Material</p>
                  <p className="font-medium text-gray-800">{result.material ?? '—'}</p>
                </div>
                <div className="bg-gray-50 rounded-lg p-3">
                  <p className="text-xs text-gray-500 mb-0.5">Tingkat Keyakinan</p>
                  <p className="font-medium text-gray-800">
                    {result.confidence != null
                      ? `${Math.round(result.confidence * 100)}%`
                      : '—'}
                  </p>
                </div>
              </div>

              {result.description && (
                <p className="text-sm text-gray-600 leading-relaxed bg-gray-50 rounded-lg p-3">
                  {result.description}
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
          </div>
        )}
      </div>
    </Layout>
  )
}
