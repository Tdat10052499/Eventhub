/**
 * Dashboard service - API calls for dashboard statistics
 */

import api from './api';

export const dashboardService = {
  /**
   * Get dashboard statistics
   */
  getStats: async () => {
    const response = await api.get('/dashboard/stats');
    return response.data;
  }
};

export default dashboardService;
