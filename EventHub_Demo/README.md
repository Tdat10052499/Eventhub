# EventHub Demo - Teambuilding Management System

## 📋 Tổng quan dự án

EventHub là hệ thống quản lý các chuyến đi Teambuilding với 2 actors chính:
- **Admin**: Quản lý trên Website (React)
- **User**: Tham gia qua Mobile App (Flutter)

## 🏗️ Kiến trúc hệ thống

```
┌─────────────────┐         ┌──────────────────┐
│   React Web     │         │   Flutter Mobile │
│   (Admin)       │         │   (User)         │
└────────┬────────┘         └────────┬─────────┘
         │                           │
         └───────────┬───────────────┘
                     │
              ┌──────▼──────┐
              │    Nginx    │ (API Gateway)
              │  (Port 80)  │
              └──────┬──────┘
                     │
              ┌──────▼──────┐
              │   FastAPI   │ (Backend)
              │  (Port 8000)│
              └──────┬──────┘
                     │
              ┌──────▼──────┐
              │ PostgreSQL  │ (Database)
              │  (Port 5432)│
              └─────────────┘
```

## 🛠️ Tech Stack

- **Frontend Web**: React + Auth0
- **Mobile**: Flutter + Auth0
- **Backend**: FastAPI + Python
- **Database**: PostgreSQL
- **API Gateway**: Nginx
- **Container**: Docker & Docker Compose
- **Authentication**: Auth0

## 📊 Database Schema

### Users
- id (PK)
- auth0_id (unique)
- email
- name
- role (admin/user)
- created_at
- updated_at

### Teambuildings
- id (PK)
- name
- description
- start_date
- end_date
- location
- image_url
- created_by (FK -> Users)
- created_at
- updated_at

### Events
- id (PK)
- teambuilding_id (FK -> Teambuildings)
- name
- description
- event_date
- location
- image_url
- max_participants
- created_at
- updated_at

### Registrations
- id (PK)
- event_id (FK -> Events)
- user_id (FK -> Users)
- registration_date
- status (pending/confirmed/cancelled)
- notes
- created_at
- updated_at

## 🚀 Luồng hoạt động

### Luồng 1: Admin tạo sự kiện
1. Admin đăng nhập (Auth0)
2. Tạo Teambuilding mới
3. Tạo Events trong Teambuilding
4. Lưu vào PostgreSQL
5. Hiển thị trên dashboard

### Luồng 2: User đăng ký sự kiện
1. User đăng nhập Mobile (Auth0)
2. Xem danh sách Events
3. Điền form đăng ký
4. Lưu vào Registrations table
5. Hiển thị trên web Admin

### Luồng 3: Admin xem danh sách đăng ký
1. Admin mở danh sách registrations
2. Hiển thị thông tin người đăng ký

## 📦 Cấu trúc thư mục

```
EventHub_Demo/
├── backend/              # FastAPI application
├── frontend/             # React web application
├── mobile/               # Flutter application
├── nginx/                # Nginx configuration
├── database/             # PostgreSQL scripts
├── docker-compose.yml    # Docker orchestration
└── README.md
```

## ⚙️ Auth0 Configuration

### Web Application (EventHub)
- **Domain**: dev-q886n3eebgb8g04f.us.auth0.com
- **Client ID**: yGm0uw9aLN9YSe8qVB2mq79ylDSvoJcL
- **Callback URLs**: http://localhost:3000/callback
- **Logout URLs**: http://localhost:3000
- **Web Origins**: http://localhost:3000

### Mobile Application (Teambuilding)
- **Domain**: dev-q886n3eebgb8g04f.us.auth0.com
- **Client ID**: 2VjwUVUqQBdMPWvUuAIVayYILciirQwW
- **Callback URLs**: com.eventhub.teambuilding://dev-q886n3eebgb8g04f.us.auth0.com/android/com.eventhub.teambuilding/callback
- **Logout URLs**: com.eventhub.teambuilding://dev-q886n3eebgb8g04f.us.auth0.com/android/com.eventhub.teambuilding/logout

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 18+ (cho development)
- Flutter SDK (cho mobile development)
- Python 3.11+ (cho backend development)

### Chạy toàn bộ hệ thống với Docker Compose

```bash
# Clone repository và di chuyển vào thư mục
cd EventHub_Demo

# Khởi động tất cả services
docker-compose up -d

# Kiểm tra logs
docker-compose logs -f

# Dừng tất cả services
docker-compose down
```

### Truy cập các services

- **React Web (Admin)**: http://localhost:3000
- **FastAPI Backend**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **PostgreSQL**: localhost:5432
- **Nginx**: http://localhost:80

## 📚 Documentation

- [Phase 1: Project Setup & Infrastructure](./docs/PHASE1_SETUP.md)
- [Phase 2: Backend Development](./docs/PHASE2_BACKEND.md)
- [Phase 3: Frontend Web Development](./docs/PHASE3_FRONTEND.md)
- [Phase 4: Mobile Development](./docs/PHASE4_MOBILE.md)
- [Phase 5: Integration & Testing](./docs/PHASE5_INTEGRATION.md)

## 📝 Development Notes

### Environment Variables
Tất cả sensitive data được quản lý qua `.env` files trong mỗi service.

### Database Migrations
Backend sử dụng Alembic cho database migrations.

### Image Upload
Images được lưu trữ local trong volume Docker và serve qua FastAPI static files.

## 👥 Contributors

- Developer: Your Name

## 📄 License

This is a demo project for learning purposes.
