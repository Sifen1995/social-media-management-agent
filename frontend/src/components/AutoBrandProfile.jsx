import { useState } from 'react'
import { brandAPI } from '../services/api'
import toast from 'react-hot-toast'
import { FiGlobe, FiInstagram, FiLinkedin, FiTwitter, FiLoader, FiCheckCircle, FiAlertCircle } from 'react-icons/fi'
import { FaTiktok, FaFacebook } from 'react-icons/fa'

export default function AutoBrandProfile({ onProfileGenerated, onCancel }) {
  const [formData, setFormData] = useState({
    website: '',
    socials: {
      instagram: '',
      linkedin: '',
      twitter: '',
      tiktok: '',
      facebook: '',
    },
    use_playwright: false,
  })
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target

    if (name === 'use_playwright') {
      setFormData((prev) => ({ ...prev, use_playwright: checked }))
    } else if (name.startsWith('social_')) {
      const platform = name.replace('social_', '')
      setFormData((prev) => ({
        ...prev,
        socials: { ...prev.socials, [platform]: value },
      }))
    } else {
      setFormData((prev) => ({ ...prev, [name]: value }))
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    if (!formData.website) {
      toast.error('Website URL is required')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await brandAPI.autoProfile(formData)

      if (response.data.success) {
        setResult(response.data)
        toast.success('Brand profile generated successfully!')
      } else {
        setError(response.data.message || 'Failed to generate brand profile')
        toast.error(response.data.message || 'Failed to generate brand profile')
      }
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Failed to generate brand profile'
      setError(errorMsg)
      toast.error(errorMsg)
    } finally {
      setLoading(false)
    }
  }

  const handleUseProfile = () => {
    if (result?.data) {
      onProfileGenerated(result.data)
    }
  }

  const handleReset = () => {
    setFormData({
      website: '',
      socials: {
        instagram: '',
        linkedin: '',
        twitter: '',
        tiktok: '',
        facebook: '',
      },
      use_playwright: false,
    })
    setResult(null)
    setError(null)
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-bold text-gray-900">Auto-Generate Brand Profile</h2>
        <p className="mt-2 text-gray-600">
          Enter your website and social media URLs. Our AI will automatically research and generate a comprehensive brand profile.
        </p>
      </div>

      {/* Form */}
      {!result && (
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Website URL */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Website URL <span className="text-red-500">*</span>
            </label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <FiGlobe className="text-gray-400" />
              </div>
              <input
                type="url"
                name="website"
                value={formData.website}
                onChange={handleChange}
                className="input pl-10"
                placeholder="https://example.com"
                required
                disabled={loading}
              />
            </div>
          </div>

          {/* Social Media URLs */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-3">
              Social Media Profiles (Optional)
            </label>
            <div className="space-y-3">
              {/* Instagram */}
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <FiInstagram className="text-pink-500" />
                </div>
                <input
                  type="url"
                  name="social_instagram"
                  value={formData.socials.instagram}
                  onChange={handleChange}
                  className="input pl-10"
                  placeholder="Instagram profile URL"
                  disabled={loading}
                />
              </div>

              {/* LinkedIn */}
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <FiLinkedin className="text-blue-600" />
                </div>
                <input
                  type="url"
                  name="social_linkedin"
                  value={formData.socials.linkedin}
                  onChange={handleChange}
                  className="input pl-10"
                  placeholder="LinkedIn company page URL"
                  disabled={loading}
                />
              </div>

              {/* Twitter */}
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <FiTwitter className="text-blue-400" />
                </div>
                <input
                  type="url"
                  name="social_twitter"
                  value={formData.socials.twitter}
                  onChange={handleChange}
                  className="input pl-10"
                  placeholder="Twitter/X profile URL"
                  disabled={loading}
                />
              </div>

              {/* TikTok */}
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <FaTiktok className="text-gray-800" />
                </div>
                <input
                  type="url"
                  name="social_tiktok"
                  value={formData.socials.tiktok}
                  onChange={handleChange}
                  className="input pl-10"
                  placeholder="TikTok profile URL"
                  disabled={loading}
                />
              </div>

              {/* Facebook */}
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <FaFacebook className="text-blue-600" />
                </div>
                <input
                  type="url"
                  name="social_facebook"
                  value={formData.socials.facebook}
                  onChange={handleChange}
                  className="input pl-10"
                  placeholder="Facebook page URL"
                  disabled={loading}
                />
              </div>
            </div>
          </div>

          {/* Advanced Options */}
          <div>
            <label className="flex items-center space-x-2">
              <input
                type="checkbox"
                name="use_playwright"
                checked={formData.use_playwright}
                onChange={handleChange}
                className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                disabled={loading}
              />
              <span className="text-sm text-gray-700">
                Use advanced scraping (slower, for JavaScript-heavy sites)
              </span>
            </label>
          </div>

          {/* Buttons */}
          <div className="flex gap-3">
            <button
              type="submit"
              disabled={loading || !formData.website}
              className="flex-1 btn btn-primary py-3 flex items-center justify-center gap-2 disabled:opacity-50"
            >
              {loading ? (
                <>
                  <FiLoader className="animate-spin" />
                  Generating Profile...
                </>
              ) : (
                <>
                  <FiGlobe />
                  Generate Brand Profile
                </>
              )}
            </button>
            <button
              type="button"
              onClick={onCancel}
              disabled={loading}
              className="btn bg-gray-200 hover:bg-gray-300 text-gray-700 px-6"
            >
              Cancel
            </button>
          </div>
        </form>
      )}

      {/* Loading State */}
      {loading && (
        <div className="card bg-blue-50 border-blue-200">
          <div className="flex items-start gap-3">
            <FiLoader className="animate-spin text-blue-600 mt-1" size={20} />
            <div>
              <h3 className="font-medium text-blue-900">Researching your brand...</h3>
              <p className="text-sm text-blue-700 mt-1">
                This may take 20-60 seconds. We're scraping your website and social media, then analyzing with AI.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Error State */}
      {error && !loading && (
        <div className="card bg-red-50 border-red-200">
          <div className="flex items-start gap-3">
            <FiAlertCircle className="text-red-600 mt-1" size={20} />
            <div className="flex-1">
              <h3 className="font-medium text-red-900">Failed to generate profile</h3>
              <p className="text-sm text-red-700 mt-1">{error}</p>
              <button
                onClick={handleReset}
                className="mt-3 text-sm text-red-600 hover:text-red-700 font-medium"
              >
                Try Again
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Success State - Show Generated Profile */}
      {result && !loading && (
        <div className="space-y-6">
          {/* Success Banner */}
          <div className="card bg-green-50 border-green-200">
            <div className="flex items-start gap-3">
              <FiCheckCircle className="text-green-600 mt-1" size={20} />
              <div className="flex-1">
                <h3 className="font-medium text-green-900">Brand profile generated successfully!</h3>
                <p className="text-sm text-green-700 mt-1">
                  Review the information below and click "Use This Profile" to auto-fill your brand form.
                </p>
              </div>
            </div>
          </div>

          {/* Generated Profile */}
          <div className="card">
            <h3 className="text-lg font-bold text-gray-900 mb-4">Generated Brand Profile</h3>

            <div className="space-y-4">
              {/* Brand Name */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Brand Name</label>
                <p className="text-gray-900 font-medium">{result.data.brand_name}</p>
              </div>

              {/* Overview */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Overview</label>
                <p className="text-gray-900">{result.data.overview}</p>
              </div>

              {/* Products/Services */}
              {result.data.products_services?.length > 0 && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Products & Services</label>
                  <div className="flex flex-wrap gap-2">
                    {result.data.products_services.map((item, idx) => (
                      <span key={idx} className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm">
                        {item}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Mission */}
              {result.data.mission && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Mission</label>
                  <p className="text-gray-900">{result.data.mission}</p>
                </div>
              )}

              {/* Tone of Voice */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Tone of Voice</label>
                <p className="text-gray-900">{result.data.tone_voice}</p>
              </div>

              {/* Target Audience */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Target Audience</label>
                <p className="text-gray-900">{result.data.target_audience}</p>
              </div>

              {/* Brand Values */}
              {result.data.brand_values?.length > 0 && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Brand Values</label>
                  <div className="flex flex-wrap gap-2">
                    {result.data.brand_values.map((value, idx) => (
                      <span key={idx} className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm">
                        {value}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Frequently Used Hashtags */}
              {result.data.frequently_used_hashtags?.length > 0 && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Frequently Used Hashtags</label>
                  <div className="flex flex-wrap gap-2">
                    {result.data.frequently_used_hashtags.slice(0, 10).map((tag, idx) => (
                      <span key={idx} className="px-2 py-1 bg-gray-100 text-gray-700 rounded text-sm">
                        #{tag}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Content Strategy */}
              {result.data.recommended_content_strategy && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Recommended Content Strategy</label>
                  <p className="text-gray-900 text-sm">{result.data.recommended_content_strategy}</p>
                </div>
              )}

              {/* Data Quality */}
              {result.metadata && (
                <div className="pt-4 border-t border-gray-200">
                  <label className="block text-sm font-medium text-gray-700 mb-2">Research Quality</label>
                  <div className="flex items-center gap-4 text-sm text-gray-600">
                    <span className="flex items-center gap-1">
                      <FiGlobe size={16} />
                      Website: {result.metadata.website_scraped ? '✓' : '✗'}
                    </span>
                    {result.metadata.social_platforms?.length > 0 && (
                      <span>
                        Social Platforms: {result.metadata.social_platforms.join(', ')}
                      </span>
                    )}
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      result.metadata.data_quality === 'excellent' ? 'bg-green-100 text-green-700' :
                      result.metadata.data_quality === 'good' ? 'bg-yellow-100 text-yellow-700' :
                      'bg-gray-100 text-gray-700'
                    }`}>
                      {result.metadata.data_quality}
                    </span>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex gap-3">
            <button
              onClick={handleUseProfile}
              className="flex-1 btn btn-primary py-3"
            >
              Use This Profile
            </button>
            <button
              onClick={handleReset}
              className="btn bg-gray-200 hover:bg-gray-300 text-gray-700 px-6"
            >
              Generate New Profile
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
