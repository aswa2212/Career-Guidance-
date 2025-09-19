import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  ArrowLeft, 
  MapPin, 
  Users, 
  Star, 
  Award, 
  Calendar,
  DollarSign,
  Globe,
  Phone,
  Mail,
  ExternalLink,
  Heart,
  Share2,
  BookOpen,
  Building,
  GraduationCap,
  TrendingUp,
  CheckCircle,
  Camera
} from 'lucide-react';
import PageLayout from '../../components/layout/PageLayout';
import Card from '../../components/ui/Card';
import Button from '../../components/ui/Button';
import Badge from '../../components/ui/Badge';
import Loading from '../../components/ui/Loading';

const CollegeDetail = () => {
  const { collegeId } = useParams();
  const collegeIdNum = parseInt(collegeId, 10);
  const navigate = useNavigate();
  const [college, setCollege] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');
  const [isFavorited, setIsFavorited] = useState(false);

  // Mock college data
  const mockCollege = {
    id: collegeId,
    name: 'Indian Institute of Technology Delhi',
    shortName: 'IIT Delhi',
    type: 'Public',
    established: 1961,
    location: {
      city: 'New Delhi',
      state: 'Delhi',
      country: 'India',
      address: 'Hauz Khas, New Delhi, Delhi 110016'
    },
    ranking: {
      nirf: 2,
      qs: 185,
      times: 401
    },
    accreditation: ['NAAC A++', 'NBA', 'AICTE'],
    website: 'https://www.iitd.ac.in',
    phone: '+91-11-2659-1000',
    email: 'info@admin.iitd.ac.in',
    description: 'Indian Institute of Technology Delhi is one of the premier engineering institutions in India. Established in 1961, IIT Delhi has been a leader in engineering education and research.',
    scholarship_details: 'Merit-based scholarships up to 100% tuition fee waiver for economically disadvantaged students. Institute Merit Scholarships for top 25% students. Research assistantships available for M.Tech and PhD programs. Special scholarships for SC/ST/OBC students as per government norms. Industry-sponsored scholarships from companies like TCS, Infosys, and Wipro.',
    images: ['/api/placeholder/800/400'],
    stats: {
      students: 11000,
      faculty: 650,
      campusSize: '325 acres',
      placementRate: 95,
      averagePackage: 1800000,
      highestPackage: 8500000
    },
    courses: [
      {
        name: 'B.Tech Computer Science',
        duration: '4 years',
        fees: 250000,
        seats: 120,
        cutoff: 'JEE Advanced Rank 1-150'
      },
      {
        name: 'B.Tech Electrical Engineering',
        duration: '4 years',
        fees: 250000,
        seats: 100,
        cutoff: 'JEE Advanced Rank 1-200'
      }
    ],
    facilities: [
      'Central Library with 400,000+ books',
      'High-speed Wi-Fi campus',
      'Modern laboratories and research centers',
      'Sports complex with swimming pool',
      'Multiple hostels for boys and girls',
      'Medical center with 24/7 services'
    ],
    placements: {
      companies: [
        { name: 'Google', package: 8500000, selected: 15 },
        { name: 'Microsoft', package: 7200000, selected: 12 },
        { name: 'Amazon', package: 6800000, selected: 18 }
      ]
    },
    reviews: [
      {
        id: 1,
        user: 'Rahul Sharma',
        course: 'B.Tech CSE',
        year: '2023',
        rating: 5,
        comment: 'Excellent faculty and research opportunities. The campus life is amazing and placements are top-notch.'
      }
    ]
  };

  useEffect(() => {
    setTimeout(() => {
      setCollege(mockCollege);
      setLoading(false);
    }, 1000);
  }, [collegeId]);

  const handleFavorite = () => {
    setIsFavorited(!isFavorited);
  };

  const handleShare = () => {
    navigator.share?.({
      title: college.name,
      text: college.description,
      url: window.location.href,
    });
  };

  if (loading) {
    return (
      <PageLayout title="College Details" subtitle="Loading college information...">
        <div className="max-w-6xl mx-auto">
          <Loading.Skeleton className="h-64 mb-6" />
        </div>
      </PageLayout>
    );
  }

  if (!college) {
    return (
      <PageLayout title="College Not Found" subtitle="The requested college could not be found">
        <div className="text-center py-12">
          <Button onClick={() => navigate('/colleges')} className="flex items-center space-x-2">
            <ArrowLeft className="w-4 h-4" />
            <span>Back to Colleges</span>
          </Button>
        </div>
      </PageLayout>
    );
  }

  const tabs = [
    { id: 'overview', label: 'Overview' },
    { id: 'courses', label: 'Courses' },
    { id: 'scholarships', label: 'Scholarships' },
    { id: 'placements', label: 'Placements' },
    { id: 'reviews', label: 'Reviews' }
  ];

  return (
    <PageLayout title={college.name} subtitle={`${college.type} University • Established ${college.established}`}>
      <div className="max-w-6xl mx-auto">
        <Button 
          variant="outline" 
          onClick={() => navigate('/colleges')}
          className="mb-6 flex items-center space-x-2"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Colleges</span>
        </Button>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
          <div className="lg:col-span-2">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="relative rounded-xl overflow-hidden mb-6"
            >
              <img 
                src={college.images[0]} 
                alt={college.name}
                className="w-full h-64 object-cover"
              />
              <div className="absolute top-4 right-4">
                <Button size="sm" variant="outline" className="bg-white/90 backdrop-blur-sm">
                  <Camera className="w-4 h-4 mr-2" />
                  View Gallery
                </Button>
              </div>
            </motion.div>

            <div className="flex flex-wrap gap-2 mb-4">
              {college.accreditation.map((acc, index) => (
                <Badge key={index} variant="success">{acc}</Badge>
              ))}
            </div>

            <div className="flex items-center space-x-6 text-sm text-gray-600 mb-6">
              <div className="flex items-center space-x-1">
                <MapPin className="w-4 h-4" />
                <span>{college.location.city}, {college.location.state}</span>
              </div>
              <div className="flex items-center space-x-1">
                <Award className="w-4 h-4" />
                <span>NIRF Rank #{college.ranking.nirf}</span>
              </div>
              <div className="flex items-center space-x-1">
                <Users className="w-4 h-4" />
                <span>{college.stats.students.toLocaleString()} students</span>
              </div>
            </div>

            <p className="text-gray-700 leading-relaxed mb-6">
              {college.description}
            </p>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="text-center p-4 bg-blue-50 rounded-lg">
                <TrendingUp className="w-8 h-8 text-blue-600 mx-auto mb-2" />
                <div className="text-2xl font-bold text-gray-900">{college.stats.placementRate}%</div>
                <div className="text-sm text-gray-600">Placement Rate</div>
              </div>
              <div className="text-center p-4 bg-green-50 rounded-lg">
                <DollarSign className="w-8 h-8 text-green-600 mx-auto mb-2" />
                <div className="text-2xl font-bold text-gray-900">₹{(college.stats.averagePackage / 100000).toFixed(1)}L</div>
                <div className="text-sm text-gray-600">Avg Package</div>
              </div>
              <div className="text-center p-4 bg-purple-50 rounded-lg">
                <Users className="w-8 h-8 text-purple-600 mx-auto mb-2" />
                <div className="text-2xl font-bold text-gray-900">{college.stats.faculty}</div>
                <div className="text-sm text-gray-600">Faculty</div>
              </div>
              <div className="text-center p-4 bg-orange-50 rounded-lg">
                <Building className="w-8 h-8 text-orange-600 mx-auto mb-2" />
                <div className="text-2xl font-bold text-gray-900">{college.stats.campusSize}</div>
                <div className="text-sm text-gray-600">Campus</div>
              </div>
            </div>
          </div>

          <div className="lg:col-span-1">
            <Card className="sticky top-6">
              <Card.Header>
                <Card.Title>Contact Information</Card.Title>
              </Card.Header>
              
              <div className="space-y-4 mb-6">
                <div className="flex items-start space-x-3">
                  <MapPin className="w-5 h-5 text-gray-400 mt-0.5" />
                  <div>
                    <div className="font-medium text-gray-900">Address</div>
                    <div className="text-sm text-gray-600">{college.location.address}</div>
                  </div>
                </div>
                
                <div className="flex items-center space-x-3">
                  <Phone className="w-5 h-5 text-gray-400" />
                  <div>
                    <div className="font-medium text-gray-900">Phone</div>
                    <div className="text-sm text-gray-600">{college.phone}</div>
                  </div>
                </div>
                
                <div className="flex items-center space-x-3">
                  <Mail className="w-5 h-5 text-gray-400" />
                  <div>
                    <div className="font-medium text-gray-900">Email</div>
                    <div className="text-sm text-gray-600">{college.email}</div>
                  </div>
                </div>
                
                <div className="flex items-center space-x-3">
                  <Globe className="w-5 h-5 text-gray-400" />
                  <div>
                    <div className="font-medium text-gray-900">Website</div>
                    <a href={college.website} target="_blank" rel="noopener noreferrer" className="text-sm text-blue-600 hover:underline">
                      Visit Website
                    </a>
                  </div>
                </div>
              </div>

              <div className="space-y-3">
                <Button className="w-full" size="lg">
                  <ExternalLink className="w-4 h-4 mr-2" />
                  Apply Now
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
            </Card>
          </div>
        </div>

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

        <motion.div
          key={activeTab}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
        >
          {activeTab === 'overview' && (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <Card>
                <Card.Header>
                  <Card.Title>Campus Facilities</Card.Title>
                </Card.Header>
                <div className="grid grid-cols-1 gap-2">
                  {college.facilities.map((facility, index) => (
                    <div key={index} className="flex items-center space-x-2">
                      <CheckCircle className="w-4 h-4 text-green-600" />
                      <span className="text-gray-700">{facility}</span>
                    </div>
                  ))}
                </div>
              </Card>

              <Card>
                <Card.Header>
                  <Card.Title>Rankings</Card.Title>
                </Card.Header>
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600">NIRF Ranking</span>
                    <Badge variant="primary">#{college.ranking.nirf}</Badge>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600">QS World Ranking</span>
                    <Badge variant="secondary">#{college.ranking.qs}</Badge>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600">Times Higher Education</span>
                    <Badge variant="secondary">#{college.ranking.times}</Badge>
                  </div>
                </div>
              </Card>
            </div>
          )}

          {activeTab === 'courses' && (
            <Card>
              <Card.Header>
                <Card.Title>Available Programs</Card.Title>
              </Card.Header>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {college.courses.map((course, index) => (
                  <div key={index} className="border rounded-lg p-4">
                    <h3 className="font-semibold text-gray-900 mb-2">{course.name}</h3>
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span className="text-gray-600">Duration:</span>
                        <span className="font-medium">{course.duration}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Annual Fees:</span>
                        <span className="font-medium">₹{course.fees.toLocaleString()}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Seats:</span>
                        <span className="font-medium">{course.seats}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Cutoff:</span>
                        <span className="font-medium text-blue-600">{course.cutoff}</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </Card>
          )}

          {activeTab === 'scholarships' && (
            <Card>
              <Card.Header>
                <div className="flex items-center space-x-2">
                  <Award className="w-5 h-5 text-yellow-600" />
                  <Card.Title>Scholarship Opportunities</Card.Title>
                </div>
                <Card.Description>
                  Financial aid and scholarship programs available for students
                </Card.Description>
              </Card.Header>
              <div className="space-y-6">
                <div className="bg-gradient-to-r from-yellow-50 to-orange-50 border border-yellow-200 rounded-lg p-6">
                  <div className="flex items-start space-x-3">
                    <Award className="w-6 h-6 text-yellow-600 mt-1" />
                    <div className="flex-1">
                      <h3 className="font-semibold text-gray-900 mb-2">Available Scholarships</h3>
                      <p className="text-gray-700 leading-relaxed">
                        {college.scholarship_details}
                      </p>
                    </div>
                  </div>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="border rounded-lg p-4">
                    <h4 className="font-semibold text-gray-900 mb-3 flex items-center">
                      <CheckCircle className="w-4 h-4 text-green-600 mr-2" />
                      Merit-Based Scholarships
                    </h4>
                    <ul className="space-y-2 text-sm text-gray-600">
                      <li>• Up to 100% tuition fee waiver</li>
                      <li>• Based on JEE Advanced rank</li>
                      <li>• Renewable annually with good grades</li>
                      <li>• Additional stipend for top performers</li>
                    </ul>
                  </div>
                  
                  <div className="border rounded-lg p-4">
                    <h4 className="font-semibold text-gray-900 mb-3 flex items-center">
                      <CheckCircle className="w-4 h-4 text-blue-600 mr-2" />
                      Need-Based Financial Aid
                    </h4>
                    <ul className="space-y-2 text-sm text-gray-600">
                      <li>• Income-based fee concessions</li>
                      <li>• Free hostel accommodation</li>
                      <li>• Book and equipment allowances</li>
                      <li>• Emergency financial support</li>
                    </ul>
                  </div>
                  
                  <div className="border rounded-lg p-4">
                    <h4 className="font-semibold text-gray-900 mb-3 flex items-center">
                      <CheckCircle className="w-4 h-4 text-purple-600 mr-2" />
                      Research Assistantships
                    </h4>
                    <ul className="space-y-2 text-sm text-gray-600">
                      <li>• Monthly stipend of ₹12,400-₹31,000</li>
                      <li>• Available for M.Tech and PhD students</li>
                      <li>• Work with faculty on research projects</li>
                      <li>• Conference travel support</li>
                    </ul>
                  </div>
                  
                  <div className="border rounded-lg p-4">
                    <h4 className="font-semibold text-gray-900 mb-3 flex items-center">
                      <CheckCircle className="w-4 h-4 text-orange-600 mr-2" />
                      Industry Scholarships
                    </h4>
                    <ul className="space-y-2 text-sm text-gray-600">
                      <li>• Sponsored by top tech companies</li>
                      <li>• Internship opportunities included</li>
                      <li>• Mentorship programs</li>
                      <li>• Potential job offers upon graduation</li>
                    </ul>
                  </div>
                </div>
                
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <h4 className="font-semibold text-blue-900 mb-2">How to Apply</h4>
                  <p className="text-blue-800 text-sm mb-3">
                    Scholarship applications are typically processed during the admission process. 
                    Contact the financial aid office for detailed eligibility criteria and application procedures.
                  </p>
                  <Button size="sm" className="bg-blue-600 hover:bg-blue-700">
                    <ExternalLink className="w-4 h-4 mr-2" />
                    Apply for Scholarships
                  </Button>
                </div>
              </div>
            </Card>
          )}

          {activeTab === 'placements' && (
            <Card>
              <Card.Header>
                <Card.Title>Top Recruiters</Card.Title>
              </Card.Header>
              <div className="space-y-3">
                {college.placements.companies.map((company, index) => (
                  <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div>
                      <div className="font-medium text-gray-900">{company.name}</div>
                      <div className="text-sm text-gray-600">{company.selected} students selected</div>
                    </div>
                    <div className="text-right">
                      <div className="font-semibold text-green-600">₹{(company.package / 100000).toFixed(1)}L</div>
                      <div className="text-xs text-gray-500">CTC</div>
                    </div>
                  </div>
                ))}
              </div>
            </Card>
          )}

          {activeTab === 'reviews' && (
            <Card>
              <Card.Header>
                <Card.Title>Student Reviews</Card.Title>
              </Card.Header>
              <div className="space-y-6">
                {college.reviews.map((review) => (
                  <div key={review.id} className="border-b border-gray-200 pb-6 last:border-b-0">
                    <div className="flex items-start justify-between mb-3">
                      <div>
                        <h4 className="font-medium text-gray-900">{review.user}</h4>
                        <p className="text-sm text-gray-600">{review.course} • Class of {review.year}</p>
                      </div>
                      <div className="flex items-center space-x-1">
                        {[...Array(5)].map((_, i) => (
                          <Star 
                            key={i} 
                            className={`w-4 h-4 ${
                              i < review.rating ? 'text-yellow-500 fill-current' : 'text-gray-300'
                            }`} 
                          />
                        ))}
                      </div>
                    </div>
                    <p className="text-gray-700">{review.comment}</p>
                  </div>
                ))}
              </div>
            </Card>
          )}
        </motion.div>
      </div>
    </PageLayout>
  );
};

export default CollegeDetail;
