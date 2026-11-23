const variants = {
  organik:    'bg-green-100 text-green-800',
  plastik:    'bg-blue-100 text-blue-800',
  kertas:     'bg-yellow-100 text-yellow-800',
  logam:      'bg-gray-200 text-gray-800',
  kaca:       'bg-cyan-100 text-cyan-800',
  elektronik: 'bg-purple-100 text-purple-800',
  b3:         'bg-red-100 text-red-800',
  lainnya:    'bg-orange-100 text-orange-800',
  mock:       'bg-amber-100 text-amber-700',
  default:    'bg-gray-100 text-gray-700',
}

export default function Badge({ label, type = 'default', className = '' }) {
  const color = variants[type?.toLowerCase()] ?? variants.default
  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${color} ${className}`}>
      {label}
    </span>
  )
}
