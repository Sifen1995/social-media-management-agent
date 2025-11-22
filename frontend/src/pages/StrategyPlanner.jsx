import { useState, useEffect } from 'react'
import { strategyAPI, brandAPI } from '../services/api'
import toast from 'react-hot-toast'
import { FiTrendingUp, FiClock, FiHash, FiTarget, FiRefreshCw } from 'react-icons/fi'

const PLATFORMS = [
  { id: 'instagram', name: 'Instagram', emoji: '📸' },
  { id: 'facebook', name: 'Facebook', emoji: '👍' },
  { id: 'twitter', name: 'Twitter/X', emoji: '🐦' },
  { id: 'linkedin', name: 'LinkedIn', emoji: '💼' },
  { id: 'tiktok', name: 'TikTok', emoji: '🎵' },
  { id: 'youtube', name: 'YouTube', emoji: '📺' },
]

export default function StrategyPlanner() {
  const [brands, setBrands] = useState([])
  const [selectedBrand, setSelectedBrand] = useState(null)
  const [selectedPlatforms, setSelectedPlatforms] = useState(['instagram', 'facebook'])
  const [loading, setLoading] = useState(false)
  const [strategyData, setStrategyData] = useState(null)

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

  const togglePlatform = (platformId) => {
    setSelectedPlatforms((prev) =>
      prev.includes(platformId)
        ? prev.filter((id) => id !== platformId)
        : [...prev, platformId]
    )
  }

  const handleGenerateStrategy = async () => {
    if (!selectedBrand) {
      toast.error('Please select a brand')
      return
    }

    if (selectedPlatforms.length === 0) {
      toast.error('Please select at least one platform')
      return
    }

    setLoading(true)
    setStrategyData(null)

    try {
      const response = await strategyAPI.generateStrategy({
        brand_profile: {
          brand_name: selectedBrand.name,
          overview: selectedBrand.overview || '',
          mission: selectedBrand.mission || '',
          tone_voice: selectedBrand.tone_voice || '',
          target_audience: selectedBrand.target_audience || '',
          niche: selectedBrand.niche || '',
          products_services: selectedBrand.products_services || [],
          brand_values: selectedBrand.brand_values || [],
        },
        platforms: selectedPlatforms,
        mode: 'comprehensive',
      })

      if (response.data.success) {
        setStrategyData(response.data.data)
        toast.success('Strategy generated successfully!')
      } else {
        toast.error(response.data.message || 'Failed to generate strategy')
      }
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to generate strategy')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Platform Strategy Planner</h1>
        <p className="mt-2 text-gray-600">
          Get platform-specific posting schedules, content formats, and best practices
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Settings Panel */}
        <div className="lg:col-span-1">
          <div className="card sticky top-6">
            <h2 className="text-xl font-bold text-gray-900 mb-6">Settings</h2>

            {/* Brand Selection */}
            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Select Brand
              </label>
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
            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-3">
                Target Platforms
              </label>
              <div className="space-y-2">
                {PLATFORMS.map((platform) => (
                  <label
                    key={platform.id}
                    className="flex items-center p-3 border-2 rounded-lg cursor-pointer transition-all hover:bg-gray-50"
                    style={{
                      borderColor: selectedPlatforms.includes(platform.id)
                        ? '#4F46E5'
                        : '#E5E7EB',
                      backgroundColor: selectedPlatforms.includes(platform.id)
                        ? '#EEF2FF'
                        : 'transparent',
                    }}
                  >
                    <input
                      type="checkbox"
                      checked={selectedPlatforms.includes(platform.id)}
                      onChange={() => togglePlatform(platform.id)}
                      className="mr-3"
                    />
                    <span className="text-xl mr-2">{platform.emoji}</span>
                    <span className="font-medium text-gray-900">{platform.name}</span>
                  </label>
                ))}
              </div>
            </div>

            {/* Generate Button */}
            <button
              onClick={handleGenerateStrategy}
              disabled={loading || !selectedBrand || selectedPlatforms.length === 0}
              className="w-full btn btn-primary py-3 flex items-center justify-center gap-2 disabled:opacity-50"
            >
              {loading ? (
                <>
                  <FiRefreshCw className="animate-spin" />
                  Generating...
                </>
              ) : (
                <>
                  <FiTrendingUp />
                  Generate Strategy
                </>
              )}
            </button>
          </div>
        </div>

        {/* Results Panel */}
        <div className="lg:col-span-2">
          {loading && (
            <div className="card">
              <div className="text-center py-12">
                <FiRefreshCw className="animate-spin mx-auto mb-4 text-primary-600" size={48} />
                <p className="text-gray-600">Analyzing platforms and generating strategies...</p>
              </div>
            </div>
          )}

          {!loading && !strategyData && (
            <div className="card">
              <div className="text-center py-12 text-gray-500">
                <FiTrendingUp className="mx-auto mb-4 text-gray-400" size={48} />
                <p className="text-lg font-medium">No strategy generated yet</p>
                <p className="text-sm mt-2">Select a brand and platforms, then click "Generate Strategy"</p>
              </div>
            </div>
          )}

          {!loading && strategyData && (
            <div className="space-y-6">
              {/* Strategy Overview */}
              {strategyData.strategy_overview && (
                <div className="card">
                  <h2 className="text-xl font-bold text-gray-900 mb-4">Strategy Overview</h2>
                  <div className="space-y-3">
                    {strategyData.strategy_overview.brand_voice_alignment && (
                      <div>
                        <p className="text-sm font-medium text-gray-700">Brand Voice Alignment</p>
                        <p className="text-gray-900">{strategyData.strategy_overview.brand_voice_alignment}</p>
                      </div>
                    )}
                    {strategyData.strategy_overview.target_audience_focus && (
                      <div>
                        <p className="text-sm font-medium text-gray-700">Target Audience Focus</p>
                        <p className="text-gray-900">{strategyData.strategy_overview.target_audience_focus}</p>
                      </div>
                    )}
                    {strategyData.strategy_overview.primary_goals && (
                      <div>
                        <p className="text-sm font-medium text-gray-700 mb-2">Primary Goals</p>
                        <div className="flex flex-wrap gap-2">
                          {strategyData.strategy_overview.primary_goals.map((goal, idx) => (
                            <span key={idx} className="px-3 py-1 bg-primary-100 text-primary-700 rounded-full text-sm">
                              {goal}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Platform-Specific Strategies */}
              {Object.entries(strategyData.platforms || {}).map(([platform, data]) => (
                <div key={platform} className="card">
                  <div className="flex items-center gap-3 mb-6">
                    <span className="text-3xl">
                      {PLATFORMS.find((p) => p.id === platform)?.emoji || '📱'}
                    </span>
                    <h3 className="text-xl font-bold text-gray-900 capitalize">{platform}</h3>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {/* Posting Schedule */}
                    {data.posting_schedule && (
                      <div className="p-4 bg-blue-50 rounded-lg">
                        <div className="flex items-center gap-2 mb-3">
                          <FiClock className="text-blue-600" />
                          <h4 className="font-semibold text-gray-900">Posting Schedule</h4>
                        </div>
                        <div className="space-y-2 text-sm">
                          <div>
                            <span className="font-medium text-gray-700">Frequency: </span>
                            <span className="text-gray-900">{data.posting_schedule.frequency}</span>
                          </div>
                          {data.posting_schedule.best_times && (
                            <div>
                              <span className="font-medium text-gray-700">Best Times: </span>
                              <span className="text-gray-900">{data.posting_schedule.best_times.join(', ')}</span>
                            </div>
                          )}
                          {data.posting_schedule.best_days && (
                            <div>
                              <span className="font-medium text-gray-700">Best Days: </span>
                              <span className="text-gray-900">{data.posting_schedule.best_days.join(', ')}</span>
                            </div>
                          )}
                        </div>
                      </div>
                    )}

                    {/* Hashtag Strategy */}
                    {data.hashtag_strategy && (
                      <div className="p-4 bg-purple-50 rounded-lg">
                        <div className="flex items-center gap-2 mb-3">
                          <FiHash className="text-purple-600" />
                          <h4 className="font-semibold text-gray-900">Hashtag Strategy</h4>
                        </div>
                        <div className="space-y-2 text-sm">
                          <div>
                            <span className="font-medium text-gray-700">Optimal Count: </span>
                            <span className="text-gray-900">{data.hashtag_strategy.optimal_count}</span>
                          </div>
                          {data.hashtag_strategy.hashtag_mix && (
                            <div>
                              <span className="font-medium text-gray-700">Mix: </span>
                              <span className="text-gray-900">{data.hashtag_strategy.hashtag_mix}</span>
                            </div>
                          )}
                          {data.hashtag_strategy.recommended_hashtags && (
                            <div className="mt-2 flex flex-wrap gap-1">
                              {data.hashtag_strategy.recommended_hashtags.slice(0, 8).map((tag, idx) => (
                                <span key={idx} className="text-xs px-2 py-1 bg-purple-200 text-purple-800 rounded">
                                  #{tag}
                                </span>
                              ))}
                            </div>
                          )}
                        </div>
                      </div>
                    )}

                    {/* Content Formats */}
                    {data.content_formats && (
                      <div className="p-4 bg-green-50 rounded-lg">
                        <div className="flex items-center gap-2 mb-3">
                          <FiTarget className="text-green-600" />
                          <h4 className="font-semibold text-gray-900">Content Formats</h4>
                        </div>
                        <div className="space-y-2 text-sm">
                          {data.content_formats.primary_formats && (
                            <div>
                              <span className="font-medium text-gray-700">Primary Formats: </span>
                              <div className="mt-1 flex flex-wrap gap-1">
                                {data.content_formats.primary_formats.map((format, idx) => (
                                  <span key={idx} className="text-xs px-2 py-1 bg-green-200 text-green-800 rounded">
                                    {format}
                                  </span>
                                ))}
                              </div>
                            </div>
                          )}
                          {data.content_formats.content_mix && (
                            <div className="mt-2">
                              <span className="font-medium text-gray-700">Content Mix: </span>
                              <span className="text-gray-900">{data.content_formats.content_mix}</span>
                            </div>
                          )}
                        </div>
                      </div>
                    )}

                    {/* Engagement Tactics */}
                    {data.engagement_tactics && data.engagement_tactics.length > 0 && (
                      <div className="p-4 bg-yellow-50 rounded-lg">
                        <h4 className="font-semibold text-gray-900 mb-3">Engagement Tactics</h4>
                        <ul className="space-y-1 text-sm">
                          {data.engagement_tactics.slice(0, 5).map((tactic, idx) => (
                            <li key={idx} className="flex items-start gap-2">
                              <span className="text-yellow-600 mt-0.5">•</span>
                              <span className="text-gray-900">{tactic}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>

                  {/* Best Practices */}
                  {data.best_practices && data.best_practices.length > 0 && (
                    <div className="mt-4 p-4 bg-gray-50 rounded-lg">
                      <h4 className="font-semibold text-gray-900 mb-3">Best Practices</h4>
                      <ul className="space-y-2 text-sm">
                        {data.best_practices.map((practice, idx) => (
                          <li key={idx} className="flex items-start gap-2">
                            <span className="text-primary-600 mt-0.5">✓</span>
                            <span className="text-gray-900">{practice}</span>
                          </li>
                        ))}
                      </ul>
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
