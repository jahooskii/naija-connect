const { ObjectId } = require('mongodb');

class Booking {
  constructor(data) {
    this._id = data._id || new ObjectId();
    this.serviceId = data.serviceId;
    this.customerId = data.customerId;
    this.providerId = data.providerId;
    this.date = data.date;
    this.time = data.time;
    this.duration = data.duration || 1;
    this.totalAmount = data.totalAmount;
    this.commission = data.commission || (data.totalAmount * 0.12); // 12% commission
    this.status = data.status || 'pending'; // pending, confirmed, completed, cancelled
    this.paymentStatus = data.paymentStatus || 'pending'; // pending, paid, refunded
    this.paymentId = data.paymentId || null;
    this.notes = data.notes || '';
    this.createdAt = data.createdAt || new Date();
    this.updatedAt = data.updatedAt || new Date();
  }

  static async create(db, bookingData) {
    const booking = new Booking(bookingData);
    const result = await db.collection('bookings').insertOne(booking);
    return { ...booking, _id: result.insertedId };
  }

  static async findById(db, id) {
    return db.collection('bookings').findOne({ _id: new ObjectId(id) });
  }

  static async findByCustomerId(db, customerId) {
    return db.collection('bookings').find({ customerId }).sort({ createdAt: -1 }).toArray();
  }

  static async findByProviderId(db, providerId) {
    return db.collection('bookings').find({ providerId }).sort({ createdAt: -1 }).toArray();
  }

  static async update(db, id, updates) {
    updates.updatedAt = new Date();
    const result = await db.collection('bookings').updateOne(
      { _id: new ObjectId(id) },
      { $set: updates }
    );
    return result.modifiedCount > 0;
  }

  static async getStats(db) {
    const pipeline = [
      {
        $group: {
          _id: '$status',
          count: { $sum: 1 },
          totalRevenue: { $sum: '$totalAmount' },
          totalCommission: { $sum: '$commission' }
        }
      }
    ];
    return db.collection('bookings').aggregate(pipeline).toArray();
  }
}

module.exports = Booking;
