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

app = Flask(__name__)
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
    
    services = db.relationship('Service', backref='provider', lazy=True)
    bookings = db.relationship('Booking', backref='customer', lazy=True)
    reviews = db.relationship('Review', backref='reviewer', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
