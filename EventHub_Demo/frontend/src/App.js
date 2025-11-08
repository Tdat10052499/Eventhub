import React, { useEffect } from 'react';
import { Auth0Provider, useAuth0 } from '@auth0/auth0-react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import './App.css';

// Components
import Layout from './components/Layout';

// Pages
import Dashboard from './pages/Dashboard';
import Teambuildings from './pages/Teambuildings';
import Events from './pages/Events';
import Registrations from './pages/Registrations';
import Login from './pages/Login';

// Auth wrapper component
function AuthWrapper({ children }) {
  const { isAuthenticated, isLoading, getAccessTokenSilently } = useAuth0();

  useEffect(() => {
    const getToken = async () => {
      if (isAuthenticated) {
        try {
          console.log('Getting access token...');
          const token = await getAccessTokenSilently();
          console.log('Token received:', token ? 'Yes' : 'No');
          console.log('Token length:', token?.length);
          localStorage.setItem('access_token', token);
          console.log('Token saved to localStorage');
        } catch (error) {
          console.error('Error getting access token:', error);
        }
      }
    };
    getToken();
  }, [isAuthenticated, getAccessTokenSilently]);

  if (isLoading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Loading...</p>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <Layout>{children}</Layout>;
}

function AppRoutes() {
  const { isAuthenticated, isLoading } = useAuth0();

  if (isLoading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Loading...</p>
      </div>
    );
  }

  return (
    <Routes>
      <Route 
        path="/login" 
        element={isAuthenticated ? <Navigate to="/dashboard" replace /> : <Login />} 
      />
      <Route
        path="/dashboard"
        element={
          <AuthWrapper>
            <Dashboard />
          </AuthWrapper>
        }
      />
      <Route
        path="/teambuildings"
        element={
          <AuthWrapper>
            <Teambuildings />
          </AuthWrapper>
        }
      />
      <Route
        path="/events"
        element={
          <AuthWrapper>
            <Events />
          </AuthWrapper>
        }
      />
      <Route
        path="/registrations"
        element={
          <AuthWrapper>
            <Registrations />
          </AuthWrapper>
        }
      />
      <Route 
        path="/" 
        element={
          isAuthenticated ? <Navigate to="/dashboard" replace /> : <Navigate to="/login" replace />
        } 
      />
    </Routes>
  );
}

function App() {
  const domain = process.env.REACT_APP_AUTH0_DOMAIN;
  const clientId = process.env.REACT_APP_AUTH0_CLIENT_ID;
  const redirectUri = window.location.origin;
  const audience = process.env.REACT_APP_AUTH0_AUDIENCE;

  // Debug: Log Auth0 configuration
  console.log('Auth0 Config:', {
    domain,
    clientId,
    redirectUri,
    audience
  });

  if (!domain || !clientId) {
    return (
      <div className="loading-container">
        <div className="error-message">
          <p>Auth0 configuration is missing!</p>
          <p>Please check your .env file</p>
        </div>
      </div>
    );
  }

  return (
    <Auth0Provider
      domain={domain}
      clientId={clientId}
      authorizationParams={{
        redirect_uri: redirectUri,
        audience: "https://eventhub-api",
        scope: "openid profile email"
      }}
      useRefreshTokens={true}
      cacheLocation="localstorage"
    >
      <BrowserRouter>
        <AppRoutes />
      </BrowserRouter>
    </Auth0Provider>
  );
}

export default App;
