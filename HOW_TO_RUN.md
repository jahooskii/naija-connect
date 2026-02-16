# 🚀 NAIJA CONNECT - HOW TO RUN

## ⚡ Quick Start (Choose Your Method)

### **Mac/Linux Users:**

#### **Method 1: Automatic (Easiest)**
```bash
# Just double-click the run.sh file, or in terminal run:
./run.sh
```

#### **Method 2: Manual**
```bash
# Navigate to the project folder
cd naija-connect-app/backend

# Install dependencies
pip3 install -r requirements.txt

# Start the server
python3 app.py
```

---

### **Windows Users:**

#### **Method 1: Automatic (Easiest)**
- Double-click `run.bat` file in the naija-connect-app folder

#### **Method 2: Manual**
```cmd
# Open Command Prompt (cmd.exe)

# Navigate to the project folder
cd Desktop\naija-connect-app\backend

# Install dependencies
pip install -r requirements.txt

# Start the server
python app.py
```

---

## ✅ When It's Running

You should see output like:
```
 * Running on http://0.0.0.0:8000
 * Press CTRL+C to quit
```

**Then open your browser and visit:**
### **http://localhost:8000**

---

## 📱 Features Ready to Use

✅ **Browse Services** - See all available services
✅ **User Registration** - Create a new account
✅ **User Login** - Sign in to your account
✅ **Search & Filter** - Find services by category
✅ **Book Services** - Reserve a service
✅ **Make Payments** - Process payments
✅ **Leave Reviews** - Rate services
✅ **View Dashboard** - Manage your bookings

---

## 🔐 Default Test Accounts

You can create new accounts, or the system automatically supports:

**Admin User (For Dashboard):**
- Username: `admin`
- Password: `admin123`

To create an admin account:
```python
python3
from backend.app import app, db, User

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

---

## 🛑 Stop the Server

Press **CTRL+C** in the terminal where it's running

---

## 📁 Project Structure

```
naija-connect-app/
├── backend/                  (Flask API)
│   ├── app.py              (Main application)
│   ├── requirements.txt     (Dependencies)
│   └── naija_connect.db    (Database - created automatically)
│
├── frontend/               (Web Interface)
│   ├── templates/
│   │   └── index.html
│   └── static/
│       ├── css/style.css
│       └── js/app.js
│
├── admin/                  (Admin tools)
├── README.md              (Full documentation)
├── QUICKSTART.md          (Quick guide)
├── run.sh                 (Mac/Linux starter)
└── run.bat                (Windows starter)
```

---

## 🔧 Troubleshooting

### **Port Already in Use**
If you see "Address already in use" error:
```bash
# Kill the process using port 8000
# Mac/Linux:
lsof -i :8000
kill -9 [PID]

# Windows:
netstat -ano | findstr :8000
taskkill /PID [PID] /F
```

### **Python Not Found**
Install Python 3 from: https://www.python.org/downloads/

### **Dependencies Won't Install**
```bash
pip3 install --upgrade pip
pip3 install -r requirements.txt --force-reinstall
```

### **Permission Denied on Mac/Linux**
```bash
chmod +x run.sh
./run.sh
```

---

## 💾 Database

The SQLite database (`naija_connect.db`) is created automatically in the `backend/` folder when you first run the app.

To reset the database:
```bash
rm backend/naija_connect.db
```

---

## 📊 What You Can Do

1. **Browse Services** - See all 6 service categories
2. **Register Account** - Sign up as customer or provider
3. **Search Services** - Filter by category or keyword
4. **Book a Service** - Schedule and pay for services
5. **Write Reviews** - Rate services 1-5 stars
6. **View Dashboard** - See your bookings & history
7. **Admin Analytics** - View statistics (if admin)

---

## 🌟 Service Categories Available

- 🏠 Home Services (Plumbing, Electrical, Cleaning)
- 💼 Professional Services (Legal, Accounting)
- 💅 Beauty & Care (Salon, Spa, Barbering)
- 💻 Tech & IT (Development, Support, Repairs)
- 🎉 Events (DJ, Photography, Catering)
- 🚗 Transport (Delivery, Moving, Logistics)

---

## 📞 API Server

The server runs on:
- **Address:** `http://localhost:8000`
- **Frontend:** `http://localhost:8000` (Browser)
- **API:** `http://localhost:8000/api/*` (For requests)

---

## ✨ That's It!

Your Naija Connect marketplace is ready to use! 🎉

For more details, see:
- `README.md` - Full documentation
- `QUICKSTART.md` - Quick setup guide
- `ARCHITECTURE.md` - System design

---

**Enjoy your service marketplace! 🇳🇬**
