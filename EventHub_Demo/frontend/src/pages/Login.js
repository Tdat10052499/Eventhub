import React from 'react';
import { useAuth0 } from '@auth0/auth0-react';

function Login() {
  const { loginWithRedirect, isLoading, error } = useAuth0();

  const handleLogin = () => {
    loginWithRedirect({
      appState: { returnTo: '/dashboard' }
    });
  };

  if (isLoading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Loading...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="loading-container">
        <div className="error-message">
          <p>Authentication Error: {error.message}</p>
        </div>
      </div>
    );
  }

  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    }}>
      <div style={{
        backgroundColor: 'white',
        padding: '50px',
        borderRadius: '10px',
        boxShadow: '0 10px 40px rgba(0,0,0,0.2)',
        textAlign: 'center',
        maxWidth: '400px',
        width: '100%',
      }}>
        <h1 style={{ marginBottom: '10px', color: '#333' }}>EventHub</h1>
        <p style={{ marginBottom: '30px', color: '#666' }}>Admin Portal</p>
        <button
          onClick={handleLogin}
          className="btn btn-primary"
          style={{ width: '100%', padding: '15px' }}
        >
          Login with Auth0
        </button>
        <p style={{ marginTop: '20px', fontSize: '12px', color: '#999' }}>
          Manage teambuilding events and registrations
        </p>
      </div>
    </div>
  );
}

export default Login;
