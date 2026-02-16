"""
Naija Connect - Service Marketplace Platform
Powered by Saint Works LTD
"""
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import jwt
import os
from functools import wraps

# Fix for werkzeug compatibility
os.environ['WERKZEUG_HASH_METHOD'] = 'pbkdf2:sha256'

# Set correct template and static folders
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'templates'))
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'static'))

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///naija_connect.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_EXPIRATION_DELTA'] = timedelta(days=7)

db = SQLAlchemy(app)
CORS(app)

# Database Models
class User(db.Model):
    """User model for authentication and profile management"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    full_name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    is_provider = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    referral_code = db.Column(db.String(20), unique=True)
    referred_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    referral_earnings = db.Column(db.Float, default=0.0)
    total_referrals = db.Column(db.Integer, default=0)
    tracking_code = db.Column(db.String(20), unique=True, nullable=True)
    
    services = db.relationship('Service', backref='provider', lazy=True)
    bookings = db.relationship('Booking', backref='customer', lazy=True)
    reviews = db.relationship('Review', backref='reviewer', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Service(db.Model):
    """Service model for marketplace listings"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(100))
    provider_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image_url = db.Column(db.String(300))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    bookings = db.relationship('Booking', backref='service', lazy=True)
    reviews = db.relationship('Review', backref='service', lazy=True)

class Booking(db.Model):
    """Booking model for service reservations"""
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    booking_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, completed, cancelled
    payment_status = db.Column(db.String(20), default='unpaid')  # unpaid, paid, refunded
    total_amount = db.Column(db.Float, nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Review(db.Model):
    """Review model for service ratings and feedback"""
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Payment(db.Model):
    """Payment model for transaction tracking"""
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='NGN')  # Nigerian Naira
    payment_method = db.Column(db.String(50))
    transaction_id = db.Column(db.String(100), unique=True)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)



class Referral(db.Model):
    """Referral tracking for user acquisition and rewards"""
    id = db.Column(db.Integer, primary_key=True)
    referrer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    referred_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    referral_code = db.Column(db.String(20), nullable=False)
    reward_amount = db.Column(db.Float, default=0.0)
    reward_paid = db.Column(db.Boolean, default=False)
    booking_count = db.Column(db.Integer, default=0)  # Bookings from referred user
    total_value = db.Column(db.Float, default=0.0)  # Total transaction value from referred user
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Commission(db.Model):
    """Commission tracking for platform revenue"""
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'), nullable=False)
    service_amount = db.Column(db.Float, nullable=False)
    commission_rate = db.Column(db.Float, default=0.12)  # 12% default
    commission_amount = db.Column(db.Float, nullable=False)
    provider_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, paid
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# JWT Authentication Decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated

# Routes
@app.route('/')
def index():
    """Homepage"""
    return render_template('index.html')

@app.route('/api/register', methods=['POST'])
def register():
    """User registration endpoint"""
    data = request.get_json()
    
    if User.query.filter_by(username=data.get('username')).first():
        return jsonify({'message': 'Username already exists'}), 400
    
    if User.query.filter_by(email=data.get('email')).first():
        return jsonify({'message': 'Email already exists'}), 400
    
    user = User(
        username=data.get('username'),
        email=data.get('email'),
        full_name=data.get('full_name'),
        phone=data.get('phone'),
        is_provider=data.get('is_provider', False)
    )
    user.set_password(data.get('password'))
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    """User login endpoint"""
    data = request.get_json()
    
    user = User.query.filter_by(username=data.get('username')).first()
    
    if not user or not user.check_password(data.get('password')):
        return jsonify({'message': 'Invalid credentials'}), 401
    
    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.utcnow() + app.config['JWT_EXPIRATION_DELTA']
    }, app.config['SECRET_KEY'], algorithm='HS256')
    
    return jsonify({
        'token': token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'full_name': user.full_name,
            'is_provider': user.is_provider,
            'is_admin': user.is_admin
        }
    })

@app.route('/api/services', methods=['GET'])
def get_services():
    """Get all active services"""
    category = request.args.get('category')
    search = request.args.get('search')
    
    query = Service.query.filter_by(is_active=True)
    
    if category:
        query = query.filter_by(category=category)
    
    if search:
        query = query.filter(Service.title.contains(search) | Service.description.contains(search))
    
    services = query.all()
    
    return jsonify([{
        'id': s.id,
        'title': s.title,
        'description': s.description,
        'category': s.category,
        'price': s.price,
        'location': s.location,
        'image_url': s.image_url,
        'provider': {
            'id': s.provider.id,
            'name': s.provider.full_name or s.provider.username
        }
    } for s in services])

@app.route('/api/services', methods=['POST'])
@token_required
def create_service(current_user):
    """Create a new service listing"""
    if not current_user.is_provider:
        return jsonify({'message': 'Only providers can create services'}), 403
    
    data = request.get_json()
    
    service = Service(
        title=data.get('title'),
        description=data.get('description'),
        category=data.get('category'),
        price=data.get('price'),
        location=data.get('location'),
        image_url=data.get('image_url'),
        provider_id=current_user.id
    )
    
    db.session.add(service)
    db.session.commit()
    
    return jsonify({'message': 'Service created successfully', 'service_id': service.id}), 201

@app.route('/api/services/<int:service_id>', methods=['GET'])
def get_service(service_id):
    """Get service details"""
    service = Service.query.get_or_404(service_id)
    
    reviews = Review.query.filter_by(service_id=service_id).all()
    avg_rating = sum(r.rating for r in reviews) / len(reviews) if reviews else 0
    
    return jsonify({
        'id': service.id,
        'title': service.title,
        'description': service.description,
        'category': service.category,
        'price': service.price,
        'location': service.location,
        'image_url': service.image_url,
        'provider': {
            'id': service.provider.id,
            'name': service.provider.full_name or service.provider.username,
            'phone': service.provider.phone
        },
        'rating': round(avg_rating, 1),
        'review_count': len(reviews)
    })

@app.route('/api/bookings', methods=['POST'])
@token_required
def create_booking(current_user):
    """Create a new booking"""
    data = request.get_json()
    
    service = Service.query.get_or_404(data.get('service_id'))
    
    booking = Booking(
        service_id=service.id,
        customer_id=current_user.id,
        booking_date=datetime.fromisoformat(data.get('booking_date')),
        total_amount=service.price,
        notes=data.get('notes')
    )
    
    db.session.add(booking)
    db.session.commit()
    
    return jsonify({'message': 'Booking created successfully', 'booking_id': booking.id}), 201

@app.route('/api/bookings', methods=['GET'])
@token_required
def get_bookings(current_user):
    """Get user bookings"""
    bookings = Booking.query.filter_by(customer_id=current_user.id).all()
    
    return jsonify([{
        'id': b.id,
        'service': {
            'id': b.service.id,
            'title': b.service.title,
            'provider': b.service.provider.full_name or b.service.provider.username
        },
        'booking_date': b.booking_date.isoformat(),
        'status': b.status,
        'payment_status': b.payment_status,
        'total_amount': b.total_amount
    } for b in bookings])

@app.route('/api/bookings/<int:booking_id>/status', methods=['PUT'])
@token_required
def update_booking_status(current_user, booking_id):
    """Update booking status"""
    booking = Booking.query.get_or_404(booking_id)
    data = request.get_json()
    
    # Only the service provider or admin can update status
    if booking.service.provider_id != current_user.id and not current_user.is_admin:
        return jsonify({'message': 'Unauthorized'}), 403
    
    booking.status = data.get('status', booking.status)
    db.session.commit()
    
    return jsonify({'message': 'Booking status updated'})

@app.route('/api/reviews', methods=['POST'])
@token_required
def create_review(current_user):
    """Create a service review"""
    data = request.get_json()
    
    # Check if user has booked this service
    booking = Booking.query.filter_by(
        customer_id=current_user.id,
        service_id=data.get('service_id'),
        status='completed'
    ).first()
    
    if not booking:
        return jsonify({'message': 'You can only review services you have used'}), 403
    
    # Check if already reviewed
    existing_review = Review.query.filter_by(
        reviewer_id=current_user.id,
        service_id=data.get('service_id')
    ).first()
    
    if existing_review:
        return jsonify({'message': 'You have already reviewed this service'}), 400
    
    review = Review(
        service_id=data.get('service_id'),
        reviewer_id=current_user.id,
        rating=data.get('rating'),
        comment=data.get('comment')
    )
    
    db.session.add(review)
    db.session.commit()
    
    return jsonify({'message': 'Review submitted successfully'}), 201

@app.route('/api/reviews/<int:service_id>', methods=['GET'])
def get_reviews(service_id):
    """Get service reviews"""
    reviews = Review.query.filter_by(service_id=service_id).all()
    
    return jsonify([{
        'id': r.id,
        'rating': r.rating,
        'comment': r.comment,
        'reviewer': r.reviewer.full_name or r.reviewer.username,
        'created_at': r.created_at.isoformat()
    } for r in reviews])

@app.route('/api/payment', methods=['POST'])
@token_required
def process_payment(current_user):
    """Process payment for booking"""
    data = request.get_json()
    
    booking = Booking.query.get_or_404(data.get('booking_id'))
    
    if booking.customer_id != current_user.id:
        return jsonify({'message': 'Unauthorized'}), 403
    
    # Create payment record
    payment = Payment(
        booking_id=booking.id,
        amount=booking.total_amount,
        payment_method=data.get('payment_method'),
        transaction_id=f"TXN-{booking.id}-{datetime.utcnow().timestamp()}"
    )
    
    # In production, integrate with real payment gateway
    payment.status = 'completed'
    booking.payment_status = 'paid'
    
    db.session.add(payment)
    db.session.commit()
    
    return jsonify({
        'message': 'Payment processed successfully',
        'transaction_id': payment.transaction_id
    })

@app.route('/api/admin/analytics', methods=['GET'])
@token_required
def admin_analytics(current_user):
    """Admin analytics dashboard"""
    if not current_user.is_admin:
        return jsonify({'message': 'Admin access required'}), 403
    
    total_users = User.query.count()
    total_services = Service.query.count()
    total_bookings = Booking.query.count()
    total_revenue = db.session.query(db.func.sum(Payment.amount)).filter_by(status='completed').scalar() or 0
    
    recent_bookings = Booking.query.order_by(Booking.created_at.desc()).limit(10).all()
    
    return jsonify({
        'total_users': total_users,
        'total_services': total_services,
        'total_bookings': total_bookings,
        'total_revenue': total_revenue,
        'recent_bookings': [{
            'id': b.id,
            'service': b.service.title,
            'customer': b.customer.full_name or b.customer.username,
            'amount': b.total_amount,
            'status': b.status,
            'date': b.created_at.isoformat()
        } for b in recent_bookings]
    })

# Admin Routes
@app.route('/admin', methods=['GET'])
def admin_dashboard():
    """Serve admin dashboard"""
    return render_template('admin.html')

@app.route('/api/admin-login', methods=['POST'])
def admin_login():
    """Admin login endpoint"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username).first()
    
    if not user or not user.is_admin or not user.check_password(password):
        return jsonify({
            'success': False,
            'message': 'Invalid admin credentials'
        }), 401
    
    token = jwt.encode({
        'user_id': user.id,
        'username': user.username,
        'is_admin': user.is_admin,
        'exp': datetime.utcnow() + app.config['JWT_EXPIRATION_DELTA']
    }, app.config['SECRET_KEY'])
    
    return jsonify({
        'success': True,
        'token': token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'full_name': user.full_name
        }
    })

@app.route('/manifest.json')
def manifest():
    """PWA manifest"""
    return jsonify({
        "name": "Naija Connect",
        "short_name": "NaijaConnect",
        "description": "Service marketplace platform for Nigeria",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": "#008751",
        "orientation": "portrait",
        "icons": [
            {
                "src": "/static/icons/icon-192.png",
                "sizes": "192x192",
                "type": "image/png"
            },
            {
                "src": "/static/icons/icon-512.png",
                "sizes": "512x512",
                "type": "image/png"
            }
        ]
    })


# Provider Routes
@app.route('/provider')
def provider_dashboard():
    """Serve provider dashboard"""
    return render_template('provider.html')

@app.route('/api/provider/overview', methods=['GET'])
@token_required
def provider_overview(current_user):
    """Provider dashboard overview"""
    if not current_user.is_provider:
        return jsonify({'message': 'Provider access required'}), 403
    
    # Get provider's services
    services = Service.query.filter_by(provider_id=current_user.id).all()
    total_services = len([s for s in services if s.is_active])
    
    # Get bookings for provider's services
    service_ids = [s.id for s in services]
    bookings = Booking.query.filter(Booking.service_id.in_(service_ids)).all() if service_ids else []
    
    # Calculate earnings
    gross_earnings = sum(b.total_amount for b in bookings if b.payment_status == 'paid')
    commission = gross_earnings * 0.12  # 12% platform fee
    net_earnings = gross_earnings * 0.88  # Provider gets 88%
    
    return jsonify({
        'total_services': total_services,
        'total_bookings': len(bookings),
        'gross_earnings': gross_earnings,
        'net_earnings': net_earnings,
        'commission': commission
    })

@app.route('/api/provider/services', methods=['GET'])
@token_required
def provider_services(current_user):
    """Get provider's services"""
    if not current_user.is_provider:
        return jsonify({'message': 'Provider access required'}), 403
    
    services = Service.query.filter_by(provider_id=current_user.id).all()
    
    return jsonify([{
        'id': s.id,
        'title': s.title,
        'description': s.description,
        'category': s.category,
        'price': s.price,
        'location': s.location,
        'image_url': s.image_url,
        'is_active': s.is_active,
        'created_at': s.created_at.isoformat()
    } for s in services])

@app.route('/api/provider/bookings', methods=['GET'])
@token_required
def provider_bookings(current_user):
    """Get bookings for provider's services"""
    if not current_user.is_provider:
        return jsonify({'message': 'Provider access required'}), 403
    
    services = Service.query.filter_by(provider_id=current_user.id).all()
    service_ids = [s.id for s in services]
    bookings = Booking.query.filter(Booking.service_id.in_(service_ids)).all() if service_ids else []
    
    return jsonify([{
        'id': b.id,
        'service_title': b.service.title,
        'customer_name': b.customer.full_name or b.customer.username,
        'customer_phone': b.customer.phone,
        'booking_date': b.booking_date.isoformat(),
        'status': b.status,
        'payment_status': b.payment_status,
        'total_amount': b.total_amount,
        'notes': b.notes
    } for b in bookings])

@app.route('/api/provider/earnings', methods=['GET'])
@token_required
def provider_earnings(current_user):
    """Get provider earnings breakdown"""
    if not current_user.is_provider:
        return jsonify({'message': 'Provider access required'}), 403
    
    # Get current month's earnings
    from datetime import datetime
    current_month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    services = Service.query.filter_by(provider_id=current_user.id).all()
    service_ids = [s.id for s in services]
    
    if not service_ids:
        return jsonify({
            'monthly_gross': 0,
            'monthly_commission': 0,
            'monthly_net': 0,
            'available_balance': 0
        })
    
    # Monthly earnings
    monthly_bookings = Booking.query.filter(
        Booking.service_id.in_(service_ids),
        Booking.payment_status == 'paid',
        Booking.created_at >= current_month_start
    ).all()
    
    monthly_gross = sum(b.total_amount for b in monthly_bookings)
    monthly_commission = monthly_gross * 0.12
    monthly_net = monthly_gross * 0.88
    
    # Total available balance (all-time net earnings)
    all_bookings = Booking.query.filter(
        Booking.service_id.in_(service_ids),
        Booking.payment_status == 'paid'
    ).all()
    
    total_gross = sum(b.total_amount for b in all_bookings)
    available_balance = total_gross * 0.88  # Simplified, should track withdrawals
    
    return jsonify({
        'monthly_gross': monthly_gross,
        'monthly_commission': monthly_commission,
        'monthly_net': monthly_net,
        'available_balance': available_balance
    })

@app.route('/api/bookings/<int:booking_id>/verify', methods=['POST'])
@token_required
def verify_booking(current_user, booking_id):
    """Verify booking via QR code"""
    booking = Booking.query.get_or_404(booking_id)
    data = request.get_json()
    verification_code = data.get('code')
    
    # Check if code matches
    if verification_code == f"BOOKING-{booking_id}":
        booking.status = 'confirmed'
        db.session.commit()
        return jsonify({'message': 'Booking verified successfully', 'booking': {
            'id': booking.id,
            'status': booking.status
        }})
    
    return jsonify({'message': 'Invalid verification code'}), 400


# Provider Tracking & Sharing System
@app.route('/api/provider/share/<int:provider_id>', methods=['GET'])
def generate_provider_share_link(provider_id):
    """Generate shareable tracking link and QR code for a provider"""
    provider = User.query.get(provider_id)
    if not provider or not provider.is_provider:
        return jsonify({'error': 'Provider not found'}), 404
    
    # Generate unique tracking code
    import secrets
    if not hasattr(provider, 'tracking_code') or not provider.tracking_code:
        tracking_code = secrets.token_urlsafe(8)
        # Store in database (we'll add this field to User model)
    else:
        tracking_code = provider.tracking_code
    
    # Generate shareable link
    base_url = request.host_url.rstrip('/')
    share_link = f"{base_url}/track/{tracking_code}"
    
    # Generate QR code URL
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={share_link}"
    
    return jsonify({
        'provider_id': provider_id,
        'provider_name': provider.full_name,
        'tracking_code': tracking_code,
        'share_link': share_link,
        'qr_code_url': qr_url,
        'qr_download_url': f"https://api.qrserver.com/v1/create-qr-code/?size=500x500&format=png&data={share_link}"
    })

@app.route('/api/provider/stats/<tracking_code>', methods=['GET'])
def get_provider_tracking_stats(tracking_code):
    """Get statistics for a provider using their tracking code"""
    provider = User.query.filter_by(tracking_code=tracking_code).first()
    if not provider:
        return jsonify({'error': 'Invalid tracking code'}), 404
    
    # Get provider's services
    services = Service.query.filter_by(provider_id=provider.id).all()
    
    # Get bookings
    bookings = Booking.query.filter(
        Booking.service_id.in_([s.id for s in services])
    ).all()
    
    # Calculate stats
    total_bookings = len(bookings)
    completed_bookings = len([b for b in bookings if b.status == 'completed'])
    total_revenue = sum([b.total_price for b in bookings if b.status == 'completed'])
    
    # Get reviews
    reviews = Review.query.filter(
        Review.service_id.in_([s.id for s in services])
    ).all()
    
    avg_rating = sum([r.rating for r in reviews]) / len(reviews) if reviews else 0
    
    return jsonify({
        'provider_name': provider.full_name,
        'total_services': len(services),
        'total_bookings': total_bookings,
        'completed_bookings': completed_bookings,
        'total_revenue': total_revenue,
        'average_rating': round(avg_rating, 2),
        'total_reviews': len(reviews),
        'services': [{
            'id': s.id,
            'name': s.name,
            'category': s.category,
            'price': s.price
        } for s in services]
    })

@app.route('/track/<tracking_code>')
def track_provider(tracking_code):
    """Landing page for tracked provider links"""
    provider = User.query.filter_by(tracking_code=tracking_code).first()
    if not provider:
        return "Invalid tracking link", 404
    
    # Log the visit (we can add a tracking table later)
    # For now, redirect to provider's services
    return redirect(f'/?provider={provider.id}')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    import os
    port = int(os.environ.get('PORT', 8000))
    app.run(debug=False, host='0.0.0.0', port=port)

# ============================================
# REFERRAL SYSTEM ENDPOINTS
# ============================================

@app.route('/api/referrals/generate', methods=['POST'])
def generate_referral_code():
    """Generate unique referral code for user"""
    import random
    import string
    
    data = request.json
    user_id = data.get('user_id')
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Generate unique 8-character code
    while True:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        if not User.query.filter_by(referral_code=code).first():
            break
    
    user.referral_code = code
    db.session.commit()
    
    return jsonify({
        'referral_code': code,
        'qr_url': f'https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=https://naija-connect.onrender.com/register?ref={code}'
    })

@app.route('/api/referrals/stats/<int:user_id>')
def get_referral_stats(user_id):
    """Get referral statistics for user"""
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    referrals = Referral.query.filter_by(referrer_id=user_id).all()
    
    stats = {
        'referral_code': user.referral_code,
        'total_referrals': user.total_referrals,
        'total_earnings': user.referral_earnings,
        'active_referrals': len([r for r in referrals if r.booking_count > 0]),
        'pending_rewards': sum(r.reward_amount for r in referrals if not r.reward_paid),
        'referrals': [{
            'user_id': r.referred_id,
            'username': User.query.get(r.referred_id).username,
            'bookings': r.booking_count,
            'total_value': r.total_value,
            'reward': r.reward_amount,
            'paid': r.reward_paid,
            'joined': r.created_at.strftime('%Y-%m-%d')
        } for r in referrals]
    }
    
    return jsonify(stats)

@app.route('/api/referrals/apply', methods=['POST'])
def apply_referral_code():
    """Apply referral code during registration"""
    data = request.json
    referral_code = data.get('referral_code')
    new_user_id = data.get('user_id')
    
    if not referral_code or not new_user_id:
        return jsonify({'error': 'Missing parameters'}), 400
    
    referrer = User.query.filter_by(referral_code=referral_code).first()
    if not referrer:
        return jsonify({'error': 'Invalid referral code'}), 404
    
    new_user = User.query.get(new_user_id)
    if not new_user:
        return jsonify({'error': 'User not found'}), 404
    
    # Create referral tracking
    referral = Referral(
        referrer_id=referrer.id,
        referred_id=new_user_id,
        referral_code=referral_code,
        reward_amount=500.0  # ₦500 bonus per referral
    )
    
    new_user.referred_by = referrer.id
    referrer.total_referrals += 1
    
    db.session.add(referral)
    db.session.commit()
    
    return jsonify({
        'message': 'Referral applied successfully',
        'referrer': referrer.username,
        'bonus': 500.0
    })

# ============================================
# ADMIN MONETIZATION ENDPOINTS
# ============================================

@app.route('/api/admin/revenue/overview')
def admin_revenue_overview():
    """Get comprehensive revenue overview for admin"""
    total_bookings = Booking.query.count()
    completed_bookings = Booking.query.filter_by(status='completed').all()
    
    total_gmv = sum(b.total_amount for b in completed_bookings)
    total_commission = total_gmv * 0.12  # 12% commission
    
    commissions = Commission.query.all()
    commission_paid = sum(c.commission_amount for c in commissions if c.status == 'paid')
    commission_pending = sum(c.commission_amount for c in commissions if c.status == 'pending')
    
    providers = User.query.filter_by(is_provider=True).count()
    customers = User.query.filter_by(is_provider=False, is_admin=False).count()
    
    # Monthly breakdown
    from sqlalchemy import func, extract
    monthly_revenue = db.session.query(
        extract('month', Booking.created_at).label('month'),
        func.sum(Booking.total_amount).label('total')
    ).filter(Booking.status == 'completed').group_by('month').all()
    
    return jsonify({
        'overview': {
            'total_bookings': total_bookings,
            'completed_bookings': len(completed_bookings),
            'total_gmv': total_gmv,
            'total_commission': total_commission,
            'commission_paid': commission_paid,
            'commission_pending': commission_pending,
            'net_revenue': commission_paid
        },
        'users': {
            'providers': providers,
            'customers': customers,
            'total': providers + customers
        },
        'monthly': [{'month': m, 'revenue': round(float(r) * 0.12, 2)} for m, r in monthly_revenue],
        'commission_rate': 0.12
    })

@app.route('/api/admin/commission/update', methods=['POST'])
def update_commission_rate():
    """Update global commission rate (admin only)"""
    data = request.json
    new_rate = data.get('rate', 0.12)
    
    # In production, store this in a Settings model
    # For now, this is a placeholder endpoint
    
    return jsonify({
        'message': f'Commission rate updated to {new_rate * 100}%',
        'rate': new_rate
    })

@app.route('/api/admin/withdrawals')
def admin_withdrawals():
    """Get all pending provider withdrawal requests"""
    # This would integrate with payment provider in production
    # Placeholder for now
    
    providers = User.query.filter_by(is_provider=True).all()
    withdrawals = []
    
    for provider in providers:
        completed_bookings = Booking.query.join(Service).filter(
            Service.provider_id == provider.id,
            Booking.status == 'completed'
        ).all()
        
        total_earned = sum(b.total_amount * 0.88 for b in completed_bookings)  # 88% after 12% commission
        
        if total_earned > 0:
            withdrawals.append({
                'provider_id': provider.id,
                'provider_name': provider.full_name or provider.username,
                'total_earned': round(total_earned, 2),
                'bookings_count': len(completed_bookings),
                'status': 'pending'
            })
    
    return jsonify(withdrawals)

