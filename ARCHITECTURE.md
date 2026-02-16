# Naija Connect - Architecture & File Organization

## 🏗️ Complete Project Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER BROWSER                              │
│              (HTML5 + CSS3 + JavaScript)                     │
└────────────────────────┬────────────────────────────────────┘
                         │
         ┌───────────────┴────────────────┐
         │                                │
    HTTP Requests                   Service Worker
    JSON API Calls                  (Offline Cache)
         │                                │
         └───────────────┬────────────────┘
                         │
┌─────────────────────────▼────────────────────────────────────┐
│              FLASK WEB SERVER (Port 5000)                    │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  /              → Serve index.html                            │
│  /static/css/*  → Serve CSS files                             │
│  /static/js/*   → Serve JavaScript files                      │
│  /manifest.json → PWA manifest                                │
│  /api/login     → User authentication                         │
│  /api/services  → Service listing & creation                  │
│  /api/bookings  → Booking management                          │
│  /api/reviews   → Review system                               │
│  /api/payment   → Payment processing                          │
│  /api/admin/*   → Admin dashboard                             │
│                                                               │
└─────────────────────────▼────────────────────────────────────┘
                         │
┌─────────────────────────▼────────────────────────────────────┐
│            SQLALCHEMY ORM & DATABASE LAYER                   │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌────────────────────────────────────────────────────┐     │
│  │              SQLite Database                        │     │
│  │         (naija_connect.db)                          │     │
│  │                                                     │     │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐         │     │
│  │  │  Users   │  │ Services │  │ Bookings │         │     │
│  │  └──────────┘  └──────────┘  └──────────┘         │     │
│  │                                                     │     │
│  │  ┌──────────┐  ┌──────────┐                        │     │
│  │  │ Reviews  │  │ Payments │                        │     │
│  │  └──────────┘  └──────────┘                        │     │
│  │                                                     │     │
│  └────────────────────────────────────────────────────┘     │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## 📂 File Organization

```
project/
│
├─ README.md ........................ Full documentation
├─ QUICKSTART.md ................... 5-minute setup
├─ PROJECT_SUMMARY.md ............. This summary
│
├─ backend/
│  │
│  ├─ app.py ........................ Main Flask app
│  │  ├─ Models (User, Service, Booking, Review, Payment)
│  │  ├─ Routes (/api/*)
│  │  ├─ Authentication (JWT)
│  │  └─ Database (SQLAlchemy)
│  │
│  └─ requirements.txt ............. Python dependencies
│
├─ frontend/
│  │
│  ├─ templates/
│  │  └─ index.html ................. Single-page application
│  │     ├─ Header & Navigation
│  │     ├─ Hero Section
│  │     ├─ Services Grid
│  │     ├─ Modals (Login, Register, Booking, etc.)
│  │     └─ Footer
│  │
│  └─ static/
│     │
│     ├─ css/
│     │  └─ style.css .............. All styling (responsive)
│     │     ├─ CSS Variables
│     │     ├─ Components
│     │     ├─ Modals
│     │     ├─ Forms
│     │     ├─ Dashboard
│     │     └─ Responsive Design
│     │
│     └─ js/
│        ├─ app.js ................. Core JavaScript
│        │  ├─ Authentication (login/register)
│        │  ├─ API Calls
│        │  ├─ Service Management
│        │  ├─ Bookings
│        │  ├─ Modals
│        │  └─ UI Interactions
│        │
│        ├─ service-worker.js ...... PWA offline support
│        │  ├─ Cache Strategy
│        │  ├─ Fetch Events
│        │  └─ Update Management
│        │
│        └─ service-worker-register.js
│           └─ Service Worker Registration
│
└─ admin/
   │
   ├─ README.md ................... Admin documentation
   └─ admin_login.py ............. Admin setup & credentials
      ├─ Admin user creation
      ├─ Default credentials
      └─ Authentication logic
```

## 🔄 Data Flow

### User Registration Flow
```
User Input (Frontend)
        ↓
form submission event
        ↓
handleRegister() function
        ↓
apiCall('/register', 'POST', data)
        ↓
Flask @app.route('/api/register', methods=['POST'])
        ↓
Create User model instance
        ↓
Hash password with Werkzeug
        ↓
Save to SQLite database
        ↓
Return JSON response
        ↓
Update localStorage with token
        ↓
Show success alert
```

### Service Listing Flow
```
Page Load
        ↓
checkAuth() - Verify user
        ↓
loadServices()
        ↓
apiCall('/services', 'GET')
        ↓
Flask retrieves from database
        ↓
Return JSON array
        ↓
JavaScript creates service cards
        ↓
Display in services-grid
```

### Booking Flow
```
Click "Book Service"
        ↓
showBookingModal()
        ↓
User fills booking form
        ↓
handleBooking() submission
        ↓
apiCall('/bookings', 'POST', data)
        ↓
Create Booking model
        ↓
Save to database
        ↓
Show payment prompt
        ↓
apiCall('/payment', 'POST', data)
        ↓
Update payment status
        ↓
Show success & transaction ID
```

## 🌐 API Endpoint Structure

```
Flask App
├─ Frontend Routes
│  ├─ GET  /                    (Serve index.html)
│  ├─ GET  /static/css/*        (Serve styles)
│  ├─ GET  /static/js/*         (Serve scripts)
│  └─ GET  /manifest.json       (PWA manifest)
│
├─ Authentication Routes
│  ├─ POST /api/register        (New user)
│  └─ POST /api/login           (User login)
│
├─ Service Routes
│  ├─ GET  /api/services        (List with filters)
│  ├─ POST /api/services        (Create service)
│  └─ GET  /api/services/<id>   (Service details)
│
├─ Booking Routes
│  ├─ POST /api/bookings        (Create booking)
│  ├─ GET  /api/bookings        (Get user bookings)
│  └─ PUT  /api/bookings/<id>/status
│
├─ Review Routes
│  ├─ POST /api/reviews         (Create review)
│  └─ GET  /api/reviews/<id>    (Get reviews)
│
├─ Payment Routes
│  └─ POST /api/payment         (Process payment)
│
└─ Admin Routes
   └─ GET  /api/admin/analytics (Dashboard data)
```

## 🗄️ Database Schema

```
User Table
├─ id (Primary Key)
├─ username (Unique)
├─ email (Unique)
├─ password_hash
├─ full_name
├─ phone
├─ is_provider (Boolean)
├─ is_admin (Boolean)
└─ created_at (Timestamp)

Service Table
├─ id (Primary Key)
├─ title
├─ description
├─ category
├─ price
├─ location
├─ provider_id (Foreign Key → User)
├─ image_url
├─ is_active
└─ created_at

Booking Table
├─ id (Primary Key)
├─ service_id (Foreign Key → Service)
├─ customer_id (Foreign Key → User)
├─ booking_date
├─ status (pending/confirmed/completed/cancelled)
├─ payment_status (unpaid/paid/refunded)
├─ total_amount
├─ notes
└─ created_at

Review Table
├─ id (Primary Key)
├─ service_id (Foreign Key → Service)
├─ reviewer_id (Foreign Key → User)
├─ rating (1-5)
├─ comment
└─ created_at

Payment Table
├─ id (Primary Key)
├─ booking_id (Foreign Key → Booking)
├─ amount
├─ currency (NGN)
├─ payment_method
├─ transaction_id (Unique)
├─ status (pending/completed/failed)
└─ created_at
```

## 🔐 Authentication Flow

```
Login Request
        ↓
Check username in database
        ↓
Verify password hash
        ↓
Generate JWT token
        ↓
Return token + user data
        ↓
Store in localStorage
        ↓
Include in future API calls
        ├─ Authorization: Bearer <token>
        │
        └─ Verified by @token_required decorator
           ├─ Extract token
           ├─ Decode with SECRET_KEY
           ├─ Get current_user from database
           └─ Pass to route function
```

## 🎨 Frontend Component Structure

```
index.html
├─ Header
│  ├─ Logo
│  ├─ Navigation Menu
│  └─ User Auth Buttons
│
├─ Hero Section
│  ├─ Title & Subtitle
│  └─ Search Box
│
├─ Services Section
│  └─ Dynamic Service Cards Grid
│
├─ Categories Section
│  └─ 6 Category Cards
│
├─ How It Works Section
│  └─ 4 Step Process
│
├─ Footer
│  ├─ About
│  ├─ Quick Links
│  └─ Contact
│
└─ Modals (Hidden)
   ├─ Login Modal
   ├─ Register Modal
   ├─ Booking Modal
   ├─ Service Details Modal
   └─ Dashboard Modal
```

## 📊 File Sizes

```
backend/
├─ app.py ..................... ~15 KB (448 lines)
└─ requirements.txt ............ <1 KB

frontend/
├─ templates/index.html ....... ~10 KB (281 lines)
└─ static/
   ├─ css/style.css ........... ~25 KB (664 lines)
   └─ js/
      ├─ app.js .............. ~15 KB (415 lines)
      ├─ service-worker.js ... ~2 KB (72 lines)
      └─ service-worker-register.js <1 KB

admin/
├─ admin_login.py ............ <1 KB
└─ README.md ................. <1 KB

Documentation/
├─ README.md ................. ~7 KB
├─ QUICKSTART.md ............. ~4 KB
└─ PROJECT_SUMMARY.md ........ ~5 KB
```

## 🚀 Deployment Strategy

```
Development
├─ Flask debug mode
├─ SQLite database
└─ localhost:5000

Production
├─ Gunicorn WSGI server
├─ PostgreSQL/MySQL database
├─ Environment variables
├─ HTTPS (SSL)
├─ CDN for static files
└─ Proper domain & DNS
```

---

**This architecture provides a complete, scalable service marketplace platform!**
