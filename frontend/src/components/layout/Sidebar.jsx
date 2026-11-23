import { NavLink, useNavigate } from 'react-router-dom'
import {
  LayoutDashboard,
  ScanLine,
  History,
  BarChart2,
  BookOpen,
  LogOut,
  Leaf,
} from 'lucide-react'
import { useAuth } from '../../context/AuthContext'

const navItems = [
  { to: '/dashboard', icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/analisis', icon: ScanLine, label: 'Analisis Sampah' },
  { to: '/riwayat', icon: History, label: 'Riwayat Analisis' },
  { to: '/statistik', icon: BarChart2, label: 'Statistik' },
  { to: '/panduan', icon: BookOpen, label: 'Panduan' },
]

export default function Sidebar() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  function handleLogout() {
    logout()
    navigate('/login')
  }

  return (
    <aside className="flex flex-col w-64 min-h-screen bg-white border-r border-gray-200 shadow-sm">
      {/* Logo */}
      <div className="flex items-center gap-2 px-6 py-5 border-b border-gray-100">
        <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
          <Leaf className="w-5 h-5 text-white" />
        </div>
        <span className="font-bold text-lg text-primary-700">WasteWise AI</span>
      </div>

      {/* Navigasi */}
      <nav className="flex-1 px-3 py-4 space-y-1">
        {navItems.map(({ to, icon: Icon, label }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                isActive
                  ? 'bg-primary-50 text-primary-700'
                  : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
              }`
            }
          >
            <Icon className="w-4 h-4 flex-shrink-0" />
            {label}
          </NavLink>
        ))}
      </nav>

      {/* User info + Logout */}
      <div className="px-4 py-4 border-t border-gray-100">
        <div className="text-xs text-gray-500 mb-1">Masuk sebagai</div>
        <div className="text-sm font-medium text-gray-800 truncate">{user?.username}</div>
        <button
          onClick={handleLogout}
          className="mt-3 flex items-center gap-2 text-sm text-red-500 hover:text-red-700 transition-colors"
        >
          <LogOut className="w-4 h-4" />
          Keluar
        </button>
      </div>
    </aside>
  )
}
