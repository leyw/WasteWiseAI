import { useEffect, useState } from 'react'
import { BookOpen, ChevronRight, ArrowLeft, Leaf, Package, FileText, Wrench, GlassWater, Monitor, AlertTriangle, HelpCircle } from 'lucide-react'
import Layout from '../components/layout/Layout'
import Card from '../components/ui/Card'
import LoadingSpinner from '../components/ui/LoadingSpinner'
import ErrorMessage from '../components/ui/ErrorMessage'
import client from '../api/client'

const ICON_MAP = {
  Leaf, Package, FileText, Wrench, GlassWater, Monitor, AlertTriangle,
}
function GuideIcon({ name, className }) {
  const Icon = ICON_MAP[name] ?? HelpCircle
  return <Icon className={className} />
}

const CATEGORY_COLORS = {
  organik: 'bg-green-100 text-green-700',
  plastik: 'bg-blue-100 text-blue-700',
  kertas:  'bg-yellow-100 text-yellow-700',
  logam:   'bg-gray-200 text-gray-700',
  kaca:    'bg-cyan-100 text-cyan-700',
  elektronik: 'bg-purple-100 text-purple-700',
  b3:      'bg-red-100 text-red-700',
  lainnya: 'bg-orange-100 text-orange-700',
}

/** Render teks Markdown sederhana (heading, bold, list) */
function SimpleMarkdown({ text }) {
  if (!text) return null
  const lines = text.split('\n')
  return (
    <div className="space-y-1 text-sm text-gray-700 leading-relaxed">
      {lines.map((line, i) => {
        if (line.startsWith('## '))
          return <h2 key={i} className="text-base font-bold text-gray-900 mt-4 mb-1">{line.slice(3)}</h2>
        if (line.startsWith('### '))
          return <h3 key={i} className="text-sm font-semibold text-gray-800 mt-3 mb-0.5">{line.slice(4)}</h3>
        if (line.startsWith('- '))
          return <li key={i} className="ml-4 list-disc">{renderInline(line.slice(2))}</li>
        if (/^\d+\. /.test(line))
          return <li key={i} className="ml-4 list-decimal">{renderInline(line.replace(/^\d+\. /, ''))}</li>
        if (line.trim() === '')
          return <div key={i} className="h-1" />
        return <p key={i}>{renderInline(line)}</p>
      })}
    </div>
  )
}

function renderInline(text) {
  // Bold: **text**
  const parts = text.split(/(\*\*[^*]+\*\*)/)
  return parts.map((part, i) =>
    part.startsWith('**') && part.endsWith('**')
      ? <strong key={i}>{part.slice(2, -2)}</strong>
      : part
  )
}

export default function GuidesPage() {
  const [guides, setGuides] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [selected, setSelected] = useState(null)

  useEffect(() => {
    async function load() {
      try {
        const { data } = await client.get('/guides')
        setGuides(data)
      } catch {
        setError('Gagal memuat panduan.')
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  async function handleSelect(id) {
    try {
      const { data } = await client.get(`/guides/${id}`)
      setSelected(data)
    } catch {
      alert('Gagal memuat isi panduan.')
    }
  }

  // ── Detail view ───────────────────────────────────────────────────────────
  if (selected) {
    const colorClass = CATEGORY_COLORS[selected.category] ?? 'bg-gray-100 text-gray-700'
    return (
      <Layout title="Panduan Pengelolaan Sampah">
        <div className="max-w-2xl">
          <button
            onClick={() => setSelected(null)}
            className="inline-flex items-center gap-1.5 text-sm text-gray-500 hover:text-gray-800 transition-colors mb-4"
          >
            <ArrowLeft className="w-4 h-4" />
            Kembali ke Daftar Panduan
          </button>

          <Card className="p-6">
            <div className="flex items-start gap-3 mb-5">
              <div className={`w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 ${colorClass}`}>
                <GuideIcon name={selected.icon} className="w-5 h-5" />
              </div>
              <div>
                <p className="text-xs text-gray-400 mb-0.5">{selected.category ?? 'Umum'}</p>
                <h2 className="text-lg font-bold text-gray-900">{selected.title}</h2>
              </div>
            </div>
            <SimpleMarkdown text={selected.content} />
          </Card>
        </div>
      </Layout>
    )
  }

  // ── List view ─────────────────────────────────────────────────────────────
  return (
    <Layout title="Panduan Pengelolaan Sampah">
      <div className="mb-5">
        <p className="text-sm text-gray-500">
          Pelajari cara mengelola setiap jenis sampah dengan benar.
        </p>
      </div>

      {loading ? (
        <div className="flex justify-center py-20"><LoadingSpinner size="lg" /></div>
      ) : error ? (
        <ErrorMessage message={error} />
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {guides.map((guide) => {
            const colorClass = CATEGORY_COLORS[guide.category] ?? 'bg-gray-100 text-gray-700'
            return (
              <button
                key={guide.id}
                onClick={() => handleSelect(guide.id)}
                className="text-left"
              >
                <Card className="p-5 hover:shadow-md hover:border-primary-200 transition-all h-full flex flex-col">
                  <div className={`w-10 h-10 rounded-xl flex items-center justify-center mb-3 ${colorClass}`}>
                    <GuideIcon name={guide.icon} className="w-5 h-5" />
                  </div>
                  <p className="text-xs text-gray-400 mb-1 capitalize">{guide.category ?? 'Umum'}</p>
                  <h3 className="text-sm font-semibold text-gray-900 flex-1">{guide.title}</h3>
                  <div className="flex items-center gap-1 text-primary-600 text-xs mt-3">
                    <BookOpen className="w-3 h-3" />
                    <span>Baca selengkapnya</span>
                    <ChevronRight className="w-3 h-3" />
                  </div>
                </Card>
              </button>
            )
          })}
        </div>
      )}
    </Layout>
  )
}
