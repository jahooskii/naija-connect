# 🎉 NAIJA CONNECT - Complete Setup Guide

## Welcome! 👋

**Naija Connect** is a modern, fully-responsive service marketplace platform designed for Nigeria and beyond. It's now ready to share and deploy!

---

## ✅ What You Get

✓ **Full-Featured Backend** - Flask REST API with JWT authentication  
✓ **Beautiful Frontend** - Responsive HTML/CSS/JavaScript  
✓ **Admin Dashboard** - Complete management interface  
✓ **Database** - SQLite with 5 core models  
✓ **PWA Support** - Progressive Web App (works offline)  
✓ **Mobile Ready** - 100% responsive on all devices  

---

## 🚀 Quick Start (5 minutes)

### Step 1: Install Python Requirements
```bash
cd naija-connect-app/backend
pip3 install -r requirements.txt
```

### Step 2: Start the Server
```bash
python3 app.py
```

### Step 3: Open in Browser
- **Main App**: `http://localhost:5001`
- **Admin Panel**: `http://localhost:5001/admin`

---

## 🔐 Admin Access

### Default Admin Credentials:
- **Username**: `admin`
- **Password**: `admin123`

### First Time Admin Setup:
```bash
cd naija-connect-app/backend
python3
```

Then run:
```python
from app import app, db, User

with app.app_context():
    admin = User(
        username='admin',
        email='admin@naijaconnect.ng',
        full_name='Admin User',
        is_admin=True
    )
    admin.set_password('admin123')
    db.session.add(admin)
    db.session.commit()
    print('✅ Admin user created successfully')
    exit()
```

---

## 📱 Main Application Features

### For Customers:
- 🔍 **Search & Browse** - Find services by category
- 📝 **Register & Login** - Secure authentication
- 🛒 **Book Services** - Reserve services with dates
- 💳 **Make Payments** - Secure payment processing
- ⭐ **Leave Reviews** - Rate and review services

### Service Categories:
- Plumbing
- Electrical
- Cleaning
- Carpentry
- Painting
- General Repairs

---

## 🎛️ Admin Dashboard Features

### Overview
- 📊 Total Users count
- 🔧 Total Services count
- 📅 Total Bookings count
- 💰 Total Revenue tracking

### Management Sections
1. **Users** - Manage user accounts
2. **Services** - Monitor all services
3. **Bookings** - Track all bookings
4. **Reviews** - Manage customer reviews
5. **Payments** - View payment transactions
6. **Analytics** - Detailed reports and insights

---

## 🛠️ Technical Details

### Backend Stack
- **Framework**: Flask 3.0.0
- **Database**: SQLAlchemy ORM with SQLite
- **Authentication**: JWT tokens
- **API**: RESTful endpoints
- **CORS**: Enabled for cross-origin requests

### Frontend Stack
- **HTML5** - Semantic markup
- **CSS3** - Modern responsive design
- **Vanilla JavaScript** - No external dependencies
- **PWA** - Service workers for offline support

### Database Models
1. **User** - Customer & provider accounts
2. **Service** - Available services
3. **Booking** - Service bookings
4. **Review** - Customer reviews
5. **Payment** - Transaction records

---

## 📁 Project Structure

```
naija-connect-app/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── requirements.txt    # Python dependencies
│   └── naija_connect.db    # SQLite database
├── frontend/
│   ├── templates/
│   │   ├── index.html      # Main application
│   │   └── admin.html      # Admin dashboard
│   └── static/
│       ├── css/
│       │   └── style.css   # Responsive styles
│       └── js/
│           ├── app.js      # Main app logic
│           ├── service-worker.js      # PWA support
│           └── service-worker-register.js
└── README.md               # This file
```

---

## 🌐 Access URLs

| Page | URL | Access |
|------|-----|--------|
| Main App | `http://localhost:5001` | Everyone |
| Admin Panel | `http://localhost:5001/admin` | Admin only |
| API Root | `http://localhost:5001/api` | Mobile/External apps |

---

## 📱 Device Compatibility

✅ **Desktop Browsers**
- Chrome/Chromium ✓
- Firefox ✓
- Safari ✓
- Edge ✓

✅ **Mobile Devices**
- iPhone (iOS 12+) ✓
- Android (5+) ✓
- Tablets ✓
- Any modern browser ✓

✅ **Responsive Breakpoints**
- Desktop (1200px+)
- Tablet (768px - 1199px)
- Mobile (480px - 767px)
- Small Mobile (<480px)

---

## 🔌 API Endpoints

### Authentication
```
POST /api/register      - Register new user
POST /api/login         - User login
POST /api/admin-login   - Admin login
```

### Services
```
GET  /api/services           - List all services
GET  /api/services/<id>      - Get service details
POST /api/services           - Create service (provider)
PUT  /api/services/<id>      - Update service
DELETE /api/services/<id>    - Delete service
```

### Bookings
```
GET  /api/bookings           - List user bookings
POST /api/bookings           - Create booking
PUT  /api/bookings/<id>      - Update booking
GET  /api/bookings/<id>      - Get booking details
```

### Reviews
```
POST /api/reviews            - Post review
GET  /api/reviews            - List reviews
DELETE /api/reviews/<id>     - Delete review
```

### Payments
```
POST /api/payment            - Process payment
GET  /api/payments           - Payment history
```

### Admin
```
GET  /api/admin/analytics    - Dashboard stats
```

---

## 🔒 Security Features

- ✅ **Password Hashing** - Werkzeug security
- ✅ **JWT Tokens** - Secure authentication
- ✅ **CORS Protection** - Cross-origin security
- ✅ **Admin Validation** - Role-based access
- ✅ **Database Isolation** - SQLAlchemy ORM

---

## 🚀 Deployment Options

### Option 1: Local Server (Development)
```bash
cd naija-connect-app/backend
python3 app.py
```

### Option 2: Production with Gunicorn
```bash
pip3 install gunicorn
gunicorn -w 4 -b 0.0.0.0:5001 app:app
```

### Option 3: Docker (Coming Soon)
```bash
docker-compose up -d
```

---

## 🔧 Troubleshooting

### Port Already in Use
```bash
# macOS/Linux
lsof -i :5001
kill -9 <PID>

# Then restart:
python3 app.py
```

### Template Not Found Error
- Make sure you're running from the `backend` folder
- Check that `../frontend/templates/` path is correct

### Database Issues
```bash
# Reset database
rm naija_connect.db
python3 app.py
```

---

## 💡 Customization

### Change App Name
Edit in `admin.html` and `app.js`:
```javascript
const APP_NAME = "Naija Connect"; // Change this
```

### Change Colors
Edit in `style.css`:
```css
--primary-color: #008751;      /* Green */
--secondary-color: #FF6B35;    /* Orange */
```

### Add New Service Categories
Edit in `app.py`:
```python
CATEGORIES = ['Plumbing', 'Electrical', 'YourNew', ...]
```

---

## 📊 Test Data

### Test User Account
- **Email**: test@example.com
- **Password**: test123

### Test Admin Account
- **Username**: admin
- **Password**: admin123

---

## 🤝 Support

For issues or questions:
1. Check the troubleshooting section
2. Review API documentation
3. Check console logs (F12 in browser)
4. Check terminal output for backend errors

---

## 📝 License

This project is created by Saint Works LTD. All rights reserved.

---

## ✨ Features Checklist

- ✅ User registration & login
- ✅ Service browsing by category
- ✅ Search functionality
- ✅ Service booking system
- ✅ Payment processing
- ✅ Review system
- ✅ Admin dashboard
- ✅ Analytics & reporting
- ✅ Mobile responsive
- ✅ PWA support
- ✅ Offline functionality
- ✅ Cross-device compatibility

---

## 🎯 Next Steps

1. ✅ Start the server
2. ✅ Open http://localhost:5001
3. ✅ Create an account
4. ✅ Browse services
5. ✅ Make a booking
6. ✅ Access admin at http://localhost:5001/admin

**Enjoy Naija Connect!** 🎉

---

**Version**: 1.0.0  
**Last Updated**: February 2026  
**Created by**: Saint Works LTD
