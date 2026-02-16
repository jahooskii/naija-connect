# Naija Connect - Service Marketplace Platform

A comprehensive service marketplace platform for Nigeria built with cross-platform compatibility and IP protection. Features user authentication, service listings, real-time bookings, payment processing, reviews, and admin analytics. Built with HTML5, CSS3, JavaScript, Python Flask, and PWA support.

## Project Structure

```
naija-connect/project/
├── backend/
│   ├── app.py                 # Flask backend application with all API endpoints
│   ├── requirements.txt       # Python dependencies
│   └── naija_connect.db      # SQLite database (created at runtime)
│
├── frontend/
│   ├── templates/
│   │   └── index.html        # Main HTML file with modals and structure
│   └── static/
│       ├── css/
│       │   └── style.css     # Complete styling with responsive design
│       └── js/
│           ├── app.js                    # Main JavaScript logic
│           ├── service-worker.js         # PWA offline support
│           └── service-worker-register.js # Service worker registration
│
└── admin/
    ├── README.md             # Admin panel documentation
    └── admin_login.py        # Admin authentication module
```

## Features

### Core Features
- ✅ User Authentication (Login/Register)
- ✅ Service Provider Management
- ✅ Service Listings & Search
- ✅ Advanced Filtering by Category
- ✅ Real-time Booking System
- ✅ Secure Payment Processing
- ✅ Service Reviews & Ratings
- ✅ User Dashboard

### Admin Features
- ✅ Admin Analytics Dashboard
- ✅ User Management
- ✅ Service Management
- ✅ Booking Monitoring
- ✅ Revenue Tracking

### Technical Features
- ✅ Progressive Web App (PWA) Support
- ✅ Offline Caching
- ✅ JWT Authentication
- ✅ CORS Support
- ✅ Responsive Design
- ✅ Mobile Optimized

## Technology Stack

### Backend
- **Framework**: Flask 3.0.0
- **Database**: SQLAlchemy (SQLite)
- **Authentication**: JWT (PyJWT)
- **Security**: Werkzeug password hashing
- **API**: RESTful API with CORS support

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with CSS variables
- **JavaScript**: Vanilla JS (no dependencies)
- **PWA**: Service Workers for offline support

### Services Marketplace
- Home Services (🏠)
- Professional Services (💼)
- Beauty & Personal Care (💅)
- Tech & IT (💻)
- Events & Entertainment (🎉)
- Transport & Logistics (🚗)

## Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Modern web browser

### Installation

1. **Clone the repository**
   ```bash
   cd /Users/thesaintworks/naija-connect/project
   ```

2. **Set up backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   cd backend
   python app.py
   ```

4. **Access the application**
   - Open your browser and go to `http://localhost:5000`
   - The frontend files will be served from the Flask server

## Database Models

### User
- ID, Username, Email, Password Hash
- Full Name, Phone
- is_provider, is_admin flags
- Created timestamp
- Relationships: Services, Bookings, Reviews

### Service
- ID, Title, Description, Category
- Price, Location
- Provider ID, Image URL
- is_active, Created timestamp
- Relationships: Bookings, Reviews

### Booking
- ID, Service ID, Customer ID
- Booking Date, Status
- Payment Status, Total Amount
- Notes, Created timestamp

### Review
- ID, Service ID, Reviewer ID
- Rating (1-5), Comment
- Created timestamp

### Payment
- ID, Booking ID
- Amount, Currency (NGN)
- Payment Method, Transaction ID
- Status, Created timestamp

## API Endpoints

### Authentication
- `POST /api/register` - Register new user
- `POST /api/login` - User login

### Services
- `GET /api/services` - Get all services (with category/search filters)
- `POST /api/services` - Create new service (providers only)
- `GET /api/services/<id>` - Get service details

### Bookings
- `POST /api/bookings` - Create booking
- `GET /api/bookings` - Get user bookings
- `PUT /api/bookings/<id>/status` - Update booking status

### Reviews
- `POST /api/reviews` - Create review
- `GET /api/reviews/<service_id>` - Get service reviews

### Payments
- `POST /api/payment` - Process payment

### Admin
- `GET /api/admin/analytics` - Get admin dashboard data

## 🔐 Default Admin Access

To create an admin user, use the Python shell:

```python
from backend.app import app, db, User

with app.app_context():
    admin = User(
        username='admin',
        email='admin@naijaconnect.ng',
        full_name='Admin User',
        is_admin=True
    )
    admin.set_password('admin123')  # Change this!
    db.session.add(admin)
    db.session.commit()
    print('Admin user created successfully')
```

**Default Credentials:**
- Username: `admin`
- Password: `admin123`

## Environment Variables

Create a `.env` file in the backend directory:

```env
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
DATABASE_URL=sqlite:///naija_connect.db
```

## PWA Features

The application includes Progressive Web App support:
- Works offline with service workers
- Installable on mobile devices
- App manifest included
- Cache strategies for fast loading

## Security Features

- Password hashing with Werkzeug
- JWT token authentication
- CORS protection
- Admin role-based access
- Input validation

## File Structure Explanation

### Backend (app.py)
- Database models with SQLAlchemy
- JWT token generation and validation
- RESTful API endpoints
- Admin analytics
- PWA manifest

### Frontend (HTML/CSS/JS)
- Single-page application design
- Modal-based interface
- Real-time API communication
- Responsive grid layouts
- Service worker registration

### Admin Module
- Admin authentication logic
- Admin panel documentation
- Role-based access control

## Development

### Running in Development Mode
```bash
export FLASK_ENV=development
export FLASK_APP=backend/app.py
python -m flask run
```

### Testing the API
Use tools like Postman or curl to test endpoints:

```bash
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@example.com","password":"test123","full_name":"Test User"}'
```

## Browser Support

- Chrome/Chromium 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Performance Optimizations

- CSS Grid for responsive layouts
- Service worker caching strategy
- Lazy loading of services
- Minimal JavaScript dependencies
- Optimized API calls

## IP Protection

© 2026 Saint Works LTD. All rights reserved.
This project is protected under intellectual property laws.

## License

Licensed by Saint Works LTD
All rights reserved.

## Support

For issues or questions, contact:
- Email: info@naijaconnect.ng
- Location: Lagos, Nigeria

## Roadmap

- [ ] Mobile app (React Native)
- [ ] Payment gateway integration (Paystack, Flutterwave)
- [ ] Email notifications
- [ ] SMS notifications
- [ ] Real-time chat
- [ ] Video call support
- [ ] Advanced analytics
- [ ] Multi-language support
- [ ] Advanced search with maps
- [ ] Insurance & warranty plans

---

**Powered by Saint Works LTD** 🇳🇬
