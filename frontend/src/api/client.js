import axios from 'axios'

const client = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
})

// Sisipkan token JWT di setiap request jika tersedia
client.interceptors.request.use((config) => {
  const token = localStorage.getItem('wastewise_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Tangani error 401 — hapus token dan redirect ke login
client.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('wastewise_token')
      localStorage.removeItem('wastewise_user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default client
