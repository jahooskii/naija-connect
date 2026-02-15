const { ObjectId } = require('mongodb');

class Service {
  constructor(data) {
    this._id = data._id || new ObjectId();
    this.providerId = data.providerId;
    this.title = data.title;
    this.description = data.description;
    this.category = data.category;
    this.price = data.price;
    this.priceType = data.priceType || 'fixed'; // fixed, hourly
    this.location = data.location || '';
    this.images = data.images || [];
    this.tags = data.tags || [];
    this.availability = data.availability || 'available'; // available, unavailable
    this.rating = data.rating || 0;
    this.reviewCount = data.reviewCount || 0;
    this.bookingCount = data.bookingCount || 0;
    this.status = data.status || 'pending'; // pending, approved, rejected
    this.createdAt = data.createdAt || new Date();
    this.updatedAt = data.updatedAt || new Date();
  }

  static async create(db, serviceData) {
    const service = new Service(serviceData);
    const result = await db.collection('services').insertOne(service);
    return { ...service, _id: result.insertedId };
  }

  static async findById(db, id) {
    return db.collection('services').findOne({ _id: new ObjectId(id) });
  }

  static async findByProviderId(db, providerId) {
    return db.collection('services').find({ providerId }).toArray();
  }

  static async findAll(db, filters = {}) {
    const query = { status: 'approved', ...filters };
    return db.collection('services').find(query).toArray();
  }

  static async update(db, id, updates) {
    updates.updatedAt = new Date();
    const result = await db.collection('services').updateOne(
      { _id: new ObjectId(id) },
      { $set: updates }
    );
    return result.modifiedCount > 0;
  }

  static async delete(db, id) {
    const result = await db.collection('services').deleteOne({ _id: new ObjectId(id) });
    return result.deletedCount > 0;
  }
}

module.exports = Service;
