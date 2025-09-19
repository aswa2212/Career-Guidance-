import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  Calendar, 
  Clock, 
  AlertCircle, 
  CheckCircle, 
  Plus,
  Filter,
  Bell,
  BookOpen,
  GraduationCap,
  FileText,
  Target
} from 'lucide-react';
import PageLayout from '../../components/layout/PageLayout';
import Card from '../../components/ui/Card';
import Button from '../../components/ui/Button';
import Loading from '../../components/ui/Loading';

const AdmissionTimeline = () => {
  const [deadlines, setDeadlines] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedFilter, setSelectedFilter] = useState('all');
  const [showAddModal, setShowAddModal] = useState(false);

  const mockDeadlines = [
    {
      id: 1,
      title: 'JEE Main 2024 Registration',
      type: 'exam',
      date: '2024-03-15',
      time: '23:59',
      status: 'upcoming',
      priority: 'high',
      description: 'Last date to register for JEE Main 2024 examination',
      college: 'NTA',
      course: 'B.Tech',
      fee: '₹1,000',
      daysLeft: 15,
      completed: false,
      documents: ['10th Certificate', '12th Certificate', 'Photo', 'Signature']
    },
    {
      id: 2,
      title: 'NEET UG Application',
      type: 'exam',
      date: '2024-03-20',
      time: '17:00',
      status: 'upcoming',
      priority: 'high',
      description: 'National Eligibility cum Entrance Test for medical courses',
      college: 'NTA',
      course: 'MBBS',
      fee: '₹1,700',
      daysLeft: 20,
      completed: false,
      documents: ['10th Certificate', '12th Certificate', 'Category Certificate']
    },
    {
      id: 3,
      title: 'DU Admission Form',
      type: 'admission',
      date: '2024-03-25',
      time: '23:59',
      status: 'upcoming',
      priority: 'medium',
      description: 'Delhi University undergraduate admission application',
      college: 'Delhi University',
      course: 'B.A/B.Sc/B.Com',
      fee: '₹250',
      daysLeft: 25,
      completed: false,
      documents: ['12th Marksheet', 'Character Certificate', 'Migration Certificate']
    },
    {
      id: 4,
      title: 'BITSAT Registration',
      type: 'exam',
      date: '2024-02-28',
      time: '17:00',
      status: 'completed',
      priority: 'high',
      description: 'BITS Admission Test registration completed',
      college: 'BITS Pilani',
      course: 'B.E/B.Tech',
      fee: '₹3,400',
      daysLeft: -5,
      completed: true,
      documents: ['10th Certificate', '12th Certificate']
    },
    {
      id: 5,
      title: 'CLAT Application',
      type: 'exam',
      date: '2024-04-10',
      time: '23:59',
      status: 'upcoming',
      priority: 'medium',
      description: 'Common Law Admission Test for law courses',
      college: 'Consortium of NLUs',
      course: 'LLB',
      fee: '₹4,000',
      daysLeft: 45,
      completed: false,
      documents: ['10th Certificate', '12th Certificate', 'Category Certificate']
    },
    {
      id: 6,
      title: 'CAT Registration',
      type: 'exam',
      date: '2024-09-15',
      time: '17:00',
      status: 'upcoming',
      priority: 'low',
      description: 'Common Admission Test for MBA programs',
      college: 'IIMs',
      course: 'MBA',
      fee: '₹2,300',
      daysLeft: 180,
      completed: false,
      documents: ['Graduation Certificate', 'Work Experience Certificate']
    }
  ];

  useEffect(() => {
    setTimeout(() => {
      setDeadlines(mockDeadlines);
      setLoading(false);
    }, 1000);
  }, []);

  const filteredDeadlines = deadlines.filter(deadline => {
    if (selectedFilter === 'all') return true;
    if (selectedFilter === 'upcoming') return deadline.status === 'upcoming';
    if (selectedFilter === 'completed') return deadline.status === 'completed';
    if (selectedFilter === 'urgent') return deadline.daysLeft <= 7 && deadline.status === 'upcoming';
    return true;
  });

  const getStatusColor = (status, priority, daysLeft) => {
    if (status === 'completed') return 'bg-green-100 text-green-800 border-green-200';
    if (daysLeft <= 3) return 'bg-red-100 text-red-800 border-red-200';
    if (daysLeft <= 7) return 'bg-yellow-100 text-yellow-800 border-yellow-200';
    if (priority === 'high') return 'bg-blue-100 text-blue-800 border-blue-200';
    return 'bg-gray-100 text-gray-800 border-gray-200';
  };

  const getTypeIcon = (type) => {
    const icons = {
      exam: BookOpen,
      admission: GraduationCap,
      document: FileText,
      interview: Target
    };
    return icons[type] || BookOpen;
  };

  const getPriorityColor = (priority) => {
    const colors = {
      high: 'text-red-600',
      medium: 'text-yellow-600',
      low: 'text-green-600'
    };
    return colors[priority] || colors.medium;
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-IN', {
      day: 'numeric',
      month: 'short',
      year: 'numeric'
    });
  };

  const upcomingCount = deadlines.filter(d => d.status === 'upcoming').length;
  const urgentCount = deadlines.filter(d => d.daysLeft <= 7 && d.status === 'upcoming').length;
  const completedCount = deadlines.filter(d => d.status === 'completed').length;

  if (loading) {
    return (
      <PageLayout title="Timeline" subtitle="Track your admission deadlines">
        <Loading size="lg" text="Loading your timeline..." />
      </PageLayout>
    );
  }

  return (
    <PageLayout 
      title="Admission Timeline" 
      subtitle="Stay on top of important deadlines and never miss an opportunity"
    >
      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <Card className="bg-gradient-to-r from-blue-50 to-blue-100 border-blue-200">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-blue-600 rounded-lg">
              <Calendar className="w-5 h-5 text-white" />
            </div>
            <div>
              <p className="text-sm text-blue-600 font-medium">Upcoming</p>
              <p className="text-2xl font-bold text-blue-900">{upcomingCount}</p>
            </div>
          </div>
        </Card>

        <Card className="bg-gradient-to-r from-red-50 to-red-100 border-red-200">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-red-600 rounded-lg">
              <AlertCircle className="w-5 h-5 text-white" />
            </div>
            <div>
              <p className="text-sm text-red-600 font-medium">Urgent</p>
              <p className="text-2xl font-bold text-red-900">{urgentCount}</p>
            </div>
          </div>
        </Card>

        <Card className="bg-gradient-to-r from-green-50 to-green-100 border-green-200">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-green-600 rounded-lg">
              <CheckCircle className="w-5 h-5 text-white" />
            </div>
            <div>
              <p className="text-sm text-green-600 font-medium">Completed</p>
              <p className="text-2xl font-bold text-green-900">{completedCount}</p>
            </div>
          </div>
        </Card>

        <Card className="bg-gradient-to-r from-purple-50 to-purple-100 border-purple-200">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-purple-600 rounded-lg">
              <Target className="w-5 h-5 text-white" />
            </div>
            <div>
              <p className="text-sm text-purple-600 font-medium">Total</p>
              <p className="text-2xl font-bold text-purple-900">{deadlines.length}</p>
            </div>
          </div>
        </Card>
      </div>

      {/* Filter and Add Button */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-2">
          <Filter className="w-4 h-4 text-gray-500" />
          <select
            value={selectedFilter}
            onChange={(e) => setSelectedFilter(e.target.value)}
            className="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="all">All Deadlines</option>
            <option value="upcoming">Upcoming</option>
            <option value="urgent">Urgent (≤7 days)</option>
            <option value="completed">Completed</option>
          </select>
        </div>
        
        <Button className="flex items-center space-x-2">
          <Plus className="w-4 h-4" />
          <span>Add Deadline</span>
        </Button>
      </div>

      {/* Timeline */}
      <div className="space-y-4">
        {filteredDeadlines.map((deadline, index) => {
          const TypeIcon = getTypeIcon(deadline.type);
          return (
            <motion.div
              key={deadline.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
            >
              <Card className={`${getStatusColor(deadline.status, deadline.priority, deadline.daysLeft)} border-l-4`}>
                <div className="flex items-start justify-between">
                  <div className="flex items-start space-x-4 flex-1">
                    <div className={`p-3 rounded-lg ${deadline.status === 'completed' ? 'bg-green-200' : 'bg-white'}`}>
                      <TypeIcon className={`w-5 h-5 ${deadline.status === 'completed' ? 'text-green-600' : 'text-gray-600'}`} />
                    </div>
                    
                    <div className="flex-1">
                      <div className="flex items-center space-x-2 mb-2">
                        <h3 className="text-lg font-semibold text-gray-900">{deadline.title}</h3>
                        <span className={`text-xs font-medium uppercase ${getPriorityColor(deadline.priority)}`}>
                          {deadline.priority}
                        </span>
                      </div>
                      
                      <p className="text-gray-600 mb-3">{deadline.description}</p>
                      
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                        <div>
                          <p className="text-xs text-gray-500 uppercase tracking-wide">College/Institution</p>
                          <p className="font-medium text-gray-900">{deadline.college}</p>
                        </div>
                        <div>
                          <p className="text-xs text-gray-500 uppercase tracking-wide">Course</p>
                          <p className="font-medium text-gray-900">{deadline.course}</p>
                        </div>
                        <div>
                          <p className="text-xs text-gray-500 uppercase tracking-wide">Application Fee</p>
                          <p className="font-medium text-gray-900">{deadline.fee}</p>
                        </div>
                      </div>

                      <div className="mb-4">
                        <p className="text-xs text-gray-500 uppercase tracking-wide mb-2">Required Documents</p>
                        <div className="flex flex-wrap gap-1">
                          {deadline.documents.map((doc, i) => (
                            <span key={i} className="bg-gray-100 text-gray-700 text-xs px-2 py-1 rounded">
                              {doc}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className="text-right ml-4">
                    <div className="flex items-center space-x-2 mb-2">
                      <Calendar className="w-4 h-4 text-gray-500" />
                      <span className="font-medium text-gray-900">{formatDate(deadline.date)}</span>
                    </div>
                    <div className="flex items-center space-x-2 mb-3">
                      <Clock className="w-4 h-4 text-gray-500" />
                      <span className="text-sm text-gray-600">{deadline.time}</span>
                    </div>
                    
                    {deadline.status === 'upcoming' && (
                      <div className={`text-sm font-medium ${
                        deadline.daysLeft <= 3 ? 'text-red-600' : 
                        deadline.daysLeft <= 7 ? 'text-yellow-600' : 'text-blue-600'
                      }`}>
                        {deadline.daysLeft > 0 ? `${deadline.daysLeft} days left` : 'Due today'}
                      </div>
                    )}
                    
                    {deadline.status === 'completed' && (
                      <div className="flex items-center space-x-1 text-green-600">
                        <CheckCircle className="w-4 h-4" />
                        <span className="text-sm font-medium">Completed</span>
                      </div>
                    )}

                    <div className="mt-3 space-y-2">
                      {deadline.status === 'upcoming' && (
                        <>
                          <Button size="sm" className="w-full">
                            Apply Now
                          </Button>
                          <Button variant="outline" size="sm" className="w-full flex items-center space-x-1">
                            <Bell className="w-3 h-3" />
                            <span>Set Reminder</span>
                          </Button>
                        </>
                      )}
                      {deadline.status === 'completed' && (
                        <Button variant="outline" size="sm" className="w-full">
                          View Details
                        </Button>
                      )}
                    </div>
                  </div>
                </div>
              </Card>
            </motion.div>
          );
        })}
      </div>

      {filteredDeadlines.length === 0 && (
        <div className="text-center py-12">
          <Calendar className="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No deadlines found</h3>
          <p className="text-gray-600 mb-4">
            {selectedFilter === 'all' 
              ? "You haven't added any deadlines yet." 
              : `No ${selectedFilter} deadlines at the moment.`}
          </p>
          <Button className="flex items-center space-x-2">
            <Plus className="w-4 h-4" />
            <span>Add Your First Deadline</span>
          </Button>
        </div>
      )}
    </PageLayout>
  );
};

export default AdmissionTimeline;
