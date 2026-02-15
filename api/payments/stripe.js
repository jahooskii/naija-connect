const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);
const { connectToDatabase } = require('../../lib/mongodb');
const { authenticateRequest } = require('../../lib/auth');
const { cors } = require('../../lib/middleware');
const Booking = require('../../models/Booking');

async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const authUser = authenticateRequest(req);
    if (!authUser) {
      return res.status(401).json({ error: 'Unauthorized' });
    }

    const { bookingId, amount, currency } = req.body;

    if (!bookingId || !amount) {
      return res.status(400).json({ error: 'Missing required fields' });
    }

    const { db } = await connectToDatabase();

    // Create payment intent
    const paymentIntent = await stripe.paymentIntents.create({
      amount: Math.round(amount * 100), // Convert to cents
      currency: currency || 'ngn',
      metadata: {
        bookingId,
        userId: authUser.userId
      }
    });

    // Update booking with payment intent
    await Booking.update(db, bookingId, {
      paymentId: paymentIntent.id,
      paymentStatus: 'processing'
    });

    return res.status(200).json({
      success: true,
      clientSecret: paymentIntent.client_secret,
      paymentIntentId: paymentIntent.id
    });

  } catch (error) {
    console.error('Payment error:', error);
    return res.status(500).json({ error: 'Internal server error' });
  }
}

module.exports = cors(handler);
