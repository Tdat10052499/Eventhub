/**
 * Authentication service
 */

import api from './api';

export const authService = {
  /**
   * Get current user profile
   */
  getProfile: async () => {
    const response = await api.get('/auth/me');
    return response.data;
  },

  /**
   * Update current user profile
   */
  updateProfile: async (userData) => {
    const response = await api.put('/auth/me', userData);
    return response.data;
  },

  /**
   * Store access token
   */
  setAccessToken: (token) => {
    localStorage.setItem('access_token', token);
  },

  /**
   * Get access token
   */
  getAccessToken: () => {
    return localStorage.getItem('access_token');
  },

  /**
   * Remove access token
   */
  removeAccessToken: () => {
    localStorage.removeItem('access_token');
  },

  /**
   * Check if user is authenticated
   */
  isAuthenticated: () => {
    return !!localStorage.getItem('access_token');
  }
};
