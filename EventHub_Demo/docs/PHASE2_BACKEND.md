# Phase 2: Backend Development (FastAPI)

## 🎯 Mục tiêu Phase 2

Trong phase này, chúng ta sẽ xây dựng:
1. Database Models (SQLAlchemy ORM)
2. Pydantic Schemas cho validation
3. Auth0 Integration cho authentication
4. API Endpoints cho:
   - Authentication & User Management
   - Teambuildings CRUD
   - Events CRUD
   - Registrations CRUD
5. Image Upload functionality
6. API Documentation (Swagger/OpenAPI)

## 📊 Database Models

### Models cần tạo:
- `User` - Quản lý users (admin & regular users)
- `Teambuilding` - Quản lý các chuyến teambuilding
- `Event` - Quản lý events trong teambuilding
- `Registration` - Quản lý đăng ký tham gia

## 🔐 Auth0 Integration

### Authentication Flow:
1. **Web App (Admin)**:
   - Login via Auth0
   - Get JWT access token
   - Verify token with Auth0 public key
   - Check user role (must be admin)
   
2. **Mobile App (User)**:
   - Login via Auth0
   - Get JWT access token
   - Verify token
   - Access allowed endpoints

### Auth0 Configuration:

#### Web Application:
```
Domain: dev-q886n3eebgb8g04f.us.auth0.com
Client ID: yGm0uw9aLN9YSe8qVB2mq79ylDSvoJcL
Callback URLs: http://localhost:3000/callback
Logout URLs: http://localhost:3000
Allowed Web Origins: http://localhost:3000
```

#### Mobile Application:
```
Domain: dev-q886n3eebgb8g04f.us.auth0.com
Client ID: 2VjwUVUqQBdMPWvUuAIVayYILciirQwW
Callback URLs: com.eventhub.teambuilding://callback
```

## 📡 API Endpoints

### Authentication Routes (`/auth`)
- `POST /auth/login` - Login và đồng bộ user từ Auth0
- `GET /auth/me` - Get current user info
- `POST /auth/logout` - Logout

### User Routes (`/users`)
- `GET /users` - List all users (Admin only)
- `GET /users/{id}` - Get user by ID
- `PUT /users/{id}` - Update user
- `DELETE /users/{id}` - Delete user (Admin only)

### Teambuilding Routes (`/teambuildings`)
- `GET /teambuildings` - List all teambuildings
- `GET /teambuildings/{id}` - Get teambuilding by ID
- `POST /teambuildings` - Create teambuilding (Admin only)
- `PUT /teambuildings/{id}` - Update teambuilding (Admin only)
- `DELETE /teambuildings/{id}` - Delete teambuilding (Admin only)
- `GET /teambuildings/{id}/events` - Get all events in teambuilding

### Event Routes (`/events`)
- `GET /events` - List all events
- `GET /events/{id}` - Get event by ID
- `POST /events` - Create event (Admin only)
- `PUT /events/{id}` - Update event (Admin only)
- `DELETE /events/{id}` - Delete event (Admin only)
- `GET /events/{id}/registrations` - Get all registrations for event

### Registration Routes (`/registrations`)
- `GET /registrations` - List all registrations (Admin only)
- `GET /registrations/{id}` - Get registration by ID
- `POST /registrations` - Create registration (User)
- `PUT /registrations/{id}` - Update registration
- `DELETE /registrations/{id}` - Cancel registration
- `GET /registrations/user/{user_id}` - Get user's registrations
- `PATCH /registrations/{id}/status` - Update registration status (Admin)

### Upload Routes (`/upload`)
- `POST /upload/image` - Upload image for events/teambuildings
- `GET /uploads/{filename}` - Get uploaded image

## 🛠️ Implementation Steps

### Step 1: Create Database Models
File: `backend/app/models/*.py`
- user.py
- teambuilding.py
- event.py
- registration.py

### Step 2: Create Pydantic Schemas
File: `backend/app/schemas/*.py`
- user.py
- teambuilding.py
- event.py
- registration.py

### Step 3: Create Auth Utilities
File: `backend/app/utils/auth.py`
- Verify Auth0 JWT token
- Get current user from token
- Check user permissions

### Step 4: Create CRUD Operations
File: `backend/app/crud/*.py`
- Generic CRUD operations
- Specific business logic

### Step 5: Create API Routes
File: `backend/app/routers/*.py`
- auth.py
- users.py
- teambuildings.py
- events.py
- registrations.py
- upload.py

### Step 6: Database Migrations
Setup Alembic for database migrations

## 🧪 Testing

### Test với Postman/Thunder Client:

1. **Health Check**:
```bash
GET http://localhost:8000/health
```

2. **Get Access Token từ Auth0**:
```bash
# Web Admin Login
POST https://dev-q886n3eebgb8g04f.us.auth0.com/oauth/token
Content-Type: application/json

{
  "client_id": "yGm0uw9aLN9YSe8qVB2mq79ylDSvoJcL",
  "client_secret": "N-SAuJxY5WT5nIxil9Jvqn_bTWXPj_hiVDtmapyhrspXfLGJxtZic1e-hkQZz0qr",
  "audience": "https://eventhub-api",
  "grant_type": "client_credentials"
}
```

3. **Create Teambuilding**:
```bash
POST http://localhost:8000/teambuildings
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "name": "Summer Camp 2025",
  "description": "Exciting summer activities",
  "start_date": "2025-06-20",
  "end_date": "2025-06-23",
  "location": "Nha Trang"
}
```

## 📚 Dependencies Added

Các packages chính:
- `fastapi` - Web framework
- `sqlalchemy` - ORM
- `pydantic` - Data validation
- `python-jose` - JWT handling
- `python-auth0` - Auth0 SDK
- `alembic` - Database migrations
- `aiofiles` - Async file operations
- `pillow` - Image processing

## ✅ Validation Checklist

- [ ] Database models tạo thành công
- [ ] Schemas validation hoạt động
- [ ] Auth0 integration hoạt động
- [ ] Có thể login và get access token
- [ ] CRUD operations cho tất cả entities
- [ ] Image upload hoạt động
- [ ] API documentation tại /docs
- [ ] Authorization checks hoạt động
- [ ] Relationships giữa tables hoạt động

## ➡️ Next Steps

Sau khi hoàn thành Phase 2:
- **Phase 3: Frontend Web Development** - Xây dựng React Admin Portal

## 🐛 Common Issues

### Issue: Auth0 token verification failed
```bash
# Kiểm tra Auth0 configuration
# Verify JWKS endpoint accessible
# Check token expiration
```

### Issue: Database connection error
```bash
# Check PostgreSQL is running
docker-compose logs postgres

# Test connection
docker exec -it eventhub_postgres psql -U postgres -d eventhub_db
```

### Issue: CORS error
```bash
# Update CORS origins in main.py
# Check frontend URL matches
```
