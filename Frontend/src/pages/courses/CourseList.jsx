import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  Search, 
  Filter, 
  BookOpen, 
  Clock, 
  Star, 
  Users,
  TrendingUp,
  MapPin,
  ChevronDown,
  X
} from 'lucide-react';
import PageLayout from '../../components/layout/PageLayout';
import apiService from '../../services/api';
import toast from 'react-hot-toast';
import Card from '../../components/ui/Card';
import Button from '../../components/ui/Button';
import { LoadingCard } from '../../components/ui/Loading';

const CourseList = () => {
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedFilters, setSelectedFilters] = useState({
    category: '',
    duration: '',
    level: '',
    mode: ''
  });
  const [showFilters, setShowFilters] = useState(false);

  const mockCourses = [
    {
      id: 1,
      title: 'Computer Science Engineering',
      category: 'Engineering',
      duration: '4 years',
      level: 'Undergraduate',
      mode: 'Full-time',
      rating: 4.8,
      students: 1250,
      description: 'Comprehensive program covering software development, algorithms, and computer systems',
      skills: ['Programming', 'Data Structures', 'Software Engineering', 'Database Management'],
      colleges: 45,
      averageFee: '₹2,50,000',
      placement: '95%',
      image: '/api/placeholder/300/200'
    },
    {
      id: 2,
      title: 'Data Science & Analytics',
      category: 'Technology',
      duration: '2 years',
      level: 'Postgraduate',
      mode: 'Full-time',
      rating: 4.9,
      students: 890,
      description: 'Advanced program in data analysis, machine learning, and statistical modeling',
      skills: ['Python', 'Machine Learning', 'Statistics', 'Data Visualization'],
      colleges: 28,
      averageFee: '₹3,75,000',
      placement: '98%',
      image: '/api/placeholder/300/200'
    },
    {
      id: 3,
      title: 'Digital Marketing',
      category: 'Business',
      duration: '6 months',
      level: 'Certificate',
      mode: 'Online',
      rating: 4.6,
      students: 2100,
      description: 'Learn modern digital marketing strategies and tools',
      skills: ['SEO', 'Social Media', 'Content Marketing', 'Analytics'],
      colleges: 15,
      averageFee: '₹45,000',
      placement: '85%',
      image: '/api/placeholder/300/200'
    },
    {
      id: 4,
      title: 'Mechanical Engineering',
      category: 'Engineering',
      duration: '4 years',
      level: 'Undergraduate',
      mode: 'Full-time',
      rating: 4.7,
      students: 980,
      description: 'Traditional engineering discipline focusing on mechanical systems',
      skills: ['CAD Design', 'Thermodynamics', 'Manufacturing', 'Materials Science'],
      colleges: 52,
      averageFee: '₹2,25,000',
      placement: '92%',
      image: '/api/placeholder/300/200'
    },
    {
      id: 5,
      title: 'MBA - Finance',
      category: 'Business',
      duration: '2 years',
      level: 'Postgraduate',
      mode: 'Full-time',
      rating: 4.8,
      students: 750,
      description: 'Master of Business Administration with specialization in Finance',
      skills: ['Financial Analysis', 'Investment Banking', 'Risk Management', 'Corporate Finance'],
      colleges: 35,
      averageFee: '₹8,50,000',
      placement: '96%',
      image: '/api/placeholder/300/200'
    },
    {
      id: 6,
      title: 'Graphic Design',
      category: 'Creative',
      duration: '1 year',
      level: 'Diploma',
      mode: 'Hybrid',
      rating: 4.5,
      students: 650,
      description: 'Creative program covering visual design and digital media',
      skills: ['Adobe Creative Suite', 'Typography', 'Branding', 'UI/UX Design'],
      colleges: 22,
      averageFee: '₹1,20,000',
      placement: '78%',
      image: '/api/placeholder/300/200'
    }
  ];

  const filterOptions = {
    category: ['Engineering', 'Technology', 'Business', 'Creative', 'Healthcare', 'Arts'],
    duration: ['6 months', '1 year', '2 years', '3 years', '4 years'],
    level: ['Certificate', 'Diploma', 'Undergraduate', 'Postgraduate'],
    mode: ['Full-time', 'Part-time', 'Online', 'Hybrid']
  };

  useEffect(() => {
    const fetchCourses = async () => {
      try {
        setLoading(true);
        const response = await apiService.getCourses();
        setCourses(response.data || mockCourses);
      } catch (error) {
        console.error('Failed to fetch courses:', error);
        toast.error('Failed to load courses. Using sample data.');
        setCourses(mockCourses);
      } finally {
        setLoading(false);
      }
    };

    fetchCourses();
  }, []);

  const filteredCourses = courses.filter(course => {
    const matchesSearch = course.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         course.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         course.skills.some(skill => skill.toLowerCase().includes(searchTerm.toLowerCase()));
    
    const matchesCategory = !selectedFilters.category || course.category === selectedFilters.category;
    const matchesDuration = !selectedFilters.duration || course.duration === selectedFilters.duration;
    const matchesLevel = !selectedFilters.level || course.level === selectedFilters.level;
    const matchesMode = !selectedFilters.mode || course.mode === selectedFilters.mode;

    return matchesSearch && matchesCategory && matchesDuration && matchesLevel && matchesMode;
  });

  const handleFilterChange = (filterType, value) => {
    setSelectedFilters(prev => ({
      ...prev,
      [filterType]: prev[filterType] === value ? '' : value
    }));
  };

  const clearFilters = () => {
    setSelectedFilters({
      category: '',
      duration: '',
      level: '',
      mode: ''
    });
  };

  const activeFiltersCount = Object.values(selectedFilters).filter(Boolean).length;

  if (loading) {
    return (
      <PageLayout title="Courses" subtitle="Explore courses and programs">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <LoadingCard key={i} />
          ))}
        </div>
      </PageLayout>
    );
  }

  return (
    <PageLayout 
      title="Course Explorer" 
      subtitle="Discover courses and programs that match your career goals"
    >
      {/* Search and Filter Bar */}
      <div className="mb-8 space-y-4">
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Search courses, skills, or keywords..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <Button
            variant="outline"
            onClick={() => setShowFilters(!showFilters)}
            className="flex items-center space-x-2"
          >
            <Filter className="w-4 h-4" />
            <span>Filters</span>
            {activeFiltersCount > 0 && (
              <span className="bg-blue-600 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                {activeFiltersCount}
              </span>
            )}
            <ChevronDown className={`w-4 h-4 transition-transform ${showFilters ? 'rotate-180' : ''}`} />
          </Button>
        </div>

        {/* Filter Panel */}
        {showFilters && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="bg-white p-6 rounded-lg border border-gray-200"
          >
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900">Filters</h3>
              {activeFiltersCount > 0 && (
                <Button variant="ghost" size="sm" onClick={clearFilters}>
                  <X className="w-4 h-4 mr-1" />
                  Clear all
                </Button>
              )}
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {Object.entries(filterOptions).map(([filterType, options]) => (
                <div key={filterType}>
                  <h4 className="text-sm font-medium text-gray-700 mb-2 capitalize">
                    {filterType}
                  </h4>
                  <div className="space-y-2">
                    {options.map(option => (
                      <label key={option} className="flex items-center">
                        <input
                          type="checkbox"
                          checked={selectedFilters[filterType] === option}
                          onChange={() => handleFilterChange(filterType, option)}
                          className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                        />
                        <span className="ml-2 text-sm text-gray-600">{option}</span>
                      </label>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </motion.div>
        )}
      </div>

      {/* Results Summary */}
      <div className="mb-6">
        <p className="text-gray-600">
          Showing {filteredCourses.length} of {courses.length} courses
          {searchTerm && ` for "${searchTerm}"`}
        </p>
      </div>

      {/* Course Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredCourses.map((course, index) => (
          <motion.div
            key={course.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: index * 0.1 }}
          >
            <Card className="h-full flex flex-col">
              <div className="relative mb-4">
                <div className="w-full h-48 bg-gradient-to-br from-blue-100 to-purple-100 rounded-lg flex items-center justify-center">
                  <BookOpen className="w-12 h-12 text-blue-600" />
                </div>
                <div className="absolute top-3 right-3 bg-white px-2 py-1 rounded-full text-xs font-medium flex items-center space-x-1">
                  <Star className="w-3 h-3 text-yellow-500 fill-current" />
                  <span>{course.rating}</span>
                </div>
              </div>

              <div className="flex-1 flex flex-col">
                <div className="mb-3">
                  <div className="flex items-center justify-between mb-2">
                    <span className="bg-blue-100 text-blue-800 text-xs font-medium px-2 py-1 rounded">
                      {course.category}
                    </span>
                    <span className="text-xs text-gray-500">{course.mode}</span>
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    {course.title}
                  </h3>
                  <p className="text-sm text-gray-600 mb-3">
                    {course.description}
                  </p>
                </div>

                <div className="mb-4">
                  <div className="flex flex-wrap gap-1">
                    {course.skills.slice(0, 3).map((skill, i) => (
                      <span key={i} className="bg-gray-100 text-gray-700 text-xs px-2 py-1 rounded">
                        {skill}
                      </span>
                    ))}
                    {course.skills.length > 3 && (
                      <span className="text-xs text-gray-500">
                        +{course.skills.length - 3} more
                      </span>
                    )}
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4 mb-4 text-sm">
                  <div className="flex items-center space-x-1">
                    <Clock className="w-4 h-4 text-gray-400" />
                    <span className="text-gray-600">{course.duration}</span>
                  </div>
                  <div className="flex items-center space-x-1">
                    <Users className="w-4 h-4 text-gray-400" />
                    <span className="text-gray-600">{course.students} students</span>
                  </div>
                  <div className="flex items-center space-x-1">
                    <MapPin className="w-4 h-4 text-gray-400" />
                    <span className="text-gray-600">{course.colleges} colleges</span>
                  </div>
                  <div className="flex items-center space-x-1">
                    <TrendingUp className="w-4 h-4 text-gray-400" />
                    <span className="text-gray-600">{course.placement}</span>
                  </div>
                </div>

                <div className="flex items-center justify-end pt-4 border-t border-gray-200 mt-auto">
                  <Link to={`/courses/${course.id}`}>
                    <Button size="sm">
                      View Details
                    </Button>
                  </Link>
                </div>
              </div>
            </Card>
          </motion.div>
        ))}
      </div>

      {filteredCourses.length === 0 && (
        <div className="text-center py-12">
          <BookOpen className="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No courses found</h3>
          <p className="text-gray-600 mb-4">
            Try adjusting your search terms or filters to find more courses.
          </p>
          <Button variant="outline" onClick={() => {
            setSearchTerm('');
            clearFilters();
          }}>
            Clear all filters
          </Button>
        </div>
      )}
    </PageLayout>
  );
};

export default CourseList;
