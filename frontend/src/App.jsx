import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import { useAuthStore } from './stores/authStore'

// Pages
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import ContentGenerator from './pages/ContentGenerator'
import ContentCalendar from './pages/ContentCalendar'
import Analytics from './pages/Analytics'
import BrandManagement from './pages/BrandManagement'
import SocialAccounts from './pages/SocialAccounts'

// Layout
import Layout from './components/Layout'

// Protected Route Component
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated } = useAuthStore()
  return isAuthenticated ? children : <Navigate to="/login" replace />
}

function App() {
  return (
    <Router>
      <Toaster position="top-right" />
      <Routes>
        {/* Public Routes */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Protected Routes */}
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <Layout />
            </ProtectedRoute>
          }
        >
          <Route index element={<Dashboard />} />
          <Route path="content/generate" element={<ContentGenerator />} />
          <Route path="content/calendar" element={<ContentCalendar />} />
          <Route path="analytics" element={<Analytics />} />
          <Route path="brands" element={<BrandManagement />} />
          <Route path="social-accounts" element={<SocialAccounts />} />
        </Route>

        {/* Fallback */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  )
}

export default App
