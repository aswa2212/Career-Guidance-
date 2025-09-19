import { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  BookOpen, 
  GraduationCap, 
  FileText, 
  TrendingUp, 
  Users, 
  Award,
  ArrowRight,
  Calendar,
  Bell
} from 'lucide-react'
import useAppStore from '../store/useAppStore'
import Card from '../components/Card'
import Button from '../components/Button'
import SearchBar from '../components/SearchBar'
import Chart from '../components/Chart'
import Navbar from '../components/layout/Navbar'
import RecommendedCourses from '../components/RecommendedCourses'

const Dashboard = () => {
  const { user, stats, isDarkMode } = useAppStore()
  const [searchQuery, setSearchQuery] = useState('')

  // Sample data for charts
  const testScoreData = [
    { name: 'Math', score: 85 },
    { name: 'Science', score: 92 },
    { name: 'English', score: 78 },
    { name: 'Reasoning', score: 88 }
  ]

  const applicationTrendData = [
    { month: 'Jan', applications: 12 },
    { month: 'Feb', applications: 19 },
    { month: 'Mar', applications: 25 },
    { month: 'Apr', applications: 31 },
    { month: 'May', applications: 28 }
  ]

  const quickStats = [
    {
      title: 'Total Colleges',
      value: stats.totalColleges.toLocaleString(),
      icon: GraduationCap,
      color: 'text-blue-600',
      bgColor: 'bg-blue-100',
      change: '+12%'
    },
    {
      title: 'Available Courses',
      value: stats.totalCourses.toLocaleString(),
      icon: BookOpen,
      color: 'text-green-600',
      bgColor: 'bg-green-100',
      change: '+8%'
    },
    {
      title: 'Tests Completed',
      value: stats.testsCompleted,
      icon: Award,
      color: 'text-purple-600',
      bgColor: 'bg-purple-100',
      change: '+3'
    },
    {
      title: 'Applications',
      value: stats.applicationsSubmitted,
      icon: FileText,
      color: 'text-orange-600',
      bgColor: 'bg-orange-100',
      change: '+2'
    }
  ]

  const recommendedCourses = [
    {
      id: 1,
      title: 'Computer Science Engineering',
      description: 'Learn programming, algorithms, and software development',
      duration: '4 Years',
      colleges: 245,
      popularity: 95
    },
    {
      id: 2,
      title: 'Data Science',
      description: 'Master data analysis, machine learning, and AI',
      duration: '2 Years',
      colleges: 156,
      popularity: 88
    },
    {
      id: 3,
      title: 'Business Administration',
      description: 'Develop leadership and management skills',
      duration: '2 Years',
      colleges: 312,
      popularity: 82
    }
  ]

  const recommendedColleges = [
    {
      id: 1,
      name: 'MIT Institute of Technology',
      location: 'Cambridge, MA',
      ranking: 1,
      acceptanceRate: '7%',
      image: '/api/placeholder/300/200'
    },
    {
      id: 2,
      name: 'Stanford University',
      location: 'Stanford, CA',
      ranking: 2,
      acceptanceRate: '4%',
      image: '/api/placeholder/300/200'
    },
    {
      id: 3,
      name: 'Harvard University',
      location: 'Cambridge, MA',
      ranking: 3,
      acceptanceRate: '5%',
      image: '/api/placeholder/300/200'
    }
  ]

  const upcomingDeadlines = [
    { name: 'JEE Main Registration', date: '2024-01-15', daysLeft: 12 },
    { name: 'NEET Application', date: '2024-01-20', daysLeft: 17 },
    { name: 'SAT Registration', date: '2024-01-25', daysLeft: 22 }
  ]

  return (
    <>
      <Navbar />
      <div className={`min-h-screen ${
        isDarkMode ? 'bg-gray-900' : 'bg-gray-50'
      } transition-colors duration-300`}>
      {/* Hero Section */}
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
              Welcome back, {user?.name || 'Student'}! 👋
            </h1>
            <p className={`text-lg mb-6 ${
              isDarkMode ? 'text-gray-300' : 'text-gray-600'
            }`}>
              Continue your journey to academic success
            </p>
            
            <div className="max-w-2xl">
              <SearchBar 
                placeholder="Search for colleges, courses, or resources..."
                onSearch={setSearchQuery}
              />
            </div>
          </motion.div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Quick Stats */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.1 }}
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8"
        >
          {quickStats.map((stat, index) => (
            <Card key={stat.title} className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className={`text-sm font-medium ${
                    isDarkMode ? 'text-gray-400' : 'text-gray-600'
                  }`}>
                    {stat.title}
                  </p>
                  <p className={`text-2xl font-bold mt-1 ${
                    isDarkMode ? 'text-white' : 'text-gray-900'
                  }`}>
                    {stat.value}
                  </p>
                  <p className="text-sm text-green-600 mt-1">
                    {stat.change} from last month
                  </p>
                </div>
                <div className={`p-3 rounded-full ${stat.bgColor} ${
                  isDarkMode ? 'bg-opacity-20' : ''
                }`}>
                  <stat.icon className={`w-6 h-6 ${stat.color} ${
                    isDarkMode ? 'text-opacity-80' : ''
                  }`} />
                </div>
              </div>
            </Card>
          ))}
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
          {/* Test Scores Chart */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="lg:col-span-2"
          >
            <Card className="p-6">
              <div className="flex items-center justify-between mb-6">
                <h3 className={`text-lg font-semibold ${
                  isDarkMode ? 'text-white' : 'text-gray-900'
                }`}>
                  Your Test Performance
                </h3>
                <Button variant="ghost" size="sm">
                  View Details
                </Button>
              </div>
              <Chart 
                type="bar"
                data={testScoreData}
                dataKey="score"
                xAxisKey="name"
                height={250}
              />
            </Card>
          </motion.div>

          {/* Upcoming Deadlines */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
          >
            <Card className="p-6">
              <div className="flex items-center justify-between mb-6">
                <h3 className={`text-lg font-semibold ${
                  isDarkMode ? 'text-white' : 'text-gray-900'
                }`}>
                  Upcoming Deadlines
                </h3>
                <Calendar className={`w-5 h-5 ${
                  isDarkMode ? 'text-gray-400' : 'text-gray-500'
                }`} />
              </div>
              <div className="space-y-4">
                {upcomingDeadlines.map((deadline, index) => (
                  <div key={index} className="flex items-center justify-between p-3 rounded-lg bg-gradient-to-r from-primary/5 to-secondary/5">
                    <div>
                      <p className={`font-medium text-sm ${
                        isDarkMode ? 'text-white' : 'text-gray-900'
                      }`}>
                        {deadline.name}
                      </p>
                      <p className={`text-xs ${
                        isDarkMode ? 'text-gray-400' : 'text-gray-500'
                      }`}>
                        {deadline.date}
                      </p>
                    </div>
                    <span className="bg-primary text-white text-xs px-2 py-1 rounded-full">
                      {deadline.daysLeft}d
                    </span>
                  </div>
                ))}
              </div>
            </Card>
          </motion.div>
        </div>

        {/* AI-Powered Recommended Courses */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          className="mb-8"
        >
          <RecommendedCourses limit={6} showHeader={true} />
        </motion.div>

        {/* Recommended Colleges */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.5 }}
        >
          <div className="flex items-center justify-between mb-6">
            <h2 className={`text-2xl font-bold ${
              isDarkMode ? 'text-white' : 'text-gray-900'
            }`}>
              Top Colleges for You
            </h2>
            <Button variant="ghost">
              View All <ArrowRight className="w-4 h-4 ml-2" />
            </Button>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {recommendedColleges.map((college) => (
              <Card key={college.id} className="overflow-hidden">
                <div className="h-48 bg-gradient-to-br from-primary/10 to-secondary/10 flex items-center justify-center">
                  <GraduationCap className="w-16 h-16 text-primary opacity-50" />
                </div>
                <div className="p-6">
                  <div className="flex items-start justify-between mb-2">
                    <h3 className={`font-semibold ${
                      isDarkMode ? 'text-white' : 'text-gray-900'
                    }`}>
                      {college.name}
                    </h3>
                    <span className="bg-primary text-white text-xs px-2 py-1 rounded-full">
                      #{college.ranking}
                    </span>
                  </div>
                  <p className={`text-sm mb-4 ${
                    isDarkMode ? 'text-gray-300' : 'text-gray-600'
                  }`}>
                    {college.location}
                  </p>
                  <div className="flex items-center justify-between text-sm mb-4">
                    <span className={isDarkMode ? 'text-gray-400' : 'text-gray-500'}>
                      Acceptance Rate
                    </span>
                    <span className="font-medium text-primary">
                      {college.acceptanceRate}
                    </span>
                  </div>
                  <Button className="w-full" size="sm" variant="outline">
                    View Details
                  </Button>
                </div>
              </Card>
            ))}
          </div>
        </motion.div>
      </div>
    </div>
    </>
  )
}

export default Dashboard
