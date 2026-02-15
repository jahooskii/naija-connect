const { connectToDatabase } = require('../../lib/mongodb');
const { authenticateRequest } = require('../../lib/auth');
const { cors } = require('../../lib/middleware');
const User = require('../../models/User');

async function handler(req, res) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    // Authenticate user
    const authUser = authenticateRequest(req);
    if (!authUser) {
      return res.status(401).json({ error: 'Unauthorized' });
    }

    const { db } = await connectToDatabase();

    // Get user profile
    const user = await User.findById(db, authUser.userId);
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }

    // Return user data (without password)
    const { password: _, ...userWithoutPassword } = user;

    return res.status(200).json({
      success: true,
      user: userWithoutPassword
    });

  } catch (error) {
    console.error('Profile error:', error);
    return res.status(500).json({ error: 'Internal server error' });
  }
}

module.exports = cors(handler);
