import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Clock, CheckCircle, XCircle, RotateCcw, Award } from 'lucide-react'
import useAppStore from '../store/useAppStore'
import Card from '../components/Card'
import Button from '../components/Button'
import ProgressBar from '../components/ProgressBar'
import Chart from '../components/Chart'

const AptitudeTest = () => {
  const { addTestResult, isDarkMode } = useAppStore()
  const [currentQuestion, setCurrentQuestion] = useState(0)
  const [selectedAnswers, setSelectedAnswers] = useState({})
  const [timeLeft, setTimeLeft] = useState(1800) // 30 minutes
  const [testStarted, setTestStarted] = useState(false)
  const [testCompleted, setTestCompleted] = useState(false)
  const [results, setResults] = useState(null)

  // Sample questions data
  const questions = [
    {
      id: 1,
      category: 'Mathematics',
      question: 'If x + 5 = 12, what is the value of x?',
      options: ['5', '6', '7', '8'],
      correct: 2
    },
    {
      id: 2,
      category: 'Logical Reasoning',
      question: 'Which number comes next in the sequence: 2, 4, 8, 16, ?',
      options: ['24', '32', '30', '20'],
      correct: 1
    },
    {
      id: 3,
      category: 'English',
      question: 'Choose the correct synonym for "abundant":',
      options: ['Scarce', 'Plentiful', 'Limited', 'Rare'],
      correct: 1
    },
    {
      id: 4,
      category: 'Science',
      question: 'What is the chemical symbol for gold?',
      options: ['Go', 'Gd', 'Au', 'Ag'],
      correct: 2
    },
    {
      id: 5,
      category: 'Mathematics',
      question: 'What is 15% of 200?',
      options: ['25', '30', '35', '40'],
      correct: 1
    },
    {
      id: 6,
      category: 'Logical Reasoning',
      question: 'If all roses are flowers and some flowers are red, which statement is definitely true?',
      options: ['All roses are red', 'Some roses are red', 'Some roses may be red', 'No roses are red'],
      correct: 2
    },
    {
      id: 7,
      category: 'English',
      question: 'Identify the grammatically correct sentence:',
      options: ['She don\'t like apples', 'She doesn\'t likes apples', 'She doesn\'t like apples', 'She not like apples'],
      correct: 2
    },
    {
      id: 8,
      category: 'Science',
      question: 'Which planet is closest to the Sun?',
      options: ['Venus', 'Mercury', 'Earth', 'Mars'],
      correct: 1
    }
  ]

  const progress = ((currentQuestion + 1) / questions.length) * 100

  useEffect(() => {
    let timer
    if (testStarted && !testCompleted && timeLeft > 0) {
      timer = setInterval(() => {
        setTimeLeft(prev => {
          if (prev <= 1) {
            handleSubmitTest()
            return 0
          }
          return prev - 1
        })
      }, 1000)
    }
    return () => clearInterval(timer)
  }, [testStarted, testCompleted, timeLeft])

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
  }

  const handleStartTest = () => {
    setTestStarted(true)
    setCurrentQuestion(0)
    setSelectedAnswers({})
    setTimeLeft(1800)
    setTestCompleted(false)
    setResults(null)
  }

  const handleAnswerSelect = (answerIndex) => {
    setSelectedAnswers(prev => ({
      ...prev,
      [currentQuestion]: answerIndex
    }))
  }

  const handleNextQuestion = () => {
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(prev => prev + 1)
    }
  }

  const handlePrevQuestion = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(prev => prev - 1)
    }
  }

  const calculateResults = () => {
    const categoryScores = {}
    let totalCorrect = 0

    questions.forEach((question, index) => {
      const userAnswer = selectedAnswers[index]
      const isCorrect = userAnswer === question.correct
      
      if (isCorrect) totalCorrect++

      if (!categoryScores[question.category]) {
        categoryScores[question.category] = { correct: 0, total: 0 }
      }
      categoryScores[question.category].total++
      if (isCorrect) categoryScores[question.category].correct++
    })

    const categoryData = Object.entries(categoryScores).map(([category, scores]) => ({
      name: category,
      score: Math.round((scores.correct / scores.total) * 100)
    }))

    return {
      totalScore: Math.round((totalCorrect / questions.length) * 100),
      totalCorrect,
      totalQuestions: questions.length,
      categoryData,
      timeTaken: 1800 - timeLeft
    }
  }

  const handleSubmitTest = () => {
    const testResults = calculateResults()
    setResults(testResults)
    setTestCompleted(true)
    addTestResult(testResults)
  }

  const handleRetakeTest = () => {
    setTestStarted(false)
    setTestCompleted(false)
    setCurrentQuestion(0)
    setSelectedAnswers({})
    setTimeLeft(1800)
    setResults(null)
  }

  if (!testStarted) {
    return (
      <div className={`min-h-screen ${
        isDarkMode ? 'bg-gray-900' : 'bg-gray-50'
      } py-8`}>
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center mb-8"
          >
            <h1 className={`text-3xl font-bold mb-4 ${
              isDarkMode ? 'text-white' : 'text-gray-900'
            }`}>
              Aptitude Test
            </h1>
            <p className={`text-lg ${
              isDarkMode ? 'text-gray-300' : 'text-gray-600'
            }`}>
              Test your knowledge across multiple subjects
            </p>
          </motion.div>

          <Card className="max-w-2xl mx-auto p-8">
            <div className="text-center mb-8">
              <div className="w-16 h-16 bg-gradient-to-br from-primary to-secondary rounded-full flex items-center justify-center mx-auto mb-4">
                <Award className="w-8 h-8 text-white" />
              </div>
              <h2 className={`text-2xl font-bold mb-4 ${
                isDarkMode ? 'text-white' : 'text-gray-900'
              }`}>
                Ready to Begin?
              </h2>
            </div>

            <div className="space-y-4 mb-8">
              <div className="flex items-center justify-between p-4 rounded-lg bg-gradient-to-r from-primary/5 to-secondary/5">
                <span className={`font-medium ${
                  isDarkMode ? 'text-white' : 'text-gray-900'
                }`}>
                  Total Questions
                </span>
                <span className="text-primary font-bold">{questions.length}</span>
              </div>
              
              <div className="flex items-center justify-between p-4 rounded-lg bg-gradient-to-r from-primary/5 to-secondary/5">
                <span className={`font-medium ${
                  isDarkMode ? 'text-white' : 'text-gray-900'
                }`}>
                  Time Limit
                </span>
                <span className="text-primary font-bold">30 minutes</span>
              </div>
              
              <div className="flex items-center justify-between p-4 rounded-lg bg-gradient-to-r from-primary/5 to-secondary/5">
                <span className={`font-medium ${
                  isDarkMode ? 'text-white' : 'text-gray-900'
                }`}>
                  Categories
                </span>
                <span className="text-primary font-bold">Math, Logic, English, Science</span>
              </div>
            </div>

            <div className={`p-4 rounded-lg mb-6 ${
              isDarkMode ? 'bg-gray-700' : 'bg-blue-50'
            }`}>
              <h3 className={`font-semibold mb-2 ${
                isDarkMode ? 'text-white' : 'text-gray-900'
              }`}>
                Instructions:
              </h3>
              <ul className={`text-sm space-y-1 ${
                isDarkMode ? 'text-gray-300' : 'text-gray-600'
              }`}>
                <li>• Read each question carefully before selecting an answer</li>
                <li>• You can navigate between questions using Next/Previous buttons</li>
                <li>• Your progress is automatically saved</li>
                <li>• Submit the test before time runs out</li>
              </ul>
            </div>

            <Button 
              onClick={handleStartTest}
              className="w-full"
              size="lg"
            >
              Start Test
            </Button>
          </Card>
        </div>
      </div>
    )
  }

  if (testCompleted && results) {
    return (
      <div className={`min-h-screen ${
        isDarkMode ? 'bg-gray-900' : 'bg-gray-50'
      } py-8`}>
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="text-center mb-8"
          >
            <div className="w-20 h-20 bg-gradient-to-br from-primary to-secondary rounded-full flex items-center justify-center mx-auto mb-4">
              <CheckCircle className="w-10 h-10 text-white" />
            </div>
            <h1 className={`text-3xl font-bold mb-2 ${
              isDarkMode ? 'text-white' : 'text-gray-900'
            }`}>
              Test Completed!
            </h1>
            <p className={`text-lg ${
              isDarkMode ? 'text-gray-300' : 'text-gray-600'
            }`}>
              Here are your results
            </p>
          </motion.div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
            <Card className="p-6 text-center">
              <h3 className={`text-lg font-semibold mb-2 ${
                isDarkMode ? 'text-white' : 'text-gray-900'
              }`}>
                Overall Score
              </h3>
              <div className="text-4xl font-bold text-primary mb-2">
                {results.totalScore}%
              </div>
              <p className={`text-sm ${
                isDarkMode ? 'text-gray-400' : 'text-gray-600'
              }`}>
                {results.totalCorrect} out of {results.totalQuestions} correct
              </p>
            </Card>

            <Card className="p-6 text-center">
              <h3 className={`text-lg font-semibold mb-2 ${
                isDarkMode ? 'text-white' : 'text-gray-900'
              }`}>
                Time Taken
              </h3>
              <div className="text-4xl font-bold text-secondary mb-2">
                {formatTime(results.timeTaken)}
              </div>
              <p className={`text-sm ${
                isDarkMode ? 'text-gray-400' : 'text-gray-600'
              }`}>
                Out of 30:00 minutes
              </p>
            </Card>

            <Card className="p-6 text-center">
              <h3 className={`text-lg font-semibold mb-2 ${
                isDarkMode ? 'text-white' : 'text-gray-900'
              }`}>
                Performance
              </h3>
              <div className={`text-4xl font-bold mb-2 ${
                results.totalScore >= 80 ? 'text-green-500' :
                results.totalScore >= 60 ? 'text-yellow-500' : 'text-red-500'
              }`}>
                {results.totalScore >= 80 ? 'Excellent' :
                 results.totalScore >= 60 ? 'Good' : 'Needs Work'}
              </div>
              <p className={`text-sm ${
                isDarkMode ? 'text-gray-400' : 'text-gray-600'
              }`}>
                Keep practicing!
              </p>
            </Card>
          </div>

          <Card className="p-6 mb-8">
            <h3 className={`text-lg font-semibold mb-6 ${
              isDarkMode ? 'text-white' : 'text-gray-900'
            }`}>
              Category-wise Performance
            </h3>
            <Chart 
              type="bar"
              data={results.categoryData}
              dataKey="score"
              xAxisKey="name"
              height={300}
            />
          </Card>

          <div className="flex justify-center space-x-4">
            <Button onClick={handleRetakeTest} variant="outline">
              <RotateCcw className="w-4 h-4 mr-2" />
              Retake Test
            </Button>
            <Button onClick={() => window.location.href = '/dashboard'}>
              Back to Dashboard
            </Button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className={`min-h-screen ${
      isDarkMode ? 'bg-gray-900' : 'bg-gray-50'
    } py-8`}>
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className={`text-2xl font-bold ${
              isDarkMode ? 'text-white' : 'text-gray-900'
            }`}>
              Aptitude Test
            </h1>
            <p className={`text-sm ${
              isDarkMode ? 'text-gray-400' : 'text-gray-600'
            }`}>
              Question {currentQuestion + 1} of {questions.length}
            </p>
          </div>
          
          <div className="flex items-center space-x-4">
            <div className={`flex items-center space-x-2 px-4 py-2 rounded-lg ${
              timeLeft < 300 ? 'bg-red-100 text-red-800' : 
              isDarkMode ? 'bg-gray-800 text-white' : 'bg-white text-gray-900'
            }`}>
              <Clock className="w-4 h-4" />
              <span className="font-mono font-medium">
                {formatTime(timeLeft)}
              </span>
            </div>
          </div>
        </div>

        {/* Progress Bar */}
        <div className="mb-8">
          <ProgressBar progress={progress} />
        </div>

        {/* Question Card */}
        <AnimatePresence mode="wait">
          <motion.div
            key={currentQuestion}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            transition={{ duration: 0.3 }}
          >
            <Card className="p-8 mb-8">
              <div className="mb-6">
                <span className="inline-block px-3 py-1 bg-primary/10 text-primary text-sm font-medium rounded-full mb-4">
                  {questions[currentQuestion].category}
                </span>
                <h2 className={`text-xl font-semibold ${
                  isDarkMode ? 'text-white' : 'text-gray-900'
                }`}>
                  {questions[currentQuestion].question}
                </h2>
              </div>

              <div className="space-y-3">
                {questions[currentQuestion].options.map((option, index) => (
                  <motion.button
                    key={index}
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={() => handleAnswerSelect(index)}
                    className={`w-full p-4 text-left rounded-xl border-2 transition-all duration-200 ${
                      selectedAnswers[currentQuestion] === index
                        ? 'border-primary bg-primary/5'
                        : isDarkMode
                          ? 'border-gray-600 hover:border-gray-500 bg-gray-800'
                          : 'border-gray-200 hover:border-gray-300 bg-white'
                    }`}
                  >
                    <div className="flex items-center">
                      <div className={`w-6 h-6 rounded-full border-2 mr-3 flex items-center justify-center ${
                        selectedAnswers[currentQuestion] === index
                          ? 'border-primary bg-primary'
                          : isDarkMode
                            ? 'border-gray-500'
                            : 'border-gray-300'
                      }`}>
                        {selectedAnswers[currentQuestion] === index && (
                          <div className="w-2 h-2 bg-white rounded-full" />
                        )}
                      </div>
                      <span className={`font-medium mr-3 ${
                        isDarkMode ? 'text-gray-300' : 'text-gray-600'
                      }`}>
                        {String.fromCharCode(65 + index)}.
                      </span>
                      <span className={isDarkMode ? 'text-white' : 'text-gray-900'}>
                        {option}
                      </span>
                    </div>
                  </motion.button>
                ))}
              </div>
            </Card>
          </motion.div>
        </AnimatePresence>

        {/* Navigation */}
        <div className="flex items-center justify-between">
          <Button
            onClick={handlePrevQuestion}
            disabled={currentQuestion === 0}
            variant="outline"
          >
            Previous
          </Button>

          <div className="flex space-x-3">
            {currentQuestion === questions.length - 1 ? (
              <Button
                onClick={handleSubmitTest}
                disabled={Object.keys(selectedAnswers).length === 0}
                className="px-8"
              >
                Submit Test
              </Button>
            ) : (
              <Button
                onClick={handleNextQuestion}
                disabled={selectedAnswers[currentQuestion] === undefined}
              >
                Next
              </Button>
            )}
          </div>
        </div>

        {/* Question Navigation */}
        <Card className="mt-8 p-6">
          <h3 className={`text-sm font-medium mb-4 ${
            isDarkMode ? 'text-gray-300' : 'text-gray-700'
          }`}>
            Question Navigation
          </h3>
          <div className="grid grid-cols-8 gap-2">
            {questions.map((_, index) => (
              <button
                key={index}
                onClick={() => setCurrentQuestion(index)}
                className={`w-10 h-10 rounded-lg text-sm font-medium transition-all duration-200 ${
                  index === currentQuestion
                    ? 'bg-primary text-white'
                    : selectedAnswers[index] !== undefined
                      ? 'bg-green-100 text-green-800 border border-green-300'
                      : isDarkMode
                        ? 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                        : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                {index + 1}
              </button>
            ))}
          </div>
        </Card>
      </div>
    </div>
  )
}

export default AptitudeTest
