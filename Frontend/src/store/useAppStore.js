import { create } from 'zustand'
import { persist } from 'zustand/middleware'

const useAppStore = create(
  persist(
    (set, get) => ({
      // Theme state
      isDarkMode: false,
      toggleDarkMode: () => set((state) => ({ isDarkMode: !state.isDarkMode })),

      // User state
      user: null,
      isAuthenticated: false,
      login: (userData) => set({ user: userData, isAuthenticated: true }),
      logout: () => set({ user: null, isAuthenticated: false }),

      // Notifications
      notifications: [
        { id: 1, title: 'Welcome!', message: 'Complete your profile to get personalized recommendations', type: 'info', unread: true },
        { id: 2, title: 'New Course Available', message: 'Computer Science Engineering applications are now open', type: 'success', unread: true },
        { id: 3, title: 'Deadline Reminder', message: 'JEE Main registration closes in 5 days', type: 'warning', unread: true }
      ],
      markNotificationAsRead: (id) => set((state) => ({
        notifications: state.notifications.map(notif => 
          notif.id === id ? { ...notif, unread: false } : notif
        )
      })),
      addNotification: (notification) => set((state) => ({
        notifications: [{ ...notification, id: Date.now(), unread: true }, ...state.notifications]
      })),

      // Aptitude test state
      testResults: [],
      currentTest: null,
      addTestResult: (result) => set((state) => ({
        testResults: [...state.testResults, { ...result, id: Date.now(), date: new Date().toISOString() }]
      })),
      setCurrentTest: (test) => set({ currentTest: test }),

      // Search state
      searchQuery: '',
      setSearchQuery: (query) => set({ searchQuery: query }),

      // Filters state
      collegeFilters: {
        location: '',
        course: '',
        ranking: '',
        sortBy: 'name'
      },
      courseFilters: {
        category: '',
        duration: '',
        sortBy: 'popularity'
      },
      resourceFilters: {
        category: '',
        type: '',
        sortBy: 'newest'
      },
      updateCollegeFilters: (filters) => set((state) => ({
        collegeFilters: { ...state.collegeFilters, ...filters }
      })),
      updateCourseFilters: (filters) => set((state) => ({
        courseFilters: { ...state.courseFilters, ...filters }
      })),
      updateResourceFilters: (filters) => set((state) => ({
        resourceFilters: { ...state.resourceFilters, ...filters }
      })),

      // Dashboard stats
      stats: {
        totalColleges: 1250,
        totalCourses: 450,
        testsCompleted: 0,
        applicationsSubmitted: 0
      },
      updateStats: (newStats) => set((state) => ({
        stats: { ...state.stats, ...newStats }
      }))
    }),
    {
      name: 'student-guidance-storage',
      partialize: (state) => ({
        isDarkMode: state.isDarkMode,
        user: state.user,
        isAuthenticated: state.isAuthenticated,
        testResults: state.testResults,
        stats: state.stats
      })
    }
  )
)

export default useAppStore
