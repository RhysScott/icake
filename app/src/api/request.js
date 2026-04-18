import router from '@/router'
import axios from 'axios'

const request = axios.create({
  baseURL: import.meta.env.VITE_BASE_URL || '/api',
  timeout: 10000
})

// 请求拦截器
request.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    console.log("token:", token)

    // 有 token 才携带
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }

    return config
  },
  (err) => Promise.reject(err)
)

// 响应拦截器（处理 401 未登录）
request.interceptors.response.use(
  (res) => res.data,
  (err) => {
    console.error('接口异常：', err)

    // 401 未登录 / token 过期
    if (err.response && err.response.status === 401) {
      localStorage.removeItem('token')
      router.push('/login')
      alert('登录已过期，请重新登录')
    }

    return Promise.reject(err)
  }
)

export default request
