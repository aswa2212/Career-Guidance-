// API service for backend communication using Axios
import apiClient from './apiClient';

const API_BASE_URL = 'http://127.0.0.1:8000';

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  // Authentication methods
  async register(userData) {
    return apiClient.post('/auth/register', userData);
  }

  async login(email, password) {
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);
  
    const data = await apiClient.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    if (data.access_token) {
      localStorage.setItem('auth-token', data.access_token);
      if (data.refresh_token) {
        localStorage.setItem('refresh-token', data.refresh_token);
      }
    }

    return data;
  }

  logout() {
    localStorage.removeItem('auth-token');
    localStorage.removeItem('refresh-token');
    localStorage.removeItem('auth-storage');
  }

  // User methods
  async getCurrentUser() {
    return apiClient.get('/users/me');
  }

  async updateUser(userData) {
    return apiClient.put('/users/me', userData);
  }

  // Assessment methods
  async getAssessments() {
    return apiClient.get('/assessments');
  }

  async getAssessment(assessmentId) {
    return apiClient.get(`/assessments/${assessmentId}`);
  }

  async submitAssessment(assessmentId, answers) {
    return apiClient.post(`/assessments/${assessmentId}/submit`, { answers });
  }

  async getAssessmentResults(assessmentId) {
    return apiClient.get(`/assessments/${assessmentId}/results`);
  }

  // Course methods
  async getCourses(params = {}) {
    return apiClient.get('/courses', { params });
  }

  async getCourse(courseId) {
    return apiClient.get(`/courses/${courseId}`);
  }

  async searchCourses(query, filters = {}) {
    return apiClient.get('/courses/search', { 
      params: { q: query, ...filters } 
    });
  }

  // Career methods
  async getCareers(params = {}) {
    return apiClient.get('/careers', { params });
  }

  async getCareer(careerId) {
    return apiClient.get(`/careers/${careerId}`);
  }

  async getCareerSuggestions() {
    return apiClient.get('/careers/suggestions');
  }

  async searchCareers(query, filters = {}) {
    return apiClient.get('/careers/search', { 
      params: { q: query, ...filters } 
    });
  }

  // College methods
  async getColleges(params = {}) {
    return apiClient.get('/colleges', { params });
  }

  async getCollege(collegeId) {
    return apiClient.get(`/colleges/${collegeId}`);
  }

  async searchColleges(query, filters = {}) {
    return apiClient.get('/colleges/search', { 
      params: { q: query, ...filters } 
    });
  }

  // Timeline methods
  async getTimeline() {
    return apiClient.get('/timeline');
  }

  async getUserTimeline() {
    return apiClient.get('/timeline');
  }

  async addDeadline(deadlineData) {
    return apiClient.post('/timeline/deadlines', deadlineData);
  }

  async updateDeadline(deadlineId, deadlineData) {
    return apiClient.put(`/timeline/deadlines/${deadlineId}`, deadlineData);
  }

  async deleteDeadline(deadlineId) {
    return apiClient.delete(`/timeline/deadlines/${deadlineId}`);
  }

  // Settings methods
  async getSettings() {
    return apiClient.get('/users/settings');
  }

  async updateSettings(settings) {
    return apiClient.put('/users/settings', settings);
  }

  async changePassword(passwordData) {
    return apiClient.post('/users/change-password', passwordData);
  }

  async exportData() {
    return apiClient.get('/users/export-data');
  }

  async deleteAccount() {
    return apiClient.delete('/users/account');
  }

  // Health check
  async healthCheck() {
    return apiClient.get('/health');
  }

  // Generic HTTP methods for direct API calls
  async get(url) {
    return apiClient.get(url);
  }

  async post(url, data) {
    return apiClient.post(url, data);
  }

  async put(url, data) {
    return apiClient.put(url, data);
  }

  async delete(url) {
    return apiClient.delete(url);
  }
}

const api = new ApiService();
export { api };
export default api;
