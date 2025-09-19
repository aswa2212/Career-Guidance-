import axios from 'axios';
import toast from 'react-hot-toast';

// Create axios instance with base configuration
const API_BASE_URL = 'http://127.0.0.1:8000';
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
    'Cache-Control': 'no-cache, no-store, must-revalidate',
    'Pragma': 'no-cache',
    'Expires': '0'
  },
});

// Request interceptor to add auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth-token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling and token refresh
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;

    // Handle network errors
    if (!error.response) {
      toast.error('Network error. Please check your connection.');
      return Promise.reject(error);
    }

    const { status, data } = error.response;

    // Handle different error status codes
    switch (status) {
      case 401:
        // Unauthorized - token expired or invalid
        if (!originalRequest._retry) {
          originalRequest._retry = true;
          
          // Clear tokens and redirect to login
          localStorage.removeItem('auth-token');
          localStorage.removeItem('refresh-token');
          localStorage.removeItem('auth-storage');
          
          // Don't redirect if already on auth page
          if (!window.location.pathname.includes('/auth')) {
            toast.error('Session expired. Please login again.');
            window.location.href = '/auth';
          }
        }
        break;

      case 403:
        toast.error('Access denied. You don\'t have permission for this action.');
        break;

      case 404:
        toast.error('Resource not found.');
        break;

      case 422:
        // Validation errors
        if (data.detail && Array.isArray(data.detail)) {
          data.detail.forEach(err => {
            toast.error(`${err.loc?.join(' ')}: ${err.msg}`);
          });
        } else {
          toast.error(data.detail || 'Validation error occurred.');
        }
        break;

      case 429:
        toast.error('Too many requests. Please try again later.');
        break;

      case 500:
        toast.error('Server error. Please try again later.');
        break;

      default:
        toast.error(data.detail || 'An unexpected error occurred.');
    }

    return Promise.reject(error);
  }
);

// API methods with retry logic
const apiMethods = {
  // GET request with retry
  get: async (url, config = {}) => {
    const maxRetries = config.retries || 3;
    let attempt = 0;

    while (attempt < maxRetries) {
      try {
        const response = await apiClient.get(url, config);
        return response.data;
      } catch (error) {
        attempt++;
        if (attempt >= maxRetries || error.response?.status < 500) {
          throw error;
        }
        // Wait before retry (exponential backoff)
        await new Promise(resolve => setTimeout(resolve, Math.pow(2, attempt) * 1000));
      }
    }
  },

  // POST request with retry
  post: async (url, data, config = {}) => {
    const maxRetries = config.retries || 3;
    let attempt = 0;

    while (attempt < maxRetries) {
      try {
        const response = await apiClient.post(url, data, config);
        return response.data;
      } catch (error) {
        attempt++;
        if (attempt >= maxRetries || error.response?.status < 500) {
          throw error;
        }
        await new Promise(resolve => setTimeout(resolve, Math.pow(2, attempt) * 1000));
      }
    }
  },

  // PUT request
  put: async (url, data, config = {}) => {
    const response = await apiClient.put(url, data, config);
    return response.data;
  },

  // PATCH request
  patch: async (url, data, config = {}) => {
    const response = await apiClient.patch(url, data, config);
    return response.data;
  },

  // DELETE request
  delete: async (url, config = {}) => {
    const response = await apiClient.delete(url, config);
    return response.data;
  },

  // Upload file with progress
  upload: async (url, formData, onProgress = null) => {
    const config = {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    };

    if (onProgress) {
      config.onUploadProgress = (progressEvent) => {
        const percentCompleted = Math.round(
          (progressEvent.loaded * 100) / progressEvent.total
        );
        onProgress(percentCompleted);
      };
    }

    const response = await apiClient.post(url, formData, config);
    return response.data;
  },
};

export default apiMethods;
