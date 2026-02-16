"""
Admin Login Module
Integrates with the main Flask app
"""

# Default admin credentials (change in production):
# Username: admin
# Email: admin@naijaconnect.ng
# Password: admin123

# To create admin user, run in Python shell:
# from app import app, db, User
# with app.app_context():
#     admin = User(
#         username='admin',
#         email='admin@naijaconnect.ng',
#         full_name='Admin User',
#         is_admin=True
#     )
#     admin.set_password('admin123')
#     db.session.add(admin)
#     db.session.commit()
#     print('Admin user created successfully')
