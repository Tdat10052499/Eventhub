/**
 * Registration service - API calls for registrations
 */

import api from './api';

export const registrationService = {
  /**
   * Get all registrations (Admin only)
   */
  getAll: async (params = {}) => {
    const response = await api.get('/registrations/', { params });
    return response.data;
  },

  /**
   * Get current user's registrations
   */
  getMy: async (params = {}) => {
    const response = await api.get('/registrations/my-registrations/', { params });
    return response.data;
  },

  /**
   * Get registrations for an event
   */
  getByEvent: async (eventId, params = {}) => {
    const response = await api.get(`/registrations/event/${eventId}`, { params });
    return response.data;
  },

  /**
   * Get registration by ID
   */
  getById: async (id) => {
    const response = await api.get(`/registrations/${id}`);
    return response.data;
  },

  /**
   * Get registrations by status
   */
  getByStatus: async (status) => {
    const response = await api.get(`/registrations/status/${status}`);
    return response.data;
  },

  /**
   * Update registration status
   */
  updateStatus: async (id, status) => {
    const response = await api.put(`/registrations/${id}/status`, { status });
    return response.data;
  },

  /**
   * Create new registration
   */
  create: async (data) => {
    const response = await api.post('/registrations/', data);
    return response.data;
  },

  /**
   * Update registration (Admin only)
   */
  update: async (id, data) => {
    const response = await api.put(`/registrations/${id}`, data);
    return response.data;
  },

  /**
   * Delete registration
   */
  delete: async (id) => {
    await api.delete(`/registrations/${id}`);
  }
};

export default registrationService;
