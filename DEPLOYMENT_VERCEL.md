# Vercel Deployment Guide

## Deploying Raven to Vercel

### Prerequisites
- Vercel account (free at vercel.com)
- GitHub repository with your code

### Step 1: Prepare Your Repository

1. **Ensure all files are committed to Git:**
   ```bash
   git add .
   git commit -m "Prepare for Vercel deployment"
   git push origin main
   ```

2. **Verify your repository structure:**
   ```
   raven/
   ├── api.py              # Flask API
   ├── vercel.json         # Vercel config
   ├── requirements.txt    # Python dependencies
   ├── frontend/          # React app
   │   ├── package.json
   │   └── src/
   └── src/               # Backend modules
   ```

### Step 2: Deploy to Vercel

1. **Go to [vercel.com](https://vercel.com) and sign in**

2. **Click "New Project"**

3. **Import your GitHub repository:**
   - Connect your GitHub account if not already connected
   - Select your `raven` repository
   - Click "Import"

4. **Configure the project:**
   - **Framework Preset**: Other
   - **Root Directory**: `./` (leave as default)
   - **Build Command**: Leave empty (Vercel will auto-detect)
   - **Output Directory**: Leave empty
   - **Install Command**: Leave empty

5. **Environment Variables (Optional):**
   - Add any email credentials if needed
   - Most features will work without them for demo purposes

6. **Click "Deploy"**

### Step 3: Get Your Live URL

After deployment (usually 2-3 minutes), Vercel will provide you with:
- **Production URL**: `https://your-project-name.vercel.app`
- **Preview URLs**: For each branch/PR

### Step 4: Test Your Deployment

1. **Visit your Vercel URL**
2. **Test the features:**
   - Dashboard loads correctly
   - Email processing (may need credentials)
   - Bank statement upload
   - Ledger view

### Troubleshooting

**If the API doesn't work:**
- Check Vercel function logs in the dashboard
- Ensure `api.py` is in the root directory
- Verify `requirements.txt` includes all dependencies

**If the frontend doesn't load:**
- Check if `frontend/package.json` exists
- Verify build process completes successfully

**Common Issues:**
- **CORS errors**: The API should handle CORS automatically
- **File upload issues**: Vercel has read-only filesystem, so file uploads won't persist
- **Email processing**: Requires proper IMAP credentials

### Demo Mode

For the demo, you can:
1. **Use sample data** without email credentials
2. **Upload sample CSV files** for bank comparison
3. **Show the UI and features** without live email processing

### Environment Variables (Optional)

If you want full functionality, add these in Vercel dashboard:
```
EMAIL_HOST=imap.gmail.com
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
```

### Final Steps

1. **Test all features** on your Vercel URL
2. **Share the URL** with your evaluators
3. **Document any limitations** (file persistence, email setup, etc.)

Your Raven application will be live at: `https://your-project-name.vercel.app` 