import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import useAuthStore from './store/authStore';
import ErrorBoundary from './components/ui/ErrorBoundary';

// Components
import AuthPage from './components/auth/AuthPage';
import Dashboard from './pages/Dashboard';

// Pages
import AssessmentList from './pages/assessments/AssessmentList';
import AptitudeTest from './pages/assessments/AptitudeTest';
import CourseList from './pages/courses/CourseList';
import CourseDetail from './pages/courses/CourseDetail';
import CareerExplorer from './pages/careers/CareerExplorer';
import CareerDetail from './pages/careers/CareerDetail';
import CollegeDirectory from './pages/colleges/CollegeDirectory';
import CollegeDetail from './pages/colleges/CollegeDetail';
import AdmissionTimeline from './pages/timeline/AdmissionTimeline';
import Profile from './pages/profile/Profile';
import Settings from './pages/settings/Settings';

// Protected Route Component
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated } = useAuthStore()
  return isAuthenticated ? children : <Navigate to="/auth" replace />
}

// Public Route Component (redirects to dashboard if already authenticated)
const PublicRoute = ({ children }) => {
  const { isAuthenticated } = useAuthStore()
  return !isAuthenticated ? children : <Navigate to="/dashboard" replace />
}

function App() {
  const { initialize } = useAuthStore()

  useEffect(() => {
    initialize()
  }, [initialize])

  return (
    <ErrorBoundary>
      <Router>
        <div className="min-h-screen bg-gray-50">
          <Routes>
            {/* Public Routes */}
            <Route 
              path="/auth" 
              element={
                <PublicRoute>
                  <AuthPage />
                </PublicRoute>
              } 
            />

          {/* Protected Routes */}
          <Route 
            path="/dashboard" 
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            } 
          />
          
          {/* Assessment Routes */}
          <Route 
            path="/assessments" 
            element={
              <ProtectedRoute>
                <AssessmentList />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/assessments/:assessmentId" 
            element={
              <ProtectedRoute>
                <AptitudeTest />
              </ProtectedRoute>
            } 
          />

          {/* Course Routes */}
          <Route 
            path="/courses" 
            element={
              <ProtectedRoute>
                <CourseList />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/courses/:courseId" 
            element={
              <ProtectedRoute>
                <CourseDetail />
              </ProtectedRoute>
            } 
          />

          {/* Career Routes */}
          <Route 
            path="/careers" 
            element={
              <ProtectedRoute>
                <CareerExplorer />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/careers/:careerId" 
            element={
              <ProtectedRoute>
                <CareerDetail />
              </ProtectedRoute>
            } 
          />

          {/* College Routes */}
          <Route 
            path="/colleges" 
            element={
              <ProtectedRoute>
                <CollegeDirectory />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/colleges/:collegeId" 
            element={
              <ProtectedRoute>
                <CollegeDetail />
              </ProtectedRoute>
            } 
          />

          {/* Timeline Routes */}
          <Route 
            path="/timeline" 
            element={
              <ProtectedRoute>
                <AdmissionTimeline />
              </ProtectedRoute>
            } 
          />

          {/* Profile & Settings Routes */}
          <Route 
            path="/profile" 
            element={
              <ProtectedRoute>
                <Profile />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/settings" 
            element={
              <ProtectedRoute>
                <Settings />
              </ProtectedRoute>
            } 
          />

          {/* Default redirects */}
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>

        {/* Toast Notifications */}
        <Toaster
          position="top-right"
          toastOptions={{
            duration: 4000,
            style: {
              background: '#ffffff',
              color: '#000000',
              border: '1px solid #E5E7EB',
            },
            success: {
              iconTheme: {
                primary: '#10B981',
                secondary: '#ffffff',
              },
            },
            error: {
              iconTheme: {
                primary: '#EF4444',
                secondary: '#ffffff',
              },
            },
          }}
        />
        </div>
      </Router>
    </ErrorBoundary>
  )
}

export default App
