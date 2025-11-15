import { create } from 'zustand'

export const useAuthStore = create((set) => ({
  user: null,
  token: null,
  isAuthenticated: false,

  login: (user, token) => {
    set({ user, token, isAuthenticated: true })
    localStorage.setItem('auth-token', token)
    localStorage.setItem('auth-user', JSON.stringify(user))
  },

  logout: () => {
    set({ user: null, token: null, isAuthenticated: false })
    localStorage.removeItem('auth-token')
    localStorage.removeItem('auth-user')
  },

  updateUser: (user) => {
    set({ user })
    localStorage.setItem('auth-user', JSON.stringify(user))
  },

  // Initialize from localStorage
  initialize: () => {
    const token = localStorage.getItem('auth-token')
    const userStr = localStorage.getItem('auth-user')
    if (token && userStr) {
      const user = JSON.parse(userStr)
      set({ user, token, isAuthenticated: true })
    }
  },
}))

// Initialize auth state from localStorage on app start
useAuthStore.getState().initialize()
