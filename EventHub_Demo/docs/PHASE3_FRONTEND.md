# Phase 3: Frontend Web Development (React)

## 🎯 Mục tiêu Phase 3

Xây dựng React Admin Portal với:
1. Auth0 Authentication Integration
2. Admin Dashboard
3. Teambuilding Management (CRUD)
4. Event Management (CRUD)
5. Registration Management (View, Update Status)
6. Image Upload UI
7. Responsive Design

## 🏗️ Component Structure

```
src/
├── components/
│   ├── Layout/
│   │   ├── Header.js
│   │   ├── Sidebar.js
│   │   └── Footer.js
│   ├── Auth/
│   │   ├── LoginButton.js
│   │   ├── LogoutButton.js
│   │   └── ProtectedRoute.js
│   ├── Dashboard/
│   │   ├── StatsCard.js
│   │   └── RecentActivity.js
│   ├── Teambuilding/
│   │   ├── TeambuildingList.js
│   │   ├── TeambuildingForm.js
│   │   └── TeambuildingCard.js
│   ├── Event/
│   │   ├── EventList.js
│   │   ├── EventForm.js
│   │   └── EventCard.js
│   ├── Registration/
│   │   ├── RegistrationList.js
│   │   └── RegistrationTable.js
│   └── Common/
│       ├── Loading.js
│       ├── ErrorMessage.js
│       └── ImageUpload.js
├── pages/
│   ├── Dashboard.js
│   ├── Teambuildings.js
│   ├── Events.js
│   ├── Registrations.js
│   └── NotFound.js
├── services/
│   ├── api.js
│   ├── auth.js
│   ├── teambuilding.js
│   ├── event.js
│   └── registration.js
├── utils/
│   ├── constants.js
│   ├── helpers.js
│   └── validation.js
├── App.js
└── index.js
```

## 🔐 Auth0 Integration

### Setup Auth0Provider
```javascript
import { Auth0Provider } from '@auth0/auth0-react';

<Auth0Provider
  domain="dev-q886n3eebgb8g04f.us.auth0.com"
  clientId="yGm0uw9aLN9YSe8qVB2mq79ylDSvoJcL"
  authorizationParams={{
    redirect_uri: window.location.origin + "/callback",
    audience: "https://eventhub-api",
    scope: "openid profile email"
  }}
>
  <App />
</Auth0Provider>
```

### Protected Routes
Chỉ admin mới truy cập được admin portal.

## 📱 Pages & Features

### 1. Dashboard Page
**Route**: `/dashboard`
**Features**:
- Tổng quan thống kê:
  - Số lượng teambuildings
  - Số lượng events
  - Số lượng registrations
  - Số người tham gia
- Recent activities
- Upcoming events

### 2. Teambuildings Page
**Route**: `/teambuildings`
**Features**:
- List tất cả teambuildings
- Search & Filter
- Create new teambuilding
- Edit teambuilding
- Delete teambuilding
- View events trong teambuilding

**Form Fields**:
- Name (required)
- Description
- Start Date (required)
- End Date (required)
- Location
- Budget
- Image Upload

### 3. Events Page
**Route**: `/events`
**Features**:
- List tất cả events
- Filter by teambuilding
- Create new event
- Edit event
- Delete event
- View registrations

**Form Fields**:
- Teambuilding (dropdown, required)
- Name (required)
- Description
- Event Date (required)
- Location
- Max Participants
- Image Upload

### 4. Registrations Page
**Route**: `/registrations`
**Features**:
- List tất cả registrations
- Filter by event, status, user
- View registration details
- Update registration status (pending/confirmed/cancelled)
- Export to CSV

**Display Fields**:
- User name & email
- Event name
- Teambuilding name
- Registration date
- Status
- Notes
- Actions (view, update status)

## 🎨 UI/UX Design

### Color Scheme
- Primary: #1976d2 (Blue)
- Secondary: #dc004e (Pink/Red)
- Success: #4caf50 (Green)
- Warning: #ff9800 (Orange)
- Error: #f44336 (Red)

### Layout
- Responsive design (mobile, tablet, desktop)
- Sidebar navigation
- Top header with user info
- Breadcrumb navigation
- Modal dialogs cho forms

### UI Libraries (Optional)
Có thể dùng:
- Material-UI (MUI)
- Ant Design
- Bootstrap
- Tailwind CSS

Hoặc custom CSS.

## 🔧 API Integration

### Axios Configuration
```javascript
// services/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL,
  timeout: 10000,
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
```

### Service Functions
```javascript
// services/teambuilding.js
export const getTeambuildings = () => api.get('/teambuildings');
export const getTeambuilding = (id) => api.get(`/teambuildings/${id}`);
export const createTeambuilding = (data) => api.post('/teambuildings', data);
export const updateTeambuilding = (id, data) => api.put(`/teambuildings/${id}`, data);
export const deleteTeambuilding = (id) => api.delete(`/teambuildings/${id}`);
```

## 📤 Image Upload

### Image Upload Component
```javascript
const ImageUpload = ({ onImageSelect }) => {
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const formData = new FormData();
      formData.append('image', file);
      
      // Upload to backend
      api.post('/upload/image', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      .then(res => onImageSelect(res.data.url))
      .catch(err => console.error(err));
    }
  };
  
  return <input type="file" accept="image/*" onChange={handleFileChange} />;
};
```

## 🧪 Testing

### Manual Testing Checklist:
- [ ] Login with Auth0 works
- [ ] Dashboard displays correct statistics
- [ ] Can create teambuilding
- [ ] Can edit teambuilding
- [ ] Can delete teambuilding
- [ ] Can create event
- [ ] Can edit event
- [ ] Can delete event
- [ ] Can view registrations
- [ ] Can update registration status
- [ ] Image upload works
- [ ] Responsive on mobile
- [ ] Error handling works

## 📦 Dependencies

```json
{
  "@auth0/auth0-react": "^2.2.3",
  "axios": "^1.6.2",
  "react": "^18.2.0",
  "react-dom": "^18.2.0",
  "react-router-dom": "^6.20.1"
}
```

Optional UI libraries:
- `@mui/material` - Material UI
- `antd` - Ant Design
- `bootstrap` - Bootstrap

## ✅ Validation Checklist

- [ ] Auth0 login hoạt động
- [ ] Protected routes hoạt động
- [ ] API calls với authentication
- [ ] CRUD operations cho Teambuildings
- [ ] CRUD operations cho Events
- [ ] View & Update Registrations
- [ ] Image upload & display
- [ ] Error handling
- [ ] Loading states
- [ ] Responsive design

## ➡️ Next Steps

Sau khi hoàn thành Phase 3:
- **Phase 4: Mobile App Development** - Xây dựng Flutter Mobile App cho Users

## 🐛 Common Issues

### Issue: CORS error from backend
```javascript
// Check backend CORS configuration
// Verify API_URL in .env
```

### Issue: Auth0 redirect not working
```javascript
// Check redirect_uri matches Auth0 settings
// Verify callback route exists
```

### Issue: Images not displaying
```javascript
// Check upload endpoint
// Verify image URL format
// Check CORS for image serving
```
