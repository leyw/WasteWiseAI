import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { Leaf, Eye, EyeOff } from 'lucide-react'
import { useAuth } from '../context/AuthContext'
import ErrorMessage from '../components/ui/ErrorMessage'

export default function RegisterPage() {
  const { register: registerUser } = useAuth()
  const navigate = useNavigate()
  const { register, handleSubmit, watch, formState: { errors, isSubmitting } } = useForm()
  const [serverError, setServerError] = useState('')
  const [showPassword, setShowPassword] = useState(false)

  async function onSubmit(data) {
    setServerError('')
    try {
      await registerUser(data.username, data.email, data.password)
      navigate('/dashboard')
    } catch (err) {
      setServerError(
        err.response?.data?.detail || 'Terjadi kesalahan. Silakan coba lagi.'
      )
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-green-100 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Logo */}
        <div className="flex items-center justify-center gap-2 mb-8">
          <div className="w-10 h-10 bg-primary-600 rounded-xl flex items-center justify-center">
            <Leaf className="w-6 h-6 text-white" />
          </div>
          <span className="text-2xl font-bold text-primary-700">WasteWise AI</span>
        </div>

        {/* Card */}
        <div className="bg-white rounded-2xl shadow-lg p-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-1">Buat Akun Baru</h2>
          <p className="text-sm text-gray-500 mb-6">Daftar untuk mulai menggunakan WasteWise AI.</p>

          <ErrorMessage message={serverError} className="mb-4" />

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Username</label>
              <input
                type="text"
                className="input-field"
                placeholder="johndoe"
                {...register('username', {
                  required: 'Username wajib diisi.',
                  minLength: { value: 3, message: 'Username minimal 3 karakter.' },
                })}
              />
              {errors.username && <p className="text-xs text-red-500 mt-1">{errors.username.message}</p>}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
              <input
                type="email"
                className="input-field"
                placeholder="nama@email.com"
                {...register('email', {
                  required: 'Email wajib diisi.',
                  pattern: { value: /^\S+@\S+\.\S+$/, message: 'Format email tidak valid.' },
                })}
              />
              {errors.email && <p className="text-xs text-red-500 mt-1">{errors.email.message}</p>}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
              <div className="relative">
                <input
                  type={showPassword ? 'text' : 'password'}
                  className="input-field pr-10"
                  placeholder="Min. 6 karakter"
                  {...register('password', {
                    required: 'Password wajib diisi.',
                    minLength: { value: 6, message: 'Password minimal 6 karakter.' },
                  })}
                />
                <button
                  type="button"
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                  onClick={() => setShowPassword(!showPassword)}
                  tabIndex={-1}
                >
                  {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
              {errors.password && <p className="text-xs text-red-500 mt-1">{errors.password.message}</p>}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Konfirmasi Password</label>
              <input
                type={showPassword ? 'text' : 'password'}
                className="input-field"
                placeholder="Ulangi password"
                {...register('confirmPassword', {
                  required: 'Konfirmasi password wajib diisi.',
                  validate: (val) => val === watch('password') || 'Password tidak sama.',
                })}
              />
              {errors.confirmPassword && <p className="text-xs text-red-500 mt-1">{errors.confirmPassword.message}</p>}
            </div>

            <button
              type="submit"
              disabled={isSubmitting}
              className="btn-primary w-full mt-2"
            >
              {isSubmitting ? 'Memproses...' : 'Daftar'}
            </button>
          </form>

          <p className="text-sm text-center text-gray-500 mt-6">
            Sudah punya akun?{' '}
            <Link to="/login" className="text-primary-600 font-medium hover:underline">
              Masuk di sini
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}
