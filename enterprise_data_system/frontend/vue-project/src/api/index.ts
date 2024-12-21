import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '../router'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token') || sessionStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    console.error('Request error:', error)
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response) {
      switch (error.response.status) {
        case 401:
          // Clear auth data
          localStorage.removeItem('token')
          localStorage.removeItem('user')
          sessionStorage.removeItem('token')
          
          // Redirect to login
          if (router.currentRoute.value.name !== 'login') {
            ElMessage.error('Session expired. Please sign in again.')
            router.push({
              name: 'login',
              query: { redirect: router.currentRoute.value.fullPath }
            })
          }
          break

        case 403:
          ElMessage.error('Access denied')
          break

        case 404:
          ElMessage.error('Resource not found')
          break

        case 422:
          // Validation errors
          const validationErrors = error.response.data.errors
          if (validationErrors) {
            Object.values(validationErrors).forEach((messages: any) => {
              messages.forEach((message: string) => {
                ElMessage.error(message)
              })
            })
          } else {
            ElMessage.error('Validation failed')
          }
          break

        case 500:
          ElMessage.error('Internal server error')
          break

        default:
          ElMessage.error(
            error.response.data?.message || 
            'An error occurred. Please try again.'
          )
      }
    } else if (error.request) {
      // Request made but no response received
      ElMessage.error('No response from server. Please check your connection.')
    } else {
      // Error in request configuration
      ElMessage.error('Request failed. Please try again.')
    }
    return Promise.reject(error)
  }
)

export default api
