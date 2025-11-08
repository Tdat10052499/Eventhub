import React, { useState, useEffect } from 'react';
import registrationService from '../services/registration';

function Registrations() {
  const [registrations, setRegistrations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filterEventId, setFilterEventId] = useState('');
  const [filterStatus, setFilterStatus] = useState('');
  const [events, setEvents] = useState([]);

  useEffect(() => {
    loadRegistrations();
  }, [filterEventId, filterStatus]);

  const loadRegistrations = async () => {
    try {
      setLoading(true);
      let data;

      if (filterEventId) {
        data = await registrationService.getByEvent(parseInt(filterEventId));
      } else if (filterStatus) {
        data = await registrationService.getByStatus(filterStatus);
      } else {
        data = await registrationService.getAll();
      }

      setRegistrations(data);

      // Extract unique events for filter dropdown
      const uniqueEvents = [...new Map(
        data.map((reg) => [reg.event_id, { id: reg.event_id, name: reg.event_name }])
      ).values()];
      setEvents(uniqueEvents);

      setError(null);
    } catch (err) {
      setError('Failed to load registrations');
      console.error('Load registrations error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleStatusUpdate = async (id, newStatus) => {
    try {
      await registrationService.updateStatus(id, newStatus);
      loadRegistrations();
    } catch (err) {
      setError('Failed to update registration status');
      console.error('Update status error:', err);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this registration?')) {
      try {
        await registrationService.delete(id);
        loadRegistrations();
      } catch (err) {
        setError('Failed to delete registration');
        console.error('Delete registration error:', err);
      }
    }
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Loading registrations...</p>
      </div>
    );
  }

  return (
    <div className="main-content">
      <div className="header">
        <h1>Registrations</h1>
        <div className="header-actions">
          <select
            value={filterEventId}
            onChange={(e) => {
              setFilterEventId(e.target.value);
              setFilterStatus('');
            }}
            style={{ padding: '10px', marginRight: '10px', borderRadius: '5px', border: '1px solid #ddd' }}
          >
            <option value="">All Events</option>
            {events.map((event) => (
              <option key={event.id} value={event.id}>
                {event.name}
              </option>
            ))}
          </select>

          <select
            value={filterStatus}
            onChange={(e) => {
              setFilterStatus(e.target.value);
              setFilterEventId('');
            }}
            style={{ padding: '10px', borderRadius: '5px', border: '1px solid #ddd' }}
          >
            <option value="">All Statuses</option>
            <option value="pending">Pending</option>
            <option value="confirmed">Confirmed</option>
            <option value="cancelled">Cancelled</option>
          </select>
        </div>
      </div>

      {error && <div className="error-message">{error}</div>}

      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>User</th>
              <th>Event</th>
              <th>Teambuilding</th>
              <th>Status</th>
              <th>Registered At</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {registrations.map((reg) => (
              <tr key={reg.id}>
                <td>{reg.user_email}</td>
                <td>{reg.event_name}</td>
                <td>{reg.teambuilding_name}</td>
                <td>
                  <select
                    value={reg.status}
                    onChange={(e) => handleStatusUpdate(reg.id, e.target.value)}
                    className={`badge badge-${reg.status.toLowerCase()}`}
                    style={{ border: 'none', cursor: 'pointer' }}
                  >
                    <option value="pending">Pending</option>
                    <option value="confirmed">Confirmed</option>
                    <option value="cancelled">Cancelled</option>
                  </select>
                </td>
                <td>{new Date(reg.registered_at).toLocaleString()}</td>
                <td>
                  <button onClick={() => handleDelete(reg.id)} className="btn btn-danger">
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Registrations;
