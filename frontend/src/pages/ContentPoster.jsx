import { useState } from 'react'
import { posterAPI } from '../services/api'
import toast from 'react-hot-toast'
import { FiSend, FiCheckCircle, FiAlertCircle, FiRefreshCw, FiInfo } from 'react-icons/fi'

const PLATFORMS = [
  { id: 'instagram', name: 'Instagram', emoji: '📸', limit: 2200 },
  { id: 'facebook', name: 'Facebook', emoji: '👍', limit: 63206 },
  { id: 'twitter', name: 'Twitter/X', emoji: '🐦', limit: 280 },
  { id: 'linkedin', name: 'LinkedIn', emoji: '💼', limit: 3000 },
  { id: 'tiktok', name: 'TikTok', emoji: '🎵', limit: 2200 },
  { id: 'youtube', name: 'YouTube', emoji: '📺', limit: 5000 },
]

const MEDIA_TYPES = [
  { id: 'IMAGE', name: 'Image' },
  { id: 'VIDEO', name: 'Video' },
  { id: 'CAROUSEL', name: 'Carousel' },
]

export default function ContentPoster() {
  const [formData, setFormData] = useState({
    caption: '',
    media_type: 'IMAGE',
    media_url: '',
  })
  const [selectedPlatforms, setSelectedPlatforms] = useState(['instagram', 'facebook'])
  const [loading, setLoading] = useState(false)
  const [validationResults, setValidationResults] = useState(null)
  const [postingMode, setPostingMode] = useState('validate') // 'validate' or 'post'

  const togglePlatform = (platformId) => {
    setSelectedPlatforms((prev) =>
      prev.includes(platformId)
        ? prev.filter((id) => id !== platformId)
        : [...prev, platformId]
    )
  }

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const handleValidate = async () => {
    if (!formData.caption.trim()) {
      toast.error('Please enter a caption')
      return
    }

    if (selectedPlatforms.length === 0) {
      toast.error('Please select at least one platform')
      return
    }

    setLoading(true)
    setValidationResults(null)

    try {
      const response = await posterAPI.validateContent({
        content: {
          caption: formData.caption,
          media_type: formData.media_type,
          media_url: formData.media_url || undefined,
        },
        platforms: selectedPlatforms,
        mode: 'validate',
      })

      if (response.data.success) {
        setValidationResults(response.data.data)
        toast.success('Validation complete!')
      } else {
        toast.error(response.data.message || 'Validation failed')
      }
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to validate content')
    } finally {
      setLoading(false)
    }
  }

  const handlePost = async () => {
    if (!formData.caption.trim()) {
      toast.error('Please enter a caption')
      return
    }

    if (selectedPlatforms.length === 0) {
      toast.error('Please select at least one platform')
      return
    }

    const confirmed = window.confirm(
      `Are you sure you want to post to ${selectedPlatforms.length} platform(s)?\n\n` +
        `Platforms: ${selectedPlatforms.join(', ')}`
    )

    if (!confirmed) return

    setLoading(true)

    try {
      const response = await posterAPI.postContent({
        content: {
          caption: formData.caption,
          media_type: formData.media_type,
          media_url: formData.media_url || undefined,
        },
        platforms: selectedPlatforms,
        mode: 'post',
      })

      if (response.data.success) {
        toast.success('Content posted successfully!')
        setFormData({ caption: '', media_type: 'IMAGE', media_url: '' })
        setValidationResults(null)
      } else {
        toast.error(response.data.message || 'Posting failed')
      }
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to post content')
    } finally {
      setLoading(false)
    }
  }

  const getStatusIcon = (valid, errors) => {
    if (valid) return <FiCheckCircle className="text-green-500" size={20} />
    if (errors && errors.length > 0) return <FiAlertCircle className="text-red-500" size={20} />
    return <FiInfo className="text-yellow-500" size={20} />
  }

  return (
    <div className="max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Content Poster & Validator</h1>
        <p className="mt-2 text-gray-600">
          Validate and post content across multiple platforms with confidence
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Input Form */}
        <div className="card">
          <h2 className="text-xl font-bold text-gray-900 mb-6">Content Details</h2>

          <div className="space-y-5">
            {/* Caption */}
            <div>
              <div className="flex items-center justify-between mb-2">
                <label className="block text-sm font-medium text-gray-700">Caption</label>
                <span className="text-xs text-gray-500">{formData.caption.length} characters</span>
              </div>
              <textarea
                name="caption"
                value={formData.caption}
                onChange={handleChange}
                className="input min-h-[150px]"
                placeholder="Enter your post caption here..."
                required
              />
            </div>

            {/* Media Type */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Media Type</label>
              <div className="grid grid-cols-3 gap-3">
                {MEDIA_TYPES.map((type) => (
                  <button
                    key={type.id}
                    type="button"
                    onClick={() => setFormData({ ...formData, media_type: type.id })}
                    className={`p-3 rounded-lg border-2 transition-all ${
                      formData.media_type === type.id
                        ? 'border-primary-600 bg-primary-50'
                        : 'border-gray-200 hover:border-gray-300'
                    }`}
                  >
                    <div className="text-sm font-medium">{type.name}</div>
                  </button>
                ))}
              </div>
            </div>

            {/* Media URL */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Media URL (Optional)
              </label>
              <input
                type="url"
                name="media_url"
                value={formData.media_url}
                onChange={handleChange}
                className="input"
                placeholder="https://example.com/image.jpg"
              />
            </div>

            {/* Platform Selection */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">
                Target Platforms
              </label>
              <div className="space-y-2">
                {PLATFORMS.map((platform) => (
                  <label
                    key={platform.id}
                    className="flex items-center justify-between p-3 border-2 rounded-lg cursor-pointer transition-all hover:bg-gray-50"
                    style={{
                      borderColor: selectedPlatforms.includes(platform.id)
                        ? '#4F46E5'
                        : '#E5E7EB',
                      backgroundColor: selectedPlatforms.includes(platform.id)
                        ? '#EEF2FF'
                        : 'transparent',
                    }}
                  >
                    <div className="flex items-center gap-3">
                      <input
                        type="checkbox"
                        checked={selectedPlatforms.includes(platform.id)}
                        onChange={() => togglePlatform(platform.id)}
                      />
                      <span className="text-xl">{platform.emoji}</span>
                      <span className="font-medium text-gray-900">{platform.name}</span>
                    </div>
                    <span className="text-xs text-gray-500">{platform.limit} chars max</span>
                  </label>
                ))}
              </div>
            </div>

            {/* Action Buttons */}
            <div className="grid grid-cols-2 gap-3 pt-4">
              <button
                onClick={handleValidate}
                disabled={loading || selectedPlatforms.length === 0 || !formData.caption.trim()}
                className="btn btn-secondary py-3 flex items-center justify-center gap-2 disabled:opacity-50"
              >
                {loading && postingMode === 'validate' ? (
                  <>
                    <FiRefreshCw className="animate-spin" />
                    Validating...
                  </>
                ) : (
                  <>
                    <FiCheckCircle />
                    Validate
                  </>
                )}
              </button>

              <button
                onClick={handlePost}
                disabled={loading || selectedPlatforms.length === 0 || !formData.caption.trim()}
                className="btn btn-primary py-3 flex items-center justify-center gap-2 disabled:opacity-50"
              >
                {loading && postingMode === 'post' ? (
                  <>
                    <FiRefreshCw className="animate-spin" />
                    Posting...
                  </>
                ) : (
                  <>
                    <FiSend />
                    Post Now
                  </>
                )}
              </button>
            </div>
          </div>
        </div>

        {/* Validation Results */}
        <div className="card">
          <h2 className="text-xl font-bold text-gray-900 mb-6">Validation Results</h2>

          {loading && (
            <div className="text-center py-12">
              <FiRefreshCw className="animate-spin mx-auto mb-4 text-primary-600" size={32} />
              <p className="text-gray-600">Validating content for all platforms...</p>
            </div>
          )}

          {!loading && !validationResults && (
            <div className="text-center py-12 text-gray-500">
              <FiCheckCircle className="mx-auto mb-4 text-gray-400" size={48} />
              <p>Validation results will appear here</p>
              <p className="text-sm mt-2">Click "Validate" to check your content</p>
            </div>
          )}

          {!loading && validationResults && (
            <div className="space-y-4">
              {/* Overall Status */}
              <div
                className={`p-4 rounded-lg border-2 ${
                  validationResults.all_valid
                    ? 'bg-green-50 border-green-200'
                    : 'bg-yellow-50 border-yellow-200'
                }`}
              >
                <div className="flex items-center gap-3">
                  {validationResults.all_valid ? (
                    <FiCheckCircle className="text-green-600" size={24} />
                  ) : (
                    <FiAlertCircle className="text-yellow-600" size={24} />
                  )}
                  <div>
                    <p className="font-semibold text-gray-900">
                      {validationResults.all_valid
                        ? 'All Platforms Valid'
                        : 'Some Adjustments Needed'}
                    </p>
                    <p className="text-sm text-gray-600">
                      {Object.keys(validationResults.validation_results || {}).length} platform(s) checked
                    </p>
                  </div>
                </div>
              </div>

              {/* Per-Platform Results */}
              {Object.entries(validationResults.validation_results || {}).map(([platform, result]) => {
                const platformData = PLATFORMS.find((p) => p.id === platform)
                return (
                  <div
                    key={platform}
                    className={`p-4 rounded-lg border-2 ${
                      result.valid
                        ? 'bg-white border-green-200'
                        : 'bg-red-50 border-red-200'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center gap-3">
                        {getStatusIcon(result.valid, result.errors)}
                        <div>
                          <p className="font-semibold text-gray-900 flex items-center gap-2">
                            <span>{platformData?.emoji}</span>
                            <span className="capitalize">{platform}</span>
                          </p>
                        </div>
                      </div>
                      <span
                        className={`text-xs px-2 py-1 rounded ${
                          result.valid
                            ? 'bg-green-100 text-green-700'
                            : 'bg-red-100 text-red-700'
                        }`}
                      >
                        {result.valid ? 'VALID' : 'INVALID'}
                      </span>
                    </div>

                    {/* Errors */}
                    {result.errors && result.errors.length > 0 && (
                      <div className="mb-3">
                        <p className="text-sm font-medium text-red-700 mb-1">Errors:</p>
                        <ul className="space-y-1">
                          {result.errors.map((error, idx) => (
                            <li key={idx} className="text-sm text-red-600 flex items-start gap-2">
                              <span className="mt-0.5">•</span>
                              <span>{error}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {/* Warnings */}
                    {result.warnings && result.warnings.length > 0 && (
                      <div className="mb-3">
                        <p className="text-sm font-medium text-yellow-700 mb-1">Warnings:</p>
                        <ul className="space-y-1">
                          {result.warnings.map((warning, idx) => (
                            <li key={idx} className="text-sm text-yellow-600 flex items-start gap-2">
                              <span className="mt-0.5">⚠</span>
                              <span>{warning}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {/* Suggestions */}
                    {result.suggestions && result.suggestions.length > 0 && (
                      <div className="mb-3">
                        <p className="text-sm font-medium text-blue-700 mb-1">Suggestions:</p>
                        <ul className="space-y-1">
                          {result.suggestions.slice(0, 3).map((suggestion, idx) => (
                            <li key={idx} className="text-sm text-blue-600 flex items-start gap-2">
                              <span className="mt-0.5">💡</span>
                              <span>{suggestion}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {/* Platform Requirements */}
                    {result.platform_requirements && (
                      <div className="text-xs text-gray-500 pt-2 border-t border-gray-200">
                        <span className="font-medium">Requirements: </span>
                        {result.platform_requirements}
                      </div>
                    )}
                  </div>
                )
              })}

              {/* Quick Stats */}
              <div className="grid grid-cols-3 gap-3 pt-4 border-t border-gray-200">
                <div className="text-center">
                  <p className="text-2xl font-bold text-green-600">
                    {Object.values(validationResults.validation_results || {}).filter((r) => r.valid).length}
                  </p>
                  <p className="text-xs text-gray-600">Valid</p>
                </div>
                <div className="text-center">
                  <p className="text-2xl font-bold text-red-600">
                    {Object.values(validationResults.validation_results || {}).filter((r) => !r.valid).length}
                  </p>
                  <p className="text-xs text-gray-600">Invalid</p>
                </div>
                <div className="text-center">
                  <p className="text-2xl font-bold text-gray-600">
                    {Object.keys(validationResults.validation_results || {}).length}
                  </p>
                  <p className="text-xs text-gray-600">Total</p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
