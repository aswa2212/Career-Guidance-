import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ChevronLeft, 
  ChevronRight, 
  Clock, 
  CheckCircle,
  AlertCircle,
  Flag,
  RotateCcw
} from 'lucide-react';
import PageLayout from '../../components/layout/PageLayout';
import Card from '../../components/ui/Card';
import Button from '../../components/ui/Button';

const AptitudeTest = () => {
  const { assessmentId } = useParams();
  const navigate = useNavigate();
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState({});
  const [timeLeft, setTimeLeft] = useState(2700); // 45 minutes in seconds
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [flaggedQuestions, setFlaggedQuestions] = useState(new Set());

  const mockQuestions = [
    {
      id: 1,
      type: 'multiple-choice',
      category: 'Logical Reasoning',
      question: 'If all roses are flowers and some flowers are red, which of the following must be true?',
      options: [
        'All roses are red',
        'Some roses are red',
        'No roses are red',
        'Some roses may be red'
      ],
      correctAnswer: 3
    },
    {
      id: 2,
      type: 'multiple-choice',
      category: 'Numerical Ability',
      question: 'What is 15% of 240?',
      options: ['32', '36', '38', '42'],
      correctAnswer: 1
    },
    {
      id: 3,
      type: 'multiple-choice',
      category: 'Pattern Recognition',
      question: 'Complete the sequence: 2, 6, 18, 54, ?',
      options: ['108', '162', '216', '270'],
      correctAnswer: 1
    },
    {
      id: 4,
      type: 'multiple-choice',
      category: 'Verbal Reasoning',
      question: 'Choose the word that best completes the analogy: Book is to Library as Car is to ?',
      options: ['Road', 'Garage', 'Driver', 'Engine'],
      correctAnswer: 1
    },
    {
      id: 5,
      type: 'multiple-choice',
      category: 'Data Interpretation',
      question: 'If a company\'s profit increased from $50,000 to $65,000, what is the percentage increase?',
      options: ['25%', '30%', '35%', '40%'],
      correctAnswer: 1
    }
  ];

  useEffect(() => {
    const timer = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev <= 1) {
          handleSubmit();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  const formatTime = (seconds) => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
  };

  const handleAnswerSelect = (questionId, answerIndex) => {
    setAnswers(prev => ({
      ...prev,
      [questionId]: answerIndex
    }));
  };

  const handleNext = () => {
    if (currentQuestion < mockQuestions.length - 1) {
      setCurrentQuestion(prev => prev + 1);
    }
  };

  const handlePrevious = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(prev => prev - 1);
    }
  };

  const handleQuestionJump = (index) => {
    setCurrentQuestion(index);
  };

  const toggleFlag = (questionId) => {
    setFlaggedQuestions(prev => {
      const newSet = new Set(prev);
      if (newSet.has(questionId)) {
        newSet.delete(questionId);
      } else {
        newSet.add(questionId);
      }
      return newSet;
    });
  };

  const handleSubmit = async () => {
    setIsSubmitting(true);
    // Simulate API call
    setTimeout(() => {
      navigate(`/assessments/${assessmentId}/results`, {
        state: { answers, questions: mockQuestions }
      });
    }, 2000);
  };

  const getQuestionStatus = (index) => {
    const question = mockQuestions[index];
    const isAnswered = answers[question.id] !== undefined;
    const isFlagged = flaggedQuestions.has(question.id);
    const isCurrent = index === currentQuestion;

    if (isCurrent) return 'current';
    if (isAnswered && isFlagged) return 'answered-flagged';
    if (isAnswered) return 'answered';
    if (isFlagged) return 'flagged';
    return 'unanswered';
  };

  const getStatusColor = (status) => {
    const colors = {
      current: 'bg-blue-600 text-white border-blue-600',
      answered: 'bg-green-100 text-green-800 border-green-300',
      'answered-flagged': 'bg-yellow-100 text-yellow-800 border-yellow-300',
      flagged: 'bg-red-100 text-red-800 border-red-300',
      unanswered: 'bg-gray-100 text-gray-600 border-gray-300'
    };
    return colors[status];
  };

  const currentQuestionData = mockQuestions[currentQuestion];
  const answeredCount = Object.keys(answers).length;
  const progress = (answeredCount / mockQuestions.length) * 100;

  return (
    <PageLayout>
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">
              {assessmentId === 'aptitude' ? 'Aptitude Assessment' : 'Assessment'}
            </h1>
            <p className="text-gray-600">
              Question {currentQuestion + 1} of {mockQuestions.length}
            </p>
          </div>
          
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2 bg-white px-4 py-2 rounded-lg border">
              <Clock className="w-4 h-4 text-gray-500" />
              <span className={`font-mono ${timeLeft < 300 ? 'text-red-600' : 'text-gray-700'}`}>
                {formatTime(timeLeft)}
              </span>
            </div>
            <Button
              variant="outline"
              onClick={() => navigate('/assessments')}
              className="text-gray-600"
            >
              Exit Test
            </Button>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Question Navigation */}
          <div className="lg:col-span-1">
            <Card className="sticky top-24">
              <Card.Header>
                <Card.Title className="text-sm">Question Navigator</Card.Title>
                <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                  <div 
                    className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${progress}%` }}
                  />
                </div>
                <p className="text-xs text-gray-500 mt-1">
                  {answeredCount}/{mockQuestions.length} answered
                </p>
              </Card.Header>
              
              <div className="grid grid-cols-5 gap-2">
                {mockQuestions.map((_, index) => {
                  const status = getQuestionStatus(index);
                  return (
                    <button
                      key={index}
                      onClick={() => handleQuestionJump(index)}
                      className={`w-8 h-8 text-xs font-medium rounded border-2 transition-all duration-200 ${getStatusColor(status)}`}
                    >
                      {index + 1}
                    </button>
                  );
                })}
              </div>

              <div className="mt-4 space-y-2 text-xs">
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 bg-green-100 border border-green-300 rounded" />
                  <span>Answered</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 bg-red-100 border border-red-300 rounded" />
                  <span>Flagged</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 bg-gray-100 border border-gray-300 rounded" />
                  <span>Not answered</span>
                </div>
              </div>
            </Card>
          </div>

          {/* Question Content */}
          <div className="lg:col-span-3">
            <AnimatePresence mode="wait">
              <motion.div
                key={currentQuestion}
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                transition={{ duration: 0.3 }}
              >
                <Card className="mb-6">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex-1">
                      <div className="flex items-center space-x-2 mb-2">
                        <span className="bg-blue-100 text-blue-800 text-xs font-medium px-2 py-1 rounded">
                          {currentQuestionData.category}
                        </span>
                        <span className="text-sm text-gray-500">
                          Question {currentQuestion + 1}
                        </span>
                      </div>
                      <h2 className="text-lg font-medium text-gray-900 leading-relaxed">
                        {currentQuestionData.question}
                      </h2>
                    </div>
                    
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => toggleFlag(currentQuestionData.id)}
                      className={`ml-4 ${flaggedQuestions.has(currentQuestionData.id) ? 'text-red-600' : 'text-gray-400'}`}
                    >
                      <Flag className="w-4 h-4" />
                    </Button>
                  </div>

                  <div className="space-y-3">
                    {currentQuestionData.options.map((option, index) => (
                      <motion.label
                        key={index}
                        whileHover={{ scale: 1.01 }}
                        whileTap={{ scale: 0.99 }}
                        className={`flex items-center p-4 rounded-lg border-2 cursor-pointer transition-all duration-200 ${
                          answers[currentQuestionData.id] === index
                            ? 'border-blue-500 bg-blue-50'
                            : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
                        }`}
                      >
                        <input
                          type="radio"
                          name={`question-${currentQuestionData.id}`}
                          value={index}
                          checked={answers[currentQuestionData.id] === index}
                          onChange={() => handleAnswerSelect(currentQuestionData.id, index)}
                          className="sr-only"
                        />
                        <div className={`w-4 h-4 rounded-full border-2 mr-3 flex items-center justify-center ${
                          answers[currentQuestionData.id] === index
                            ? 'border-blue-500 bg-blue-500'
                            : 'border-gray-300'
                        }`}>
                          {answers[currentQuestionData.id] === index && (
                            <div className="w-2 h-2 bg-white rounded-full" />
                          )}
                        </div>
                        <span className="text-gray-700">{option}</span>
                      </motion.label>
                    ))}
                  </div>
                </Card>
              </motion.div>
            </AnimatePresence>

            {/* Navigation Controls */}
            <div className="flex items-center justify-between">
              <Button
                variant="outline"
                onClick={handlePrevious}
                disabled={currentQuestion === 0}
                className="flex items-center space-x-2"
              >
                <ChevronLeft className="w-4 h-4" />
                <span>Previous</span>
              </Button>

              <div className="flex items-center space-x-3">
                {currentQuestion === mockQuestions.length - 1 ? (
                  <Button
                    onClick={handleSubmit}
                    loading={isSubmitting}
                    className="flex items-center space-x-2"
                  >
                    <CheckCircle className="w-4 h-4" />
                    <span>Submit Test</span>
                  </Button>
                ) : (
                  <Button
                    onClick={handleNext}
                    className="flex items-center space-x-2"
                  >
                    <span>Next</span>
                    <ChevronRight className="w-4 h-4" />
                  </Button>
                )}
              </div>
            </div>

            {/* Warning for unanswered questions */}
            {answeredCount < mockQuestions.length && currentQuestion === mockQuestions.length - 1 && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="mt-4 p-4 bg-yellow-50 border border-yellow-200 rounded-lg"
              >
                <div className="flex items-center space-x-2">
                  <AlertCircle className="w-5 h-5 text-yellow-600" />
                  <div>
                    <p className="text-sm font-medium text-yellow-800">
                      You have {mockQuestions.length - answeredCount} unanswered questions
                    </p>
                    <p className="text-sm text-yellow-700">
                      Review your answers before submitting the test.
                    </p>
                  </div>
                </div>
              </motion.div>
            )}
          </div>
        </div>
      </div>
    </PageLayout>
  );
};

export default AptitudeTest;
