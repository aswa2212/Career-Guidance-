import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  Search, 
  Filter, 
  Briefcase, 
  TrendingUp, 
  DollarSign, 
  MapPin,
  Users,
  Clock,
  Star,
  ChevronDown,
  X,
  BarChart3
} from 'lucide-react';
import PageLayout from '../../components/layout/PageLayout';
import apiService from '../../services/api';
import toast from 'react-hot-toast';
import Card from '../../components/ui/Card';
import Button from '../../components/ui/Button';
import { LoadingCard } from '../../components/ui/Loading';

const CareerExplorer = () => {
  const [careers, setCareers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedFilters, setSelectedFilters] = useState({
    industry: '',
    experience: '',
    salary: '',
    growth: ''
  });
  const [showFilters, setShowFilters] = useState(false);

  const mockCareers = [
    {
      id: 1,
      title: 'Software Engineer',
      industry: 'Technology',
      description: 'Design, develop, and maintain software applications and systems',
      averageSalary: '₹8,50,000',
      salaryRange: '₹5,00,000 - ₹15,00,000',
      experience: 'Entry Level',
      growth: 'High',
      demand: 'Very High',
      skills: ['JavaScript', 'Python', 'React', 'Node.js', 'SQL'],
      education: 'Bachelor\'s in Computer Science or related field',
      jobOpenings: 12500,
      companies: ['Google', 'Microsoft', 'Amazon', 'Flipkart', 'Zomato'],
      workEnvironment: 'Office/Remote',
      rating: 4.6
    },
    {
      id: 2,
      title: 'Data Scientist',
      industry: 'Technology',
      description: 'Analyze complex data to help organizations make informed decisions',
      averageSalary: '₹12,00,000',
      salaryRange: '₹7,00,000 - ₹25,00,000',
      experience: 'Mid Level',
      growth: 'Very High',
      demand: 'High',
      skills: ['Python', 'Machine Learning', 'Statistics', 'SQL', 'Tableau'],
      education: 'Master\'s in Data Science, Statistics, or related field',
      jobOpenings: 8500,
      companies: ['Netflix', 'Uber', 'Swiggy', 'PayTM', 'BYJU\'S'],
      workEnvironment: 'Office/Hybrid',
      rating: 4.8
    },
    {
      id: 3,
      title: 'Digital Marketing Manager',
      industry: 'Marketing',
      description: 'Plan and execute digital marketing campaigns across various channels',
      averageSalary: '₹6,50,000',
      salaryRange: '₹4,00,000 - ₹12,00,000',
      experience: 'Mid Level',
      growth: 'High',
      demand: 'High',
      skills: ['SEO', 'Google Ads', 'Social Media', 'Analytics', 'Content Strategy'],
      education: 'Bachelor\'s in Marketing, Business, or related field',
      jobOpenings: 9200,
      companies: ['Unilever', 'P&G', 'Ogilvy', 'Dentsu', 'WPP'],
      workEnvironment: 'Office',
      rating: 4.4
    },
    {
      id: 4,
      title: 'Product Manager',
      industry: 'Technology',
      description: 'Lead product development from conception to launch and beyond',
      averageSalary: '₹15,00,000',
      salaryRange: '₹10,00,000 - ₹30,00,000',
      experience: 'Senior Level',
      growth: 'Very High',
      demand: 'High',
      skills: ['Product Strategy', 'User Research', 'Analytics', 'Agile', 'Leadership'],
      education: 'Bachelor\'s/Master\'s in Business, Engineering, or related field',
      jobOpenings: 4500,
      companies: ['Facebook', 'Google', 'Amazon', 'Flipkart', 'PhonePe'],
      workEnvironment: 'Office/Hybrid',
      rating: 4.7
    },
    {
      id: 5,
      title: 'Financial Analyst',
      industry: 'Finance',
      description: 'Analyze financial data and trends to guide investment decisions',
      averageSalary: '₹7,00,000',
      salaryRange: '₹4,50,000 - ₹15,00,000',
      experience: 'Entry Level',
      growth: 'Medium',
      demand: 'Medium',
      skills: ['Excel', 'Financial Modeling', 'SQL', 'Python', 'Bloomberg'],
      education: 'Bachelor\'s in Finance, Economics, or related field',
      jobOpenings: 6800,
      companies: ['Goldman Sachs', 'JP Morgan', 'HDFC Bank', 'ICICI Bank', 'Kotak'],
      workEnvironment: 'Office',
      rating: 4.3
    },
    {
      id: 6,
      title: 'UX Designer',
      industry: 'Design',
      description: 'Create intuitive and engaging user experiences for digital products',
      averageSalary: '₹9,00,000',
      salaryRange: '₹5,50,000 - ₹18,00,000',
      experience: 'Mid Level',
      growth: 'High',
      demand: 'High',
      skills: ['Figma', 'User Research', 'Prototyping', 'Wireframing', 'Design Systems'],
      education: 'Bachelor\'s in Design, HCI, or related field',
      jobOpenings: 5200,
      companies: ['Adobe', 'Airbnb', 'Spotify', 'Razorpay', 'Cred'],
      workEnvironment: 'Office/Remote',
      rating: 4.5
    }
  ];

  const filterOptions = {
    industry: ['Technology', 'Finance', 'Healthcare', 'Marketing', 'Design', 'Consulting'],
    experience: ['Entry Level', 'Mid Level', 'Senior Level', 'Executive'],
    salary: ['0-5L', '5-10L', '10-15L', '15-25L', '25L+'],
    growth: ['Low', 'Medium', 'High', 'Very High']
  };

  useEffect(() => {
    const fetchCareers = async () => {
      try {
        setLoading(true);
        const response = await apiService.getCareers();
        setCareers(response.data || mockCareers);
      } catch (error) {
        console.error('Failed to fetch careers:', error);
        toast.error('Failed to load careers. Using sample data.');
        setCareers(mockCareers);
      } finally {
        setLoading(false);
      }
    };

    fetchCareers();
  }, []);

  const filteredCareers = careers.filter(career => {
    const matchesSearch = career.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         career.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         career.skills.some(skill => skill.toLowerCase().includes(searchTerm.toLowerCase()));
    
    const matchesIndustry = !selectedFilters.industry || career.industry === selectedFilters.industry;
    const matchesExperience = !selectedFilters.experience || career.experience === selectedFilters.experience;
    const matchesGrowth = !selectedFilters.growth || career.growth === selectedFilters.growth;
    
    let matchesSalary = true;
    if (selectedFilters.salary) {
      const salaryNum = parseInt(career.averageSalary.replace(/[₹,]/g, ''));
      switch (selectedFilters.salary) {
        case '0-5L':
          matchesSalary = salaryNum <= 500000;
          break;
        case '5-10L':
          matchesSalary = salaryNum > 500000 && salaryNum <= 1000000;
          break;
        case '10-15L':
          matchesSalary = salaryNum > 1000000 && salaryNum <= 1500000;
          break;
        case '15-25L':
          matchesSalary = salaryNum > 1500000 && salaryNum <= 2500000;
          break;
        case '25L+':
          matchesSalary = salaryNum > 2500000;
          break;
      }
    }

    return matchesSearch && matchesIndustry && matchesExperience && matchesGrowth && matchesSalary;
  });

  const handleFilterChange = (filterType, value) => {
    setSelectedFilters(prev => ({
      ...prev,
      [filterType]: prev[filterType] === value ? '' : value
    }));
  };

  const clearFilters = () => {
    setSelectedFilters({
      industry: '',
      experience: '',
      salary: '',
      growth: ''
    });
  };

  const activeFiltersCount = Object.values(selectedFilters).filter(Boolean).length;

  const getDemandColor = (demand) => {
    const colors = {
      'Low': 'bg-red-100 text-red-800',
      'Medium': 'bg-yellow-100 text-yellow-800',
      'High': 'bg-green-100 text-green-800',
      'Very High': 'bg-blue-100 text-blue-800'
    };
    return colors[demand] || colors.Medium;
  };

  const getGrowthColor = (growth) => {
    const colors = {
      'Low': 'text-red-600',
      'Medium': 'text-yellow-600',
      'High': 'text-green-600',
      'Very High': 'text-blue-600'
    };
    return colors[growth] || colors.Medium;
  };

  if (loading) {
    return (
      <PageLayout title="Careers" subtitle="Explore career opportunities">
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
      title="Career Explorer" 
      subtitle="Discover career paths that match your skills and interests"
    >
      {/* Search and Filter Bar */}
      <div className="mb-8 space-y-4">
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Search careers, skills, or companies..."
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
                    {filterType === 'salary' ? 'Salary Range' : filterType}
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
          Showing {filteredCareers.length} of {careers.length} careers
          {searchTerm && ` for "${searchTerm}"`}
        </p>
      </div>

      {/* Career Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {filteredCareers.map((career, index) => (
          <motion.div
            key={career.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: index * 0.1 }}
          >
            <Card className="h-full">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center space-x-3">
                  <div className="w-12 h-12 bg-gradient-to-br from-blue-100 to-purple-100 rounded-lg flex items-center justify-center">
                    <Briefcase className="w-6 h-6 text-blue-600" />
                  </div>
                  <div>
                    <h3 className="text-xl font-semibold text-gray-900">{career.title}</h3>
                    <p className="text-sm text-gray-600">{career.industry}</p>
                  </div>
                </div>
                <div className="flex items-center space-x-1">
                  <Star className="w-4 h-4 text-yellow-500 fill-current" />
                  <span className="text-sm font-medium">{career.rating}</span>
                </div>
              </div>

              <p className="text-gray-600 mb-4">{career.description}</p>

              <div className="grid grid-cols-2 gap-4 mb-4">
                <div className="flex items-center space-x-2">
                  <DollarSign className="w-4 h-4 text-green-600" />
                  <div>
                    <p className="text-sm text-gray-500">Average Salary</p>
                    <p className="font-semibold text-gray-900">{career.averageSalary}</p>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <TrendingUp className={`w-4 h-4 ${getGrowthColor(career.growth)}`} />
                  <div>
                    <p className="text-sm text-gray-500">Growth</p>
                    <p className="font-semibold text-gray-900">{career.growth}</p>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <Users className="w-4 h-4 text-blue-600" />
                  <div>
                    <p className="text-sm text-gray-500">Job Openings</p>
                    <p className="font-semibold text-gray-900">{career.jobOpenings.toLocaleString()}</p>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <Clock className="w-4 h-4 text-purple-600" />
                  <div>
                    <p className="text-sm text-gray-500">Experience</p>
                    <p className="font-semibold text-gray-900">{career.experience}</p>
                  </div>
                </div>
              </div>

              <div className="mb-4">
                <div className="flex items-center justify-between mb-2">
                  <p className="text-sm font-medium text-gray-700">Market Demand</p>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${getDemandColor(career.demand)}`}>
                    {career.demand}
                  </span>
                </div>
              </div>

              <div className="mb-4">
                <p className="text-sm font-medium text-gray-700 mb-2">Key Skills</p>
                <div className="flex flex-wrap gap-1">
                  {career.skills.slice(0, 4).map((skill, i) => (
                    <span key={i} className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded">
                      {skill}
                    </span>
                  ))}
                  {career.skills.length > 4 && (
                    <span className="text-xs text-gray-500">
                      +{career.skills.length - 4} more
                    </span>
                  )}
                </div>
              </div>

              <div className="mb-4">
                <p className="text-sm font-medium text-gray-700 mb-2">Top Companies</p>
                <div className="flex flex-wrap gap-1">
                  {career.companies.slice(0, 3).map((company, i) => (
                    <span key={i} className="bg-gray-100 text-gray-700 text-xs px-2 py-1 rounded">
                      {company}
                    </span>
                  ))}
                  {career.companies.length > 3 && (
                    <span className="text-xs text-gray-500">
                      +{career.companies.length - 3} more
                    </span>
                  )}
                </div>
              </div>

              <div className="flex items-center justify-between pt-4 border-t border-gray-200">
                <div className="text-sm text-gray-600">
                  <MapPin className="w-4 h-4 inline mr-1" />
                  {career.workEnvironment}
                </div>
                <Link to={`/careers/${career.id}`}>
                  <Button size="sm" className="flex items-center space-x-1">
                    <span>View Details</span>
                    <BarChart3 className="w-4 h-4" />
                  </Button>
                </Link>
              </div>
            </Card>
          </motion.div>
        ))}
      </div>

      {filteredCareers.length === 0 && (
        <div className="text-center py-12">
          <Briefcase className="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No careers found</h3>
          <p className="text-gray-600 mb-4">
            Try adjusting your search terms or filters to find more career opportunities.
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

export default CareerExplorer;
