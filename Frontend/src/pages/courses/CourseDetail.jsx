import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  ArrowLeft, 
  Clock, 
  Users, 
  Star, 
  BookOpen, 
  Award, 
  Calendar,
  DollarSign,
  Globe,
  Play,
  Download,
  Heart,
  Share2,
  CheckCircle
} from 'lucide-react';
import PageLayout from '../../components/layout/PageLayout';
import Card from '../../components/ui/Card';
import Button from '../../components/ui/Button';
import Badge from '../../components/ui/Badge';
import Loading from '../../components/ui/Loading';

const CourseDetail = () => {
  const { courseId } = useParams();
  const courseIdNum = parseInt(courseId, 10);
  const navigate = useNavigate();
  const [course, setCourse] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');
  const [isEnrolled, setIsEnrolled] = useState(false);
  const [isFavorited, setIsFavorited] = useState(false);

  // Mock course data
  const mockCourse = {
    id: courseId,
    title: 'Full Stack Web Development Bootcamp',
    subtitle: 'Master modern web development with React, Node.js, and MongoDB',
    description: 'This comprehensive bootcamp will take you from beginner to professional web developer. Learn the latest technologies and best practices used by top tech companies.',
    instructor: {
      name: 'Dr. Sarah Johnson',
      title: 'Senior Software Engineer at Google',
      avatar: '/api/placeholder/64/64',
      rating: 4.9,
      students: 15420,
      courses: 12
    },
    rating: 4.8,
    reviewCount: 2847,
    students: 18500,
    duration: '16 weeks',
    level: 'Beginner to Advanced',
    language: 'English',
    price: 15999,
    originalPrice: 24999,
    category: 'Technology',
    tags: ['Web Development', 'React', 'Node.js', 'JavaScript', 'MongoDB'],
    thumbnail: '/api/placeholder/800/400',
    lastUpdated: '2024-01-15',
    certificate: true,
    prerequisites: ['Basic computer skills', 'No programming experience required'],
    learningOutcomes: [
      'Build full-stack web applications from scratch',
      'Master React.js and modern JavaScript (ES6+)',
      'Create RESTful APIs with Node.js and Express',
      'Work with databases using MongoDB',
      'Deploy applications to cloud platforms',
      'Implement authentication and security best practices',
      'Use Git for version control and collaboration',
      'Apply responsive design principles'
    ],
    curriculum: [
      {
        title: 'Introduction to Web Development',
        lessons: 8,
        duration: '2 weeks',
        topics: ['HTML5 & CSS3', 'JavaScript Fundamentals', 'DOM Manipulation', 'Responsive Design']
      },
      {
        title: 'Frontend Development with React',
        lessons: 12,
        duration: '4 weeks',
        topics: ['React Components', 'State Management', 'Hooks', 'React Router', 'Context API']
      },
      {
        title: 'Backend Development with Node.js',
        lessons: 10,
        duration: '3 weeks',
        topics: ['Express.js', 'RESTful APIs', 'Middleware', 'Authentication', 'Error Handling']
      },
      {
        title: 'Database Design & MongoDB',
        lessons: 8,
        duration: '2 weeks',
        topics: ['Database Design', 'MongoDB', 'Mongoose', 'Data Modeling', 'Aggregation']
      },
      {
        title: 'Full Stack Integration',
        lessons: 15,
        duration: '4 weeks',
        topics: ['API Integration', 'State Management', 'Testing', 'Performance Optimization']
      },
      {
        title: 'Deployment & DevOps',
        lessons: 6,
        duration: '1 week',
        topics: ['Cloud Deployment', 'CI/CD', 'Docker', 'Monitoring', 'Security']
      }
    ],
    features: [
      'Lifetime access to course materials',
      '24/7 community support',
      'Live coding sessions',
      'Real-world projects',
      'Career guidance and mentorship',
      'Job placement assistance'
    ],
    reviews: [
      {
        id: 1,
        user: 'Alex Chen',
        avatar: '/api/placeholder/40/40',
        rating: 5,
        date: '2024-01-10',
        comment: 'Excellent course! The instructor explains complex concepts very clearly. I landed my first developer job after completing this course.'
      },
      {
        id: 2,
        user: 'Maria Rodriguez',
        avatar: '/api/placeholder/40/40',
        rating: 5,
        date: '2024-01-08',
        comment: 'Best investment I\'ve made in my career. The projects are challenging and the support is amazing.'
      },
      {
        id: 3,
        user: 'David Kim',
        avatar: '/api/placeholder/40/40',
        rating: 4,
        date: '2024-01-05',
        comment: 'Great content and well-structured curriculum. Would recommend to anyone starting in web development.'
      }
    ]
  };

  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      setCourse(mockCourse);
      setLoading(false);
    }, 1000);
  }, [courseId]);

  const handleEnroll = () => {
    setIsEnrolled(true);
    // Handle enrollment logic
  };

  const handleFavorite = () => {
    setIsFavorited(!isFavorited);
    // Handle favorite logic
  };

  const handleShare = () => {
    navigator.share?.({
      title: course.title,
      text: course.subtitle,
      url: window.location.href,
    });
  };

  if (loading) {
    return (
      <PageLayout title="Course Details" subtitle="Loading course information...">
        <div className="max-w-6xl mx-auto">
          <Loading.Skeleton className="h-64 mb-6" />
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2 space-y-4">
              <Loading.Skeleton className="h-8" />
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

  if (!course) {
    return (
      <PageLayout title="Course Not Found" subtitle="The requested course could not be found">
        <div className="text-center py-12">
          <Button onClick={() => navigate('/courses')} className="flex items-center space-x-2">
            <ArrowLeft className="w-4 h-4" />
            <span>Back to Courses</span>
          </Button>
        </div>
      </PageLayout>
    );
  }

  const tabs = [
    { id: 'overview', label: 'Overview' },
    { id: 'curriculum', label: 'Curriculum' },
    { id: 'instructor', label: 'Instructor' },
    { id: 'reviews', label: 'Reviews' }
  ];

  return (
    <PageLayout title={course.title} subtitle={course.subtitle}>
      <div className="max-w-6xl mx-auto">
        {/* Back Button */}
        <Button 
          variant="outline" 
          onClick={() => navigate('/courses')}
          className="mb-6 flex items-center space-x-2"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Courses</span>
        </Button>

        {/* Course Header */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
          <div className="lg:col-span-2">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="relative rounded-xl overflow-hidden mb-6"
            >
              <img 
                src={course.thumbnail} 
                alt={course.title}
                className="w-full h-64 object-cover"
              />
              <div className="absolute inset-0 bg-black bg-opacity-40 flex items-center justify-center">
                <Button size="lg" className="flex items-center space-x-2">
                  <Play className="w-5 h-5" />
                  <span>Preview Course</span>
                </Button>
              </div>
            </motion.div>

            <div className="flex flex-wrap gap-2 mb-4">
              {course.tags.map((tag, index) => (
                <Badge key={index} variant="primary">{tag}</Badge>
              ))}
            </div>

            <div className="flex items-center space-x-6 text-sm text-gray-600 mb-6">
              <div className="flex items-center space-x-1">
                <Star className="w-4 h-4 text-yellow-500 fill-current" />
                <span className="font-medium">{course.rating}</span>
                <span>({course.reviewCount} reviews)</span>
              </div>
              <div className="flex items-center space-x-1">
                <Users className="w-4 h-4" />
                <span>{course.students.toLocaleString()} students</span>
              </div>
              <div className="flex items-center space-x-1">
                <Clock className="w-4 h-4" />
                <span>{course.duration}</span>
              </div>
            </div>
          </div>

          {/* Enrollment Card */}
          <div className="lg:col-span-1">
            <Card className="sticky top-6">
              <div className="p-6">
                <div className="text-center mb-6">
                  <div className="flex items-center justify-center space-x-2 mb-2">
                    <span className="text-3xl font-bold text-gray-900">₹{course.price.toLocaleString()}</span>
                    <span className="text-lg text-gray-500 line-through">₹{course.originalPrice.toLocaleString()}</span>
                  </div>
                  <Badge variant="success" className="text-sm">
                    {Math.round((1 - course.price / course.originalPrice) * 100)}% OFF
                  </Badge>
                </div>

                <div className="space-y-4 mb-6">
                  <Button 
                    onClick={handleEnroll}
                    disabled={isEnrolled}
                    className="w-full"
                    size="lg"
                  >
                    {isEnrolled ? 'Enrolled' : 'Enroll Now'}
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
                  <div className="flex items-center space-x-2">
                    <CheckCircle className="w-4 h-4 text-green-600" />
                    <span>Lifetime access</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <CheckCircle className="w-4 h-4 text-green-600" />
                    <span>Certificate of completion</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <CheckCircle className="w-4 h-4 text-green-600" />
                    <span>30-day money-back guarantee</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <CheckCircle className="w-4 h-4 text-green-600" />
                    <span>Mobile and desktop access</span>
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
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              <div className="lg:col-span-2 space-y-8">
                <Card>
                  <Card.Header>
                    <Card.Title>About This Course</Card.Title>
                  </Card.Header>
                  <p className="text-gray-700 leading-relaxed">{course.description}</p>
                </Card>

                <Card>
                  <Card.Header>
                    <Card.Title>What You'll Learn</Card.Title>
                  </Card.Header>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {course.learningOutcomes.map((outcome, index) => (
                      <div key={index} className="flex items-start space-x-2">
                        <CheckCircle className="w-5 h-5 text-green-600 mt-0.5 flex-shrink-0" />
                        <span className="text-gray-700">{outcome}</span>
                      </div>
                    ))}
                  </div>
                </Card>

                <Card>
                  <Card.Header>
                    <Card.Title>Prerequisites</Card.Title>
                  </Card.Header>
                  <ul className="space-y-2">
                    {course.prerequisites.map((prereq, index) => (
                      <li key={index} className="flex items-center space-x-2">
                        <div className="w-2 h-2 bg-blue-600 rounded-full"></div>
                        <span className="text-gray-700">{prereq}</span>
                      </li>
                    ))}
                  </ul>
                </Card>
              </div>

              <div className="space-y-6">
                <Card>
                  <Card.Header>
                    <Card.Title>Course Features</Card.Title>
                  </Card.Header>
                  <div className="space-y-3">
                    {course.features.map((feature, index) => (
                      <div key={index} className="flex items-center space-x-2">
                        <CheckCircle className="w-4 h-4 text-green-600" />
                        <span className="text-sm text-gray-700">{feature}</span>
                      </div>
                    ))}
                  </div>
                </Card>

                <Card>
                  <Card.Header>
                    <Card.Title>Course Info</Card.Title>
                  </Card.Header>
                  <div className="space-y-3 text-sm">
                    <div className="flex justify-between">
                      <span className="text-gray-600">Level:</span>
                      <span className="font-medium">{course.level}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Duration:</span>
                      <span className="font-medium">{course.duration}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Language:</span>
                      <span className="font-medium">{course.language}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Certificate:</span>
                      <span className="font-medium">{course.certificate ? 'Yes' : 'No'}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Last Updated:</span>
                      <span className="font-medium">{new Date(course.lastUpdated).toLocaleDateString()}</span>
                    </div>
                  </div>
                </Card>
              </div>
            </div>
          )}

          {activeTab === 'curriculum' && (
            <div className="space-y-4">
              {course.curriculum.map((section, index) => (
                <Card key={index}>
                  <Card.Header>
                    <div className="flex items-center justify-between">
                      <Card.Title>{section.title}</Card.Title>
                      <div className="flex items-center space-x-4 text-sm text-gray-600">
                        <span>{section.lessons} lessons</span>
                        <span>{section.duration}</span>
                      </div>
                    </div>
                  </Card.Header>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
                    {section.topics.map((topic, topicIndex) => (
                      <Badge key={topicIndex} variant="secondary" className="text-xs">
                        {topic}
                      </Badge>
                    ))}
                  </div>
                </Card>
              ))}
            </div>
          )}

          {activeTab === 'instructor' && (
            <Card>
              <div className="flex items-start space-x-6">
                <img 
                  src={course.instructor.avatar} 
                  alt={course.instructor.name}
                  className="w-24 h-24 rounded-full"
                />
                <div className="flex-1">
                  <h3 className="text-xl font-bold text-gray-900 mb-1">{course.instructor.name}</h3>
                  <p className="text-gray-600 mb-4">{course.instructor.title}</p>
                  
                  <div className="grid grid-cols-3 gap-4 mb-6">
                    <div className="text-center">
                      <div className="text-2xl font-bold text-gray-900">{course.instructor.rating}</div>
                      <div className="text-sm text-gray-600">Instructor Rating</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-bold text-gray-900">{course.instructor.students.toLocaleString()}</div>
                      <div className="text-sm text-gray-600">Students</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-bold text-gray-900">{course.instructor.courses}</div>
                      <div className="text-sm text-gray-600">Courses</div>
                    </div>
                  </div>
                </div>
              </div>
            </Card>
          )}

          {activeTab === 'reviews' && (
            <div className="space-y-6">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-semibold">Student Reviews</h3>
                <div className="flex items-center space-x-2">
                  <Star className="w-5 h-5 text-yellow-500 fill-current" />
                  <span className="font-medium">{course.rating}</span>
                  <span className="text-gray-600">({course.reviewCount} reviews)</span>
                </div>
              </div>

              <div className="space-y-4">
                {course.reviews.map((review) => (
                  <Card key={review.id}>
                    <div className="flex items-start space-x-4">
                      <img 
                        src={review.avatar} 
                        alt={review.user}
                        className="w-10 h-10 rounded-full"
                      />
                      <div className="flex-1">
                        <div className="flex items-center justify-between mb-2">
                          <h4 className="font-medium text-gray-900">{review.user}</h4>
                          <span className="text-sm text-gray-500">{new Date(review.date).toLocaleDateString()}</span>
                        </div>
                        <div className="flex items-center space-x-1 mb-2">
                          {[...Array(5)].map((_, i) => (
                            <Star 
                              key={i} 
                              className={`w-4 h-4 ${
                                i < review.rating ? 'text-yellow-500 fill-current' : 'text-gray-300'
                              }`} 
                            />
                          ))}
                        </div>
                        <p className="text-gray-700">{review.comment}</p>
                      </div>
                    </div>
                  </Card>
                ))}
              </div>
            </div>
          )}
        </motion.div>
      </div>
    </PageLayout>
  );
};

export default CourseDetail;
