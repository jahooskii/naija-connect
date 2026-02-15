const { ObjectId } = require('mongodb');

class User {
  constructor(data) {
    this._id = data._id || new ObjectId();
    this.email = data.email;
    this.password = data.password; // Should be hashed
    this.firstName = data.firstName;
    this.lastName = data.lastName;
    this.phone = data.phone;
    this.role = data.role || 'user'; // user, provider, admin
    this.isProvider = data.isProvider || false;
    this.profileImage = data.profileImage || '';
    this.address = data.address || '';
    this.city = data.city || '';
    this.state = data.state || '';
    this.verified = data.verified || false;
    this.referralCode = data.referralCode || this.generateReferralCode();
    this.referredBy = data.referredBy || null;
    this.earnings = data.earnings || 0;
    this.createdAt = data.createdAt || new Date();
    this.updatedAt = data.updatedAt || new Date();
  }

  generateReferralCode() {
    return Math.random().toString(36).substring(2, 10).toUpperCase();
  }

  static async create(db, userData) {
    const user = new User(userData);
    const result = await db.collection('users').insertOne(user);
    return { ...user, _id: result.insertedId };
  }

  static async findByEmail(db, email) {
    return db.collection('users').findOne({ email });
  }

  static async findById(db, id) {
    return db.collection('users').findOne({ _id: new ObjectId(id) });
  }

  static async update(db, id, updates) {
    updates.updatedAt = new Date();
    const result = await db.collection('users').updateOne(
      { _id: new ObjectId(id) },
      { $set: updates }
    );
    return result.modifiedCount > 0;
  }
}

module.exports = User;
