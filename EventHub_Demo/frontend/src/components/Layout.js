import React from 'react';
import { NavLink } from 'react-router-dom';
import { useAuth0 } from '@auth0/auth0-react';

function Layout({ children }) {
  const { user, logout } = useAuth0();

  const handleLogout = () => {
    logout({ returnTo: window.location.origin });
  };

  return (
    <div className="layout">
      <aside className="sidebar">
        <div className="sidebar-header">
          <h2>EventHub</h2>
          <p>Admin Portal</p>
        </div>

        <nav>
          <ul className="sidebar-nav">
            <li>
              <NavLink to="/dashboard" className={({ isActive }) => isActive ? 'active' : ''}>
                <span>📊</span>
                <span>Dashboard</span>
              </NavLink>
            </li>
            <li>
              <NavLink to="/teambuildings" className={({ isActive }) => isActive ? 'active' : ''}>
                <span>🏢</span>
                <span>Teambuildings</span>
              </NavLink>
            </li>
            <li>
              <NavLink to="/events" className={({ isActive }) => isActive ? 'active' : ''}>
                <span>📅</span>
                <span>Events</span>
              </NavLink>
            </li>
            <li>
              <NavLink to="/registrations" className={({ isActive }) => isActive ? 'active' : ''}>
                <span>📝</span>
                <span>Registrations</span>
              </NavLink>
            </li>
          </ul>
        </nav>

        <div style={{ marginTop: 'auto', paddingTop: '20px', borderTop: '1px solid #444' }}>
          <div style={{ marginBottom: '15px', padding: '10px', backgroundColor: '#1a1d23', borderRadius: '5px' }}>
            <p style={{ fontSize: '12px', marginBottom: '5px', color: '#aaa' }}>Logged in as:</p>
            <p style={{ fontSize: '14px', fontWeight: 'bold' }}>{user?.name || user?.email}</p>
          </div>
          <button onClick={handleLogout} className="btn btn-danger" style={{ width: '100%' }}>
            Logout
          </button>
        </div>
      </aside>

      <main className="main-content">
        {children}
      </main>
    </div>
  );
}

export default Layout;
