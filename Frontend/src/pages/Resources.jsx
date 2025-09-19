import { useState, useMemo } from 'react'
import { motion } from 'framer-motion'
import { 
  FileText, 
  Download, 
  Eye, 
  BookOpen, 
  Video, 
  FileImage,
  Filter,
  Star,
  Calendar,
  User
} from 'lucide-react'
import useAppStore from '../store/useAppStore'
import Card from '../components/Card'
import Button from '../components/Button'
import SearchBar from '../components/SearchBar'

const Resources = () => {
  const { resourceFilters, updateResourceFilters, searchQuery, isDarkMode } = useAppStore()

  // Sample resources data
  const resources = [
    {
      id: 1,
      title: 'Complete Guide to Computer Science Engineering',
      description: 'Comprehensive guide covering all aspects of CSE curriculum, career paths, and industry insights',
      type: 'PDF',
      category: 'Engineering',
      size: '15.2 MB',
      downloads: 12450,
      rating: 4.8,
      author: 'Dr. Sarah Johnson',
      publishedDate: '2024-01-15',
      tags: ['Computer Science', 'Engineering', 'Career Guide'],
      thumbnail: '/api/placeholder/300/200',
      featured: true
    },
    {
      id: 2,
      title: 'Data Science Fundamentals Video Series',
      description: '20-hour comprehensive video course on data science basics, Python programming, and machine learning',
      type: 'Video',
      category: 'Technology',
      size: '2.1 GB',
      downloads: 8930,
      rating: 4.9,
      author: 'Prof. Michael Chen',
      publishedDate: '2024-01-10',
      tags: ['Data Science', 'Python', 'Machine Learning'],
      thumbnail: '/api/placeholder/300/200',
      featured: true
    },
    {
      id: 3,
      title: 'MBA Application Strategy Handbook',
      description: 'Step-by-step guide to MBA applications, essay writing, and interview preparation',
      type: 'PDF',
      category: 'Business',
      size: '8.7 MB',
      downloads: 6720,
      rating: 4.6,
      author: 'Lisa Anderson',
      publishedDate: '2024-01-08',
      tags: ['MBA', 'Applications', 'Business School'],
      thumbnail: '/api/placeholder/300/200',
      featured: false
    },
    {
      id: 4,
      title: 'Medical School Preparation Notes',
      description: 'Detailed study notes for MCAT preparation and medical school entrance exams',
      type: 'PDF',
      category: 'Healthcare',
      size: '22.4 MB',
      downloads: 9840,
      rating: 4.7,
      author: 'Dr. Emily Rodriguez',
      publishedDate: '2024-01-05',
      tags: ['Medicine', 'MCAT', 'Study Notes'],
      thumbnail: '/api/placeholder/300/200',
      featured: false
    },
    {
      id: 5,
      title: 'Digital Marketing Masterclass',
      description: 'Complete video course on modern digital marketing strategies and tools',
      type: 'Video',
      category: 'Marketing',
      size: '1.8 GB',
      downloads: 5620,
      rating: 4.5,
      author: 'Mark Thompson',
      publishedDate: '2024-01-03',
      tags: ['Digital Marketing', 'SEO', 'Social Media'],
      thumbnail: '/api/placeholder/300/200',
      featured: false
    },
    {
      id: 6,
      title: 'Engineering Mathematics Formula Sheet',
      description: 'Quick reference sheet with all essential formulas for engineering mathematics',
      type: 'PDF',
      category: 'Engineering',
      size: '2.1 MB',
      downloads: 15670,
      rating: 4.4,
      author: 'Prof. David Kumar',
      publishedDate: '2023-12-28',
      tags: ['Mathematics', 'Engineering', 'Formulas'],
      thumbnail: '/api/placeholder/300/200',
      featured: false
    },
    {
      id: 7,
      title: 'Career Transition Guide for Professionals',
      description: 'Comprehensive guide for professionals looking to switch careers or industries',
      type: 'PDF',
      category: 'Career',
      size: '12.3 MB',
      downloads: 4890,
      rating: 4.6,
      author: 'Jennifer Walsh',
      publishedDate: '2023-12-25',
      tags: ['Career Change', 'Professional Development'],
      thumbnail: '/api/placeholder/300/200',
      featured: false
    },
    {
      id: 8,
      title: 'Python Programming Bootcamp',
      description: '40-hour intensive Python programming course from basics to advanced concepts',
      type: 'Video',
      category: 'Technology',
      size: '3.2 GB',
      downloads: 11230,
      rating: 4.8,
      author: 'Alex Rivera',
      publishedDate: '2023-12-20',
      tags: ['Python', 'Programming', 'Bootcamp'],
      thumbnail: '/api/placeholder/300/200',
      featured: true
    }
  ]

  const categories = [...new Set(resources.map(resource => resource.category))]
  const types = [...new Set(resources.map(resource => resource.type))]

  const filteredResources = useMemo(() => {
    let filtered = resources

    // Search filter
    if (searchQuery) {
      filtered = filtered.filter(resource =>
        resource.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        resource.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
        resource.category.toLowerCase().includes(searchQuery.toLowerCase()) ||
        resource.tags.some(tag => 
          tag.toLowerCase().includes(searchQuery.toLowerCase())
        )
      )
    }

    // Category filter
    if (resourceFilters.category) {
      filtered = filtered.filter(resource => resource.category === resourceFilters.category)
    }

    // Type filter
    if (resourceFilters.type) {
      filtered = filtered.filter(resource => resource.type === resourceFilters.type)
    }

    // Sort
    switch (resourceFilters.sortBy) {
      case 'newest':
        filtered.sort((a, b) => new Date(b.publishedDate) - new Date(a.publishedDate))
        break
      case 'oldest':
        filtered.sort((a, b) => new Date(a.publishedDate) - new Date(b.publishedDate))
        break
      case 'popular':
        filtered.sort((a, b) => b.downloads - a.downloads)
        break
      case 'rating':
        filtered.sort((a, b) => b.rating - a.rating)
        break
      case 'title':
        filtered.sort((a, b) => a.title.localeCompare(b.title))
        break
      default:
        break
    }

    return filtered
  }, [resources, searchQuery, resourceFilters])

  const handleFilterChange = (key, value) => {
    updateResourceFilters({ [key]: value })
  }

  const clearFilters = () => {
    updateResourceFilters({
      category: '',
      type: '',
      sortBy: 'newest'
    })
  }

  const getTypeIcon = (type) => {
    switch (type) {
      case 'Video':
        return <Video className="w-5 h-5" />
      case 'PDF':
        return <FileText className="w-5 h-5" />
      case 'Image':
        return <FileImage className="w-5 h-5" />
      default:
        return <BookOpen className="w-5 h-5" />
    }
  }

  const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'short', 
      day: 'numeric' 
    })
  }

  const featuredResources = resources.filter(resource => resource.featured)

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
              Learning Resources
            </h1>
            <p className={`text-lg mb-6 ${
              isDarkMode ? 'text-gray-300' : 'text-gray-600'
            }`}>
              Access study materials, guides, and courses to boost your learning
            </p>
            
            <div className="max-w-2xl">
              <SearchBar placeholder="Search resources, topics, or authors..." />
            </div>
          </motion.div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Featured Resources */}
        {featuredResources.length > 0 && (
          <div className="mb-12">
            <h2 className={`text-2xl font-bold mb-6 ${
              isDarkMode ? 'text-white' : 'text-gray-900'
            }`}>
              Featured Resources
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {featuredResources.map((resource, index) => (
                <motion.div
                  key={resource.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3, delay: index * 0.1 }}
                >
                  <Card className="overflow-hidden hover:shadow-xl transition-all duration-300">
                    <div className="h-48 bg-gradient-to-br from-primary/10 to-secondary/10 flex items-center justify-center">
                      {getTypeIcon(resource.type)}
                    </div>
                    <div className="p-6">
                      <div className="flex items-center justify-between mb-2">
                        <span className="bg-primary text-white text-xs px-2 py-1 rounded-full">
                          Featured
                        </span>
                        <div className="flex items-center space-x-1">
                          <Star className="w-4 h-4 text-yellow-500 fill-current" />
                          <span className={`text-sm ${
                            isDarkMode ? 'text-gray-300' : 'text-gray-600'
                          }`}>
                            {resource.rating}
                          </span>
                        </div>
                      </div>
                      <h3 className={`font-semibold mb-2 ${
                        isDarkMode ? 'text-white' : 'text-gray-900'
                      }`}>
                        {resource.title}
                      </h3>
                      <p className={`text-sm mb-4 ${
                        isDarkMode ? 'text-gray-300' : 'text-gray-600'
                      }`}>
                        {resource.description.length > 100 
                          ? `${resource.description.substring(0, 100)}...` 
                          : resource.description}
                      </p>
                      <div className="flex items-center justify-between">
                        <span className={`text-xs ${
                          isDarkMode ? 'text-gray-400' : 'text-gray-500'
                        }`}>
                          {resource.downloads.toLocaleString()} downloads
                        </span>
                        <Button size="sm">
                          <Download className="w-4 h-4 mr-1" />
                          Download
                        </Button>
                      </div>
                    </div>
                  </Card>
                </motion.div>
              ))}
            </div>
          </div>
        )}

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
                {/* Category Filter */}
                <div>
                  <label className={`block text-sm font-medium mb-2 ${
                    isDarkMode ? 'text-gray-300' : 'text-gray-700'
                  }`}>
                    Category
                  </label>
                  <select
                    value={resourceFilters.category}
                    onChange={(e) => handleFilterChange('category', e.target.value)}
                    className={`w-full p-3 rounded-lg border transition-colors duration-200 ${
                      isDarkMode
                        ? 'bg-gray-700 border-gray-600 text-white'
                        : 'bg-white border-gray-300 text-gray-900'
                    } focus:outline-none focus:ring-2 focus:ring-primary`}
                  >
                    <option value="">All Categories</option>
                    {categories.map(category => (
                      <option key={category} value={category}>{category}</option>
                    ))}
                  </select>
                </div>

                {/* Type Filter */}
                <div>
                  <label className={`block text-sm font-medium mb-2 ${
                    isDarkMode ? 'text-gray-300' : 'text-gray-700'
                  }`}>
                    Resource Type
                  </label>
                  <select
                    value={resourceFilters.type}
                    onChange={(e) => handleFilterChange('type', e.target.value)}
                    className={`w-full p-3 rounded-lg border transition-colors duration-200 ${
                      isDarkMode
                        ? 'bg-gray-700 border-gray-600 text-white'
                        : 'bg-white border-gray-300 text-gray-900'
                    } focus:outline-none focus:ring-2 focus:ring-primary`}
                  >
                    <option value="">All Types</option>
                    {types.map(type => (
                      <option key={type} value={type}>{type}</option>
                    ))}
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
                    value={resourceFilters.sortBy}
                    onChange={(e) => handleFilterChange('sortBy', e.target.value)}
                    className={`w-full p-3 rounded-lg border transition-colors duration-200 ${
                      isDarkMode
                        ? 'bg-gray-700 border-gray-600 text-white'
                        : 'bg-white border-gray-300 text-gray-900'
                    } focus:outline-none focus:ring-2 focus:ring-primary`}
                  >
                    <option value="newest">Newest First</option>
                    <option value="oldest">Oldest First</option>
                    <option value="popular">Most Downloaded</option>
                    <option value="rating">Highest Rated</option>
                    <option value="title">Title (A-Z)</option>
                  </select>
                </div>
              </div>
            </Card>
          </div>

          {/* Resources List */}
          <div className="flex-1">
            <div className="flex items-center justify-between mb-6">
              <p className={`text-sm ${
                isDarkMode ? 'text-gray-400' : 'text-gray-600'
              }`}>
                Showing {filteredResources.length} resources
              </p>
            </div>

            <div className="grid grid-cols-1 gap-6">
              {filteredResources.map((resource, index) => (
                <motion.div
                  key={resource.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3, delay: index * 0.1 }}
                >
                  <Card className="p-6 hover:shadow-xl transition-all duration-300">
                    <div className="flex flex-col md:flex-row gap-6">
                      {/* Resource Thumbnail */}
                      <div className="md:w-48 h-32 bg-gradient-to-br from-primary/10 to-secondary/10 rounded-lg flex items-center justify-center flex-shrink-0">
                        <div className={`p-4 rounded-full ${
                          isDarkMode ? 'bg-gray-700' : 'bg-white'
                        } shadow-lg`}>
                          {getTypeIcon(resource.type)}
                        </div>
                      </div>

                      {/* Resource Info */}
                      <div className="flex-1">
                        <div className="flex items-start justify-between mb-3">
                          <div>
                            <h3 className={`text-xl font-bold mb-2 ${
                              isDarkMode ? 'text-white' : 'text-gray-900'
                            }`}>
                              {resource.title}
                            </h3>
                            <div className="flex items-center space-x-4 text-sm mb-2">
                              <span className="bg-primary/10 text-primary px-2 py-1 rounded-full">
                                {resource.category}
                              </span>
                              <span className="bg-secondary/10 text-gray-700 px-2 py-1 rounded-full">
                                {resource.type}
                              </span>
                              <div className="flex items-center space-x-1">
                                <Star className="w-4 h-4 text-yellow-500 fill-current" />
                                <span className={isDarkMode ? 'text-gray-300' : 'text-gray-600'}>
                                  {resource.rating}
                                </span>
                              </div>
                            </div>
                          </div>
                        </div>

                        <p className={`text-sm mb-4 ${
                          isDarkMode ? 'text-gray-300' : 'text-gray-600'
                        }`}>
                          {resource.description}
                        </p>

                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                          <div>
                            <p className={`text-xs ${
                              isDarkMode ? 'text-gray-400' : 'text-gray-500'
                            }`}>
                              Author
                            </p>
                            <p className={`font-medium ${
                              isDarkMode ? 'text-white' : 'text-gray-900'
                            }`}>
                              {resource.author}
                            </p>
                          </div>
                          
                          <div>
                            <p className={`text-xs ${
                              isDarkMode ? 'text-gray-400' : 'text-gray-500'
                            }`}>
                              Size
                            </p>
                            <p className={`font-medium ${
                              isDarkMode ? 'text-white' : 'text-gray-900'
                            }`}>
                              {resource.size}
                            </p>
                          </div>
                          
                          <div>
                            <p className={`text-xs ${
                              isDarkMode ? 'text-gray-400' : 'text-gray-500'
                            }`}>
                              Downloads
                            </p>
                            <p className={`font-medium ${
                              isDarkMode ? 'text-white' : 'text-gray-900'
                            }`}>
                              {resource.downloads.toLocaleString()}
                            </p>
                          </div>
                          
                          <div>
                            <p className={`text-xs ${
                              isDarkMode ? 'text-gray-400' : 'text-gray-500'
                            }`}>
                              Published
                            </p>
                            <p className={`font-medium ${
                              isDarkMode ? 'text-white' : 'text-gray-900'
                            }`}>
                              {formatDate(resource.publishedDate)}
                            </p>
                          </div>
                        </div>

                        <div className="mb-4">
                          <div className="flex flex-wrap gap-2">
                            {resource.tags.map((tag, idx) => (
                              <span
                                key={idx}
                                className="bg-accent/20 text-gray-800 text-xs px-2 py-1 rounded-full"
                              >
                                {tag}
                              </span>
                            ))}
                          </div>
                        </div>

                        <div className="flex space-x-3">
                          <Button>
                            <Download className="w-4 h-4 mr-2" />
                            Download
                          </Button>
                          <Button variant="outline">
                            <Eye className="w-4 h-4 mr-2" />
                            Preview
                          </Button>
                        </div>
                      </div>
                    </div>
                  </Card>
                </motion.div>
              ))}
            </div>

            {filteredResources.length === 0 && (
              <Card className="p-12 text-center">
                <BookOpen className={`w-16 h-16 mx-auto mb-4 ${
                  isDarkMode ? 'text-gray-600' : 'text-gray-400'
                }`} />
                <h3 className={`text-xl font-semibold mb-2 ${
                  isDarkMode ? 'text-white' : 'text-gray-900'
                }`}>
                  No resources found
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

export default Resources
