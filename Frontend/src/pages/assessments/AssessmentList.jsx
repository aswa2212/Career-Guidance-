import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  BrainCircuit, 
  Heart, 
  Clock, 
  CheckCircle, 
  ArrowRight,
  Trophy,
  Target,
  Zap
} from 'lucide-react';
import PageLayout from '../../components/layout/PageLayout';
import Card from '../../components/ui/Card';
import Button from '../../components/ui/Button';
import { LoadingCard } from '../../components/ui/Loading';

const AssessmentList = () => {
  const [assessments, setAssessments] = useState([]);
  const [loading, setLoading] = useState(true);

  const mockAssessments = [
    {
      id: 'aptitude',
      title: 'Aptitude Assessment',
      description: 'Evaluate your logical reasoning, numerical ability, and problem-solving skills',
      icon: BrainCircuit,
      duration: '45 minutes',
      questions: 50,
      completed: false,
      difficulty: 'Medium',
      color: 'blue',
      benefits: ['Identify your strengths', 'Discover suitable career paths', 'Get personalized recommendations']
    },
    {
      id: 'interest',
      title: 'Interest Profiling',
      description: 'Discover your passions and interests to find careers that align with your personality',
      icon: Heart,
      duration: '30 minutes',
      questions: 40,
      completed: true,
      difficulty: 'Easy',
      color: 'pink',
      benefits: ['Understand your motivations', 'Find fulfilling career options', 'Match interests with opportunities']
    },
    {
      id: 'personality',
      title: 'Personality Assessment',
      description: 'Understand your work style, communication preferences, and team dynamics',
      icon: Target,
      duration: '35 minutes',
      questions: 45,
      completed: false,
      difficulty: 'Medium',
      color: 'green',
      benefits: ['Know your work style', 'Improve team collaboration', 'Choose suitable work environments']
    },
    {
      id: 'skills',
      title: 'Skills Evaluation',
      description: 'Assess your current technical and soft skills across various domains',
      icon: Zap,
      duration: '60 minutes',
      questions: 75,
      completed: false,
      difficulty: 'Hard',
      color: 'yellow',
      benefits: ['Map your skill gaps', 'Plan skill development', 'Showcase your abilities']
    }
  ];

  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      setAssessments(mockAssessments);
      setLoading(false);
    }, 1000);
  }, []);

  const getColorClasses = (color, completed) => {
    const colors = {
      blue: completed ? 'bg-blue-50 border-blue-200' : 'bg-blue-50 border-blue-300',
      pink: completed ? 'bg-pink-50 border-pink-200' : 'bg-pink-50 border-pink-300',
      green: completed ? 'bg-green-50 border-green-200' : 'bg-green-50 border-green-300',
      yellow: completed ? 'bg-yellow-50 border-yellow-200' : 'bg-yellow-50 border-yellow-300',
    };
    return colors[color] || colors.blue;
  };

  const getIconColor = (color) => {
    const colors = {
      blue: 'text-blue-600',
      pink: 'text-pink-600',
      green: 'text-green-600',
      yellow: 'text-yellow-600',
    };
    return colors[color] || colors.blue;
  };

  const getDifficultyColor = (difficulty) => {
    const colors = {
      Easy: 'bg-green-100 text-green-800',
      Medium: 'bg-yellow-100 text-yellow-800',
      Hard: 'bg-red-100 text-red-800',
    };
    return colors[difficulty] || colors.Medium;
  };

  if (loading) {
    return (
      <PageLayout title="Assessments" subtitle="Discover your strengths and interests">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {[1, 2, 3, 4].map((i) => (
            <LoadingCard key={i} />
          ))}
        </div>
      </PageLayout>
    );
  }

  return (
    <PageLayout 
      title="Career Assessments" 
      subtitle="Take comprehensive assessments to discover your ideal career path"
    >
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {assessments.map((assessment, index) => {
          const Icon = assessment.icon;
          return (
            <motion.div
              key={assessment.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
            >
              <Card className={`relative overflow-hidden ${getColorClasses(assessment.color, assessment.completed)}`}>
                {assessment.completed && (
                  <div className="absolute top-4 right-4">
                    <div className="flex items-center space-x-1 bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs font-medium">
                      <CheckCircle className="w-3 h-3" />
                      <span>Completed</span>
                    </div>
                  </div>
                )}

                <div className="flex items-start space-x-4">
                  <div className={`p-3 rounded-lg bg-white shadow-sm`}>
                    <Icon className={`w-6 h-6 ${getIconColor(assessment.color)}`} />
                  </div>
                  
                  <div className="flex-1">
                    <h3 className="text-xl font-semibold text-gray-900 mb-2">
                      {assessment.title}
                    </h3>
                    <p className="text-gray-600 mb-4">
                      {assessment.description}
                    </p>

                    <div className="flex items-center space-x-4 mb-4 text-sm text-gray-500">
                      <div className="flex items-center space-x-1">
                        <Clock className="w-4 h-4" />
                        <span>{assessment.duration}</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <Trophy className="w-4 h-4" />
                        <span>{assessment.questions} questions</span>
                      </div>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getDifficultyColor(assessment.difficulty)}`}>
                        {assessment.difficulty}
                      </span>
                    </div>

                    <div className="mb-4">
                      <h4 className="text-sm font-medium text-gray-900 mb-2">What you'll gain:</h4>
                      <ul className="text-sm text-gray-600 space-y-1">
                        {assessment.benefits.map((benefit, i) => (
                          <li key={i} className="flex items-center space-x-2">
                            <div className="w-1.5 h-1.5 bg-gray-400 rounded-full" />
                            <span>{benefit}</span>
                          </li>
                        ))}
                      </ul>
                    </div>

                    <div className="flex items-center justify-between">
                      <Link to={`/assessments/${assessment.id}`}>
                        <Button 
                          variant={assessment.completed ? "secondary" : "primary"}
                          className="flex items-center space-x-2"
                        >
                          <span>{assessment.completed ? 'View Results' : 'Start Assessment'}</span>
                          <ArrowRight className="w-4 h-4" />
                        </Button>
                      </Link>
                      
                      {assessment.completed && (
                        <Link 
                          to={`/assessments/${assessment.id}/results`}
                          className="text-sm text-blue-600 hover:text-blue-800 font-medium"
                        >
                          View detailed results
                        </Link>
                      )}
                    </div>
                  </div>
                </div>
              </Card>
            </motion.div>
          );
        })}
      </div>

      {/* Progress Summary */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.4 }}
        className="mt-8"
      >
        <Card className="bg-gradient-to-r from-blue-50 to-purple-50 border-blue-200">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Assessment Progress
              </h3>
              <p className="text-gray-600">
                Complete all assessments to get comprehensive career recommendations
              </p>
            </div>
            <div className="text-right">
              <div className="text-2xl font-bold text-blue-600">
                {assessments.filter(a => a.completed).length}/{assessments.length}
              </div>
              <div className="text-sm text-gray-500">Completed</div>
            </div>
          </div>
          
          <div className="mt-4">
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div 
                className="bg-gradient-to-r from-blue-600 to-purple-600 h-2 rounded-full transition-all duration-500"
                style={{ 
                  width: `${(assessments.filter(a => a.completed).length / assessments.length) * 100}%` 
                }}
              />
            </div>
          </div>
        </Card>
      </motion.div>
    </PageLayout>
  );
};

export default AssessmentList;
