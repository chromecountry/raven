# Render Deployment Guide

## Deploy to Render

### 1. Create Render Account
- Go to [render.com](https://render.com)
- Sign up with GitHub account

### 2. Deploy from GitHub
1. **Connect GitHub repository**
   - Click "New +" → "Web Service"
   - Connect your GitHub account
   - Select the `raven` repository

2. **Configure the service**
   - **Name**: `raven-receipt-processor`
   - **Environment**: `Python`
   - **Build Command**: `pip install -r cfg/prd/requirements.txt`
   - **Start Command**: `./start.sh`
   - **Plan**: Free

3. **Environment Variables**
   Add these environment variables in Render dashboard:
   ```
   EMAIL_HOST=imap.gmail.com
   EMAIL_PORT=993
   EMAIL_USER=your-email@gmail.com
   EMAIL_PASSWORD=your-app-password
   FAVA_HOST=0.0.0.0
   FAVA_PORT=$PORT
   ```

### 3. Deploy
- Click "Create Web Service"
- Render will automatically deploy your application
- Wait for build to complete (usually 2-3 minutes)

### 4. Access Your Application
- Once deployed, you'll get a URL like: `https://raven-receipt-processor.onrender.com`
- This is your Fava web interface
- You can also access API endpoints at `/api/*`

## API Endpoints

### Process Emails
```bash
curl -X POST https://your-app.onrender.com/api/process-emails
```

### Upload Bank Statement
```bash
curl -X POST https://your-app.onrender.com/api/upload-bank-statement \
  -F "file=@bank_statement.csv"
```

### View Ledger
```bash
curl https://your-app.onrender.com/api/ledger
```

### Health Check
```bash
curl https://your-app.onrender.com/api/health
```

## Features Available

✅ **Fava Web Interface** - Professional accounting interface
✅ **Email Processing** - Automatic receipt processing
✅ **Bank Statement Comparison** - Upload and compare CSV files
✅ **API Endpoints** - Programmatic access to all features
✅ **Ledger Management** - Beancount double-entry bookkeeping

## Troubleshooting

### Build Issues
- Check that all dependencies are in `cfg/prd/requirements.txt`
- Ensure `start.sh` is executable

### Runtime Issues
- Check Render logs for error messages
- Verify environment variables are set correctly
- Ensure email credentials are valid

### Performance
- Free tier may have cold starts
- Consider upgrading to paid plan for better performance 