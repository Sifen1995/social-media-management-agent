import { FiShare2, FiInstagram, FiTwitter, FiLinkedin } from 'react-icons/fi'

const platforms = [
  { id: 'instagram', name: 'Instagram', icon: FiInstagram, color: 'bg-pink-500' },
  { id: 'twitter', name: 'Twitter/X', icon: FiTwitter, color: 'bg-blue-400' },
  { id: 'linkedin', name: 'LinkedIn', icon: FiLinkedin, color: 'bg-blue-700' },
]

export default function SocialAccounts() {
  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Social Accounts</h1>
        <p className="mt-2 text-gray-600">Connect and manage your social media accounts</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {platforms.map((platform) => (
          <div key={platform.id} className="card text-center">
            <div className={`${platform.color} w-16 h-16 rounded-full mx-auto mb-4 flex items-center justify-center`}>
              <platform.icon className="text-white" size={32} />
            </div>
            <h3 className="text-lg font-bold text-gray-900 mb-2">{platform.name}</h3>
            <button className="btn btn-primary w-full">Connect</button>
          </div>
        ))}
      </div>

      <div className="card mt-8">
        <div className="text-center py-8">
          <FiShare2 className="mx-auto mb-4 text-gray-400" size={48} />
          <h3 className="text-lg font-medium text-gray-900 mb-2">OAuth Integration Required</h3>
          <p className="text-gray-600 text-sm">
            Social account connections require OAuth setup with each platform
          </p>
        </div>
      </div>
    </div>
  )
}
