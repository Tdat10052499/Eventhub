-- EventHub Database Seed Data
-- Sample data for testing and development

-- Insert sample admin user
INSERT INTO users (auth0_id, email, name, role, phone) VALUES
('auth0|admin001', 'admin@eventhub.com', 'Admin User', 'admin', '+84901234567'),
('auth0|user001', 'user1@example.com', 'Nguyen Van A', 'user', '+84901234568'),
('auth0|user002', 'user2@example.com', 'Tran Thi B', 'user', '+84901234569'),
('auth0|user003', 'user3@example.com', 'Le Van C', 'user', '+84901234570'),
('auth0|user004', 'user4@example.com', 'Pham Thi D', 'user', '+84901234571');

-- Insert sample teambuildings
INSERT INTO teambuildings (name, description, start_date, end_date, location, budget, created_by) VALUES
(
    'Team Building Mùa Xuân 2025',
    'Chuyến teambuilding đầu năm 2025 tại Đà Lạt với nhiều hoạt động thú vị và ý nghĩa.',
    '2025-03-15',
    '2025-03-17',
    'Đà Lạt, Lâm Đồng',
    50000000.00,
    1
),
(
    'Summer Camp 2025',
    'Hành trình khám phá biển đảo Nha Trang với các hoạt động dưới nước và dã ngoại.',
    '2025-06-20',
    '2025-06-23',
    'Nha Trang, Khánh Hòa',
    75000000.00,
    1
),
(
    'Teambuilding Mùa Thu 2025',
    'Trải nghiệm văn hóa và ẩm thực tại Hội An cùng các hoạt động gắn kết đội nhóm.',
    '2025-09-10',
    '2025-09-12',
    'Hội An, Quảng Nam',
    60000000.00,
    1
);

-- Insert sample events for Teambuilding 1 (Mùa Xuân)
INSERT INTO events (teambuilding_id, name, description, event_date, location, max_participants, status) VALUES
(
    1,
    'Lễ Khai Mạc và Ice Breaking',
    'Hoạt động khởi động với các trò chơi ice breaking giúp mọi người làm quen và gắn kết.',
    '2025-03-15 14:00:00',
    'Resort Dalat Wonder',
    100,
    'open'
),
(
    1,
    'Team Challenge - Leo Núi Langbiang',
    'Thử thách leo núi Langbiang với độ cao 2,167m. Mỗi team sẽ cùng nhau vượt qua thử thách.',
    '2025-03-16 06:00:00',
    'Núi Langbiang',
    80,
    'open'
),
(
    1,
    'Đêm Lửa Trại và Gala Dinner',
    'Buổi tối gala dinner với BBQ, đốt lửa trại, và các tiết mục văn nghệ của các team.',
    '2025-03-16 18:00:00',
    'Resort Dalat Wonder',
    100,
    'open'
),
(
    1,
    'Workshop: Kỹ Năng Làm Việc Nhóm',
    'Workshop về kỹ năng làm việc nhóm hiệu quả và giải quyết xung đột.',
    '2025-03-17 09:00:00',
    'Resort Dalat Wonder',
    50,
    'open'
);

-- Insert sample events for Teambuilding 2 (Summer Camp)
INSERT INTO events (teambuilding_id, name, description, event_date, location, max_participants, status) VALUES
(
    2,
    'Beach Activities & Water Sports',
    'Các hoạt động thể thao dưới nước: lặn biển, lướt ván, kayak.',
    '2025-06-20 08:00:00',
    'Bãi biển Nha Trang',
    60,
    'open'
),
(
    2,
    'Island Hopping Tour',
    'Tour tham quan các đảo: Hòn Mun, Hòn Tằm, Hòn Miễu.',
    '2025-06-21 07:00:00',
    'Các đảo Nha Trang',
    80,
    'open'
),
(
    2,
    'Beach Party & BBQ Night',
    'Tiệc BBQ trên bãi biển với DJ và các trò chơi team building.',
    '2025-06-21 18:00:00',
    'Beach Club Nha Trang',
    100,
    'open'
);

-- Insert sample events for Teambuilding 3 (Mùa Thu)
INSERT INTO events (teambuilding_id, name, description, event_date, location, max_participants, status) VALUES
(
    3,
    'Walking Tour Phố Cổ Hội An',
    'Tham quan phố cổ Hội An, tìm hiểu văn hóa và lịch sử.',
    '2025-09-10 15:00:00',
    'Phố Cổ Hội An',
    80,
    'open'
),
(
    3,
    'Cooking Class - Ẩm Thực Việt',
    'Học nấu các món ăn truyền thống Việt Nam theo nhóm.',
    '2025-09-11 09:00:00',
    'Red Bridge Cooking School',
    40,
    'open'
),
(
    3,
    'Thả Đèn Lồng Sông Hoài',
    'Hoạt động thả đèn lồng trên sông Hoài vào buổi tối.',
    '2025-09-11 19:00:00',
    'Sông Hoài, Hội An',
    100,
    'open'
);

-- Insert sample registrations
INSERT INTO registrations (event_id, user_id, status, notes) VALUES
-- User 1 registrations
(1, 2, 'confirmed', 'Đã xác nhận tham gia'),
(2, 2, 'confirmed', 'Sẵn sàng cho thử thách'),
(3, 2, 'confirmed', 'Rất mong chờ'),

-- User 2 registrations
(1, 3, 'confirmed', 'Đã thanh toán'),
(2, 3, 'pending', 'Đang chờ xác nhận sức khỏe'),
(4, 3, 'confirmed', 'Đăng ký tham gia workshop'),

-- User 3 registrations
(5, 4, 'confirmed', 'Thích hoạt động dưới nước'),
(6, 4, 'confirmed', 'Đã đăng ký tour'),

-- User 4 registrations
(8, 5, 'confirmed', 'Yêu thích Hội An'),
(9, 5, 'pending', 'Cần xác nhận lịch'),
(10, 5, 'confirmed', 'Mong chờ hoạt động này');

-- Success message
DO $$
DECLARE
    user_count INTEGER;
    teambuilding_count INTEGER;
    event_count INTEGER;
    registration_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO user_count FROM users;
    SELECT COUNT(*) INTO teambuilding_count FROM teambuildings;
    SELECT COUNT(*) INTO event_count FROM events;
    SELECT COUNT(*) INTO registration_count FROM registrations;
    
    RAISE NOTICE '========================================';
    RAISE NOTICE 'Sample data inserted successfully!';
    RAISE NOTICE '========================================';
    RAISE NOTICE 'Users: %', user_count;
    RAISE NOTICE 'Teambuildings: %', teambuilding_count;
    RAISE NOTICE 'Events: %', event_count;
    RAISE NOTICE 'Registrations: %', registration_count;
    RAISE NOTICE '========================================';
END $$;
