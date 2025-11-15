import { useState, useEffect } from 'react'
import { contentAPI, brandAPI } from '../services/api'
import toast from 'react-hot-toast'
import { FiSend, FiCopy, FiCheck, FiRefreshCw } from 'react-icons/fi'

const PLATFORMS = [
  { id: 'instagram', name: 'Instagram', emoji: '📸' },
  { id: 'facebook', name: 'Facebook', emoji: '👍' },
  { id: 'twitter', name: 'Twitter/X', emoji: '🐦' },
  { id: 'linkedin', name: 'LinkedIn', emoji: '💼' },
  { id: 'tiktok', name: 'TikTok', emoji: '🎵' },
]

const CONTENT_TYPES = [
  { id: 'post', name: 'Post' },
  { id: 'story', name: 'Story' },
  { id: 'reel', name: 'Reel/Video' },
  { id: 'thread', name: 'Thread' },
]

export default function ContentGenerator() {
  const [brands, setBrands] = useState([])
  const [formData, setFormData] = useState({
    brand_id: '',
    platform: 'instagram',
    topic: '',
    content_type: 'post',
    count: 2,
    additional_instructions: '',
  })
  const [loading, setLoading] = useState(false)
  const [generatedContent, setGeneratedContent] = useState([])
  const [copiedIndex, setCopiedIndex] = useState(null)

  useEffect(() => {
    fetchBrands()
  }, [])

  const fetchBrands = async () => {
    try {
      const response = await brandAPI.getAll()
      setBrands(response.data)
      if (response.data.length > 0) {
        setFormData((prev) => ({ ...prev, brand_id: response.data[0].id }))
      }
    } catch (error) {
      toast.error('Failed to load brands')
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setGeneratedContent([])

    try {
      const response = await contentAPI.generate(formData)

      if (response.data.success) {
        setGeneratedContent(response.data.data || [])
        toast.success(`Generated ${response.data.data?.length || 0} content piece(s)!`)
      } else {
        toast.error(response.data.message || 'Generation failed')
      }
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to generate content')
    } finally {
      setLoading(false)
    }
  }

  const handleCopy = (text, index) => {
    navigator.clipboard.writeText(text)
    setCopiedIndex(index)
    toast.success('Copied to clipboard!')
    setTimeout(() => setCopiedIndex(null), 2000)
  }

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  return (
    <div className="max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Generate Content</h1>
        <p className="mt-2 text-gray-600">
          Let AI create engaging social media content for your brand
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Input Form */}
        <div className="card">
          <h2 className="text-xl font-bold text-gray-900 mb-6">
            Content Settings
          </h2>

          <form onSubmit={handleSubmit} className="space-y-5">
            {/* Brand Selection */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Brand
              </label>
              <select
                name="brand_id"
                value={formData.brand_id}
                onChange={handleChange}
                className="input"
                required
              >
                {brands.length === 0 ? (
                  <option>No brands available</option>
                ) : (
                  brands.map((brand) => (
                    <option key={brand.id} value={brand.id}>
                      {brand.name}
                    </option>
                  ))
                )}
              </select>
            </div>

            {/* Platform Selection */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Platform
              </label>
              <div className="grid grid-cols-3 gap-3">
                {PLATFORMS.map((platform) => (
                  <button
                    key={platform.id}
                    type="button"
                    onClick={() => setFormData({ ...formData, platform: platform.id })}
                    className={`p-3 rounded-lg border-2 transition-all ${
                      formData.platform === platform.id
                        ? 'border-primary-600 bg-primary-50'
                        : 'border-gray-200 hover:border-gray-300'
                    }`}
                  >
                    <div className="text-2xl mb-1">{platform.emoji}</div>
                    <div className="text-xs font-medium">{platform.name}</div>
                  </button>
                ))}
              </div>
            </div>

            {/* Content Type */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Content Type
              </label>
              <select
                name="content_type"
                value={formData.content_type}
                onChange={handleChange}
                className="input"
              >
                {CONTENT_TYPES.map((type) => (
                  <option key={type.id} value={type.id}>
                    {type.name}
                  </option>
                ))}
              </select>
            </div>

            {/* Topic */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Topic / Theme
              </label>
              <textarea
                name="topic"
                value={formData.topic}
                onChange={handleChange}
                className="input min-h-[100px]"
                placeholder="e.g., 'Morning workout motivation' or 'Summer product launch announcement'"
                required
              />
            </div>

            {/* Number of Variations */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Number of Variations
              </label>
              <input
                type="number"
                name="count"
                value={formData.count}
                onChange={handleChange}
                min="1"
                max="5"
                className="input"
              />
            </div>

            {/* Additional Instructions */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Additional Instructions (Optional)
              </label>
              <textarea
                name="additional_instructions"
                value={formData.additional_instructions}
                onChange={handleChange}
                className="input"
                placeholder="Any specific requirements or preferences..."
                rows="3"
              />
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading || brands.length === 0}
              className="w-full btn btn-primary py-3 flex items-center justify-center gap-2 disabled:opacity-50"
            >
              {loading ? (
                <>
                  <FiRefreshCw className="animate-spin" />
                  Generating...
                </>
              ) : (
                <>
                  <FiSend />
                  Generate Content
                </>
              )}
            </button>
          </form>
        </div>

        {/* Generated Content Display */}
        <div className="card">
          <h2 className="text-xl font-bold text-gray-900 mb-6">
            Generated Content
          </h2>

          {loading && (
            <div className="text-center py-12">
              <FiRefreshCw className="animate-spin mx-auto mb-4 text-primary-600" size={32} />
              <p className="text-gray-600">AI is creating your content...</p>
            </div>
          )}

          {!loading && generatedContent.length === 0 && (
            <div className="text-center py-12 text-gray-500">
              <p>Your generated content will appear here</p>
              <p className="text-sm mt-2">Fill out the form and click "Generate Content"</p>
            </div>
          )}

          {!loading && generatedContent.length > 0 && (
            <div className="space-y-6">
              {generatedContent.map((content, index) => (
                <div key={index} className="border border-gray-200 rounded-lg p-4">
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-sm font-medium text-gray-700">
                      Variation {content.variation || index + 1}
                    </span>
                    <button
                      onClick={() => handleCopy(content.caption, index)}
                      className="flex items-center gap-2 text-sm text-primary-600 hover:text-primary-700"
                    >
                      {copiedIndex === index ? (
                        <>
                          <FiCheck size={16} />
                          Copied!
                        </>
                      ) : (
                        <>
                          <FiCopy size={16} />
                          Copy
                        </>
                      )}
                    </button>
                  </div>

                  {/* Caption */}
                  <div className="mb-4">
                    <p className="text-sm font-medium text-gray-700 mb-2">Caption:</p>
                    <div className="bg-gray-50 p-3 rounded text-sm text-gray-900 whitespace-pre-wrap">
                      {content.caption}
                    </div>
                  </div>

                  {/* Hashtags */}
                  {content.hashtags && content.hashtags.length > 0 && (
                    <div className="mb-4">
                      <p className="text-sm font-medium text-gray-700 mb-2">Hashtags:</p>
                      <div className="flex flex-wrap gap-2">
                        {content.hashtags.map((tag, i) => (
                          <span key={i} className="px-2 py-1 bg-blue-100 text-blue-700 rounded text-xs">
                            #{tag}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* CTA */}
                  {content.cta && (
                    <div>
                      <p className="text-sm font-medium text-gray-700 mb-2">Call to Action:</p>
                      <p className="text-sm text-gray-900 bg-green-50 p-2 rounded">
                        {content.cta}
                      </p>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
