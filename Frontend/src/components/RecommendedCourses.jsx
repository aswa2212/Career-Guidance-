import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  BookOpen, 
  Clock, 
  TrendingUp, 
  Star, 
  ArrowRight,
  RefreshCw,
  AlertCircle,
  Sparkles
} from 'lucide-react';
import { api } from '../services/api';
import Card from './ui/Card';
import Button from './ui/Button';
import toast from 'react-hot-toast';

const RecommendedCourses = ({ limit = 6, showHeader = true }) => {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [userInterests, setUserInterests] = useState([]);

  useEffect(() => {
    loadRecommendations();
  }, [limit]);

  const loadRecommendations = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await api.get(`/recommendations/?limit=${limit}`);
      console.log('Recommendations API response:', response);
      
      if (response) {
        // Handle different response structures
        let recData = response.data || response;
        setRecommendations(recData.recommendations || []);
        setUserInterests(recData.user_interests || []);
        
        console.log('User interests loaded:', recData.user_interests);
        console.log('Recommendations loaded:', recData.recommendations?.length);
        
        if (recData.error) {
          toast.error('Using fallback recommendations');
        }
      }
    } catch (error) {
      console.error('Failed to load recommendations:', error);
      setError('Failed to load recommendations');
      toast.error('Failed to load recommendations');
      
      // Set fallback recommendations
      setRecommendations(getFallbackRecommendations());
    } finally {
      setLoading(false);
    }
  };

  const getFallbackRecommendations = () => [
    {
      course_id: 1,
      course_name: "Computer Science Engineering",
      description: "Comprehensive program covering programming, algorithms, data structures, and software engineering",
      required_skills: ["Programming", "Algorithms", "Data Structures", "Software Engineering"],
      career_paths: ["Software Developer", "Data Scientist", "System Architect", "Tech Lead"],
      duration: "4 years",
      level: "Undergraduate",
      match_percentage: 90
    },
    {
      course_id: 2,
      course_name: "Data Science",
      description: "Master data analysis, machine learning, statistics, and big data technologies",
      required_skills: ["Python", "Statistics", "Machine Learning", "Data Analysis"],
      career_paths: ["Data Scientist", "ML Engineer", "Business Analyst", "Research Scientist"],
      duration: "2 years",
      level: "Postgraduate",
      match_percentage: 87
    },
    {
      course_id: 4,
      course_name: "Web Development",
      description: "Full-stack web development with modern frameworks and technologies",
      required_skills: ["HTML", "CSS", "JavaScript", "React", "Node.js"],
      career_paths: ["Frontend Developer", "Backend Developer", "Full Stack Developer", "Web Designer"],
      duration: "6 months",
      level: "Certificate",
      match_percentage: 83
    }
  ];

  const handleRefresh = () => {
    loadRecommendations();
  };

  const handleCourseClick = (courseId) => {
    // Navigate to course details or handle course selection
    console.log('Course clicked:', courseId);
    toast.success('Course details coming soon!');
  };

  const getMatchColor = (percentage) => {
    if (percentage >= 85) return 'text-green-600 bg-green-100';
    if (percentage >= 70) return 'text-blue-600 bg-blue-100';
    if (percentage >= 60) return 'text-yellow-600 bg-yellow-100';
    return 'text-gray-600 bg-gray-100';
  };

  const getLevelColor = (level) => {
    switch (level?.toLowerCase()) {
      case 'undergraduate':
        return 'text-blue-600 bg-blue-100';
      case 'postgraduate':
        return 'text-purple-600 bg-purple-100';
      case 'certificate':
        return 'text-green-600 bg-green-100';
      default:
        return 'text-gray-600 bg-gray-100';
    }
  };

  if (loading) {
    return (
      <div className="space-y-4">
        {showHeader && (
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-bold text-gray-900 flex items-center">
              <Sparkles className="w-6 h-6 mr-2 text-yellow-500" />
              Recommended for You
            </h2>
          </div>
        )}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[...Array(limit)].map((_, index) => (
            <Card key={index} className="animate-pulse">
              <div className="h-4 bg-gray-200 rounded mb-4"></div>
              <div className="h-3 bg-gray-200 rounded mb-2"></div>
              <div className="h-3 bg-gray-200 rounded mb-4"></div>
              <div className="h-8 bg-gray-200 rounded"></div>
            </Card>
          ))}
        </div>
      </div>
    );
  }

  if (error && recommendations.length === 0) {
    return (
      <div className="text-center py-8">
        <AlertCircle className="w-12 h-12 text-red-500 mx-auto mb-4" />
        <h3 className="text-lg font-semibold text-gray-900 mb-2">Unable to Load Recommendations</h3>
        <p className="text-gray-600 mb-4">{error}</p>
        <Button onClick={handleRefresh} className="flex items-center space-x-2">
          <RefreshCw className="w-4 h-4" />
          <span>Try Again</span>
        </Button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {showHeader && (
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold text-gray-900 flex items-center">
              <Sparkles className="w-6 h-6 mr-2 text-yellow-500" />
              Recommended for You
            </h2>
            {userInterests.length > 0 ? (
              <div className="mt-2">
                <p className="text-gray-600 mb-2">
                  Based on your interests:
                </p>
                <div className="flex flex-wrap gap-2">
                  {userInterests.slice(0, 5).map((interest, index) => (
                    <span
                      key={index}
                      className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
                    >
                      {interest}
                    </span>
                  ))}
                  {userInterests.length > 5 && (
                    <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-600">
                      +{userInterests.length - 5} more
                    </span>
                  )}
                </div>
              </div>
            ) : (
              <p className="text-gray-500 mt-1 text-sm">
                Add interests in Settings to get personalized recommendations
              </p>
            )}
          </div>
          <Button 
            variant="ghost" 
            onClick={handleRefresh}
            className="flex items-center space-x-2"
            disabled={loading}
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            <span>Refresh</span>
          </Button>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {recommendations.map((course, index) => (
          <motion.div
            key={course.course_id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: index * 0.1 }}
          >
            <Card className="h-full hover:shadow-lg transition-all duration-300 cursor-pointer group">
              <div className="p-6 h-full flex flex-col">
                {/* Header */}
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center space-x-2">
                    <BookOpen className="w-6 h-6 text-blue-600" />
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getLevelColor(course.level)}`}>
                      {course.level}
                    </span>
                  </div>
                  <div className={`px-2 py-1 rounded-full text-xs font-bold ${getMatchColor(course.match_percentage)}`}>
                    {course.match_percentage}% Match
                  </div>
                </div>

                {/* Course Title */}
                <h3 className="text-lg font-semibold text-gray-900 mb-2 group-hover:text-blue-600 transition-colors">
                  {course.course_name}
                </h3>

                {/* Description */}
                <p className="text-gray-600 text-sm mb-4 flex-grow line-clamp-3">
                  {course.description}
                </p>

                {/* Duration */}
                <div className="flex items-center text-sm text-gray-500 mb-4">
                  <Clock className="w-4 h-4 mr-1" />
                  <span>{course.duration}</span>
                </div>

                {/* Skills */}
                {course.required_skills && course.required_skills.length > 0 && (
                  <div className="mb-4">
                    <p className="text-xs font-medium text-gray-700 mb-2">Key Skills:</p>
                    <div className="flex flex-wrap gap-1">
                      {course.required_skills.slice(0, 3).map((skill, skillIndex) => (
                        <span 
                          key={skillIndex}
                          className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded-full"
                        >
                          {skill.trim()}
                        </span>
                      ))}
                      {course.required_skills.length > 3 && (
                        <span className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded-full">
                          +{course.required_skills.length - 3} more
                        </span>
                      )}
                    </div>
                  </div>
                )}

                {/* Career Paths */}
                {course.career_paths && course.career_paths.length > 0 && (
                  <div className="mb-4">
                    <p className="text-xs font-medium text-gray-700 mb-2">Career Paths:</p>
                    <div className="flex flex-wrap gap-1">
                      {course.career_paths.slice(0, 2).map((career, careerIndex) => (
                        <span 
                          key={careerIndex}
                          className="px-2 py-1 bg-blue-50 text-blue-700 text-xs rounded-full"
                        >
                          {career.trim()}
                        </span>
                      ))}
                      {course.career_paths.length > 2 && (
                        <span className="px-2 py-1 bg-blue-50 text-blue-700 text-xs rounded-full">
                          +{course.career_paths.length - 2} more
                        </span>
                      )}
                    </div>
                  </div>
                )}

                {/* Action Button */}
                <Button 
                  onClick={() => handleCourseClick(course.course_id)}
                  className="w-full mt-auto flex items-center justify-center space-x-2 group-hover:bg-blue-700 transition-colors"
                >
                  <span>Explore Course</span>
                  <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                </Button>
              </div>
            </Card>
          </motion.div>
        ))}
      </div>

      {recommendations.length === 0 && !loading && (
        <div className="text-center py-8">
          <BookOpen className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 mb-2">No Recommendations Available</h3>
          <p className="text-gray-600 mb-4">
            Add some interests in your profile settings to get personalized recommendations.
          </p>
          <Button onClick={() => window.location.href = '/settings'}>
            Update Interests
          </Button>
        </div>
      )}
    </div>
  );
};

export default RecommendedCourses;
