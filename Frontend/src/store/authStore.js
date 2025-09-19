import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import apiService from '../services/api';
import toast from 'react-hot-toast';

const useAuthStore = create(
  persist(
    (set, get) => ({
      // State
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: false,

      // Actions
      login: async (email, password) => {
        set({ isLoading: true });
        try {
          const response = await apiService.login(email, password);
          
          // Get user data after successful login
          const user = await apiService.getCurrentUser();
          
          set({
            user: user,
            token: response.access_token,
            isAuthenticated: true,
            isLoading: false,
          });
          
          toast.success('Login successful!');
          return { success: true };
        } catch (error) {
          set({ isLoading: false });
          const errorMessage = error.response?.data?.detail || 'Login failed';
          toast.error(errorMessage);
          return { 
            success: false, 
            error: errorMessage
          };
        }
      },

      register: async (userData) => {
        set({ isLoading: true });
        try {
          const response = await apiService.register(userData);
          
          // Auto-login after registration
          const loginResult = await get().login(userData.email, userData.password);
          
          if (loginResult.success) {
            toast.success('Registration successful!');
            return { success: true };
          }
          
          return loginResult;
        } catch (error) {
          set({ isLoading: false });
          const errorMessage = error.response?.data?.detail || 'Registration failed';
          toast.error(errorMessage);
          return { 
            success: false, 
            error: errorMessage
          };
        }
      },

      logout: () => {
        apiService.logout();
        localStorage.removeItem('auth-token');
        localStorage.removeItem('auth-storage');
        set({
          user: null,
          token: null,
          isAuthenticated: false,
        });
        toast.success('Logged out successfully');
      },

      // Initialize auth state from localStorage
      initialize: async () => {
        const token = localStorage.getItem('auth-token');
        if (token) {
          try {
            // Try to get current user with the token
            const user = await apiService.getCurrentUser();
            set({
              user: user,
              token,
              isAuthenticated: true,
            });
          } catch (error) {
            // Token is invalid, clear it
            console.log('Token invalid, logging out');
            get().logout();
          }
        } else {
          // No token found, user needs to login
          set({
            user: null,
            token: null,
            isAuthenticated: false,
          });
        }
      },

      // Update user profile
      updateUser: (userData) => {
        set((state) => ({
          user: { ...state.user, ...userData },
        }));
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        token: state.token,
        user: state.user,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);

export default useAuthStore;
