const { connectToDatabase } = require('../../lib/mongodb');
const { authenticateRequest } = require('../../lib/auth');
const { cors } = require('../../lib/middleware');
const Review = require('../../models/Review');

async function handler(req, res) {
  try {
    const { db } = await connectToDatabase();

    if (req.method === 'GET') {
      // Get reviews by service ID
      const { serviceId } = req.query;
      if (!serviceId) {
        return res.status(400).json({ error: 'Service ID required' });
      }

      const reviews = await Review.findByServiceId(db, serviceId);
      return res.status(200).json({ success: true, reviews });
    }

    if (req.method === 'POST') {
      // Create review (requires authentication)
      const authUser = authenticateRequest(req);
      if (!authUser) {
        return res.status(401).json({ error: 'Unauthorized' });
      }

      const { serviceId, bookingId, providerId, rating, comment } = req.body;

      if (!serviceId || !bookingId || !providerId || !rating) {
        return res.status(400).json({ error: 'Missing required fields' });
      }

      if (rating < 1 || rating > 5) {
        return res.status(400).json({ error: 'Rating must be between 1 and 5' });
      }

      const reviewData = {
        serviceId,
        bookingId,
        customerId: authUser.userId,
        providerId,
        rating: parseInt(rating),
        comment: comment || ''
      };

      const review = await Review.create(db, reviewData);
      return res.status(201).json({ success: true, review });
    }

    return res.status(405).json({ error: 'Method not allowed' });

  } catch (error) {
    console.error('Reviews error:', error);
    return res.status(500).json({ error: 'Internal server error' });
  }
}

module.exports = cors(handler);
