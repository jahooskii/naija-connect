#!/usr/bin/env python3
"""
Admin User Setup Script
Run this to create the admin user for Naija Connect
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User

def create_admin_user():
    """Create default admin user"""
    with app.app_context():
        # Check if admin already exists
        admin = User.query.filter_by(username='admin').first()
        
        if admin:
            admin.email = 'admin@naijaconnect.ng'
            admin.full_name = 'Administrator'
            admin.is_admin = True
            admin.is_provider = False
            admin.set_password('admin123')
            db.session.commit()

            print("✅ Admin user updated successfully!")
            print("\n   Login credentials:")
            print("   Username: admin")
            print("   Password: admin123")
            print("\n   ⚠️  IMPORTANT: Change password in production!")
            return
        
        # Create new admin user
        new_admin = User(
            username='admin',
            email='admin@naijaconnect.ng',
            full_name='Administrator',
            is_admin=True,
            is_provider=False
        )
        new_admin.set_password('admin123')
        
        db.session.add(new_admin)
        db.session.commit()
        
        print("✅ Admin user created successfully!")
        print("\n   Login credentials:")
        print("   Username: admin")
        print("   Password: admin123")
        print("\n   ⚠️  IMPORTANT: Change password in production!")

if __name__ == '__main__':
    print("\n🔐 Creating Naija Connect Admin User...\n")
    create_admin_user()
    print("\n✨ Setup complete!\n")
