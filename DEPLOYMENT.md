# Deployment Guide for Naija Connect

## Prerequisites

Before deploying, ensure you have:

1. **MongoDB Atlas Account**
   - Sign up at https://www.mongodb.com/cloud/atlas
   - Create a free cluster
   - Get your connection string
   - Whitelist all IPs (0.0.0.0/0) for serverless access

2. **Stripe Account**
   - Sign up at https://stripe.com
   - Get your test API keys
   - Enable Nigerian Naira (NGN) currency

3. **Vercel Account**
   - Sign up at https://vercel.com
   - Connect your GitHub account

## Step 1: Prepare MongoDB Database

1. Log into MongoDB Atlas
2. Create a database named `naija-connect`
3. Copy your connection string
4. Replace `<password>` with your database password
5. Example: `mongodb+srv://user:password@cluster.mongodb.net/naija-connect?retryWrites=true&w=majority`

## Step 2: Configure Stripe

1. Log into Stripe Dashboard
2. Navigate to Developers > API Keys
3. Copy your Publishable Key (starts with `pk_test_`)
4. Copy your Secret Key (starts with `sk_test_`)
5. Enable NGN currency in Settings > Payment Methods

## Step 3: Deploy to Vercel

### Option A: Deploy via Vercel Dashboard (Recommended)

1. Go to https://vercel.com/new
2. Import your GitHub repository `jahooskii/naija-connect`
3. Configure project:
   - Framework Preset: Other
   - Root Directory: ./
   - Build Command: (leave empty)
   - Output Directory: public
   - Install Command: npm install

4. Add Environment Variables:
   ```
   MONGODB_URI=your_mongodb_connection_string
   JWT_SECRET=your_random_secret_key_min_32_chars
   STRIPE_SECRET_KEY=sk_test_your_stripe_secret
   STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable
   NODE_ENV=production
   ```

5. Click "Deploy"

### Option B: Deploy via CLI

1. Install Vercel CLI:
   ```bash
   npm install -g vercel
   ```

2. Login:
   ```bash
   vercel login
   ```

3. Deploy:
   ```bash
   vercel
   ```

4. Follow prompts and set up environment variables:
   ```bash
   vercel env add MONGODB_URI
   vercel env add JWT_SECRET
   vercel env add STRIPE_SECRET_KEY
   vercel env add STRIPE_PUBLISHABLE_KEY
   vercel env add NODE_ENV
   ```

5. Deploy to production:
   ```bash
   vercel --prod
   ```

## Step 4: Verify Deployment

1. Visit your Vercel deployment URL
2. Test the landing page loads correctly
3. Try creating an account at `/pages/register.html`
4. Test login at `/pages/login.html`
5. Verify dashboard loads after login
6. Check admin dashboard (create admin user first)

## Step 5: Create Admin User

Since the first user won't be an admin, you'll need to manually update a user in MongoDB:

1. Register a regular account through the UI
2. Log into MongoDB Atlas
3. Browse Collections > users
4. Find your user
5. Edit the document and change `role` to `"admin"`
6. Save changes
7. Log out and log back in to access admin dashboard

## Step 6: Test Features

### Test Registration
1. Go to `/pages/register.html`
2. Fill out the form
3. Click "Create Account"
4. Should redirect to dashboard

### Test Login
1. Go to `/pages/login.html`
2. Enter credentials
3. Should redirect to dashboard

### Test Service Browsing
1. Login to dashboard
2. Services should load (empty if none created)
3. Try creating a service (provider account needed)

### Test Admin Dashboard
1. Login with admin account
2. Go to `/pages/admin-dashboard.html`
3. Should see statistics
4. QR code should display with your production URL

## Step 7: Configure Custom Domain (Optional)

1. Go to Vercel Project Settings
2. Navigate to Domains
3. Add your custom domain
4. Follow DNS configuration instructions
5. Wait for DNS propagation
6. QR code will automatically update with custom domain

## Troubleshooting

### API Errors
- Check Vercel logs for error details
- Verify environment variables are set
- Ensure MongoDB Atlas allows connections from 0.0.0.0/0

### Authentication Issues
- Clear browser localStorage
- Check JWT_SECRET is set
- Verify user exists in database

### Database Connection Errors
- Verify MONGODB_URI is correct
- Check MongoDB Atlas network access
- Ensure database user has read/write permissions

### Payment Errors
- Verify Stripe keys are correct
- Check Stripe dashboard for error logs
- Ensure NGN currency is enabled

## Security Checklist

- [ ] JWT_SECRET is a strong random string (32+ characters)
- [ ] MongoDB connection string uses strong password
- [ ] Environment variables are set in Vercel (not in code)
- [ ] CORS is configured correctly
- [ ] API routes require authentication where needed
- [ ] Passwords are hashed with bcrypt
- [ ] Input validation is in place

## Post-Deployment

1. Monitor Vercel Analytics
2. Check MongoDB Atlas metrics
3. Review Stripe dashboard for transactions
4. Update QR code if using custom domain
5. Share deployment URL with users

## Production URL

After deployment, your app will be available at:
- Vercel URL: `https://your-project.vercel.app`
- Custom domain: `https://your-domain.com` (if configured)

The QR code in the admin dashboard will automatically use your production URL.

## Support

If you encounter issues:
1. Check Vercel deployment logs
2. Review MongoDB Atlas logs
3. Check Stripe webhook logs
4. Create an issue on GitHub
5. Contact: admin@naija-connect.com

## Next Steps

After successful deployment:
1. Create test services
2. Test booking flow
3. Configure Stripe webhooks for production
4. Set up monitoring and alerts
5. Add analytics tracking
6. Configure backup strategy
7. Set up CI/CD pipeline

---

**Congratulations! Your Naija Connect marketplace is now live! 🎉**
