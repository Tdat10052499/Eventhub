/**
 * Auth0 Action: Add User Profile to Token
 * 
 * This Action adds email, name, and role to the access token.
 * 
 * To use:
 * 1. Go to Auth0 Dashboard → Actions → Flows → Login
 * 2. Click "+" → "Build Custom"
 * 3. Name: "Add User Profile to Token"
 * 4. Copy this code
 * 5. Deploy and add to Login flow
 */

exports.onExecutePostLogin = async (event, api) => {
  const namespace = 'https://eventhub-api';
  
  // Add email to token
  if (event.user.email) {
    api.accessToken.setCustomClaim(`${namespace}/email`, event.user.email);
  }
  
  // Add name to token
  if (event.user.name) {
    api.accessToken.setCustomClaim(`${namespace}/name`, event.user.name);
  } else if (event.user.nickname) {
    api.accessToken.setCustomClaim(`${namespace}/name`, event.user.nickname);
  }
  
  // Add role (from user metadata)
  if (event.user.app_metadata && event.user.app_metadata.role) {
    api.accessToken.setCustomClaim(`${namespace}/role`, event.user.app_metadata.role);
  } else {
    // Default role
    api.accessToken.setCustomClaim(`${namespace}/role`, 'user');
  }
};
