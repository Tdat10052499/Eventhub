import React, { useState, useEffect } from 'react';
import { useAuth0 } from '@auth0/auth0-react';
import dashboardService from '../services/dashboard';

function Dashboard() {
  const { user } = useAuth0();
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadDashboardStats();
  }, []);

  const loadDashboardStats = async () => {
    try {
      setLoading(true);
      const data = await dashboardService.getStats();
      setStats(data);
      setError(null);
    } catch (err) {
      setError('Failed to load dashboard statistics');
      console.error('Dashboard error:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Loading dashboard...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="main-content">
        <div className="error-message">{error}</div>
      </div>
    );
  }

  return (
    <div className="main-content">
      <div className="header">
        <div>
          <h1>Dashboard</h1>
          <p>Welcome back, {user?.name || user?.email}</p>
        </div>
        <div className="header-actions">
          <button onClick={loadDashboardStats} className="btn btn-secondary">
            Refresh
          </button>
        </div>
      </div>

      <div className="card-grid">
        <div className="card">
          <h3 style={{ color: '#1976d2', marginBottom: '10px' }}>Total Teambuildings</h3>
          <p style={{ fontSize: '36px', fontWeight: 'bold', color: '#333' }}>
            {stats?.total_teambuildings || 0}
          </p>
        </div>

        <div className="card">
          <h3 style={{ color: '#4caf50', marginBottom: '10px' }}>Total Events</h3>
          <p style={{ fontSize: '36px', fontWeight: 'bold', color: '#333' }}>
            {stats?.total_events || 0}
          </p>
        </div>

        <div className="card">
          <h3 style={{ color: '#ff9800', marginBottom: '10px' }}>Total Registrations</h3>
          <p style={{ fontSize: '36px', fontWeight: 'bold', color: '#333' }}>
            {stats?.total_registrations || 0}
          </p>
        </div>

        <div className="card">
          <h3 style={{ color: '#9c27b0', marginBottom: '10px' }}>Active Teambuildings</h3>
          <p style={{ fontSize: '36px', fontWeight: 'bold', color: '#333' }}>
            {stats?.active_teambuildings || 0}
          </p>
        </div>
      </div>

      <div className="card">
        <h2 style={{ marginBottom: '20px' }}>Recent Activity</h2>
        {stats?.recent_registrations && stats.recent_registrations.length > 0 ? (
          <table>
            <thead>
              <tr>
                <th>User</th>
                <th>Event</th>
                <th>Status</th>
                <th>Registered At</th>
              </tr>
            </thead>
            <tbody>
              {stats.recent_registrations.map((reg) => (
                <tr key={reg.id}>
                  <td>{reg.user_email}</td>
                  <td>{reg.event_name}</td>
                  <td>
                    <span className={`badge badge-${reg.status.toLowerCase()}`}>
                      {reg.status}
                    </span>
                  </td>
                  <td>{new Date(reg.registered_at).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p style={{ color: '#999' }}>No recent registrations</p>
        )}
      </div>
    </div>
  );
}

export default Dashboard;
