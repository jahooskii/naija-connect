# 🇳🇬 Naija Connect - Service Marketplace for Nigeria

A comprehensive service marketplace platform for Nigeria built with cross-platform compatibility and IP protection. Features user authentication, service listings, real-time bookings, payment processing, reviews, and admin analytics. Built with HTML5, CSS3, JavaScript, Python Flask, and PWA support.

**Powered by Saint Works LTD** ⚠️ Intellectual Property Protected

## 🌟 Features

### Core Features
- **User Authentication** - Secure JWT-based authentication system
- **Service Listings** - Browse and search service providers by category
- **Real-time Bookings** - Schedule appointments with service providers
- **Payment Processing** - Integrated payment system supporting Nigerian Naira (₦)
- **Reviews & Ratings** - Customer feedback and 5-star rating system
- **Admin Analytics** - Comprehensive dashboard for business insights

### Technical Features
- **PWA Support** - Install as a mobile/desktop app with offline functionality
- **Cross-platform** - Works on all devices and browsers
- **Responsive Design** - Mobile-first, fully responsive UI
- **RESTful API** - Clean API architecture for easy integration
- **IP Protection** - Copyright and security measures implemented

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Web browser (Chrome, Firefox, Safari, Edge)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/jahooskii/naija-connect.git
cd naija-connect
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Run the application**
```bash
python app.py
```

5. **Access the application**
Open your browser and navigate to:
```
http://localhost:5000
```

## 📱 PWA Installation

To install Naija Connect as a Progressive Web App:

1. Open the app in Chrome or Edge
2. Click the install icon in the address bar
3. Follow the prompts to add to home screen

The app will work offline and provide a native app-like experience!

## 🔐 Default Admin Access

To create an admin user, use the Python shell:

```python
from app import app, db, User

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
```

## 📖 API Documentation

### Authentication Endpoints

**POST /api/register** - Register a new user
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "phone": "+234XXXXXXXXXX",
  "password": "password123",
  "is_provider": false
}
```

**POST /api/login** - Login user
```json
{
  "username": "john_doe",
  "password": "password123"
}
```

### Service Endpoints

**GET /api/services** - Get all services
- Query params: `category`, `search`

**POST /api/services** - Create service (requires auth & provider status)
```json
{
  "title": "Plumbing Services",
  "description": "Professional plumbing for homes and offices",
  "category": "home",
  "price": 5000,
  "location": "Lagos",
  "image_url": "https://example.com/image.jpg"
}
```

**GET /api/services/:id** - Get service details

### Booking Endpoints

**POST /api/bookings** - Create booking (requires auth)
```json
{
  "service_id": 1,
  "booking_date": "2026-02-20T10:00:00",
  "notes": "Please call before arrival"
}
```

**GET /api/bookings** - Get user bookings (requires auth)

**PUT /api/bookings/:id/status** - Update booking status (provider/admin only)

### Review Endpoints

**POST /api/reviews** - Create review (requires auth & completed booking)
```json
{
  "service_id": 1,
  "rating": 5,
  "comment": "Excellent service!"
}
```

**GET /api/reviews/:service_id** - Get service reviews

### Payment Endpoints

**POST /api/payment** - Process payment (requires auth)
```json
{
  "booking_id": 1,
  "payment_method": "card"
}
```

### Admin Endpoints

**GET /api/admin/analytics** - Get analytics dashboard (admin only)

## 🏗️ Project Structure

```
naija-connect/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── templates/
│   └── index.html        # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css     # Application styles
│   ├── js/
│   │   ├── app.js        # Main JavaScript
│   │   ├── service-worker.js          # PWA service worker
│   │   └── service-worker-register.js # Service worker registration
│   └── icons/            # PWA icons
└── README.md             # This file
```

## 🎨 Categories

The platform supports the following service categories:
- 🏠 **Home Services** - Plumbing, Electrical, Cleaning
- 💼 **Professional Services** - Legal, Accounting, Consulting
- 💅 **Beauty & Personal Care** - Salon, Spa, Barbering
- 💻 **Tech & IT** - Development, Support, Repairs
- 🎉 **Events & Entertainment** - DJ, Photography, Catering
- 🚗 **Transport & Logistics** - Delivery, Moving, Logistics

## 🔒 Security Features

- JWT-based authentication
- Password hashing with Werkzeug
- CORS protection
- SQL injection prevention with SQLAlchemy ORM
- Secure session management
- IP protection notices

## 💳 Payment Integration

Currently supports Nigerian Naira (₦) currency. For production deployment, integrate with:
- Paystack
- Flutterwave
- Interswitch

## 🌐 Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+
- Mobile browsers (iOS Safari, Chrome Mobile)

## 📄 License

MIT License - Copyright (c) 2026 Saint Works LTD

See [LICENSE](LICENSE) file for details.

## ⚠️ Intellectual Property Notice

This software is protected by copyright law and international treaties. Unauthorized reproduction or distribution of this program, or any portion of it, may result in severe civil and criminal penalties.

**Powered by Saint Works LTD** - All rights reserved.

## 🤝 Contributing

This is a proprietary project by Saint Works LTD. For partnership or collaboration inquiries, please contact:
- Email: info@saintworks.com
- Website: www.saintworks.com

## 📞 Support

For support, email support@naijaconnect.ng or visit our help center.

## 🗺️ Roadmap

- [ ] SMS notifications
- [ ] Email notifications
- [ ] Advanced search filters
- [ ] Multi-language support (Yoruba, Igbo, Hausa)
- [ ] Mobile apps (iOS & Android)
- [ ] Video consultations
- [ ] Subscription plans
- [ ] Loyalty rewards program

---

**Made with ❤️ in Nigeria** 🇳🇬
