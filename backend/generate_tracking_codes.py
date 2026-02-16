#!/usr/bin/env python3
"""Generate tracking codes for existing providers"""

import secrets
from app import app, db, User

with app.app_context():
    # Get all providers
    providers = User.query.filter_by(is_provider=True).all()
    
    updated = 0
    for provider in providers:
        if not provider.tracking_code:
            provider.tracking_code = secrets.token_urlsafe(8)
            updated += 1
    
    db.session.commit()
    
    print(f"✅ Generated tracking codes for {updated} providers")
    
    # Display some examples
    if providers:
        print("\n📊 Sample Provider Tracking Links:")
        for provider in providers[:3]:
            print(f"\n{provider.full_name}:")
            print(f"  Code: {provider.tracking_code}")
            print(f"  Link: http://localhost:8000/track/{provider.tracking_code}")

