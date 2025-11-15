import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { analyticsAPI, contentAPI, brandAPI } from '../services/api'
import { FiTrendingUp, FiEdit3, FiCalendar, FiUsers, FiArrowRight } from 'react-icons/fi'
import toast from 'react-hot-toast'

export default function Dashboard() {
  const [stats, setStats] = useState({
    totalContent: 0,
    scheduledContent: 0,
    totalBrands: 0,
    engagement: 0,
  })
  const [recentContent, setRecentContent] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      const [brandsRes, contentRes] = await Promise.all([
        brandAPI.getAll(),
        contentAPI.getAll({ limit: 5 }),
      ])

      setStats({
        totalContent: contentRes.data.total || 0,
        scheduledContent: 12, // Placeholder
        totalBrands: brandsRes.data.length || 0,
        engagement: 87.5, // Placeholder
      })

      setRecentContent(contentRes.data.items || contentRes.data || [])
    } catch (error) {
      toast.error('Failed to load dashboard data')
    } finally {
      setLoading(false)
    }
  }

  const statCards = [
    {
      name: 'Total Content',
      value: stats.totalContent,
      icon: FiEdit3,
      color: 'bg-blue-500',
      change: '+12%',
    },
    {
      name: 'Scheduled Posts',
      value: stats.scheduledContent,
      icon: FiCalendar,
      color: 'bg-purple-500',
      change: '+8%',
    },
    {
      name: 'Active Brands',
      value: stats.totalBrands,
      icon: FiUsers,
      color: 'bg-green-500',
      change: '+2',
    },
    {
      name: 'Avg. Engagement',
      value: `${stats.engagement}%`,
      icon: FiTrendingUp,
      color: 'bg-orange-500',
      change: '+5.2%',
    },
  ]

  return (
    <div className="max-w-7xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="mt-2 text-gray-600">
          Welcome back! Here's what's happening with your social media.
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {statCards.map((stat) => (
          <div key={stat.name} className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 mb-1">{stat.name}</p>
                <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
                <p className="text-sm text-green-600 mt-1">{stat.change}</p>
              </div>
              <div className={`${stat.color} w-12 h-12 rounded-lg flex items-center justify-center`}>
                <stat.icon className="text-white" size={24} />
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Quick Actions */}
      <div className="card mb-8">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Link
            to="/content/generate"
            className="flex items-center gap-3 p-4 bg-primary-50 hover:bg-primary-100 rounded-lg transition-colors group"
          >
            <div className="w-10 h-10 bg-primary-600 rounded-lg flex items-center justify-center">
              <FiEdit3 className="text-white" />
            </div>
            <div className="flex-1">
              <p className="font-medium text-gray-900">Generate Content</p>
              <p className="text-sm text-gray-600">Create AI-powered posts</p>
            </div>
            <FiArrowRight className="text-primary-600 group-hover:translate-x-1 transition-transform" />
          </Link>

          <Link
            to="/content/calendar"
            className="flex items-center gap-3 p-4 bg-purple-50 hover:bg-purple-100 rounded-lg transition-colors group"
          >
            <div className="w-10 h-10 bg-purple-600 rounded-lg flex items-center justify-center">
              <FiCalendar className="text-white" />
            </div>
            <div className="flex-1">
              <p className="font-medium text-gray-900">View Calendar</p>
              <p className="text-sm text-gray-600">Manage your schedule</p>
            </div>
            <FiArrowRight className="text-purple-600 group-hover:translate-x-1 transition-transform" />
          </Link>

          <Link
            to="/analytics"
            className="flex items-center gap-3 p-4 bg-green-50 hover:bg-green-100 rounded-lg transition-colors group"
          >
            <div className="w-10 h-10 bg-green-600 rounded-lg flex items-center justify-center">
              <FiTrendingUp className="text-white" />
            </div>
            <div className="flex-1">
              <p className="font-medium text-gray-900">View Analytics</p>
              <p className="text-sm text-gray-600">Track performance</p>
            </div>
            <FiArrowRight className="text-green-600 group-hover:translate-x-1 transition-transform" />
          </Link>
        </div>
      </div>

      {/* Recent Content */}
      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-bold text-gray-900">Recent Content</h2>
          <Link to="/content/generate" className="text-primary-600 hover:text-primary-700 text-sm font-medium">
            View All
          </Link>
        </div>

        {loading ? (
          <div className="text-center py-8 text-gray-500">Loading...</div>
        ) : recentContent.length === 0 ? (
          <div className="text-center py-8">
            <p className="text-gray-500 mb-4">No content yet</p>
            <Link to="/content/generate" className="btn btn-primary">
              Create Your First Post
            </Link>
          </div>
        ) : (
          <div className="space-y-4">
            {recentContent.map((content) => (
              <div
                key={content.id}
                className="flex items-start gap-4 p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
              >
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <span className="px-2 py-1 bg-primary-100 text-primary-700 rounded text-xs font-medium">
                      {content.platform}
                    </span>
                    <span className="text-sm text-gray-500">
                      {new Date(content.created_at).toLocaleDateString()}
                    </span>
                  </div>
                  <p className="text-gray-900 line-clamp-2">
                    {content.caption || content.text || 'No content'}
                  </p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
