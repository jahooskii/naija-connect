const { connectToDatabase } = require('../../lib/mongodb');
const { authenticateRequest } = require('../../lib/auth');
const { cors } = require('../../lib/middleware');
const Booking = require('../../models/Booking');

async function handler(req, res) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const authUser = authenticateRequest(req);
    if (!authUser || authUser.role !== 'admin') {
      return res.status(403).json({ error: 'Admin access required' });
    }

    const { db } = await connectToDatabase();

    // Get statistics
    const [
      totalUsers,
      totalServices,
      totalBookings,
      bookingStats
    ] = await Promise.all([
      db.collection('users').countDocuments(),
      db.collection('services').countDocuments(),
      db.collection('bookings').countDocuments(),
      Booking.getStats(db)
    ]);

    // Calculate revenue
    const completedBookings = bookingStats.find(s => s._id === 'completed') || {};
    const totalRevenue = completedBookings.totalRevenue || 0;
    const totalCommission = completedBookings.totalCommission || 0;

    // Get recent bookings
    const recentBookings = await db.collection('bookings')
      .find()
      .sort({ createdAt: -1 })
      .limit(10)
      .toArray();

    // Get service categories distribution
    const servicesByCategory = await db.collection('services').aggregate([
      { $group: { _id: '$category', count: { $sum: 1 } } }
    ]).toArray();

    return res.status(200).json({
      success: true,
      stats: {
        totalUsers,
        totalServices,
        totalBookings,
        totalRevenue,
        totalCommission,
        bookingStats,
        recentBookings,
        servicesByCategory
      }
    });

  } catch (error) {
    console.error('Admin stats error:', error);
    return res.status(500).json({ error: 'Internal server error' });
  }
}

module.exports = cors(handler);
