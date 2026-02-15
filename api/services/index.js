const { connectToDatabase } = require('../../lib/mongodb');
const { authenticateRequest } = require('../../lib/auth');
const { cors } = require('../../lib/middleware');
const Service = require('../../models/Service');

async function handler(req, res) {
  try {
    const { db } = await connectToDatabase();

    if (req.method === 'GET') {
      // Get all approved services or filter by category
      const { category, search } = req.query;
      const filters = {};
      
      if (category) {
        filters.category = category;
      }
      
      if (search) {
        filters.$or = [
          { title: { $regex: search, $options: 'i' } },
          { description: { $regex: search, $options: 'i' } }
        ];
      }

      const services = await Service.findAll(db, filters);
      return res.status(200).json({ success: true, services });
    }

    if (req.method === 'POST') {
      // Create new service (requires authentication)
      const authUser = authenticateRequest(req);
      if (!authUser) {
        return res.status(401).json({ error: 'Unauthorized' });
      }

      const { title, description, category, price, priceType, location, images, tags } = req.body;

      if (!title || !description || !category || !price) {
        return res.status(400).json({ error: 'Missing required fields' });
      }

      const serviceData = {
        providerId: authUser.userId,
        title,
        description,
        category,
        price: parseFloat(price),
        priceType: priceType || 'fixed',
        location: location || '',
        images: images || [],
        tags: tags || []
      };

      const service = await Service.create(db, serviceData);
      return res.status(201).json({ success: true, service });
    }

    return res.status(405).json({ error: 'Method not allowed' });

  } catch (error) {
    console.error('Services error:', error);
    return res.status(500).json({ error: 'Internal server error' });
  }
}

module.exports = cors(handler);
