# Phase 4: Mobile App Development (Flutter)

## 🎯 Mục tiêu Phase 4

Xây dựng Flutter Mobile App cho Users với:
1. Auth0 Authentication
2. Event Listing & Details
3. Event Registration
4. User Profile
5. Registration History
6. Cross-platform (iOS & Android)

## 📱 App Structure

```
lib/
├── main.dart
├── config/
│   ├── auth_config.dart
│   └── api_config.dart
├── models/
│   ├── user.dart
│   ├── teambuilding.dart
│   ├── event.dart
│   └── registration.dart
├── services/
│   ├── auth_service.dart
│   ├── api_service.dart
│   ├── event_service.dart
│   └── registration_service.dart
├── providers/
│   ├── auth_provider.dart
│   ├── event_provider.dart
│   └── registration_provider.dart
├── screens/
│   ├── splash_screen.dart
│   ├── login_screen.dart
│   ├── home_screen.dart
│   ├── event_list_screen.dart
│   ├── event_detail_screen.dart
│   ├── registration_form_screen.dart
│   ├── registration_history_screen.dart
│   └── profile_screen.dart
├── widgets/
│   ├── event_card.dart
│   ├── registration_card.dart
│   ├── custom_button.dart
│   ├── loading_widget.dart
│   └── error_widget.dart
└── utils/
    ├── constants.dart
    ├── helpers.dart
    └── validators.dart
```

## 🔐 Auth0 Integration

### Dependencies
```yaml
dependencies:
  flutter_appauth: ^6.0.2
  flutter_secure_storage: ^9.0.0
  http: ^1.1.0
  provider: ^6.1.1
```

### Auth0 Configuration
```dart
// config/auth_config.dart
class Auth0Config {
  static const String domain = 'dev-q886n3eebgb8g04f.us.auth0.com';
  static const String clientId = '2VjwUVUqQBdMPWvUuAIVayYILciirQwW';
  static const String redirectUri = 'com.eventhub.teambuilding://callback';
  static const String audience = 'https://eventhub-api';
}
```

### Auth Service
```dart
class AuthService {
  final FlutterAppAuth appAuth = FlutterAppAuth();
  final FlutterSecureStorage secureStorage = FlutterSecureStorage();

  Future<void> login() async {
    final AuthorizationTokenResponse result = await appAuth.authorizeAndExchangeCode(
      AuthorizationTokenRequest(
        Auth0Config.clientId,
        Auth0Config.redirectUri,
        issuer: 'https://${Auth0Config.domain}',
        scopes: ['openid', 'profile', 'email', 'offline_access'],
        audience: Auth0Config.audience,
      ),
    );
    
    await secureStorage.write(key: 'access_token', value: result.accessToken);
  }

  Future<void> logout() async {
    await secureStorage.delete(key: 'access_token');
  }
}
```

## 📱 Screens & Features

### 1. Splash Screen
- Logo animation
- Check authentication status
- Navigate to Login hoặc Home

### 2. Login Screen
**Features**:
- Auth0 login button
- Social login (Google, Facebook)
- App branding

### 3. Home Screen
**Features**:
- Welcome message với user name
- Quick stats (upcoming events, my registrations)
- Navigation to main features
- Bottom navigation bar

### 4. Event List Screen
**Features**:
- List tất cả available events
- Filter by teambuilding
- Search events
- Sort by date, name
- Pull to refresh
- Event card với:
  - Event image
  - Event name
  - Date & location
  - Available slots
  - Register button

### 5. Event Detail Screen
**Features**:
- Full event information
- Image gallery
- Event description
- Date, time, location
- Max participants & available slots
- Teambuilding info
- Register button
- Share event

### 6. Registration Form Screen
**Features**:
- Event summary
- User info (pre-filled from profile)
- Additional notes field
- Terms & conditions checkbox
- Submit registration
- Loading state
- Success/Error feedback

**Form Fields**:
- User name (pre-filled)
- Email (pre-filled)
- Phone (editable)
- Notes (optional)

### 7. Registration History Screen
**Features**:
- List user's registrations
- Filter by status (all, pending, confirmed, cancelled)
- Registration card với:
  - Event name & image
  - Registration date
  - Status badge
  - View details button
  - Cancel registration option

### 8. Profile Screen
**Features**:
- User avatar
- User info (name, email, phone)
- Edit profile
- My statistics
- Settings
- Logout button

## 🎨 UI/UX Design

### Color Scheme
```dart
// utils/constants.dart
class AppColors {
  static const Color primary = Color(0xFF1976D2);
  static const Color secondary = Color(0xFFDC004E);
  static const Color success = Color(0xFF4CAF50);
  static const Color warning = Color(0xFFFF9800);
  static const Color error = Color(0xFFF44336);
  static const Color background = Color(0xFFF5F5F5);
  static const Color white = Color(0xFFFFFFFF);
  static const Color text = Color(0xFF212121);
  static const Color textLight = Color(0xFF757575);
}
```

### Typography
```dart
class AppTextStyles {
  static const TextStyle heading1 = TextStyle(
    fontSize: 24,
    fontWeight: FontWeight.bold,
    color: AppColors.text,
  );
  
  static const TextStyle body = TextStyle(
    fontSize: 16,
    color: AppColors.text,
  );
}
```

## 🔧 API Integration

### API Service
```dart
class ApiService {
  final String baseUrl = 'http://localhost/api';
  final FlutterSecureStorage storage = FlutterSecureStorage();

  Future<Map<String, String>> _getHeaders() async {
    final token = await storage.read(key: 'access_token');
    return {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer $token',
    };
  }

  Future<List<Event>> getEvents() async {
    final response = await http.get(
      Uri.parse('$baseUrl/events'),
      headers: await _getHeaders(),
    );
    
    if (response.statusCode == 200) {
      final List<dynamic> data = json.decode(response.body);
      return data.map((json) => Event.fromJson(json)).toList();
    } else {
      throw Exception('Failed to load events');
    }
  }

  Future<Registration> createRegistration(int eventId, String notes) async {
    final response = await http.post(
      Uri.parse('$baseUrl/registrations'),
      headers: await _getHeaders(),
      body: json.encode({
        'event_id': eventId,
        'notes': notes,
      }),
    );
    
    if (response.statusCode == 201) {
      return Registration.fromJson(json.decode(response.body));
    } else {
      throw Exception('Failed to create registration');
    }
  }
}
```

## 🏗️ State Management

### Using Provider

```dart
// providers/event_provider.dart
class EventProvider with ChangeNotifier {
  List<Event> _events = [];
  bool _loading = false;
  String? _error;

  List<Event> get events => _events;
  bool get loading => _loading;
  String? get error => _error;

  Future<void> fetchEvents() async {
    _loading = true;
    _error = null;
    notifyListeners();

    try {
      _events = await ApiService().getEvents();
    } catch (e) {
      _error = e.toString();
    } finally {
      _loading = false;
      notifyListeners();
    }
  }
}
```

## 📦 Dependencies

### pubspec.yaml
```yaml
name: teambuilding
description: EventHub Teambuilding Mobile App

dependencies:
  flutter:
    sdk: flutter
  
  # State Management
  provider: ^6.1.1
  
  # Authentication
  flutter_appauth: ^6.0.2
  flutter_secure_storage: ^9.0.0
  
  # HTTP & API
  http: ^1.1.0
  dio: ^5.4.0
  
  # UI Components
  cached_network_image: ^3.3.0
  flutter_svg: ^2.0.9
  intl: ^0.18.1
  
  # Navigation
  go_router: ^12.1.3
  
  # Utilities
  shared_preferences: ^2.2.2
  url_launcher: ^6.2.2
  image_picker: ^1.0.5

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.0
```

## 🧪 Testing

### Manual Testing Checklist:
- [ ] Login with Auth0 works on iOS
- [ ] Login with Auth0 works on Android
- [ ] Can view event list
- [ ] Can view event details
- [ ] Can register for event
- [ ] Registration appears in history
- [ ] Can view registration history
- [ ] Can filter registrations
- [ ] Can view profile
- [ ] Can edit profile
- [ ] Logout works
- [ ] Images load properly
- [ ] Offline handling
- [ ] Error messages display

## 🚀 Build & Run

### Development
```bash
# Get dependencies
flutter pub get

# Run on Android emulator
flutter run -d android

# Run on iOS simulator (macOS only)
flutter run -d ios

# Run on physical device
flutter devices
flutter run -d <device_id>
```

### Build APK
```bash
# Build APK for Android
flutter build apk --release

# Build App Bundle
flutter build appbundle --release
```

### Build iOS (macOS only)
```bash
# Build iOS app
flutter build ios --release
```

## 📱 Platform-Specific Setup

### Android (android/app/src/main/AndroidManifest.xml)
```xml
<intent-filter>
    <action android:name="android.intent.action.VIEW" />
    <category android:name="android.intent.category.DEFAULT" />
    <category android:name="android.intent.category.BROWSABLE" />
    <data
        android:scheme="com.eventhub.teambuilding"
        android:host="callback" />
</intent-filter>
```

### iOS (ios/Runner/Info.plist)
```xml
<key>CFBundleURLTypes</key>
<array>
    <dict>
        <key>CFBundleURLSchemes</key>
        <array>
            <string>com.eventhub.teambuilding</string>
        </array>
    </dict>
</array>
```

## ✅ Validation Checklist

- [ ] Auth0 login works
- [ ] Token stored securely
- [ ] API calls authenticated
- [ ] Event list displays
- [ ] Event details displays
- [ ] Registration form works
- [ ] Registration history works
- [ ] Profile displays
- [ ] Logout works
- [ ] Cross-platform compatible
- [ ] Error handling
- [ ] Loading states

## ➡️ Next Steps

Sau khi hoàn thành Phase 4:
- **Phase 5: Integration & Testing** - End-to-end testing và deployment

## 🐛 Common Issues

### Issue: Auth0 redirect not working
```dart
// Check callback URL scheme
// Verify platform-specific setup
```

### Issue: Network connection error
```dart
// Check API_URL configuration
// Test on real device/emulator with network
// Check Android network permissions
```

### Issue: Build failed
```bash
# Clean and rebuild
flutter clean
flutter pub get
flutter build apk
```
