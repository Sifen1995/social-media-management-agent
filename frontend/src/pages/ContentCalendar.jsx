import { useState } from 'react'
import { FiCalendar } from 'react-icons/fi'

export default function ContentCalendar() {
  const [selectedDate, setSelectedDate] = useState(new Date())

  return (
    <div className="max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Content Calendar</h1>
        <p className="mt-2 text-gray-600">Schedule and manage your content publishing</p>
      </div>

      <div className="card">
        <div className="text-center py-12">
          <FiCalendar className="mx-auto mb-4 text-gray-400" size={64} />
          <h3 className="text-xl font-medium text-gray-900 mb-2">Calendar View</h3>
          <p className="text-gray-600">Calendar integration coming soon</p>
        </div>
      </div>
    </div>
  )
}
