import { useState, useEffect } from 'react'
import { graphicsAPI, brandAPI } from '../services/api'
import toast from 'react-hot-toast'
import { FiImage, FiCopy, FiCheck, FiRefreshCw, FiDownload } from 'react-icons/fi'

const PLATFORMS = [
  { id: 'instagram', name: 'Instagram', emoji: '📸', desc: 'Square/Portrait posts' },
  { id: 'facebook', name: 'Facebook', emoji: '👍', desc: 'Landscape posts' },
  { id: 'twitter', name: 'Twitter/X', emoji: '🐦', desc: 'Landscape tweets' },
  { id: 'linkedin', name: 'LinkedIn', emoji: '💼', desc: 'Professional posts' },
  { id: 'tiktok', name: 'TikTok', emoji: '🎵', desc: 'Vertical videos' },
  { id: 'youtube', name: 'YouTube', emoji: '📺', desc: 'Thumbnails' },
]

export default function GraphicsGenerator() {
  const [brands, setBrands] = useState([])
  const [selectedBrand, setSelectedBrand] = useState(null)
  const [formData, setFormData] = useState({
    platform: 'instagram',
    caption: '',
    theme: '',
    requirements: '',
  })
  const [loading, setLoading] = useState(false)
  const [graphicSpec, setGraphicSpec] = useState(null)
  const [copiedPrompt, setCopiedPrompt] = useState(false)

  useEffect(() => {
    fetchBrands()
  }, [])

  const fetchBrands = async () => {
    try {
      const response = await brandAPI.getAll()
      setBrands(response.data)
      if (response.data.length > 0) {
        setSelectedBrand(response.data[0])
      }
    } catch (error) {
      toast.error('Failed to load brands')
    }
  }

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const handleGenerate = async (e) => {
    e.preventDefault()

    if (!selectedBrand) {
      toast.error('Please select a brand')
      return
    }

    setLoading(true)
    setGraphicSpec(null)

    try {
      const response = await graphicsAPI.generateGraphic({
        content: {
          caption: formData.caption,
          content_type: 'post',
          theme: formData.theme,
          requirements: formData.requirements,
        },
        platform: formData.platform,
        mode: 'specification',
        brand_profile: {
          brand_name: selectedBrand.name,
          brand_colors: selectedBrand.brand_colors || [],
          brand_fonts: selectedBrand.brand_fonts || 'Arial, Sans-serif',
          tone_voice: selectedBrand.tone_voice || '',
        },
      })

      if (response.data.success) {
        setGraphicSpec(response.data.data)
        toast.success('Graphic specification generated!')
      } else {
        toast.error(response.data.message || 'Failed to generate specification')
      }
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to generate specification')
    } finally {
      setLoading(false)
    }
  }

  const copyPrompt = (text) => {
    navigator.clipboard.writeText(text)
    setCopiedPrompt(true)
    toast.success('Copied to clipboard!')
    setTimeout(() => setCopiedPrompt(false), 2000)
  }

  return (
    <div className="max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Graphics Generator</h1>
        <p className="mt-2 text-gray-600">
          Create platform-specific graphic specifications and AI image prompts
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Input Form */}
        <div className="card">
          <h2 className="text-xl font-bold text-gray-900 mb-6">Content Details</h2>

          <form onSubmit={handleGenerate} className="space-y-5">
            {/* Brand Selection */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Brand</label>
              <select
                value={selectedBrand?.id || ''}
                onChange={(e) => {
                  const brand = brands.find((b) => b.id === e.target.value)
                  setSelectedBrand(brand)
                }}
                className="input"
                disabled={brands.length === 0}
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
              <label className="block text-sm font-medium text-gray-700 mb-3">Platform</label>
              <div className="grid grid-cols-2 gap-3">
                {PLATFORMS.map((platform) => (
                  <button
                    key={platform.id}
                    type="button"
                    onClick={() => setFormData({ ...formData, platform: platform.id })}
                    className={`p-3 rounded-lg border-2 transition-all text-left ${
                      formData.platform === platform.id
                        ? 'border-primary-600 bg-primary-50'
                        : 'border-gray-200 hover:border-gray-300'
                    }`}
                  >
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-xl">{platform.emoji}</span>
                      <span className="font-medium text-sm">{platform.name}</span>
                    </div>
                    <div className="text-xs text-gray-500">{platform.desc}</div>
                  </button>
                ))}
              </div>
            </div>

            {/* Caption/Content */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Post Caption/Content
              </label>
              <textarea
                name="caption"
                value={formData.caption}
                onChange={handleChange}
                className="input min-h-[100px]"
                placeholder="Enter the text that will accompany the graphic..."
                required
              />
            </div>

            {/* Theme */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Theme/Concept
              </label>
              <input
                type="text"
                name="theme"
                value={formData.theme}
                onChange={handleChange}
                className="input"
                placeholder="e.g., 'product launch', 'motivational quote', 'event announcement'"
                required
              />
            </div>

            {/* Requirements */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Design Requirements (Optional)
              </label>
              <textarea
                name="requirements"
                value={formData.requirements}
                onChange={handleChange}
                className="input"
                placeholder="Any specific design requirements, must-have elements, or style preferences..."
                rows="3"
              />
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading || !selectedBrand}
              className="w-full btn btn-primary py-3 flex items-center justify-center gap-2 disabled:opacity-50"
            >
              {loading ? (
                <>
                  <FiRefreshCw className="animate-spin" />
                  Generating...
                </>
              ) : (
                <>
                  <FiImage />
                  Generate Graphic Spec
                </>
              )}
            </button>
          </form>
        </div>

        {/* Results Panel */}
        <div className="card">
          <h2 className="text-xl font-bold text-gray-900 mb-6">Graphic Specification</h2>

          {loading && (
            <div className="text-center py-12">
              <FiRefreshCw className="animate-spin mx-auto mb-4 text-primary-600" size={32} />
              <p className="text-gray-600">Creating graphic specification...</p>
            </div>
          )}

          {!loading && !graphicSpec && (
            <div className="text-center py-12 text-gray-500">
              <FiImage className="mx-auto mb-4 text-gray-400" size={48} />
              <p>Your graphic specification will appear here</p>
              <p className="text-sm mt-2">Fill out the form and click "Generate"</p>
            </div>
          )}

          {!loading && graphicSpec && (
            <div className="space-y-6">
              {/* Dimensions */}
              {graphicSpec.specification?.dimensions && (
                <div className="p-4 bg-blue-50 rounded-lg">
                  <h3 className="font-semibold text-gray-900 mb-3 flex items-center gap-2">
                    📐 Dimensions
                  </h3>
                  <p className="text-lg font-mono text-gray-900">
                    {graphicSpec.specification.dimensions.width} x{' '}
                    {graphicSpec.specification.dimensions.height}{' '}
                    {graphicSpec.specification.dimensions.unit}
                  </p>
                  <p className="text-sm text-gray-600 mt-1">
                    Aspect Ratio: {graphicSpec.specification.dimensions.aspect_ratio}
                  </p>
                </div>
              )}

              {/* Color Scheme */}
              {graphicSpec.specification?.color_scheme && (
                <div className="p-4 bg-purple-50 rounded-lg">
                  <h3 className="font-semibold text-gray-900 mb-3 flex items-center gap-2">
                    🎨 Color Scheme
                  </h3>
                  <div className="grid grid-cols-2 gap-3">
                    {Object.entries(graphicSpec.specification.color_scheme).map(([key, value]) => (
                      <div key={key} className="flex items-center gap-2">
                        <div
                          className="w-8 h-8 rounded border border-gray-300"
                          style={{ backgroundColor: value }}
                        />
                        <div>
                          <p className="text-xs text-gray-600 capitalize">{key.replace('_', ' ')}</p>
                          <p className="text-xs font-mono text-gray-900">{value}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Typography */}
              {graphicSpec.specification?.typography && (
                <div className="p-4 bg-green-50 rounded-lg">
                  <h3 className="font-semibold text-gray-900 mb-3 flex items-center gap-2">
                    ✏️ Typography
                  </h3>
                  {graphicSpec.specification.typography.headline && (
                    <div className="mb-3">
                      <p className="text-xs text-gray-600 mb-1">Headline</p>
                      <p className="font-semibold text-gray-900">
                        {graphicSpec.specification.typography.headline.text}
                      </p>
                      <p className="text-xs text-gray-600 mt-1">
                        Font: {graphicSpec.specification.typography.headline.font} •
                        Size: {graphicSpec.specification.typography.headline.size}
                      </p>
                    </div>
                  )}
                  {graphicSpec.specification.typography.subheadline && (
                    <div>
                      <p className="text-xs text-gray-600 mb-1">Subheadline</p>
                      <p className="text-sm text-gray-900">
                        {graphicSpec.specification.typography.subheadline.text}
                      </p>
                      <p className="text-xs text-gray-600 mt-1">
                        Font: {graphicSpec.specification.typography.subheadline.font}
                      </p>
                    </div>
                  )}
                </div>
              )}

              {/* Visual Elements */}
              {graphicSpec.specification?.visual_elements && (
                <div className="p-4 bg-yellow-50 rounded-lg">
                  <h3 className="font-semibold text-gray-900 mb-3 flex items-center gap-2">
                    🖼️ Visual Elements
                  </h3>
                  {graphicSpec.specification.visual_elements.images && (
                    <div className="mb-2">
                      <p className="text-xs font-medium text-gray-700 mb-1">Suggested Images:</p>
                      <ul className="text-sm text-gray-900 space-y-1">
                        {graphicSpec.specification.visual_elements.images.map((img, idx) => (
                          <li key={idx}>• {img}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              )}

              {/* Canva Template */}
              {graphicSpec.specification?.canva_template_suggestion && (
                <div className="p-4 bg-indigo-50 rounded-lg">
                  <h3 className="font-semibold text-gray-900 mb-2 flex items-center gap-2">
                    🎯 Canva Template
                  </h3>
                  <p className="text-sm text-gray-900">
                    {graphicSpec.specification.canva_template_suggestion}
                  </p>
                </div>
              )}

              {/* AI Image Generation Prompt */}
              {graphicSpec.image?.prompt && (
                <div className="p-4 bg-gray-50 rounded-lg border-2 border-gray-200">
                  <div className="flex items-center justify-between mb-3">
                    <h3 className="font-semibold text-gray-900 flex items-center gap-2">
                      🤖 AI Image Prompt
                    </h3>
                    <button
                      onClick={() => copyPrompt(graphicSpec.image.prompt)}
                      className="flex items-center gap-2 text-sm text-primary-600 hover:text-primary-700"
                    >
                      {copiedPrompt ? (
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
                  <p className="text-sm text-gray-900 leading-relaxed">{graphicSpec.image.prompt}</p>
                  <p className="text-xs text-gray-500 mt-3">
                    Use this prompt with MidJourney, DALL-E, or Stable Diffusion
                  </p>
                </div>
              )}

              {/* Download Spec */}
              <button
                onClick={() => {
                  const blob = new Blob([JSON.stringify(graphicSpec, null, 2)], {
                    type: 'application/json',
                  })
                  const url = URL.createObjectURL(blob)
                  const a = document.createElement('a')
                  a.href = url
                  a.download = `graphic-spec-${formData.platform}-${Date.now()}.json`
                  a.click()
                  toast.success('Specification downloaded!')
                }}
                className="w-full btn btn-secondary py-2 flex items-center justify-center gap-2"
              >
                <FiDownload />
                Download Full Specification
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
