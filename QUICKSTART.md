# Quick Start Guide - Naija Connect

## 🚀 Fast Setup (5 minutes)

### 1. Install Dependencies
```bash
cd /Users/thesaintworks/naija-connect/project/backend
pip install -r requirements.txt
```

### 2. Start the Server
```bash
python app.py
```

You should see:
```
 * Running on http://0.0.0.0:5000
 * Press CTRL+C to quit
```

### 3. Open in Browser
Visit: **http://localhost:5000**

## 📁 Project Organization

```
project/
├── backend/              # Flask API Server
│   ├── app.py           # All backend logic & models
│   └── requirements.txt  # Python packages
│
├── frontend/            # Web Interface
│   ├── templates/       # HTML files
│   └── static/          # CSS, JS, Images
│
└── admin/               # Admin Features
    └── admin_login.py   # Admin authentication
```

## 🔐 First Time Setup

### Create Admin User
```bash
python
```

Then in Python shell:
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
    print('Admin created!')
```

## 👥 Test Accounts

### Regular User
- Username: `testuser`
- Password: `test123`

### Provider
- Username: `provider`
- Password: `provider123`

### Admin
- Username: `admin`
- Password: `admin123`

## 📋 Main Features

| Feature | Path | Access |
|---------|------|--------|
| Browse Services | `/` | Public |
| Login | Modal | Public |
| Register | Modal | Public |
| Create Service | API | Providers |
| Book Service | Modal | Logged In |
| Dashboard | Modal | Logged In |
| Admin Panel | `/api/admin/analytics` | Admin Only |

## 🔧 Key Files

| File | Purpose |
|------|---------|
| `backend/app.py` | All API endpoints & database |
| `frontend/templates/index.html` | Main interface |
| `frontend/static/css/style.css` | Styling |
| `frontend/static/js/app.js` | Frontend logic |
| `admin/admin_login.py` | Admin setup |

## 🌐 Service Categories

- 🏠 Home Services
- 💼 Professional Services
- 💅 Beauty & Care
- 💻 Tech & IT
- 🎉 Events
- 🚗 Transport

## 💾 Database

**Type:** SQLite (naija_connect.db)

**Tables:**
- users
- services
- bookings
- reviews
- payments

## 🧪 Testing with curl

### Register User
```bash
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "username":"testuser",
    "email":"test@example.com",
    "password":"test123",
    "full_name":"Test User"
  }'
```

### Login
```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{
    "username":"testuser",
    "password":"test123"
  }'
```

### Get Services
```bash
curl http://localhost:5000/api/services
```

## 📱 Mobile Access

Open on your phone:
```
http://[YOUR-PC-IP]:5000
```

Replace `[YOUR-PC-IP]` with your computer's IP address.

## 🐛 Troubleshooting

### Port 5000 Already in Use
```bash
# Find process using port 5000
lsof -i :5000

# Kill it (macOS/Linux)
kill -9 <PID>
```

### Database Issues
```bash
# Delete old database and restart
rm backend/naija_connect.db
python backend/app.py
```

### Dependencies Missing
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

## 📚 Learning Resources

- Review `backend/app.py` for API structure
- Check `frontend/static/js/app.js` for frontend logic
- See `frontend/templates/index.html` for HTML structure
- Read `admin/admin_login.py` for admin setup

## 🎯 Common Tasks

### Add Service Provider
1. Register as user
2. Check "I want to offer services"
3. Login & use `/api/services` endpoint

### Create Admin User
See "First Time Setup" section above

### Deploy to Production
1. Set `FLASK_ENV=production`
2. Use production WSGI server (Gunicorn)
3. Add environment variables from `.env.example`

## 📞 Contact

**Saint Works LTD**
- Email: info@naijaconnect.ng
- Location: Lagos, Nigeria
- Year: 2026

---

**Happy building! 🚀**
