import React, { useState, useEffect } from 'react';
import eventService from '../services/event';
import teambuildingService from '../services/teambuilding';
import uploadService from '../services/upload';

function Events() {
  const [events, setEvents] = useState([]);
  const [teambuildings, setTeambuildings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [filterTeambuildingId, setFilterTeambuildingId] = useState('');
  const [uploading, setUploading] = useState(false);
  const [formData, setFormData] = useState({
    teambuilding_id: '',
    name: '',
    description: '',
    event_date: '',
    location: '',
    max_participants: 50,
    image_url: '',
  });

  useEffect(() => {
    loadData();
  }, [filterTeambuildingId]);

  const loadData = async () => {
    try {
      setLoading(true);
      const [eventsData, teambuildingsData] = await Promise.all([
        filterTeambuildingId 
          ? eventService.getByTeambuilding(parseInt(filterTeambuildingId))
          : eventService.getAll(),
        teambuildingService.getAll(),
      ]);
      setEvents(eventsData);
      setTeambuildings(teambuildingsData);
      setError(null);
    } catch (err) {
      setError('Failed to load events');
      console.error('Load events error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleImageUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    try {
      setUploading(true);
      const response = await uploadService.uploadImage(file);
      setFormData({ ...formData, image_url: response.url });
      setError(null);
    } catch (err) {
      setError('Failed to upload image');
      console.error('Upload error:', err);
    } finally {
      setUploading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const submitData = {
        ...formData,
        teambuilding_id: parseInt(formData.teambuilding_id),
        max_participants: parseInt(formData.max_participants),
      };

      if (editingId) {
        await eventService.update(editingId, submitData);
      } else {
        await eventService.create(submitData);
      }
      setShowForm(false);
      setEditingId(null);
      setFormData({
        teambuilding_id: '',
        name: '',
        description: '',
        event_date: '',
        location: '',
        max_participants: 50,
        image_url: '',
      });
      loadData();
    } catch (err) {
      setError('Failed to save event');
      console.error('Save event error:', err);
    }
  };

  const handleEdit = (event) => {
    setEditingId(event.id);
    // Format datetime for datetime-local input (YYYY-MM-DDThh:mm)
    const eventDateTime = event.event_date.substring(0, 16);
    setFormData({
      teambuilding_id: event.teambuilding_id.toString(),
      name: event.name,
      description: event.description || '',
      event_date: eventDateTime,
      location: event.location || '',
      max_participants: event.max_participants,
      image_url: event.image_url || '',
    });
    setShowForm(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this event?')) {
      try {
        await eventService.delete(id);
        loadData();
      } catch (err) {
        setError('Failed to delete event');
        console.error('Delete event error:', err);
      }
    }
  };

  const handleCancel = () => {
    setShowForm(false);
    setEditingId(null);
    setFormData({
      teambuilding_id: '',
      name: '',
      description: '',
      event_date: '',
      location: '',
      max_participants: 50,
      image_url: '',
    });
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Loading events...</p>
      </div>
    );
  }

  return (
    <div className="main-content">
      <div className="header">
        <h1>Events</h1>
        <div className="header-actions">
          <select
            value={filterTeambuildingId}
            onChange={(e) => setFilterTeambuildingId(e.target.value)}
            style={{ padding: '10px', marginRight: '10px', borderRadius: '5px', border: '1px solid #ddd' }}
          >
            <option value="">All Teambuildings</option>
            {teambuildings.map((tb) => (
              <option key={tb.id} value={tb.id}>
                {tb.name}
              </option>
            ))}
          </select>
          <button onClick={() => setShowForm(true)} className="btn btn-primary">
            + New Event
          </button>
        </div>
      </div>

      {error && <div className="error-message">{error}</div>}

      {showForm && (
        <div className="card">
          <h2>{editingId ? 'Edit Event' : 'New Event'}</h2>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Teambuilding *</label>
              <select
                value={formData.teambuilding_id}
                onChange={(e) => setFormData({ ...formData, teambuilding_id: e.target.value })}
                required
              >
                <option value="">Select Teambuilding</option>
                {teambuildings.map((tb) => (
                  <option key={tb.id} value={tb.id}>
                    {tb.name}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>Name *</label>
              <input
                type="text"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                required
              />
            </div>

            <div className="form-group">
              <label>Description</label>
              <textarea
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              />
            </div>

            <div className="form-group">
              <label>Event Date & Time *</label>
              <input
                type="datetime-local"
                value={formData.event_date}
                onChange={(e) => setFormData({ ...formData, event_date: e.target.value })}
                required
              />
            </div>

            <div className="form-group">
              <label>Location</label>
              <input
                type="text"
                value={formData.location}
                onChange={(e) => setFormData({ ...formData, location: e.target.value })}
              />
            </div>

            <div className="form-group">
              <label>Max Participants *</label>
              <input
                type="number"
                value={formData.max_participants}
                onChange={(e) => setFormData({ ...formData, max_participants: e.target.value })}
                min="1"
                required
              />
            </div>

            <div className="form-group">
              <label>Image</label>
              <input
                type="file"
                accept="image/*"
                onChange={handleImageUpload}
                disabled={uploading}
              />
              {uploading && <p>Uploading...</p>}
              {formData.image_url && (
                <img
                  src={`http://localhost:8000${formData.image_url}`}
                  alt="Preview"
                  style={{ maxWidth: '200px', marginTop: '10px' }}
                />
              )}
            </div>

            <div style={{ display: 'flex', gap: '10px' }}>
              <button type="submit" className="btn btn-success" disabled={uploading}>
                {editingId ? 'Update' : 'Create'}
              </button>
              <button type="button" onClick={handleCancel} className="btn btn-secondary">
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>Image</th>
              <th>Name</th>
              <th>Teambuilding</th>
              <th>Date</th>
              <th>Participants</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {events.map((event) => (
              <tr key={event.id}>
                <td>
                  {event.image_url ? (
                    <img
                      src={`http://localhost:8000${event.image_url}`}
                      alt={event.name}
                      style={{ width: '50px', height: '50px', objectFit: 'cover', borderRadius: '5px' }}
                    />
                  ) : (
                    <div style={{ width: '50px', height: '50px', backgroundColor: '#eee', borderRadius: '5px' }}></div>
                  )}
                </td>
                <td>{event.name}</td>
                <td>{event.teambuilding_name}</td>
                <td>{new Date(event.event_date).toLocaleDateString()}</td>
                <td>
                  {event.current_participants} / {event.max_participants}
                </td>
                <td>
                  <button onClick={() => handleEdit(event)} className="btn btn-secondary" style={{ marginRight: '5px' }}>
                    Edit
                  </button>
                  <button onClick={() => handleDelete(event.id)} className="btn btn-danger">
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

export default Events;
