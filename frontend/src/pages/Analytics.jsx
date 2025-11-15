import { FiTrendingUp, FiBarChart2 } from 'react-icons/fi'

export default function Analytics() {
  return (
    <div className="max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Analytics Dashboard</h1>
        <p className="mt-2 text-gray-600">Track your social media performance</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <div className="card">
          <FiTrendingUp className="text-green-600 mb-2" size={32} />
          <h3 className="text-2xl font-bold text-gray-900">12.5K</h3>
          <p className="text-gray-600">Total Engagement</p>
        </div>
        <div className="card">
          <FiBarChart2 className="text-blue-600 mb-2" size={32} />
          <h3 className="text-2xl font-bold text-gray-900">87.5%</h3>
          <p className="text-gray-600">Engagement Rate</p>
        </div>
        <div className="card">
          <FiTrendingUp className="text-purple-600 mb-2" size={32} />
          <h3 className="text-2xl font-bold text-gray-900">+2.4K</h3>
          <p className="text-gray-600">New Followers</p>
        </div>
      </div>

      <div className="card">
        <div className="text-center py-12">
          <FiBarChart2 className="mx-auto mb-4 text-gray-400" size={64} />
          <h3 className="text-xl font-medium text-gray-900 mb-2">Detailed Analytics</h3>
          <p className="text-gray-600">Connect your social accounts to view detailed analytics</p>
        </div>
      </div>
    </div>
  )
}
