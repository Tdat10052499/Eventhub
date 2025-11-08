# Auth0 User Sync - Hướng Dẫn & Test

## 🎯 Tính năng đã implement

**Phương pháp 2: Sync User từ Auth0 vào Database**

Khi user đăng nhập qua Auth0:
1. ✅ Auth0 verify credentials
2. ✅ Frontend nhận JWT token
3. ✅ Frontend tự động gọi `/auth/me`
4. ✅ Backend tự động tạo/update user trong database
5. ✅ User data được lưu vào localStorage

## 📋 Cấu trúc Database

```sql
Table: users
- id (PK)
- auth0_id (UNIQUE) -- Auth0 'sub' claim
- email (UNIQUE)
- name
- role (admin/user)
- phone
- avatar_url
- created_at
- updated_at
```

## 🔄 Flow hoạt động

```
User Login (Auth0)
    ↓
Auth0 verify
    ↓
Frontend nhận token
    ↓
Frontend gọi GET /auth/me (với token)
    ↓
Backend verify token
    ↓
Backend extract: auth0_id, email, name
    ↓
Check database:
    - Nếu auth0_id đã tồn tại → Return existing user
    - Nếu chưa → Create new user → Return
    ↓
Frontend lưu user vào localStorage
```

## 🧪 Cách Test

### **Bước 1: Xóa cache và logout**
1. Mở http://localhost:3000
2. Mở DevTools (F12) → Console
3. Clear localStorage:
   ```javascript
   localStorage.clear();
   ```
4. Logout nếu đang login

### **Bước 2: Login với tài khoản mới**
1. Click "Login with Auth0"
2. Đăng nhập bằng tài khoản Auth0 của bạn
3. Sau khi redirect về dashboard, check Console logs:
   ```
   ✅ Getting access token...
   ✅ Token received: Yes
   ✅ Token saved to localStorage
   ✅ Syncing user with backend...
   ✅ User synced: {id: X, email: "...", name: "...", ...}
   ```

### **Bước 3: Kiểm tra Database**
```powershell
# Check user vừa tạo trong database
docker exec eventhub_postgres psql -U postgres -d eventhub_db -c "SELECT id, auth0_id, email, name, role, created_at FROM users ORDER BY created_at DESC LIMIT 5;"
```

Bạn sẽ thấy user mới được tạo với:
- ✅ `auth0_id` từ Auth0 (format: `auth0|xxxxx`)
- ✅ `email` từ Auth0
- ✅ `name` từ Auth0 profile
- ✅ `role` = 'user' (default)

### **Bước 4: Test Login lần 2**
1. Logout
2. Login lại với cùng tài khoản
3. Check database - số lượng users **không tăng** (vì đã tồn tại)
4. Console log:
   ```
   ✅ User synced: {id: X, ...} // Same ID as before
   ```

## 🔍 Debug Commands

### Xem tất cả users
```powershell
docker exec eventhub_postgres psql -U postgres -d eventhub_db -c "SELECT * FROM users;"
```

### Đếm users theo role
```powershell
docker exec eventhub_postgres psql -U postgres -d eventhub_db -c "SELECT role, COUNT(*) FROM users GROUP BY role;"
```

### Xem user mới nhất
```powershell
docker exec eventhub_postgres psql -U postgres -d eventhub_db -c "SELECT id, auth0_id, email, name, role, created_at FROM users ORDER BY created_at DESC LIMIT 1;"
```

### Xóa user test (nếu cần)
```powershell
docker exec eventhub_postgres psql -U postgres -d eventhub_db -c "DELETE FROM users WHERE email = 'your-test-email@example.com';"
```

## 📊 Expected Results

### **Lần đăng nhập đầu tiên:**
- ✅ User mới được tạo trong database
- ✅ `auth0_id` match với Auth0 sub claim
- ✅ `email`, `name` từ Auth0
- ✅ `role` = 'user' (default)
- ✅ Browser console: "User synced: {...}"

### **Lần đăng nhập thứ 2 trở đi:**
- ✅ Không tạo user mới (dùng existing user)
- ✅ Return cùng `id`
- ✅ User data có thể được update nếu Auth0 profile thay đổi

## 🎉 Benefits

1. **Authentication:** Auth0 handle security
2. **Authorization:** Database có user data để check permissions
3. **Relationships:** Can JOIN users ↔ registrations ↔ events
4. **Flexibility:** Có thể add custom fields (phone, address, ...)
5. **Reporting:** Query users dễ dàng

## 🚨 Troubleshooting

### Lỗi: "User synced failed"
- Check backend logs: `docker-compose logs backend --tail 50`
- Verify token có đúng audience: `https://eventhub-api`

### Lỗi: "duplicate key value violates unique constraint"
- User đã tồn tại với email/auth0_id
- Check: `SELECT * FROM users WHERE email = '...';`

### User không được tạo
- Check Console logs
- Verify API call: Network tab → `/auth/me` → Response
- Check backend endpoint working: `curl http://localhost:8000/docs`

## ✅ Success Criteria

- [ ] User mới được tạo sau login lần đầu
- [ ] User không duplicate khi login lại
- [ ] `auth0_id` match với Auth0
- [ ] Can query users from database
- [ ] Registrations có đúng `user_id`

---

**Status:** ✅ Implemented & Ready to Test
**Date:** November 8, 2025
