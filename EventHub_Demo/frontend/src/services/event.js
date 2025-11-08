/**
 * Event service - API calls for events
 */

import api from './api';

export const eventService = {
  /**
   * Get all events
   */
  getAll: async (params = {}) => {
    const response = await api.get('/events/', { params });
    return response.data;
  },

  /**
   * Get upcoming events
   */
  getUpcoming: async (limit = 10) => {
    const response = await api.get('/events/upcoming/', { params: { limit } });
    return response.data;
  },

  /**
   * Get event by ID
   */
  getById: async (id) => {
    const response = await api.get(`/events/${id}`);
    return response.data;
  },

  /**
   * Get events by teambuilding
   */
  getByTeambuilding: async (teambuildingId) => {
    const response = await api.get(`/events/teambuilding/${teambuildingId}`);
    return response.data;
  },

  /**
   * Check event availability
   */
  checkAvailability: async (id) => {
    const response = await api.get(`/events/${id}/availability/`);
    return response.data;
  },

  /**
   * Create new event
   */
  create: async (data) => {
    const response = await api.post('/events/', data);
    return response.data;
  },

  /**
   * Update event
   */
  update: async (id, data) => {
    const response = await api.put(`/events/${id}`, data);
    return response.data;
  },

  /**
   * Delete event
   */
  delete: async (id) => {
    await api.delete(`/events/${id}`);
  }
};

export default eventService;
