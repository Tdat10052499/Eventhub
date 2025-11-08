# Phase 1: Project Setup & Infrastructure

## 🎯 Mục tiêu Phase 1

Trong phase này, chúng ta sẽ thiết lập:
1. ✅ Cấu trúc thư mục project
2. ✅ Docker & Docker Compose configuration
3. ✅ PostgreSQL setup với schema ban đầu
4. ✅ Nginx configuration cho API Gateway
5. ✅ Environment variables configuration

## 📂 Cấu trúc thư mục đã tạo

```
EventHub_Demo/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models/
│   │   ├── routers/
│   │   ├── schemas/
│   │   └── utils/
│   ├── alembic/
│   ├── uploads/              # Thư mục lưu ảnh upload
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── utils/
│   │   ├── App.js
│   │   └── index.js
│   ├── package.json
│   ├── Dockerfile
│   └── .env
│
├── mobile/
│   ├── lib/
│   │   ├── main.dart
│   │   ├── screens/
│   │   ├── services/
│   │   ├── models/
│   │   └── widgets/
│   ├── pubspec.yaml
│   └── .env
│
├── nginx/
│   ├── nginx.conf
│   └── Dockerfile
│
├── database/
│   ├── init.sql              # Initial database schema
│   └── seed.sql              # Sample data
│
├── docs/
│   ├── PHASE1_SETUP.md
│   ├── PHASE2_BACKEND.md
│   ├── PHASE3_FRONTEND.md
│   ├── PHASE4_MOBILE.md
│   └── PHASE5_INTEGRATION.md
│
├── docker-compose.yml
├── .gitignore
└── README.md
```

## 🐳 Docker Services

### 1. PostgreSQL Database
- **Container name**: eventhub_postgres
- **Port**: 5432
- **Database**: eventhub_db
- **Username**: postgres
- **Password**: postgres123
- **Volume**: Persistent data storage

### 2. FastAPI Backend
- **Container name**: eventhub_backend
- **Port**: 8000
- **Dependencies**: PostgreSQL
- **Features**:
  - Hot reload enabled
  - Volume mapping cho development
  - Image upload support

### 3. React Frontend
- **Container name**: eventhub_frontend
- **Port**: 3000
- **Dependencies**: Backend API
- **Features**:
  - Hot reload enabled
  - Auth0 integration

### 4. Nginx API Gateway
- **Container name**: eventhub_nginx
- **Port**: 80
- **Function**: Route requests to appropriate services
- **Routes**:
  - `/api/*` → Backend (port 8000)
  - `/*` → Frontend (port 3000)

## 🗄️ Database Schema

### Table: users
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    auth0_id VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'user',
    avatar_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Table: teambuildings
```sql
CREATE TABLE teambuildings (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    location VARCHAR(255),
    image_url VARCHAR(500),
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Table: events
```sql
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    teambuilding_id INTEGER REFERENCES teambuildings(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    event_date TIMESTAMP NOT NULL,
    location VARCHAR(255),
    image_url VARCHAR(500),
    max_participants INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Table: registrations
```sql
CREATE TABLE registrations (
    id SERIAL PRIMARY KEY,
    event_id INTEGER REFERENCES events(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id),
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'pending',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(event_id, user_id)
);
```

## 🔧 Configuration Files

### docker-compose.yml
Orchestrate tất cả services với dependencies và networking.

### Backend .env
```env
DATABASE_URL=postgresql://postgres:postgres123@eventhub_postgres:5432/eventhub_db
AUTH0_DOMAIN=dev-q886n3eebgb8g04f.us.auth0.com
AUTH0_API_AUDIENCE=https://eventhub-api
AUTH0_ALGORITHMS=RS256
AUTH0_ISSUER=https://dev-q886n3eebgb8g04f.us.auth0.com/
UPLOAD_DIR=/app/uploads
```

### Frontend .env
```env
REACT_APP_API_URL=http://localhost/api
REACT_APP_AUTH0_DOMAIN=dev-q886n3eebgb8g04f.us.auth0.com
REACT_APP_AUTH0_CLIENT_ID=yGm0uw9aLN9YSe8qVB2mq79ylDSvoJcL
REACT_APP_AUTH0_REDIRECT_URI=http://localhost:3000/callback
REACT_APP_AUTH0_AUDIENCE=https://eventhub-api
```

### Nginx nginx.conf
Routes configuration cho API Gateway.

## 🚀 Cách chạy

### Bước 1: Khởi động tất cả services
```bash
cd EventHub_Demo
docker-compose up -d
```

### Bước 2: Kiểm tra services đang chạy
```bash
docker-compose ps
```

### Bước 3: Xem logs
```bash
# Xem tất cả logs
docker-compose logs -f

# Xem logs của service cụ thể
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
docker-compose logs -f nginx
```

### Bước 4: Kiểm tra database
```bash
# Kết nối vào PostgreSQL container
docker exec -it eventhub_postgres psql -U postgres -d eventhub_db

# Kiểm tra tables
\dt

# Thoát
\q
```

### Bước 5: Test API
```bash
# Health check
curl http://localhost/api/health

# API Documentation
# Mở browser: http://localhost:8000/docs
```

## 🛠️ Troubleshooting

### Problem: Port đã được sử dụng
```bash
# Kiểm tra port đang sử dụng
netstat -ano | findstr :80
netstat -ano | findstr :3000
netstat -ano | findstr :5432
netstat -ano | findstr :8000

# Dừng process hoặc thay đổi port trong docker-compose.yml
```

### Problem: Database connection failed
```bash
# Kiểm tra PostgreSQL đã chạy chưa
docker-compose logs postgres

# Restart PostgreSQL
docker-compose restart postgres
```

### Problem: Container không start
```bash
# Xem chi tiết lỗi
docker-compose logs [service_name]

# Rebuild container
docker-compose up -d --build [service_name]
```

## 🧪 Validation Checklist

- [ ] Docker Compose khởi động thành công tất cả 4 services
- [ ] PostgreSQL accessible tại localhost:5432
- [ ] Backend API accessible tại http://localhost:8000
- [ ] Backend API docs accessible tại http://localhost:8000/docs
- [ ] Frontend accessible tại http://localhost:3000
- [ ] Nginx routing hoạt động: http://localhost/api → backend
- [ ] Database tables được tạo thành công
- [ ] Có thể insert test data vào database

## ➡️ Next Steps

Sau khi hoàn thành Phase 1, chuyển sang:
- **Phase 2: Backend Development** - Xây dựng FastAPI endpoints với Auth0 integration

## 📚 Resources

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
