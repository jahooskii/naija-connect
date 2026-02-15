const bcrypt = require('bcryptjs');
const { connectToDatabase } = require('../../lib/mongodb');
const { generateToken } = require('../../lib/auth');
const { cors } = require('../../lib/middleware');
const User = require('../../models/User');

async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { email, password, firstName, lastName, phone, role, referralCode } = req.body;

    // Validation
    if (!email || !password || !firstName || !lastName) {
      return res.status(400).json({ error: 'Missing required fields' });
    }

    if (password.length < 6) {
      return res.status(400).json({ error: 'Password must be at least 6 characters' });
    }

    const { db } = await connectToDatabase();

    // Check if user already exists
    const existingUser = await User.findByEmail(db, email);
    if (existingUser) {
      return res.status(400).json({ error: 'User already exists' });
    }

    // Hash password
    const hashedPassword = await bcrypt.hash(password, 10);

    // Handle referral
    let referredBy = null;
    if (referralCode) {
      const referrer = await db.collection('users').findOne({ referralCode });
      if (referrer) {
        referredBy = referrer._id.toString();
        // Award referral bonus
        await User.update(db, referrer._id.toString(), {
          earnings: (referrer.earnings || 0) + 500
        });
      }
    }

    // Create user
    const userData = {
      email,
      password: hashedPassword,
      firstName,
      lastName,
      phone: phone || '',
      role: role || 'user',
      isProvider: role === 'provider',
      referredBy
    };

    const user = await User.create(db, userData);

    // Generate JWT token
    const token = generateToken(user);

    // Return user data (without password)
    const { password: _, ...userWithoutPassword } = user;

    return res.status(201).json({
      success: true,
      user: userWithoutPassword,
      token
    });

  } catch (error) {
    console.error('Register error:', error);
    return res.status(500).json({ error: 'Internal server error' });
  }
}

module.exports = cors(handler);
