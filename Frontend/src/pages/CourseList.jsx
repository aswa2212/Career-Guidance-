import { useState, useMemo } from 'react'
import { motion } from 'framer-motion'
import { 
  BookOpen, 
  Clock, 
  DollarSign, 
  TrendingUp, 
  Users, 
  Award,
  Filter,
  Star,
  ArrowRight,
  Building
} from 'lucide-react'
import useAppStore from '../store/useAppStore'
import Card from '../components/Card'
import Button from '../components/Button'
import SearchBar from '../components/SearchBar'
import Chart from '../components/Chart'

const CourseList = () => {
  const { courseFilters, updateCourseFilters, searchQuery, isDarkMode } = useAppStore()
  const [selectedCourse, setSelectedCourse] = useState(null)

  // Sample course data
  const courses = [
    {
      id: 1,
      title: 'Computer Science Engineering',
      description: 'Learn programming, algorithms, data structures, and software development',
      category: 'Engineering',
      duration: '4 Years',
      averageFee: 120000,
      popularity: 95,
      jobProspects: 92,
      averageSalary: 85000,
      colleges: 245,
      rating: 4.8,
      skills: ['Programming', 'Algorithms', 'Data Structures', 'Software Engineering'],
      careerPaths: [
        { role: 'Software Engineer', percentage: 35 },
        { role: 'Data Scientist', percentage: 25 },
        { role: 'Product Manager', percentage: 20 },
        { role: 'DevOps Engineer', percentage: 20 }
      ],
      topColleges: ['MIT', 'Stanford', 'Carnegie Mellon', 'UC Berkeley']
    },
    {
      id: 2,
      title: 'Data Science',
      description: 'Master data analysis, machine learning, and artificial intelligence',
      category: 'Technology',
      duration: '2 Years',
      averageFee: 80000,
      popularity: 88,
      jobProspects: 89,
      averageSalary: 78000,
      colleges: 156,
      rating: 4.7,
      skills: ['Python', 'Machine Learning', 'Statistics', 'Data Visualization'],
      careerPaths: [
        { role: 'Data Scientist', percentage: 40 },
        { role: 'ML Engineer', percentage: 30 },
        { role: 'Data Analyst', percentage: 20 },
        { role: 'Research Scientist', percentage: 10 }
      ],
      topColleges: ['Stanford', 'MIT', 'Harvard', 'UC Berkeley']
    },
    {
      id: 3,
      title: 'Business Administration (MBA)',
      description: 'Develop leadership, management, and strategic business skills',
      category: 'Business',
      duration: '2 Years',
      averageFee: 150000,
      popularity: 82,
      jobProspects: 85,
      averageSalary: 95000,
      colleges: 312,
      rating: 4.6,
      skills: ['Leadership', 'Strategy', 'Finance', 'Marketing'],
      careerPaths: [
        { role: 'Product Manager', percentage: 30 },
        { role: 'Consultant', percentage: 25 },
        { role: 'Investment Banker', percentage: 25 },
        { role: 'Entrepreneur', percentage: 20 }
      ],
      topColleges: ['Harvard', 'Wharton', 'Stanford', 'MIT Sloan']
    },
    {
      id: 4,
      title: 'Mechanical Engineering',
      description: 'Design, develop, and manufacture mechanical systems and devices',
      category: 'Engineering',
      duration: '4 Years',
      averageFee: 100000,
      popularity: 75,
      jobProspects: 78,
      averageSalary: 72000,
      colleges: 189,
      rating: 4.4,
      skills: ['CAD Design', 'Thermodynamics', 'Materials Science', 'Manufacturing'],
      careerPaths: [
        { role: 'Design Engineer', percentage: 35 },
        { role: 'Manufacturing Engineer', percentage: 25 },
        { role: 'Project Manager', percentage: 25 },
        { role: 'Research Engineer', percentage: 15 }
      ],
      topColleges: ['MIT', 'Stanford', 'Georgia Tech', 'Caltech']
    },
    {
      id: 5,
      title: 'Digital Marketing',
      description: 'Master online marketing strategies, social media, and digital advertising',
      category: 'Marketing',
      duration: '1 Year',
      averageFee: 45000,
      popularity: 79,
      jobProspects: 81,
      averageSalary: 55000,
      colleges: 98,
      rating: 4.3,
      skills: ['SEO', 'Social Media', 'Content Marketing', 'Analytics'],
      careerPaths: [
        { role: 'Digital Marketer', percentage: 40 },
        { role: 'Social Media Manager', percentage: 25 },
        { role: 'Content Strategist', percentage: 20 },
        { role: 'Marketing Analyst', percentage: 15 }
      ],
      topColleges: ['Northwestern', 'NYU', 'USC', 'Boston University']
    },
    {
      id: 6,
      title: 'Medicine (MBBS)',
      description: 'Comprehensive medical education to become a practicing physician',
      category: 'Healthcare',
      duration: '5.5 Years',
      averageFee: 200000,
      popularity: 90,
      jobProspects: 95,
      averageSalary: 120000,
      colleges: 78,
      rating: 4.9,
      skills: ['Anatomy', 'Physiology', 'Pathology', 'Clinical Skills'],
      careerPaths: [
        { role: 'General Practitioner', percentage: 30 },
        { role: 'Specialist Doctor', percentage: 40 },
        { role: 'Surgeon', percentage: 20 },
        { role: 'Medical Researcher', percentage: 10 }
      ],
      topColleges: ['Harvard Medical', 'Johns Hopkins', 'UCSF', 'Mayo Clinic']
    }
  ]

  const categories = [...new Set(courses.map(course => course.category))]
  const durations = [...new Set(courses.map(course => course.duration))]

  const filteredCourses = useMemo(() => {
    let filtered = courses

    // Search filter
    if (searchQuery) {
      filtered = filtered.filter(course =>
        course.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        course.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
        course.category.toLowerCase().includes(searchQuery.toLowerCase()) ||
        course.skills.some(skill => 
          skill.toLowerCase().includes(searchQuery.toLowerCase())
        )
      )
    }

    // Category filter
    if (courseFilters.category) {
      filtered = filtered.filter(course => course.category === courseFilters.category)
    }

    // Duration filter
    if (courseFilters.duration) {
      filtered = filtered.filter(course => course.duration === courseFilters.duration)
    }

    // Sort
    switch (courseFilters.sortBy) {
      case 'popularity':
        filtered.sort((a, b) => b.popularity - a.popularity)
        break
      case 'salary':
        filtered.sort((a, b) => b.averageSalary - a.averageSalary)
        break
      case 'duration':
        filtered.sort((a, b) => parseFloat(a.duration) - parseFloat(b.duration))
        break
      case 'rating':
        filtered.sort((a, b) => b.rating - a.rating)
        break
      default:
        break
    }

    return filtered
  }, [courses, searchQuery, courseFilters])

  const handleFilterChange = (key, value) => {
    updateCourseFilters({ [key]: value })
  }

  const clearFilters = () => {
    updateCourseFilters({
      category: '',
      duration: '',
      sortBy: 'popularity'
    })
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
              Course Directory
            </h1>
            <p className={`text-lg mb-6 ${
              isDarkMode ? 'text-gray-300' : 'text-gray-600'
            }`}>
              Explore career paths and find the perfect course for your future
            </p>
            
            <div className="max-w-2xl">
              <SearchBar placeholder="Search courses, skills, or career paths..." />
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
                {/* Category Filter */}
                <div>
                  <label className={`block text-sm font-medium mb-2 ${
                    isDarkMode ? 'text-gray-300' : 'text-gray-700'
                  }`}>
                    Category
                  </label>
                  <select
                    value={courseFilters.category}
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

                {/* Duration Filter */}
                <div>
                  <label className={`block text-sm font-medium mb-2 ${
                    isDarkMode ? 'text-gray-300' : 'text-gray-700'
                  }`}>
                    Duration
                  </label>
                  <select
                    value={courseFilters.duration}
                    onChange={(e) => handleFilterChange('duration', e.target.value)}
                    className={`w-full p-3 rounded-lg border transition-colors duration-200 ${
                      isDarkMode
                        ? 'bg-gray-700 border-gray-600 text-white'
                        : 'bg-white border-gray-300 text-gray-900'
                    } focus:outline-none focus:ring-2 focus:ring-primary`}
                  >
                    <option value="">All Durations</option>
                    {durations.map(duration => (
                      <option key={duration} value={duration}>{duration}</option>
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
                    value={courseFilters.sortBy}
                    onChange={(e) => handleFilterChange('sortBy', e.target.value)}
                    className={`w-full p-3 rounded-lg border transition-colors duration-200 ${
                      isDarkMode
                        ? 'bg-gray-700 border-gray-600 text-white'
                        : 'bg-white border-gray-300 text-gray-900'
                    } focus:outline-none focus:ring-2 focus:ring-primary`}
                  >
                    <option value="popularity">Popularity</option>
                    <option value="salary">Average Salary</option>
                    <option value="duration">Duration</option>
                    <option value="rating">Rating</option>
                  </select>
                </div>
              </div>
            </Card>
          </div>

          {/* Course List */}
          <div className="flex-1">
            <div className="flex items-center justify-between mb-6">
              <p className={`text-sm ${
                isDarkMode ? 'text-gray-400' : 'text-gray-600'
              }`}>
                Showing {filteredCourses.length} courses
              </p>
            </div>

            <div className="grid grid-cols-1 gap-6">
              {filteredCourses.map((course, index) => (
                <motion.div
                  key={course.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3, delay: index * 0.1 }}
                >
                  <Card className="p-6 hover:shadow-xl transition-all duration-300">
                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                      {/* Course Info */}
                      <div className="lg:col-span-2">
                        <div className="flex items-start justify-between mb-4">
                          <div>
                            <div className="flex items-center space-x-3 mb-2">
                              <h3 className={`text-xl font-bold ${
                                isDarkMode ? 'text-white' : 'text-gray-900'
                              }`}>
                                {course.title}
                              </h3>
                              <span className="bg-accent text-gray-800 text-xs px-2 py-1 rounded-full">
                                {course.popularity}% Match
                              </span>
                            </div>
                            
                            <div className="flex items-center space-x-4 text-sm mb-3">
                              <span className="bg-primary/10 text-primary px-2 py-1 rounded-full">
                                {course.category}
                              </span>
                              <div className="flex items-center space-x-1">
                                <Star className="w-4 h-4 text-yellow-500 fill-current" />
                                <span className={isDarkMode ? 'text-gray-300' : 'text-gray-600'}>
                                  {course.rating}
                                </span>
                              </div>
                            </div>
                          </div>
                        </div>

                        <p className={`text-sm mb-4 ${
                          isDarkMode ? 'text-gray-300' : 'text-gray-600'
                        }`}>
                          {course.description}
                        </p>

                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                          <div className="text-center p-3 rounded-lg bg-gradient-to-br from-primary/5 to-secondary/5">
                            <Clock className={`w-5 h-5 mx-auto mb-1 ${
                              isDarkMode ? 'text-gray-400' : 'text-gray-500'
                            }`} />
                            <p className={`text-xs ${
                              isDarkMode ? 'text-gray-400' : 'text-gray-500'
                            }`}>
                              Duration
                            </p>
                            <p className={`font-semibold ${
                              isDarkMode ? 'text-white' : 'text-gray-900'
                            }`}>
                              {course.duration}
                            </p>
                          </div>


                          <div className="text-center p-3 rounded-lg bg-gradient-to-br from-primary/5 to-secondary/5">
                            <TrendingUp className={`w-5 h-5 mx-auto mb-1 ${
                              isDarkMode ? 'text-gray-400' : 'text-gray-500'
                            }`} />
                            <p className={`text-xs ${
                              isDarkMode ? 'text-gray-400' : 'text-gray-500'
                            }`}>
                              Avg. Salary
                            </p>
                            <p className={`font-semibold ${
                              isDarkMode ? 'text-white' : 'text-gray-900'
                            }`}>
                              ${course.averageSalary.toLocaleString()}
                            </p>
                          </div>

                          <div className="text-center p-3 rounded-lg bg-gradient-to-br from-primary/5 to-secondary/5">
                            <Building className={`w-5 h-5 mx-auto mb-1 ${
                              isDarkMode ? 'text-gray-400' : 'text-gray-500'
                            }`} />
                            <p className={`text-xs ${
                              isDarkMode ? 'text-gray-400' : 'text-gray-500'
                            }`}>
                              Colleges
                            </p>
                            <p className={`font-semibold ${
                              isDarkMode ? 'text-white' : 'text-gray-900'
                            }`}>
                              {course.colleges}
                            </p>
                          </div>
                        </div>

                        <div className="mb-4">
                          <p className={`text-sm font-medium mb-2 ${
                            isDarkMode ? 'text-gray-300' : 'text-gray-700'
                          }`}>
                            Key Skills:
                          </p>
                          <div className="flex flex-wrap gap-2">
                            {course.skills.map((skill, idx) => (
                              <span
                                key={idx}
                                className="bg-secondary/20 text-primary text-xs px-2 py-1 rounded-full"
                              >
                                {skill}
                              </span>
                            ))}
                          </div>
                        </div>

                        <div className="mb-4">
                          <p className={`text-sm font-medium mb-2 ${
                            isDarkMode ? 'text-gray-300' : 'text-gray-700'
                          }`}>
                            Top Colleges:
                          </p>
                          <p className={`text-sm ${
                            isDarkMode ? 'text-gray-400' : 'text-gray-600'
                          }`}>
                            {course.topColleges.join(', ')}
                          </p>
                        </div>
                      </div>

                      {/* Career Path Chart */}
                      <div className="lg:col-span-1">
                        <div className="mb-4">
                          <h4 className={`text-sm font-medium mb-3 ${
                            isDarkMode ? 'text-gray-300' : 'text-gray-700'
                          }`}>
                            Career Opportunities
                          </h4>
                          <Chart 
                            type="pie"
                            data={course.careerPaths}
                            dataKey="percentage"
                            height={200}
                          />
                        </div>

                        <div className="space-y-3">
                          <Button 
                            className="w-full"
                            onClick={() => setSelectedCourse(course)}
                          >
                            View Details
                          </Button>
                          <Button variant="outline" className="w-full">
                            Find Colleges
                          </Button>
                        </div>
                      </div>
                    </div>
                  </Card>
                </motion.div>
              ))}
            </div>

            {filteredCourses.length === 0 && (
              <Card className="p-12 text-center">
                <BookOpen className={`w-16 h-16 mx-auto mb-4 ${
                  isDarkMode ? 'text-gray-600' : 'text-gray-400'
                }`} />
                <h3 className={`text-xl font-semibold mb-2 ${
                  isDarkMode ? 'text-white' : 'text-gray-900'
                }`}>
                  No courses found
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

export default CourseList
