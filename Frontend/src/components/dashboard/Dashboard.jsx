import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { 
  User, 
  BookOpen, 
  Target, 
  Calendar, 
  TrendingUp,
  School,
  LogOut
} from 'lucide-react';
import useAuthStore from '../../store/authStore';
import apiService from '../../services/api';
import toast from 'react-hot-toast';

const Dashboard = () => {
  const { user, logout } = useAuthStore();
  const navigate = useNavigate();
  const [careerSuggestions, setCareerSuggestions] = useState([]);
  const [colleges, setColleges] = useState([]);
  const [timeline, setTimeline] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      
      // Load career suggestions from database
      try {
        const suggestions = await apiService.getCareerSuggestions();
        setCareerSuggestions(suggestions.slice(0, 3)); // Show top 3
        console.log('Career suggestions loaded:', suggestions);
      } catch (error) {
        console.log('Career suggestions error:', error);
        // Fallback to mock data if API fails
        setCareerSuggestions([
          { id: 1, title: 'Software Engineer', field: 'Technology', median_salary: '$85,000', job_outlook: 'Growing' },
          { id: 2, title: 'Data Scientist', field: 'Technology', median_salary: '$95,000', job_outlook: 'High Growth' }
        ]);
      }

      // Load colleges from database
      try {
        const collegeData = await apiService.getColleges();
        setColleges(collegeData.slice(0, 3)); // Show top 3
        console.log('Colleges loaded:', collegeData);
      } catch (error) {
        console.log('Colleges error:', error);
        // Fallback to mock data if API fails
        setColleges([
          { id: 1, name: 'IIT Delhi', city: 'New Delhi', state: 'Delhi' },
          { id: 2, name: 'IIT Bombay', city: 'Mumbai', state: 'Maharashtra' }
        ]);
      }

      // Load timeline (mock for now)
      try {
        const timelineData = await apiService.getTimeline();
        setTimeline(timelineData.slice(0, 3)); // Show next 3 deadlines
      } catch (error) {
        console.log('Timeline not available yet');
        // Mock timeline data
        setTimeline([
          { id: 1, title: 'Application Deadline', date: '2024-03-15' },
          { id: 2, title: 'Entrance Exam', date: '2024-04-20' }
        ]);
      }

    } catch (error) {
      console.error('Dashboard data loading error:', error);
      toast.error('Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
  };

  // Navigation handlers
  const handleStartTest = () => {
    navigate('/assessments');
  };

  const handleExploreColleges = () => {
    navigate('/colleges');
  };

  const handlePlanTimeline = () => {
    navigate('/timeline');
  };

  const handleViewCareerDetails = (careerId) => {
    navigate(`/careers/${careerId}`);
  };

  const handleViewCollegeDetails = (collegeId) => {
    navigate(`/colleges/${collegeId}`);
  };

  const handleCompleteProfile = () => {
    navigate('/profile');
  };

  const handleViewCourses = () => {
    navigate('/courses');
  };

  const handleViewCareers = () => {
    navigate('/careers');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading your dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-gray-900">Career Guidance Platform</h1>
            </div>
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <User className="w-5 h-5 text-gray-600" />
                <span className="text-gray-700">{user?.full_name || user?.email}</span>
              </div>
              <button
                onClick={handleLogout}
                className="flex items-center space-x-2 px-4 py-2 text-gray-600 hover:text-gray-900 transition-colors"
              >
                <LogOut className="w-4 h-4" />
                <span>Logout</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h2 className="text-3xl font-bold text-gray-900 mb-2">
            Welcome back, {user?.full_name?.split(' ')[0] || 'Student'}!
          </h2>
          <p className="text-gray-600">Here's your career guidance overview</p>
        </motion.div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="bg-white rounded-lg shadow p-6"
          >
            <div className="flex items-center">
              <Target className="w-8 h-8 text-blue-600" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Career Matches</p>
                <p className="text-2xl font-bold text-gray-900">{careerSuggestions.length}</p>
              </div>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="bg-white rounded-lg shadow p-6"
          >
            <div className="flex items-center">
              <School className="w-8 h-8 text-green-600" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Colleges</p>
                <p className="text-2xl font-bold text-gray-900">{colleges.length}</p>
              </div>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="bg-white rounded-lg shadow p-6"
          >
            <div className="flex items-center">
              <Calendar className="w-8 h-8 text-purple-600" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Deadlines</p>
                <p className="text-2xl font-bold text-gray-900">{timeline.length}</p>
              </div>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="bg-white rounded-lg shadow p-6"
          >
            <div className="flex items-center">
              <TrendingUp className="w-8 h-8 text-orange-600" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Progress</p>
                <p className="text-2xl font-bold text-gray-900">85%</p>
              </div>
            </div>
          </motion.div>
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Career Suggestions */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.5 }}
            className="bg-white rounded-lg shadow"
          >
            <div className="p-6 border-b">
              <h3 className="text-lg font-semibold text-gray-900 flex items-center">
                <Target className="w-5 h-5 mr-2 text-blue-600" />
                Career Suggestions
              </h3>
            </div>
            <div className="p-6">
              {careerSuggestions.length > 0 ? (
                <div className="space-y-4">
                  {careerSuggestions.map((career, index) => (
                    <div key={index} className="flex items-center p-4 bg-gray-50 rounded-lg">
                      <div className="flex-1">
                        <h4 className="font-medium text-gray-900">{career.title}</h4>
                        <p className="text-sm text-gray-600">{career.field}</p>
                      </div>
                      <div className="text-right">
                        <p className="text-sm font-medium text-green-600">{career.median_salary}</p>
                        <p className="text-xs text-gray-500">{career.job_outlook}</p>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-8">
                  <BookOpen className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-600">Take an aptitude test to get career suggestions</p>
                  <button 
                    onClick={handleStartTest}
                    className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                  >
                    Start Test
                  </button>
                </div>
              )}
            </div>
          </motion.div>

          {/* Recommended Colleges */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.6 }}
            className="bg-white rounded-lg shadow"
          >
            <div className="p-6 border-b">
              <h3 className="text-lg font-semibold text-gray-900 flex items-center">
                <School className="w-5 h-5 mr-2 text-green-600" />
                Recommended Colleges
              </h3>
            </div>
            <div className="p-6">
              {colleges.length > 0 ? (
                <div className="space-y-4">
                  {colleges.map((college, index) => (
                    <div key={index} className="flex items-center p-4 bg-gray-50 rounded-lg">
                      <div className="flex-1">
                        <h4 className="font-medium text-gray-900">{college.name}</h4>
                        <p className="text-sm text-gray-600">{college.city}, {college.state}</p>
                      </div>
                      <button 
                        onClick={() => handleViewCollegeDetails(college.id || index + 1)}
                        className="px-3 py-1 text-sm bg-green-100 text-green-700 rounded-full hover:bg-green-200"
                      >
                        View Details
                      </button>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-8">
                  <School className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-600">Complete your profile to get college recommendations</p>
                  <button 
                    onClick={handleCompleteProfile}
                    className="mt-4 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
                  >
                    Complete Profile
                  </button>
                </div>
              )}
            </div>
          </motion.div>
        </div>

        {/* Quick Actions */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.7 }}
          className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6"
        >
          <button 
            onClick={handleStartTest}
            className="p-6 bg-white rounded-lg shadow hover:shadow-md transition-shadow text-left"
          >
            <BookOpen className="w-8 h-8 text-blue-600 mb-4" />
            <h3 className="font-semibold text-gray-900 mb-2">Take Aptitude Test</h3>
            <p className="text-gray-600 text-sm">Discover your strengths and get personalized career suggestions</p>
          </button>

          <button 
            onClick={handleExploreColleges}
            className="p-6 bg-white rounded-lg shadow hover:shadow-md transition-shadow text-left"
          >
            <School className="w-8 h-8 text-green-600 mb-4" />
            <h3 className="font-semibold text-gray-900 mb-2">Explore Colleges</h3>
            <p className="text-gray-600 text-sm">Find the best colleges for your career goals</p>
          </button>

          <button 
            onClick={handlePlanTimeline}
            className="p-6 bg-white rounded-lg shadow hover:shadow-md transition-shadow text-left"
          >
            <Calendar className="w-8 h-8 text-purple-600 mb-4" />
            <h3 className="font-semibold text-gray-900 mb-2">Plan Timeline</h3>
            <p className="text-gray-600 text-sm">Track important deadlines and milestones</p>
          </button>
        </motion.div>
      </main>
    </div>
  );
};

export default Dashboard;
