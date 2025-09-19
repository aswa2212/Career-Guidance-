import { useState, useMemo } from 'react'
import { motion } from 'framer-motion'
import { 
  MapPin, 
  Star, 
  Users, 
  Calendar, 
  Filter, 
  SortAsc, 
  ExternalLink,
  GraduationCap,
  DollarSign,
  Clock
} from 'lucide-react'
import useAppStore from '../store/useAppStore'
import Card from '../components/Card'
import Button from '../components/Button'
import SearchBar from '../components/SearchBar'

const CollegeList = () => {
  const { collegeFilters, updateCollegeFilters, searchQuery, isDarkMode } = useAppStore()
  const [showFilters, setShowFilters] = useState(false)

  // Sample college data
  const colleges = [
    {
      id: 1,
      name: 'MIT Institute of Technology',
      location: 'Cambridge, MA',
      ranking: 1,
      acceptanceRate: 7,
      tuitionFee: 53790,
      studentCount: 11520,
      establishedYear: 1861,
      courses: ['Computer Science', 'Engineering', 'Physics', 'Mathematics'],
      applicationDeadline: '2024-01-01',
      rating: 4.8,
      type: 'Private',
      category: 'Engineering'
    },
    {
      id: 2,
      name: 'Stanford University',
      location: 'Stanford, CA',
      ranking: 2,
      acceptanceRate: 4,
      tuitionFee: 56169,
      studentCount: 17249,
      establishedYear: 1885,
      courses: ['Computer Science', 'Business', 'Medicine', 'Law'],
      applicationDeadline: '2024-01-02',
      rating: 4.9,
      type: 'Private',
      category: 'Engineering'
    },
    {
      id: 3,
      name: 'Harvard University',
      location: 'Cambridge, MA',
      ranking: 3,
      acceptanceRate: 5,
      tuitionFee: 54269,
      studentCount: 23731,
      establishedYear: 1636,
      courses: ['Law', 'Medicine', 'Business', 'Liberal Arts'],
      applicationDeadline: '2024-01-01',
      rating: 4.7,
      type: 'Private',
      category: 'Liberal Arts'
    },
    {
      id: 4,
      name: 'UC Berkeley',
      location: 'Berkeley, CA',
      ranking: 4,
      acceptanceRate: 17,
      tuitionFee: 14312,
      studentCount: 45057,
      establishedYear: 1868,
      courses: ['Engineering', 'Computer Science', 'Business', 'Sciences'],
      applicationDeadline: '2023-11-30',
      rating: 4.6,
      type: 'Public',
      category: 'Engineering'
    },
    {
      id: 5,
      name: 'Carnegie Mellon University',
      location: 'Pittsburgh, PA',
      ranking: 5,
      acceptanceRate: 15,
      tuitionFee: 58924,
      studentCount: 14799,
      establishedYear: 1900,
      courses: ['Computer Science', 'Engineering', 'Arts', 'Business'],
      applicationDeadline: '2024-01-03',
      rating: 4.5,
      type: 'Private',
      category: 'Engineering'
    },
    {
      id: 6,
      name: 'Yale University',
      location: 'New Haven, CT',
      ranking: 6,
      acceptanceRate: 6,
      tuitionFee: 59950,
      studentCount: 13609,
      establishedYear: 1701,
      courses: ['Liberal Arts', 'Law', 'Medicine', 'Drama'],
      applicationDeadline: '2024-01-02',
      rating: 4.8,
      type: 'Private',
      category: 'Liberal Arts'
    }
  ]

  const locations = [...new Set(colleges.map(college => college.location.split(', ')[1]))]
  const categories = [...new Set(colleges.map(college => college.category))]

  const filteredColleges = useMemo(() => {
    let filtered = colleges

    // Search filter
    if (searchQuery) {
      filtered = filtered.filter(college =>
        college.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        college.location.toLowerCase().includes(searchQuery.toLowerCase()) ||
        college.courses.some(course => 
          course.toLowerCase().includes(searchQuery.toLowerCase())
        )
      )
    }

    // Location filter
    if (collegeFilters.location) {
      filtered = filtered.filter(college =>
        college.location.includes(collegeFilters.location)
      )
    }

    // Category filter
    if (collegeFilters.course) {
      filtered = filtered.filter(college =>
        college.courses.some(course =>
          course.toLowerCase().includes(collegeFilters.course.toLowerCase())
        )
      )
    }

    // Ranking filter
    if (collegeFilters.ranking) {
      const rankingNum = parseInt(collegeFilters.ranking)
      filtered = filtered.filter(college => college.ranking <= rankingNum)
    }

    // Sort
    switch (collegeFilters.sortBy) {
      case 'name':
        filtered.sort((a, b) => a.name.localeCompare(b.name))
        break
      case 'ranking':
        filtered.sort((a, b) => a.ranking - b.ranking)
        break
      case 'deadline':
        filtered.sort((a, b) => new Date(a.applicationDeadline) - new Date(b.applicationDeadline))
        break
      case 'tuition':
        filtered.sort((a, b) => a.tuitionFee - b.tuitionFee)
        break
      default:
        break
    }

    return filtered
  }, [colleges, searchQuery, collegeFilters])

  const handleFilterChange = (key, value) => {
    updateCollegeFilters({ [key]: value })
  }

  const clearFilters = () => {
    updateCollegeFilters({
      location: '',
      course: '',
      ranking: '',
      sortBy: 'name'
    })
  }

  const formatDeadline = (deadline) => {
    const date = new Date(deadline)
    const now = new Date()
    const diffTime = date - now
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
    
    if (diffDays < 0) return 'Deadline passed'
    if (diffDays === 0) return 'Today'
    if (diffDays === 1) return 'Tomorrow'
    return `${diffDays} days left`
  }

  return (
    <div className={`min-h-screen ${
      isDarkMode ? 'bg-gray-900' : 'bg-gray-50'
    } transition-colors duration-300`}>
      {/* Header */}
      <div className={`${
        isDarkMode ? 'bg-gray-800' : 'bg-white'
      } border-b transition-colors duration-300`}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <h1 className={`text-3xl font-bold mb-2 ${
              isDarkMode ? 'text-white' : 'text-gray-900'
            }`}>
              College Directory
            </h1>
            <p className={`text-lg mb-6 ${
              isDarkMode ? 'text-gray-300' : 'text-gray-600'
            }`}>
              Discover and compare top colleges worldwide
            </p>
            
            <div className="max-w-2xl">
              <SearchBar placeholder="Search colleges, locations, or courses..." />
            </div>
          </motion.div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex flex-col lg:flex-row gap-8">
          {/* Filters Sidebar */}
          <div className="lg:w-80">
            <Card className="p-6 sticky top-24">
              <div className="flex items-center justify-between mb-6">
                <h3 className={`text-lg font-semibold ${
                  isDarkMode ? 'text-white' : 'text-gray-900'
                }`}>
                  Filters
                </h3>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={clearFilters}
                  className="text-primary"
                >
                  Clear All
                </Button>
              </div>

              <div className="space-y-6">
                {/* Location Filter */}
                <div>
                  <label className={`block text-sm font-medium mb-2 ${
                    isDarkMode ? 'text-gray-300' : 'text-gray-700'
                  }`}>
                    Location
                  </label>
                  <select
                    value={collegeFilters.location}
                    onChange={(e) => handleFilterChange('location', e.target.value)}
                    className={`w-full p-3 rounded-lg border transition-colors duration-200 ${
                      isDarkMode
                        ? 'bg-gray-700 border-gray-600 text-white'
                        : 'bg-white border-gray-300 text-gray-900'
                    } focus:outline-none focus:ring-2 focus:ring-primary`}
                  >
                    <option value="">All Locations</option>
                    {locations.map(location => (
                      <option key={location} value={location}>{location}</option>
                    ))}
                  </select>
                </div>

                {/* Course Filter */}
                <div>
                  <label className={`block text-sm font-medium mb-2 ${
                    isDarkMode ? 'text-gray-300' : 'text-gray-700'
                  }`}>
                    Course/Field
                  </label>
                  <input
                    type="text"
                    value={collegeFilters.course}
                    onChange={(e) => handleFilterChange('course', e.target.value)}
                    placeholder="e.g., Computer Science"
                    className={`w-full p-3 rounded-lg border transition-colors duration-200 ${
                      isDarkMode
                        ? 'bg-gray-700 border-gray-600 text-white placeholder-gray-400'
                        : 'bg-white border-gray-300 text-gray-900 placeholder-gray-500'
                    } focus:outline-none focus:ring-2 focus:ring-primary`}
                  />
                </div>

                {/* Ranking Filter */}
                <div>
                  <label className={`block text-sm font-medium mb-2 ${
                    isDarkMode ? 'text-gray-300' : 'text-gray-700'
                  }`}>
                    Top Ranked (Up to)
                  </label>
                  <select
                    value={collegeFilters.ranking}
                    onChange={(e) => handleFilterChange('ranking', e.target.value)}
                    className={`w-full p-3 rounded-lg border transition-colors duration-200 ${
                      isDarkMode
                        ? 'bg-gray-700 border-gray-600 text-white'
                        : 'bg-white border-gray-300 text-gray-900'
                    } focus:outline-none focus:ring-2 focus:ring-primary`}
                  >
                    <option value="">All Rankings</option>
                    <option value="10">Top 10</option>
                    <option value="25">Top 25</option>
                    <option value="50">Top 50</option>
                    <option value="100">Top 100</option>
                  </select>
                </div>

                {/* Sort By */}
                <div>
                  <label className={`block text-sm font-medium mb-2 ${
                    isDarkMode ? 'text-gray-300' : 'text-gray-700'
                  }`}>
                    Sort By
                  </label>
                  <select
                    value={collegeFilters.sortBy}
                    onChange={(e) => handleFilterChange('sortBy', e.target.value)}
                    className={`w-full p-3 rounded-lg border transition-colors duration-200 ${
                      isDarkMode
                        ? 'bg-gray-700 border-gray-600 text-white'
                        : 'bg-white border-gray-300 text-gray-900'
                    } focus:outline-none focus:ring-2 focus:ring-primary`}
                  >
                    <option value="name">Name (A-Z)</option>
                    <option value="ranking">Ranking</option>
                    <option value="deadline">Application Deadline</option>
                    <option value="tuition">Tuition Fee</option>
                  </select>
                </div>
              </div>
            </Card>
          </div>

          {/* College List */}
          <div className="flex-1">
            <div className="flex items-center justify-between mb-6">
              <p className={`text-sm ${
                isDarkMode ? 'text-gray-400' : 'text-gray-600'
              }`}>
                Showing {filteredColleges.length} colleges
              </p>
              
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setShowFilters(!showFilters)}
                className="lg:hidden"
              >
                <Filter className="w-4 h-4 mr-2" />
                Filters
              </Button>
            </div>

            <div className="grid grid-cols-1 gap-6">
              {filteredColleges.map((college, index) => (
                <motion.div
                  key={college.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3, delay: index * 0.1 }}
                >
                  <Card className="p-6 hover:shadow-xl transition-all duration-300">
                    <div className="flex flex-col lg:flex-row lg:items-center justify-between">
                      <div className="flex-1">
                        <div className="flex items-start justify-between mb-4">
                          <div>
                            <div className="flex items-center space-x-3 mb-2">
                              <h3 className={`text-xl font-bold ${
                                isDarkMode ? 'text-white' : 'text-gray-900'
                              }`}>
                                {college.name}
                              </h3>
                              <span className="bg-primary text-white text-xs px-2 py-1 rounded-full">
                                #{college.ranking}
                              </span>
                            </div>
                            
                            <div className="flex items-center space-x-4 text-sm mb-3">
                              <div className="flex items-center space-x-1">
                                <MapPin className={`w-4 h-4 ${
                                  isDarkMode ? 'text-gray-400' : 'text-gray-500'
                                }`} />
                                <span className={isDarkMode ? 'text-gray-300' : 'text-gray-600'}>
                                  {college.location}
                                </span>
                              </div>
                              
                              <div className="flex items-center space-x-1">
                                <Star className="w-4 h-4 text-yellow-500 fill-current" />
                                <span className={isDarkMode ? 'text-gray-300' : 'text-gray-600'}>
                                  {college.rating}
                                </span>
                              </div>
                              
                              <div className="flex items-center space-x-1">
                                <Users className={`w-4 h-4 ${
                                  isDarkMode ? 'text-gray-400' : 'text-gray-500'
                                }`} />
                                <span className={isDarkMode ? 'text-gray-300' : 'text-gray-600'}>
                                  {college.studentCount.toLocaleString()} students
                                </span>
                              </div>
                            </div>
                          </div>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                          <div className="flex items-center space-x-2">
                            <DollarSign className={`w-4 h-4 ${
                              isDarkMode ? 'text-gray-400' : 'text-gray-500'
                            }`} />
                            <div>
                              <p className={`text-xs ${
                                isDarkMode ? 'text-gray-400' : 'text-gray-500'
                              }`}>
                                Annual Tuition
                              </p>
                              <p className={`font-semibold ${
                                isDarkMode ? 'text-white' : 'text-gray-900'
                              }`}>
                                ${college.tuitionFee.toLocaleString()}
                              </p>
                            </div>
                          </div>
                          
                          <div className="flex items-center space-x-2">
                            <GraduationCap className={`w-4 h-4 ${
                              isDarkMode ? 'text-gray-400' : 'text-gray-500'
                            }`} />
                            <div>
                              <p className={`text-xs ${
                                isDarkMode ? 'text-gray-400' : 'text-gray-500'
                              }`}>
                                Acceptance Rate
                              </p>
                              <p className={`font-semibold ${
                                isDarkMode ? 'text-white' : 'text-gray-900'
                              }`}>
                                {college.acceptanceRate}%
                              </p>
                            </div>
                          </div>
                          
                          <div className="flex items-center space-x-2">
                            <Clock className={`w-4 h-4 ${
                              isDarkMode ? 'text-gray-400' : 'text-gray-500'
                            }`} />
                            <div>
                              <p className={`text-xs ${
                                isDarkMode ? 'text-gray-400' : 'text-gray-500'
                              }`}>
                                Application Deadline
                              </p>
                              <p className={`font-semibold ${
                                formatDeadline(college.applicationDeadline).includes('passed') 
                                  ? 'text-red-500' 
                                  : formatDeadline(college.applicationDeadline).includes('days left') && 
                                    parseInt(formatDeadline(college.applicationDeadline)) <= 7
                                    ? 'text-yellow-500'
                                    : 'text-green-500'
                              }`}>
                                {formatDeadline(college.applicationDeadline)}
                              </p>
                            </div>
                          </div>
                        </div>

                        <div className="mb-4">
                          <p className={`text-sm font-medium mb-2 ${
                            isDarkMode ? 'text-gray-300' : 'text-gray-700'
                          }`}>
                            Popular Courses:
                          </p>
                          <div className="flex flex-wrap gap-2">
                            {college.courses.slice(0, 4).map((course, idx) => (
                              <span
                                key={idx}
                                className="bg-secondary/20 text-primary text-xs px-2 py-1 rounded-full"
                              >
                                {course}
                              </span>
                            ))}
                            {college.courses.length > 4 && (
                              <span className={`text-xs ${
                                isDarkMode ? 'text-gray-400' : 'text-gray-500'
                              }`}>
                                +{college.courses.length - 4} more
                              </span>
                            )}
                          </div>
                        </div>
                      </div>

                      <div className="flex flex-col space-y-3 lg:ml-6 mt-4 lg:mt-0">
                        <Button className="w-full lg:w-auto">
                          Apply Now
                        </Button>
                        <Button variant="outline" className="w-full lg:w-auto">
                          <ExternalLink className="w-4 h-4 mr-2" />
                          View Details
                        </Button>
                      </div>
                    </div>
                  </Card>
                </motion.div>
              ))}
            </div>

            {filteredColleges.length === 0 && (
              <Card className="p-12 text-center">
                <GraduationCap className={`w-16 h-16 mx-auto mb-4 ${
                  isDarkMode ? 'text-gray-600' : 'text-gray-400'
                }`} />
                <h3 className={`text-xl font-semibold mb-2 ${
                  isDarkMode ? 'text-white' : 'text-gray-900'
                }`}>
                  No colleges found
                </h3>
                <p className={`${
                  isDarkMode ? 'text-gray-400' : 'text-gray-600'
                } mb-4`}>
                  Try adjusting your search criteria or filters
                </p>
                <Button onClick={clearFilters} variant="outline">
                  Clear Filters
                </Button>
              </Card>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default CollegeList
