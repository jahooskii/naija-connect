const { connectToDatabase } = require('../../lib/mongodb');
const { authenticateRequest } = require('../../lib/auth');
const { cors } = require('../../lib/middleware');
const Booking = require('../../models/Booking');

async function handler(req, res) {
  try {
    const authUser = authenticateRequest(req);
    if (!authUser) {
      return res.status(401).json({ error: 'Unauthorized' });
    }

    const { db } = await connectToDatabase();

    if (req.method === 'GET') {
      // Get user's bookings
      let bookings;
      if (authUser.role === 'provider') {
        bookings = await Booking.findByProviderId(db, authUser.userId);
      } else {
        bookings = await Booking.findByCustomerId(db, authUser.userId);
      }
      return res.status(200).json({ success: true, bookings });
    }

    if (req.method === 'POST') {
      // Create new booking
      const { serviceId, providerId, date, time, duration, totalAmount, notes } = req.body;

      if (!serviceId || !providerId || !date || !time || !totalAmount) {
        return res.status(400).json({ error: 'Missing required fields' });
      }

      const bookingData = {
        serviceId,
        customerId: authUser.userId,
        providerId,
        date,
        time,
        duration: duration || 1,
        totalAmount: parseFloat(totalAmount),
        notes: notes || ''
      };

      const booking = await Booking.create(db, bookingData);
      return res.status(201).json({ success: true, booking });
    }

    return res.status(405).json({ error: 'Method not allowed' });

  } catch (error) {
    console.error('Bookings error:', error);
    return res.status(500).json({ error: 'Internal server error' });
  }
}

module.exports = cors(handler);
