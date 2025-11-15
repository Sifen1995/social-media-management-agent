import { useState, useEffect } from 'react'
import { brandAPI } from '../services/api'
import toast from 'react-hot-toast'
import { FiPlus, FiEdit2, FiTrash2, FiBriefcase } from 'react-icons/fi'

export default function BrandManagement() {
  const [brands, setBrands] = useState([])
  const [loading, setLoading] = useState(true)
  const [showModal, setShowModal] = useState(false)
  const [editingBrand, setEditingBrand] = useState(null)
  const [formData, setFormData] = useState({
    name: '',
    niche: '',
    brand_voice: '',
    target_audience: '',
    goals: '',
  })

  useEffect(() => {
    fetchBrands()
  }, [])

  const fetchBrands = async () => {
    try {
      const response = await brandAPI.getAll()
      setBrands(response.data)
    } catch (error) {
      toast.error('Failed to load brands')
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const data = {
        ...formData,
        goals: formData.goals.split(',').map(g => g.trim()),
      }

      if (editingBrand) {
        await brandAPI.update(editingBrand.id, data)
        toast.success('Brand updated successfully')
      } else {
        await brandAPI.create(data)
        toast.success('Brand created successfully')
      }

      setShowModal(false)
      setEditingBrand(null)
      setFormData({ name: '', niche: '', brand_voice: '', target_audience: '', goals: '' })
      fetchBrands()
    } catch (error) {
      toast.error('Failed to save brand')
    }
  }

  const handleEdit = (brand) => {
    setEditingBrand(brand)
    setFormData({
      name: brand.name,
      niche: brand.niche || '',
      brand_voice: brand.brand_voice || '',
      target_audience: brand.target_audience || '',
      goals: brand.goals?.join(', ') || '',
    })
    setShowModal(true)
  }

  const handleDelete = async (id) => {
    if (!confirm('Are you sure you want to delete this brand?')) return

    try {
      await brandAPI.delete(id)
      toast.success('Brand deleted successfully')
      fetchBrands()
    } catch (error) {
      toast.error('Failed to delete brand')
    }
  }

  return (
    <div className="max-w-6xl mx-auto">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Brand Management</h1>
          <p className="mt-2 text-gray-600">Manage your brand profiles and settings</p>
        </div>
        <button onClick={() => setShowModal(true)} className="btn btn-primary flex items-center gap-2">
          <FiPlus /> Add Brand
        </button>
      </div>

      {loading ? (
        <div className="text-center py-12">Loading...</div>
      ) : brands.length === 0 ? (
        <div className="card text-center py-12">
          <FiBriefcase className="mx-auto mb-4 text-gray-400" size={48} />
          <h3 className="text-xl font-medium text-gray-900 mb-2">No brands yet</h3>
          <p className="text-gray-600 mb-6">Create your first brand to get started</p>
          <button onClick={() => setShowModal(true)} className="btn btn-primary">
            <FiPlus className="inline mr-2" /> Add Your First Brand
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {brands.map((brand) => (
            <div key={brand.id} className="card hover:shadow-md transition-shadow">
              <div className="flex items-start justify-between mb-4">
                <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center">
                  <FiBriefcase className="text-primary-600" size={24} />
                </div>
                <div className="flex gap-2">
                  <button onClick={() => handleEdit(brand)} className="text-blue-600 hover:text-blue-700">
                    <FiEdit2 size={18} />
                  </button>
                  <button onClick={() => handleDelete(brand.id)} className="text-red-600 hover:text-red-700">
                    <FiTrash2 size={18} />
                  </button>
                </div>
              </div>
              <h3 className="text-lg font-bold text-gray-900 mb-2">{brand.name}</h3>
              <p className="text-sm text-gray-600 mb-3">{brand.niche}</p>
              <div className="text-xs space-y-1">
                <p><span className="font-medium">Voice:</span> {brand.brand_voice}</p>
                <p><span className="font-medium">Audience:</span> {brand.target_audience}</p>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl max-w-md w-full p-6">
            <h2 className="text-xl font-bold mb-4">{editingBrand ? 'Edit' : 'Add'} Brand</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">Brand Name</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="input"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Niche</label>
                <input
                  type="text"
                  value={formData.niche}
                  onChange={(e) => setFormData({ ...formData, niche: e.target.value })}
                  className="input"
                  placeholder="e.g., Fitness & Wellness"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Brand Voice</label>
                <input
                  type="text"
                  value={formData.brand_voice}
                  onChange={(e) => setFormData({ ...formData, brand_voice: e.target.value })}
                  className="input"
                  placeholder="e.g., Friendly, professional"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Target Audience</label>
                <input
                  type="text"
                  value={formData.target_audience}
                  onChange={(e) => setFormData({ ...formData, target_audience: e.target.value })}
                  className="input"
                  placeholder="e.g., Young professionals 25-40"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Goals (comma-separated)</label>
                <input
                  type="text"
                  value={formData.goals}
                  onChange={(e) => setFormData({ ...formData, goals: e.target.value })}
                  className="input"
                  placeholder="e.g., Increase engagement, Build community"
                />
              </div>
              <div className="flex gap-3 pt-4">
                <button type="submit" className="btn btn-primary flex-1">Save</button>
                <button
                  type="button"
                  onClick={() => {
                    setShowModal(false)
                    setEditingBrand(null)
                    setFormData({ name: '', niche: '', brand_voice: '', target_audience: '', goals: '' })
                  }}
                  className="btn btn-secondary"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}
