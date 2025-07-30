# Render Deployment Guide

## Deploying Raven to Render

### Why Render?
- **No size limits** for Python dependencies (unlike Vercel's 250MB limit)
- **Free tier** available
- **Easy deployment** with automatic builds
- **Persistent storage** for file uploads

### Prerequisites
- Render account (free at render.com)
- GitHub repository with your code

### Step 1: Prepare Your Repository

1. **Ensure all files are committed to Git:**
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

2. **Verify your repository structure:**
   ```
   raven/
   ├── api.py              # Flask API
   ├── render.yaml         # Render config
   ├── requirements.txt    # Python dependencies
   ├── frontend/          # React app
   │   ├── package.json
   │   └── src/
   └── src/               # Backend modules
   ```

### Step 2: Deploy to Render

1. **Go to [render.com](https://render.com) and sign in**

2. **Click "New +" and select "Blueprint"**

3. **Connect your GitHub repository:**
   - Connect your GitHub account if not already connected
   - Select your `raven` repository
   - Click "Connect"

4. **Render will automatically detect the services from render.yaml:**
   - **raven-api**: Python web service
   - **raven-frontend**: Static site

5. **Click "Apply" to deploy both services**

### Step 3: Get Your Live URLs

After deployment (usually 5-10 minutes), Render will provide:
- **API URL**: `https://raven-api.onrender.com`
- **Frontend URL**: `https://raven-frontend.onrender.com`

### Step 4: Configure Environment Variables (Optional)

For full functionality, add these in the Render dashboard:

**For raven-api service:**
```
EMAIL_HOST=imap.gmail.com
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
```

### Step 5: Test Your Deployment

1. **Visit your frontend URL**
2. **Test the features:**
   - Dashboard loads correctly
   - Email processing (may need credentials)
   - Bank statement upload
   - Ledger view

### Troubleshooting

**If the API doesn't work:**
- Check Render logs in the dashboard
- Ensure `api.py` is in the root directory
- Verify `requirements.txt` includes all dependencies

**If the frontend doesn't load:**
- Check if `frontend/package.json` exists
- Verify build process completes successfully
- Check the REACT_APP_API_URL environment variable

**Common Issues:**
- **CORS errors**: The API should handle CORS automatically
- **File upload issues**: Render has persistent storage, so uploads will work
- **Email processing**: Requires proper IMAP credentials

### Demo Mode

For the demo, you can:
1. **Use sample data** without email credentials
2. **Upload sample CSV files** for bank comparison
3. **Show the UI and features** without live email processing

### Environment Variables (Optional)

If you want full functionality, add these in Render dashboard for the API service:
```
EMAIL_HOST=imap.gmail.com
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
```

### Final Steps

1. **Test all features** on your Render URLs
2. **Share the frontend URL** with your evaluators
3. **Document any limitations** (email setup, etc.)

Your Raven application will be live at:
- **Frontend**: `https://raven-frontend.onrender.com`
- **API**: `https://raven-api.onrender.com`

### Advantages of Render over Vercel

✅ **No size limits** - Can handle large Python dependencies
✅ **Persistent storage** - File uploads work properly
✅ **Better for Python** - Optimized for Python applications
✅ **Free tier** - Generous free tier available
✅ **Easy scaling** - Can upgrade to paid plans if needed 