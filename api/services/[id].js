const { connectToDatabase } = require('../../lib/mongodb');
const { authenticateRequest } = require('../../lib/auth');
const { cors } = require('../../lib/middleware');
const Service = require('../../models/Service');

async function handler(req, res) {
  try {
    const { id } = req.query;
    const { db } = await connectToDatabase();

    if (req.method === 'GET') {
      // Get service by ID
      const service = await Service.findById(db, id);
      if (!service) {
        return res.status(404).json({ error: 'Service not found' });
      }
      return res.status(200).json({ success: true, service });
    }

    if (req.method === 'PUT') {
      // Update service (requires authentication and ownership)
      const authUser = authenticateRequest(req);
      if (!authUser) {
        return res.status(401).json({ error: 'Unauthorized' });
      }

      const service = await Service.findById(db, id);
      if (!service) {
        return res.status(404).json({ error: 'Service not found' });
      }

      if (service.providerId !== authUser.userId && authUser.role !== 'admin') {
        return res.status(403).json({ error: 'Forbidden' });
      }

      const updates = req.body;
      delete updates._id;
      delete updates.providerId;

      await Service.update(db, id, updates);
      return res.status(200).json({ success: true, message: 'Service updated' });
    }

    if (req.method === 'DELETE') {
      // Delete service (requires authentication and ownership)
      const authUser = authenticateRequest(req);
      if (!authUser) {
        return res.status(401).json({ error: 'Unauthorized' });
      }

      const service = await Service.findById(db, id);
      if (!service) {
        return res.status(404).json({ error: 'Service not found' });
      }

      if (service.providerId !== authUser.userId && authUser.role !== 'admin') {
        return res.status(403).json({ error: 'Forbidden' });
      }

      await Service.delete(db, id);
      return res.status(200).json({ success: true, message: 'Service deleted' });
    }

    return res.status(405).json({ error: 'Method not allowed' });

  } catch (error) {
    console.error('Service detail error:', error);
    return res.status(500).json({ error: 'Internal server error' });
  }
}

module.exports = cors(handler);
