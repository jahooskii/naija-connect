const { ObjectId } = require('mongodb');

class Review {
  constructor(data) {
    this._id = data._id || new ObjectId();
    this.serviceId = data.serviceId;
    this.bookingId = data.bookingId;
    this.customerId = data.customerId;
    this.providerId = data.providerId;
    this.rating = data.rating; // 1-5
    this.comment = data.comment || '';
    this.response = data.response || '';
    this.createdAt = data.createdAt || new Date();
    this.updatedAt = data.updatedAt || new Date();
  }

  static async create(db, reviewData) {
    const review = new Review(reviewData);
    const result = await db.collection('reviews').insertOne(review);
    
    // Update service rating
    await this.updateServiceRating(db, reviewData.serviceId);
    
    return { ...review, _id: result.insertedId };
  }

  static async findByServiceId(db, serviceId) {
    return db.collection('reviews').find({ serviceId }).sort({ createdAt: -1 }).toArray();
  }

  static async updateServiceRating(db, serviceId) {
    const reviews = await this.findByServiceId(db, serviceId);
    const avgRating = reviews.reduce((sum, r) => sum + r.rating, 0) / reviews.length;
    
    await db.collection('services').updateOne(
      { _id: new ObjectId(serviceId) },
      { 
        $set: { 
          rating: Math.round(avgRating * 10) / 10,
          reviewCount: reviews.length 
        } 
      }
    );
  }
}

module.exports = Review;
