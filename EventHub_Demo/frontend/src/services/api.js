/**
 * Axios instance and API configuration
 */

import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost/api';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor - Add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor - Handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Server responded with error
      const { status, data } = error.response;
      
      if (status === 401) {
        // Unauthorized - clear token and redirect to login
        localStorage.removeItem('access_token');
        window.location.href = '/';
      } else if (status === 403) {
        // Forbidden
        console.error('Access forbidden:', data.detail);
      }
      
      return Promise.reject(data);
    } else if (error.request) {
      // Request made but no response
      return Promise.reject({ detail: 'Network error. Please check your connection.' });
    } else {
      // Other errors
      return Promise.reject({ detail: error.message });
    }
  }
);

export default api;
