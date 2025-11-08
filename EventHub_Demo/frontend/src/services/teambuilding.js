/**
 * Teambuilding service - API calls for teambuildings
 */

import api from './api';

export const teambuildingService = {
  /**
   * Get all teambuildings
   */
  getAll: async (params = {}) => {
    const response = await api.get('/teambuildings/', { params });
    return response.data;
  },

  /**
   * Get active teambuildings
   */
  getActive: async () => {
    const response = await api.get('/teambuildings/active/');
    return response.data;
  },

  /**
   * Get teambuilding by ID
   */
  getById: async (id) => {
    const response = await api.get(`/teambuildings/${id}/`);
    return response.data;
  },

  /**
   * Create new teambuilding
   */
  create: async (data) => {
    const response = await api.post('/teambuildings/', data);
    return response.data;
  },

  /**
   * Update teambuilding
   */
  update: async (id, data) => {
    const response = await api.put(`/teambuildings/${id}/`, data);
    return response.data;
  },

  /**
   * Delete teambuilding
   */
  delete: async (id) => {
    await api.delete(`/teambuildings/${id}/`);
  }
};

export default teambuildingService;
