import { Menu } from 'lucide-react'

export default function Navbar({ title, onMenuClick }) {
  return (
    <header className="h-14 bg-white border-b border-gray-200 flex items-center px-4 md:px-6 gap-3">
      {onMenuClick && (
        <button
          onClick={onMenuClick}
          className="md:hidden p-1 rounded text-gray-500 hover:text-gray-700"
          aria-label="Toggle menu"
        >
          <Menu className="w-5 h-5" />
        </button>
      )}
      <h1 className="text-base font-semibold text-gray-800">{title}</h1>
    </header>
  )
}
