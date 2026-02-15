# Naija Connect - Service Marketplace Platform

A comprehensive service marketplace platform for Nigeria built with modern web technologies, featuring user authentication, service listings, real-time bookings, payment processing, and admin analytics.

## 🚀 Features

### For Customers
- **Browse Services**: Discover trusted service providers across multiple categories
- **Book Services**: Easy booking system with date/time selection
- **Secure Payments**: Integrated Stripe payment processing (Nigerian Naira support)
- **Reviews & Ratings**: Leave feedback and read reviews from other customers
- **Referral Program**: Earn ₦500 for every successful referral

### For Service Providers
- **Service Listings**: Create and manage your service offerings
- **Booking Management**: Track and manage customer bookings
- **Earnings Dashboard**: Monitor your revenue and commission (12%)
- **Profile Management**: Build your professional profile

### For Administrators
- **Real-time Analytics**: View platform statistics and metrics
- **User Management**: Manage users and service providers
- **Service Approval**: Review and approve service listings
- **Revenue Tracking**: Monitor platform commission and transactions
- **QR Code Generation**: Dynamic QR code for app access

## 🛠️ Tech Stack

### Backend
- **Runtime**: Node.js serverless functions (Vercel)
- **Database**: MongoDB Atlas
- **Authentication**: JWT (JSON Web Tokens)
- **Password Security**: bcryptjs
- **Payment Processing**: Stripe API

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern responsive design
- **JavaScript**: Vanilla JS (no framework dependencies)
- **PWA**: Progressive Web App with offline support
- **API Client**: RESTful API integration

## 🚦 Getting Started

### Prerequisites
- Node.js 18+ installed
- MongoDB Atlas account (free tier available)
- Stripe account for payments (test mode)
- Vercel account for deployment

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/jahooskii/naija-connect.git
   cd naija-connect
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Update `.env` with your credentials:
   - `MONGODB_URI`: Your MongoDB connection string
   - `JWT_SECRET`: Random secret for JWT tokens
   - `STRIPE_SECRET_KEY`: Your Stripe secret key
   - `STRIPE_PUBLISHABLE_KEY`: Your Stripe publishable key

4. **Run locally**
   ```bash
   npm run dev
   ```
   
   The app will be available at `http://localhost:3000`

## 🚀 Deployment to Vercel

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy**
   ```bash
   vercel
   ```

4. **Set environment variables**
   - Go to your Vercel project settings
   - Add all environment variables from `.env.example`
   - Redeploy for changes to take effect

## 🔐 API Documentation

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `GET /api/auth/profile` - Get user profile (requires auth)

### Services
- `GET /api/services` - List all services
- `POST /api/services` - Create service (requires auth)
- `GET /api/services/[id]` - Get service by ID
- `PUT /api/services/[id]` - Update service (requires auth)
- `DELETE /api/services/[id]` - Delete service (requires auth)

### Bookings
- `GET /api/bookings` - List user bookings (requires auth)
- `POST /api/bookings` - Create booking (requires auth)

### Reviews
- `GET /api/reviews?serviceId=xxx` - Get service reviews
- `POST /api/reviews` - Create review (requires auth)

### Payments
- `POST /api/payments/stripe` - Create payment intent (requires auth)

### Admin
- `GET /api/admin/stats` - Get platform statistics (requires admin auth)

## 💳 Payment Integration

Integrated with Stripe for secure payment processing:
- Nigerian Naira (NGN) currency support
- 12% platform commission on all bookings
- Secure payment processing
- Automatic booking status updates

## 🔒 Security Features

- Password hashing with bcryptjs
- JWT authentication with 7-day expiration
- CORS protection
- Input validation
- Environment variables protection
- Protected API routes

## 📊 Database Models

- **Users**: Authentication and profile data
- **Services**: Service listings with ratings
- **Bookings**: Booking records with payment status
- **Reviews**: Customer reviews and ratings

## 🎯 NRS Compliance

- 12% platform commission in line with NRS regulations
- Transaction tracking for tax reporting
- Referral program with ₦500 bonus

## 📱 PWA Support

- Installable on mobile devices
- Offline functionality
- Service worker caching
- App-like experience

## 📄 License

MIT License - Powered by Saint Works LTD

## 🇳🇬 Made in Nigeria

Building Nigeria's digital economy, one connection at a time.

---

For support, visit our website or contact admin@naija-connect.com
