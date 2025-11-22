import axios from 'axios'
import toast from 'react-hot-toast'
import { useAuthStore } from '../stores/authStore'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = useAuthStore.getState().token
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout()
      window.location.href = '/login'
      toast.error('Session expired. Please login again.')
    }
    return Promise.reject(error)
  }
)

// Auth API
export const authAPI = {
  login: (credentials) => api.post('/auth/login', credentials),
  register: (userData) => api.post('/auth/register', userData),
  getCurrentUser: () => api.get('/auth/me'),
}

// Brand API
export const brandAPI = {
  getAll: () => api.get('/brands'),
  getById: (id) => api.get(`/brands/${id}`),
  create: (data) => api.post('/brands', data),
  update: (id, data) => api.put(`/brands/${id}`, data),
  delete: (id) => api.delete(`/brands/${id}`),
  autoProfile: (data) => api.post('/brands/auto_profile', data),
}

// Content API
export const contentAPI = {
  generate: (data) => api.post('/content/generate', data),
  getAll: (params) => api.get('/content', { params }),
  getById: (id) => api.get(`/content/${id}`),
  update: (id, data) => api.put(`/content/${id}`, data),
  delete: (id) => api.delete(`/content/${id}`),
}

// Scheduler API
export const schedulerAPI = {
  getCalendar: (params) => api.get('/scheduler/calendar', { params }),
  scheduleContent: (data) => api.post('/scheduler/schedule', data),
  getScheduled: (params) => api.get('/scheduler/scheduled', { params }),
  updateSchedule: (id, data) => api.put(`/scheduler/${id}`, data),
}

// Analytics API
export const analyticsAPI = {
  getOverview: (params) => api.get('/analytics/overview', { params }),
  getContentPerformance: (params) => api.get('/analytics/content', { params }),
  getEngagement: (params) => api.get('/analytics/engagement', { params }),
}

// Social Accounts API
export const socialAccountsAPI = {
  getAll: () => api.get('/social-accounts'),
  getByBrand: (brandId) => api.get(`/social-accounts/brand/${brandId}`),
  create: (data) => api.post('/social-accounts', data),
  update: (id, data) => api.put(`/social-accounts/${id}`, data),
  delete: (id) => api.delete(`/social-accounts/${id}`),
  refresh: (id) => api.post(`/social-accounts/${id}/refresh`),
}

// Tasks API
export const tasksAPI = {
  create: (data) => api.post('/tasks', data),
  getAll: (params) => api.get('/tasks', { params }),
  getById: (id) => api.get(`/tasks/${id}`),
  getStatus: (id) => api.get(`/tasks/${id}/status`),
}

// Strategy Agent API
export const strategyAPI = {
  generateStrategy: (data) => api.post('/agents/strategy', data),
}

// Graphics Agent API
export const graphicsAPI = {
  generateGraphic: (data) => api.post('/agents/graphics', data),
}

// Poster Agent API
export const posterAPI = {
  validateContent: (data) => api.post('/agents/poster/validate', data),
  postContent: (data) => api.post('/agents/poster/post', data),
}

export default api
