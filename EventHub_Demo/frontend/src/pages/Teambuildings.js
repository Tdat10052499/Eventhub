import React, { useState, useEffect } from 'react';
import teambuildingService from '../services/teambuilding';

function Teambuildings() {
  const [teambuildings, setTeambuildings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    start_date: '',
    end_date: '',
    location: '',
    budget: '',
    status: 'active',
  });

  useEffect(() => {
    loadTeambuildings();
  }, []);

  const loadTeambuildings = async () => {
    try {
      setLoading(true);
      const data = await teambuildingService.getAll();
      setTeambuildings(data);
      setError(null);
    } catch (err) {
      setError('Failed to load teambuildings');
      console.error('Load teambuildings error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingId) {
        await teambuildingService.update(editingId, formData);
      } else {
        await teambuildingService.create(formData);
      }
      setShowForm(false);
      setEditingId(null);
      setFormData({ name: '', description: '', start_date: '', end_date: '', location: '', budget: '', status: 'active' });
      loadTeambuildings();
    } catch (err) {
      setError('Failed to save teambuilding');
      console.error('Save teambuilding error:', err);
    }
  };

  const handleEdit = (teambuilding) => {
    setEditingId(teambuilding.id);
    setFormData({
      name: teambuilding.name,
      description: teambuilding.description || '',
      start_date: teambuilding.start_date || '',
      end_date: teambuilding.end_date || '',
      location: teambuilding.location || '',
      budget: teambuilding.budget || '',
      status: teambuilding.status || 'active',
    });
    setShowForm(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this teambuilding?')) {
      try {
        await teambuildingService.delete(id);
        loadTeambuildings();
      } catch (err) {
        setError('Failed to delete teambuilding');
        console.error('Delete teambuilding error:', err);
      }
    }
  };

  const handleCancel = () => {
    setShowForm(false);
    setEditingId(null);
    setFormData({ name: '', description: '', start_date: '', end_date: '', location: '', budget: '', status: 'active' });
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Loading teambuildings...</p>
      </div>
    );
  }

  return (
    <div className="main-content">
      <div className="header">
        <h1>Teambuildings</h1>
        <div className="header-actions">
          <button onClick={() => setShowForm(true)} className="btn btn-primary">
            + New Teambuilding
          </button>
        </div>
      </div>

      {error && <div className="error-message">{error}</div>}

      {showForm && (
        <div className="card">
          <h2>{editingId ? 'Edit Teambuilding' : 'New Teambuilding'}</h2>
          <form onSubmit={handleSubmit}>
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
              <label>Start Date *</label>
              <input
                type="date"
                value={formData.start_date}
                onChange={(e) => setFormData({ ...formData, start_date: e.target.value })}
                required
              />
            </div>

            <div className="form-group">
              <label>End Date *</label>
              <input
                type="date"
                value={formData.end_date}
                onChange={(e) => setFormData({ ...formData, end_date: e.target.value })}
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
              <label>Budget</label>
              <input
                type="number"
                step="0.01"
                value={formData.budget}
                onChange={(e) => setFormData({ ...formData, budget: e.target.value })}
              />
            </div>

            <div className="form-group">
              <label>Status</label>
              <select
                value={formData.status}
                onChange={(e) => setFormData({ ...formData, status: e.target.value })}
              >
                <option value="active">Active</option>
                <option value="inactive">Inactive</option>
              </select>
            </div>

            <div style={{ display: 'flex', gap: '10px' }}>
              <button type="submit" className="btn btn-success">
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
              <th>Name</th>
              <th>Description</th>
              <th>Location</th>
              <th>Status</th>
              <th>Events</th>
              <th>Total Participants</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {teambuildings.map((tb) => (
              <tr key={tb.id}>
                <td>{tb.name}</td>
                <td>{tb.description || '-'}</td>
                <td>{tb.location || '-'}</td>
                <td>
                  <span className={`badge ${tb.status === 'active' ? 'badge-active' : 'badge-cancelled'}`}>
                    {tb.status === 'active' ? 'Active' : 'Inactive'}
                  </span>
                </td>
                <td>{tb.total_events || 0}</td>
                <td>{tb.total_participants || 0}</td>
                <td>
                  <button onClick={() => handleEdit(tb)} className="btn btn-secondary" style={{ marginRight: '5px' }}>
                    Edit
                  </button>
                  <button onClick={() => handleDelete(tb.id)} className="btn btn-danger">
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

export default Teambuildings;
