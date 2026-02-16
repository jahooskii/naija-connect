# 🚀 Deploy Naija Connect to Render (FREE)

Everything is ready! Follow these steps to get your public URL:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Step 1: Create Render Account (2 minutes)

1. Go to: https://render.com
2. Click "Get Started for Free"
3. Sign up with:
   - GitHub (easiest)
   - OR Google
   - OR Email

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Step 2: Upload Your Code (2 options)

### OPTION A: GitHub (Recommended - Auto Updates)

1. Go to https://github.com
2. Create new repository: "naija-connect"
3. In your Mac terminal:
   ```bash
   cd ~/Desktop/naija-connect-app
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/naija-connect.git
   git push -u origin main
   ```

### OPTION B: Direct Upload (Faster, No GitHub Needed)

1. In Render dashboard, click "New +"
2. Select "Web Service"
3. Click "Public Git repository"
4. Paste: https://github.com/YOUR_USERNAME/naija-connect
5. OR use the "Deploy from Render Blueprint" option

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Step 3: Configure Render (1 minute)

On Render's setup page, enter:

**Name:** naija-connect
**Region:** Frankfurt (closest to Nigeria)
**Branch:** main
**Build Command:** pip install -r requirements.txt
**Start Command:** cd backend && python app.py

**Environment:**
- Python

**Instance Type:** Free

Click "Create Web Service"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Step 4: Wait for Deployment (2-3 minutes)

Render will:
1. Install Python packages ⏳
2. Start your app ⏳
3. Give you a public URL ✅

Watch the build logs in real-time!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Step 5: Get Your Public URL! 🎉

Render gives you:

**https://naija-connect.onrender.com**

This URL:
✅ Works on ALL devices (iPhone, Android, desktop)
✅ Works when shared on WhatsApp
✅ Auto HTTPS (secure)
✅ FREE forever
✅ Global access

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## ⚠️ IMPORTANT: Free Tier Notes

**Free tier includes:**
- ✅ 750 hours/month (plenty for starting)
- ✅ Automatic HTTPS
- ✅ Auto deploys from GitHub
- ⚠️ Sleeps after 15 min inactivity
- ⚠️ Wakes up in ~30 seconds on first visit

**To keep it always on:**
- Upgrade to $7/month (when you start making money)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 📱 Share Your App

After deployment, share this message on WhatsApp:

```
🇳🇬 Naija Connect is LIVE! 🚀

Find trusted service providers in Nigeria:
✅ Hairstylists
✅ Plumbers
✅ Electricians
✅ Caterers
✅ And more!

Try it now: https://naija-connect.onrender.com

Works on all phones! 📱
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 🔄 How to Update Later

When you make changes:

**If using GitHub:**
```bash
cd ~/Desktop/naija-connect-app
git add .
git commit -m "Update description"
git push
```
Render auto-deploys in 2 minutes!

**If not using GitHub:**
Re-upload files through Render dashboard

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## ✅ Files Ready for Render

✓ requirements.txt (dependencies)
✓ Procfile (start command)
✓ runtime.txt (Python version)
✓ render.yaml (configuration)
✓ app.py (updated for Render PORT)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 🎯 Next Steps

1. Go to https://render.com
2. Create account
3. Deploy your app
4. Get your public URL
5. Start sharing and monetizing! 💰

**Need help? Tell me where you got stuck!**

