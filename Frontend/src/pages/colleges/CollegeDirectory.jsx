import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  Search, 
  Filter, 
  MapPin, 
  Star, 
  Users,
  GraduationCap,
  Award,
  Globe,
  Phone,
  Mail,
  ChevronDown,
  X,
  Navigation
} from 'lucide-react';
import PageLayout from '../../components/layout/PageLayout';
import apiService from '../../services/api';
import toast from 'react-hot-toast';
import Card from '../../components/ui/Card';
import Button from '../../components/ui/Button';
import { LoadingCard } from '../../components/ui/Loading';

const CollegeDirectory = () => {
  const [colleges, setColleges] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedFilters, setSelectedFilters] = useState({
    type: '',
    location: '',
    ranking: '',
    fees: ''
  });
  const [showFilters, setShowFilters] = useState(false);

  const mockColleges = [
    {
      id: 1,
      name: 'Indian Institute of Technology Delhi',
      shortName: 'IIT Delhi',
      type: 'Government',
      location: 'New Delhi',
      state: 'Delhi',
      established: 1961,
      rating: 4.9,
      ranking: 2,
      students: 8500,
      faculty: 650,
      courses: ['B.Tech', 'M.Tech', 'PhD', 'MBA'],
      specializations: ['Computer Science', 'Electrical', 'Mechanical', 'Civil'],
      fees: '₹2,50,000',
      placement: '98%',
      averagePackage: '₹18,00,000',
      topRecruiters: ['Google', 'Microsoft', 'Amazon', 'Goldman Sachs'],
      facilities: ['Library', 'Hostel', 'Sports Complex', 'Research Labs'],
      website: 'https://www.iitd.ac.in',
      phone: '+91-11-2659-1000',
      email: 'info@iitd.ac.in',
      image: '/api/placeholder/400/250',
      accreditation: 'NAAC A++',
      distance: '5.2 km'
    },
    {
      id: 2,
      name: 'Delhi University',
      shortName: 'DU',
      type: 'Government',
      location: 'New Delhi',
      state: 'Delhi',
      established: 1922,
      rating: 4.6,
      ranking: 12,
      students: 132000,
      faculty: 1800,
      courses: ['B.A', 'B.Sc', 'B.Com', 'M.A', 'M.Sc', 'PhD'],
      specializations: ['Arts', 'Science', 'Commerce', 'Law'],
      fees: '₹15,000',
      placement: '85%',
      averagePackage: '₹6,50,000',
      topRecruiters: ['TCS', 'Infosys', 'Wipro', 'Deloitte'],
      facilities: ['Central Library', 'Sports Facilities', 'Cultural Centers'],
      website: 'https://www.du.ac.in',
      phone: '+91-11-2766-7049',
      email: 'info@du.ac.in',
      image: '/api/placeholder/400/250',
      accreditation: 'NAAC A+',
      distance: '8.7 km'
    },
    {
      id: 3,
      name: 'Manipal Institute of Technology',
      shortName: 'MIT Manipal',
      type: 'Private',
      location: 'Manipal',
      state: 'Karnataka',
      established: 1957,
      rating: 4.4,
      ranking: 45,
      students: 6500,
      faculty: 420,
      courses: ['B.Tech', 'M.Tech', 'MBA', 'MCA'],
      specializations: ['Computer Science', 'Electronics', 'Information Technology'],
      fees: '₹3,50,000',
      placement: '92%',
      averagePackage: '₹8,50,000',
      topRecruiters: ['Accenture', 'IBM', 'Cognizant', 'Capgemini'],
      facilities: ['Modern Labs', 'Hostel', 'Sports Complex', 'Medical Center'],
      website: 'https://www.manipal.edu',
      phone: '+91-820-292-3000',
      email: 'info@manipal.edu',
      image: '/api/placeholder/400/250',
      accreditation: 'NAAC A',
      distance: '1250 km'
    },
    {
      id: 4,
      name: 'Lovely Professional University',
      shortName: 'LPU',
      type: 'Private',
      location: 'Phagwara',
      state: 'Punjab',
      established: 2005,
      rating: 4.2,
      ranking: 78,
      students: 30000,
      faculty: 2000,
      courses: ['B.Tech', 'BBA', 'B.Sc', 'M.Tech', 'MBA'],
      specializations: ['Engineering', 'Management', 'Design', 'Agriculture'],
      fees: '₹1,80,000',
      placement: '88%',
      averagePackage: '₹5,25,000',
      topRecruiters: ['Amazon', 'Flipkart', 'Paytm', 'Zomato'],
      facilities: ['Campus WiFi', 'Hostels', 'Sports Facilities', 'Food Courts'],
      website: 'https://www.lpu.in',
      phone: '+91-1824-517-000',
      email: 'info@lpu.co.in',
      image: '/api/placeholder/400/250',
      accreditation: 'NAAC A+',
      distance: '350 km'
    },
    {
      id: 5,
      name: 'Symbiosis Institute of Technology',
      shortName: 'SIT Pune',
      type: 'Private',
      location: 'Pune',
      state: 'Maharashtra',
      established: 2008,
      rating: 4.3,
      ranking: 65,
      students: 2800,
      faculty: 180,
      courses: ['B.Tech', 'M.Tech'],
      specializations: ['Computer Science', 'Electronics', 'Civil', 'Mechanical'],
      fees: '₹4,20,000',
      placement: '95%',
      averagePackage: '₹7,80,000',
      topRecruiters: ['Infosys', 'TCS', 'L&T', 'Bajaj Auto'],
      facilities: ['Research Centers', 'Innovation Labs', 'Incubation Center'],
      website: 'https://www.sitpune.edu.in',
      phone: '+91-20-2858-1000',
      email: 'info@sitpune.edu.in',
      image: '/api/placeholder/400/250',
      accreditation: 'NAAC A',
      distance: '1450 km'
    },
    {
      id: 6,
      name: 'Amity University',
      shortName: 'Amity Noida',
      type: 'Private',
      location: 'Noida',
      state: 'Uttar Pradesh',
      established: 2005,
      rating: 4.1,
      ranking: 85,
      students: 15000,
      faculty: 1200,
      courses: ['B.Tech', 'BBA', 'B.Sc', 'MBA', 'M.Tech'],
      specializations: ['Engineering', 'Management', 'Law', 'Journalism'],
      fees: '₹2,80,000',
      placement: '90%',
      averagePackage: '₹6,20,000',
      topRecruiters: ['HCL', 'Tech Mahindra', 'Wipro', 'Genpact'],
      facilities: ['Smart Classrooms', 'Research Labs', 'Sports Complex'],
      website: 'https://www.amity.edu',
      phone: '+91-120-4392-555',
      email: 'info@amity.edu',
      image: '/api/placeholder/400/250',
      accreditation: 'NAAC A+',
      distance: '25 km'
    }
  ];

  const filterOptions = {
    type: ['Government', 'Private', 'Deemed'],
    location: ['Delhi', 'Mumbai', 'Bangalore', 'Chennai', 'Pune', 'Hyderabad'],
    ranking: ['Top 10', 'Top 25', 'Top 50', 'Top 100'],
    fees: ['Under 1L', '1-3L', '3-5L', '5L+']
  };

  useEffect(() => {
    const fetchColleges = async () => {
      try {
        setLoading(true);
        const response = await apiService.getColleges();
        setColleges(response.data || mockColleges);
      } catch (error) {
        console.error('Failed to fetch colleges:', error);
        toast.error('Failed to load colleges. Using sample data.');
        setColleges(mockColleges);
      } finally {
        setLoading(false);
      }
    };

    fetchColleges();
  }, []);

  const filteredColleges = colleges.filter(college => {
    const matchesSearch = college.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         college.location.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         college.courses.some(course => course.toLowerCase().includes(searchTerm.toLowerCase()));
    
    const matchesType = !selectedFilters.type || college.type === selectedFilters.type;
    const matchesLocation = !selectedFilters.location || college.location.includes(selectedFilters.location);
    
    let matchesRanking = true;
    if (selectedFilters.ranking) {
      switch (selectedFilters.ranking) {
        case 'Top 10':
          matchesRanking = college.ranking <= 10;
          break;
        case 'Top 25':
          matchesRanking = college.ranking <= 25;
          break;
        case 'Top 50':
          matchesRanking = college.ranking <= 50;
          break;
        case 'Top 100':
          matchesRanking = college.ranking <= 100;
          break;
      }
    }

    let matchesFees = true;
    if (selectedFilters.fees) {
      const feeAmount = parseInt(college.fees.replace(/[₹,]/g, ''));
      switch (selectedFilters.fees) {
        case 'Under 1L':
          matchesFees = feeAmount < 100000;
          break;
        case '1-3L':
          matchesFees = feeAmount >= 100000 && feeAmount <= 300000;
          break;
        case '3-5L':
          matchesFees = feeAmount > 300000 && feeAmount <= 500000;
          break;
        case '5L+':
          matchesFees = feeAmount > 500000;
          break;
      }
    }

    return matchesSearch && matchesType && matchesLocation && matchesRanking && matchesFees;
  });

  const handleFilterChange = (filterType, value) => {
    setSelectedFilters(prev => ({
      ...prev,
      [filterType]: prev[filterType] === value ? '' : value
    }));
  };

  const clearFilters = () => {
    setSelectedFilters({
      type: '',
      location: '',
      ranking: '',
      fees: ''
    });
  };

  const activeFiltersCount = Object.values(selectedFilters).filter(Boolean).length;

  if (loading) {
    return (
      <PageLayout title="Colleges" subtitle="Find the perfect college for your career">
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
      title="College Directory" 
      subtitle="Discover top colleges and universities across India"
    >
      {/* Search and Filter Bar */}
      <div className="mb-8 space-y-4">
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Search colleges, courses, or locations..."
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
          Showing {filteredColleges.length} of {colleges.length} colleges
          {searchTerm && ` for "${searchTerm}"`}
        </p>
      </div>

      {/* College Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {filteredColleges.map((college, index) => (
          <motion.div
            key={college.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: index * 0.1 }}
          >
            <Card className="h-full">
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <div className="flex items-center space-x-2 mb-2">
                    <h3 className="text-xl font-semibold text-gray-900">{college.name}</h3>
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      college.type === 'Government' ? 'bg-green-100 text-green-800' : 'bg-blue-100 text-blue-800'
                    }`}>
                      {college.type}
                    </span>
                  </div>
                  <div className="flex items-center space-x-4 text-sm text-gray-600 mb-2">
                    <div className="flex items-center space-x-1">
                      <MapPin className="w-4 h-4" />
                      <span>{college.location}, {college.state}</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <Award className="w-4 h-4" />
                      <span>Rank #{college.ranking}</span>
                    </div>
                  </div>
                  <div className="flex items-center space-x-1 mb-3">
                    <Star className="w-4 h-4 text-yellow-500 fill-current" />
                    <span className="font-medium">{college.rating}</span>
                    <span className="text-sm text-gray-500">({college.accreditation})</span>
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4 mb-4 text-sm">
                <div className="flex items-center space-x-2">
                  <Users className="w-4 h-4 text-blue-600" />
                  <div>
                    <p className="text-gray-500">Students</p>
                    <p className="font-semibold">{college.students.toLocaleString()}</p>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <GraduationCap className="w-4 h-4 text-green-600" />
                  <div>
                    <p className="text-gray-500">Placement</p>
                    <p className="font-semibold">{college.placement}</p>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <Navigation className="w-4 h-4 text-purple-600" />
                  <div>
                    <p className="text-gray-500">Distance</p>
                    <p className="font-semibold">{college.distance}</p>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <Award className="w-4 h-4 text-orange-600" />
                  <div>
                    <p className="text-gray-500">Avg Package</p>
                    <p className="font-semibold">{college.averagePackage}</p>
                  </div>
                </div>
              </div>

              <div className="mb-4">
                <p className="text-sm font-medium text-gray-700 mb-2">Popular Courses</p>
                <div className="flex flex-wrap gap-1">
                  {college.courses.slice(0, 4).map((course, i) => (
                    <span key={i} className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded">
                      {course}
                    </span>
                  ))}
                  {college.courses.length > 4 && (
                    <span className="text-xs text-gray-500">
                      +{college.courses.length - 4} more
                    </span>
                  )}
                </div>
              </div>

              <div className="mb-4">
                <p className="text-sm font-medium text-gray-700 mb-2">Top Recruiters</p>
                <div className="flex flex-wrap gap-1">
                  {college.topRecruiters.slice(0, 3).map((recruiter, i) => (
                    <span key={i} className="bg-gray-100 text-gray-700 text-xs px-2 py-1 rounded">
                      {recruiter}
                    </span>
                  ))}
                  {college.topRecruiters.length > 3 && (
                    <span className="text-xs text-gray-500">
                      +{college.topRecruiters.length - 3} more
                    </span>
                  )}
                </div>
              </div>

              <div className="flex items-center justify-between pt-4 border-t border-gray-200">
                <div className="flex items-center space-x-2">
                  <Button 
                    variant="outline" 
                    size="sm" 
                    className="flex items-center space-x-1 bg-yellow-50 border-yellow-300 text-yellow-700 hover:bg-yellow-100"
                    onClick={() => window.open('https://scholarships.gov.in/All-Scholarships#:~:text=Pm%20Usp%20Special%20Scholarship%20Scheme,MNO%20Verification%20%3A%20Opening%20Soon', '_blank')}
                  >
                    <Award className="w-3 h-3" />
                    <span>Scholarships</span>
                  </Button>
                  <Button variant="outline" size="sm" className="flex items-center space-x-1">
                    <Phone className="w-3 h-3" />
                    <span>Contact</span>
                  </Button>
                </div>
                <div>
                  <Link to={`/colleges/${college.id}`}>
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

      {filteredColleges.length === 0 && (
        <div className="text-center py-12">
          <GraduationCap className="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No colleges found</h3>
          <p className="text-gray-600 mb-4">
            Try adjusting your search terms or filters to find more colleges.
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

export default CollegeDirectory;
