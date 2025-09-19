import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  ArrowLeft, 
  TrendingUp, 
  DollarSign, 
  MapPin, 
  Users, 
  Clock,
  BookOpen,
  Award,
  Briefcase,
  GraduationCap,
  Target,
  Star,
  Building,
  Heart,
  Share2,
  ExternalLink
} from 'lucide-react';
import PageLayout from '../../components/layout/PageLayout';
import Card from '../../components/ui/Card';
import Button from '../../components/ui/Button';
import Badge from '../../components/ui/Badge';
import Loading from '../../components/ui/Loading';

const CareerDetail = () => {
  const { careerId } = useParams();
  const careerIdNum = parseInt(careerId, 10);
  const navigate = useNavigate();
  const [career, setCareer] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');
  const [isFavorited, setIsFavorited] = useState(false);

  // Mock career data
  const mockCareer = {
    id: careerId,
    title: 'Full Stack Developer',
    description: 'Full stack developers work on both front-end and back-end portions of applications. They have a broad skill set and understand how web services and applications work at every level.',
    industry: 'Technology',
    category: 'Software Development',
    experience: 'Entry to Senior Level',
    salaryRange: {
      min: 400000,
      max: 2500000,
      currency: 'INR'
    },
    growth: 'High',
    demand: 'Very High',
    locations: ['Bangalore', 'Mumbai', 'Delhi', 'Hyderabad', 'Pune', 'Chennai'],
    workEnvironment: 'Office/Remote/Hybrid',
    education: 'Bachelor\'s in Computer Science or related field',
    skills: {
      technical: [
        'JavaScript', 'Python', 'React', 'Node.js', 'SQL', 'MongoDB',
        'HTML/CSS', 'Git', 'AWS', 'Docker', 'REST APIs', 'GraphQL'
      ],
      soft: [
        'Problem Solving', 'Communication', 'Teamwork', 'Time Management',
        'Adaptability', 'Critical Thinking', 'Attention to Detail'
      ]
    },
    responsibilities: [
      'Develop and maintain web applications using modern frameworks',
      'Design and implement database schemas and APIs',
      'Collaborate with designers and product managers',
      'Write clean, maintainable, and efficient code',
      'Participate in code reviews and testing',
      'Debug and troubleshoot application issues',
      'Stay updated with latest technology trends',
      'Mentor junior developers'
    ],
    careerPath: [
      {
        level: 'Junior Developer',
        experience: '0-2 years',
        salary: '₹4-8 LPA',
        responsibilities: ['Learn frameworks', 'Fix bugs', 'Implement features']
      },
      {
        level: 'Mid-level Developer',
        experience: '2-5 years',
        salary: '₹8-15 LPA',
        responsibilities: ['Lead small projects', 'Mentor juniors', 'Architecture decisions']
      },
      {
        level: 'Senior Developer',
        experience: '5-8 years',
        salary: '₹15-25 LPA',
        responsibilities: ['System design', 'Team leadership', 'Strategic planning']
      },
      {
        level: 'Tech Lead/Architect',
        experience: '8+ years',
        salary: '₹25+ LPA',
        responsibilities: ['Technical strategy', 'Cross-team collaboration', 'Innovation']
      }
    ],
    companies: [
      { name: 'Google', logo: '/api/placeholder/40/40', openings: 45 },
      { name: 'Microsoft', logo: '/api/placeholder/40/40', openings: 32 },
      { name: 'Amazon', logo: '/api/placeholder/40/40', openings: 67 },
      { name: 'Flipkart', logo: '/api/placeholder/40/40', openings: 28 },
      { name: 'Zomato', logo: '/api/placeholder/40/40', openings: 15 },
      { name: 'Paytm', logo: '/api/placeholder/40/40', openings: 22 }
    ],
    relatedCareers: [
      'Frontend Developer',
      'Backend Developer',
      'DevOps Engineer',
      'Software Architect',
      'Product Manager'
    ],
    courses: [
      {
        title: 'Complete Web Development Bootcamp',
        provider: 'TechEd',
        duration: '16 weeks',
        rating: 4.8,
        price: '₹15,999'
      },
      {
        title: 'Advanced React Development',
        provider: 'CodeAcademy',
        duration: '8 weeks',
        rating: 4.7,
        price: '₹8,999'
      },
      {
        title: 'Node.js Backend Development',
        provider: 'DevSkills',
        duration: '12 weeks',
        rating: 4.6,
        price: '₹12,999'
      }
    ],
    dayInLife: [
      { time: '9:00 AM', activity: 'Check emails and plan daily tasks' },
      { time: '9:30 AM', activity: 'Stand-up meeting with team' },
      { time: '10:00 AM', activity: 'Code review and merge pull requests' },
      { time: '11:00 AM', activity: 'Develop new features or fix bugs' },
      { time: '1:00 PM', activity: 'Lunch break' },
      { time: '2:00 PM', activity: 'Collaborate with designers on UI/UX' },
      { time: '3:30 PM', activity: 'Write unit tests and documentation' },
      { time: '4:30 PM', activity: 'Team meeting or client call' },
      { time: '5:30 PM', activity: 'Learning new technologies or tools' }
    ],
    pros: [
      'High demand and job security',
      'Excellent salary potential',
      'Creative and challenging work',
      'Remote work opportunities',
      'Continuous learning and growth',
      'Global career opportunities'
    ],
    cons: [
      'Rapidly changing technology landscape',
      'Can be stressful with tight deadlines',
      'Long hours during project launches',
      'Requires continuous skill updates',
      'High competition for top positions'
    ]
  };

  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      setCareer(mockCareer);
      setLoading(false);
    }, 1000);
  }, [careerId]);

  const handleFavorite = () => {
    setIsFavorited(!isFavorited);
  };

  const handleShare = () => {
    navigator.share?.({
      title: career.title,
      text: career.description,
      url: window.location.href,
    });
  };

  if (loading) {
    return (
      <PageLayout title="Career Details" subtitle="Loading career information...">
        <div className="max-w-6xl mx-auto">
          <Loading.Skeleton className="h-8 mb-6" />
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2 space-y-4">
              <Loading.Skeleton className="h-32" />
              <Loading.Skeleton className="h-48" />
            </div>
            <div className="space-y-4">
              <Loading.Skeleton className="h-64" />
            </div>
          </div>
        </div>
      </PageLayout>
    );
  }

  if (!career) {
    return (
      <PageLayout title="Career Not Found" subtitle="The requested career could not be found">
        <div className="text-center py-12">
          <Button onClick={() => navigate('/careers')} className="flex items-center space-x-2">
            <ArrowLeft className="w-4 h-4" />
            <span>Back to Careers</span>
          </Button>
        </div>
      </PageLayout>
    );
  }

  const tabs = [
    { id: 'overview', label: 'Overview' },
    { id: 'path', label: 'Career Path' },
    { id: 'companies', label: 'Companies' },
    { id: 'courses', label: 'Courses' }
  ];

  return (
    <PageLayout title={career.title} subtitle={`Explore the ${career.title} career path`}>
      <div className="max-w-6xl mx-auto">
        {/* Back Button */}
        <Button 
          variant="outline" 
          onClick={() => navigate('/careers')}
          className="mb-6 flex items-center space-x-2"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Careers</span>
        </Button>

        {/* Career Header */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
          <div className="lg:col-span-2">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="mb-6"
            >
              <div className="flex items-center space-x-3 mb-4">
                <Badge variant="primary">{career.industry}</Badge>
                <Badge variant="secondary">{career.category}</Badge>
              </div>

              <p className="text-gray-700 text-lg leading-relaxed mb-6">
                {career.description}
              </p>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="text-center p-4 bg-blue-50 rounded-lg">
                  <DollarSign className="w-8 h-8 text-blue-600 mx-auto mb-2" />
                  <div className="text-sm text-gray-600">Salary Range</div>
                  <div className="font-semibold text-gray-900">
                    ₹{(career.salaryRange.min / 100000).toFixed(0)}-{(career.salaryRange.max / 100000).toFixed(0)} LPA
                  </div>
                </div>
                <div className="text-center p-4 bg-green-50 rounded-lg">
                  <TrendingUp className="w-8 h-8 text-green-600 mx-auto mb-2" />
                  <div className="text-sm text-gray-600">Growth</div>
                  <div className="font-semibold text-gray-900">{career.growth}</div>
                </div>
                <div className="text-center p-4 bg-purple-50 rounded-lg">
                  <Users className="w-8 h-8 text-purple-600 mx-auto mb-2" />
                  <div className="text-sm text-gray-600">Demand</div>
                  <div className="font-semibold text-gray-900">{career.demand}</div>
                </div>
                <div className="text-center p-4 bg-orange-50 rounded-lg">
                  <MapPin className="w-8 h-8 text-orange-600 mx-auto mb-2" />
                  <div className="text-sm text-gray-600">Locations</div>
                  <div className="font-semibold text-gray-900">{career.locations.length}+ Cities</div>
                </div>
              </div>
            </motion.div>
          </div>

          {/* Action Card */}
          <div className="lg:col-span-1">
            <Card className="sticky top-6">
              <div className="p-6">
                <div className="space-y-4 mb-6">
                  <Button className="w-full" size="lg">
                    <Briefcase className="w-4 h-4 mr-2" />
                    Find Jobs
                  </Button>
                  
                  <div className="flex space-x-2">
                    <Button 
                      variant="outline" 
                      onClick={handleFavorite}
                      className={`flex-1 flex items-center justify-center space-x-2 ${
                        isFavorited ? 'text-red-600 border-red-600' : ''
                      }`}
                    >
                      <Heart className={`w-4 h-4 ${isFavorited ? 'fill-current' : ''}`} />
                      <span>Save</span>
                    </Button>
                    <Button 
                      variant="outline" 
                      onClick={handleShare}
                      className="flex-1 flex items-center justify-center space-x-2"
                    >
                      <Share2 className="w-4 h-4" />
                      <span>Share</span>
                    </Button>
                  </div>
                </div>

                <div className="space-y-3 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Experience:</span>
                    <span className="font-medium">{career.experience}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Education:</span>
                    <span className="font-medium">Bachelor's Degree</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Work Style:</span>
                    <span className="font-medium">{career.workEnvironment}</span>
                  </div>
                </div>
              </div>
            </Card>
          </div>
        </div>

        {/* Tabs */}
        <div className="border-b border-gray-200 mb-8">
          <nav className="flex space-x-8">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </nav>
        </div>

        {/* Tab Content */}
        <motion.div
          key={activeTab}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
        >
          {activeTab === 'overview' && (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <div className="space-y-6">
                <Card>
                  <Card.Header>
                    <Card.Title className="flex items-center space-x-2">
                      <Target className="w-5 h-5" />
                      <span>Key Responsibilities</span>
                    </Card.Title>
                  </Card.Header>
                  <ul className="space-y-2">
                    {career.responsibilities.map((responsibility, index) => (
                      <li key={index} className="flex items-start space-x-2">
                        <div className="w-2 h-2 bg-blue-600 rounded-full mt-2 flex-shrink-0"></div>
                        <span className="text-gray-700">{responsibility}</span>
                      </li>
                    ))}
                  </ul>
                </Card>

                <Card>
                  <Card.Header>
                    <Card.Title className="flex items-center space-x-2">
                      <BookOpen className="w-5 h-5" />
                      <span>Required Skills</span>
                    </Card.Title>
                  </Card.Header>
                  <div className="space-y-4">
                    <div>
                      <h4 className="font-medium text-gray-900 mb-2">Technical Skills</h4>
                      <div className="flex flex-wrap gap-2">
                        {career.skills.technical.map((skill, index) => (
                          <Badge key={index} variant="primary">{skill}</Badge>
                        ))}
                      </div>
                    </div>
                    <div>
                      <h4 className="font-medium text-gray-900 mb-2">Soft Skills</h4>
                      <div className="flex flex-wrap gap-2">
                        {career.skills.soft.map((skill, index) => (
                          <Badge key={index} variant="secondary">{skill}</Badge>
                        ))}
                      </div>
                    </div>
                  </div>
                </Card>
              </div>

              <div className="space-y-6">
                <Card>
                  <Card.Header>
                    <Card.Title>A Day in the Life</Card.Title>
                  </Card.Header>
                  <div className="space-y-3">
                    {career.dayInLife.map((item, index) => (
                      <div key={index} className="flex items-start space-x-3">
                        <div className="bg-blue-100 text-blue-800 text-xs font-medium px-2 py-1 rounded">
                          {item.time}
                        </div>
                        <span className="text-gray-700 text-sm">{item.activity}</span>
                      </div>
                    ))}
                  </div>
                </Card>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <Card>
                    <Card.Header>
                      <Card.Title className="text-green-600">Pros</Card.Title>
                    </Card.Header>
                    <ul className="space-y-2">
                      {career.pros.map((pro, index) => (
                        <li key={index} className="flex items-start space-x-2">
                          <div className="w-2 h-2 bg-green-600 rounded-full mt-2 flex-shrink-0"></div>
                          <span className="text-sm text-gray-700">{pro}</span>
                        </li>
                      ))}
                    </ul>
                  </Card>

                  <Card>
                    <Card.Header>
                      <Card.Title className="text-red-600">Cons</Card.Title>
                    </Card.Header>
                    <ul className="space-y-2">
                      {career.cons.map((con, index) => (
                        <li key={index} className="flex items-start space-x-2">
                          <div className="w-2 h-2 bg-red-600 rounded-full mt-2 flex-shrink-0"></div>
                          <span className="text-sm text-gray-700">{con}</span>
                        </li>
                      ))}
                    </ul>
                  </Card>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'path' && (
            <div className="space-y-6">
              <Card>
                <Card.Header>
                  <Card.Title>Career Progression Path</Card.Title>
                  <Card.Description>
                    Typical career advancement opportunities in this field
                  </Card.Description>
                </Card.Header>
                <div className="space-y-6">
                  {career.careerPath.map((level, index) => (
                    <div key={index} className="relative">
                      {index < career.careerPath.length - 1 && (
                        <div className="absolute left-6 top-12 w-0.5 h-16 bg-gray-300"></div>
                      )}
                      <div className="flex items-start space-x-4">
                        <div className="w-12 h-12 bg-blue-600 text-white rounded-full flex items-center justify-center font-bold">
                          {index + 1}
                        </div>
                        <div className="flex-1">
                          <h3 className="text-lg font-semibold text-gray-900">{level.level}</h3>
                          <div className="flex items-center space-x-4 text-sm text-gray-600 mb-2">
                            <span>{level.experience}</span>
                            <span>•</span>
                            <span className="font-medium text-green-600">{level.salary}</span>
                          </div>
                          <ul className="space-y-1">
                            {level.responsibilities.map((resp, respIndex) => (
                              <li key={respIndex} className="text-gray-700 text-sm">
                                • {resp}
                              </li>
                            ))}
                          </ul>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </Card>

              <Card>
                <Card.Header>
                  <Card.Title>Related Career Paths</Card.Title>
                </Card.Header>
                <div className="flex flex-wrap gap-2">
                  {career.relatedCareers.map((relatedCareer, index) => (
                    <Badge key={index} variant="outline" className="cursor-pointer hover:bg-blue-50">
                      {relatedCareer}
                    </Badge>
                  ))}
                </div>
              </Card>
            </div>
          )}

          {activeTab === 'companies' && (
            <div className="space-y-6">
              <Card>
                <Card.Header>
                  <Card.Title>Top Hiring Companies</Card.Title>
                  <Card.Description>
                    Companies actively hiring for {career.title} positions
                  </Card.Description>
                </Card.Header>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {career.companies.map((company, index) => (
                    <div key={index} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
                      <div className="flex items-center space-x-3 mb-3">
                        <img 
                          src={company.logo} 
                          alt={company.name}
                          className="w-10 h-10 rounded"
                        />
                        <div>
                          <h3 className="font-medium text-gray-900">{company.name}</h3>
                          <p className="text-sm text-gray-600">{company.openings} open positions</p>
                        </div>
                      </div>
                      <Button variant="outline" size="sm" className="w-full">
                        <ExternalLink className="w-4 h-4 mr-2" />
                        View Jobs
                      </Button>
                    </div>
                  ))}
                </div>
              </Card>
            </div>
          )}

          {activeTab === 'courses' && (
            <div className="space-y-6">
              <Card>
                <Card.Header>
                  <Card.Title>Recommended Courses</Card.Title>
                  <Card.Description>
                    Build the skills needed for a successful {career.title} career
                  </Card.Description>
                </Card.Header>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {career.courses.map((course, index) => (
                    <div key={index} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
                      <h3 className="font-medium text-gray-900 mb-2">{course.title}</h3>
                      <p className="text-sm text-gray-600 mb-3">by {course.provider}</p>
                      
                      <div className="flex items-center justify-between text-sm mb-3">
                        <div className="flex items-center space-x-1">
                          <Clock className="w-4 h-4 text-gray-400" />
                          <span>{course.duration}</span>
                        </div>
                        <div className="flex items-center space-x-1">
                          <Star className="w-4 h-4 text-yellow-500 fill-current" />
                          <span>{course.rating}</span>
                        </div>
                      </div>
                      
                      <div className="flex items-center justify-between">
                        <span className="font-semibold text-gray-900">{course.price}</span>
                        <Button size="sm">
                          View Course
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              </Card>
            </div>
          )}
        </motion.div>
      </div>
    </PageLayout>
  );
};

export default CareerDetail;
