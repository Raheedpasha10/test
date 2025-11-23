# 🚀 Student Compass - Render Deployment Guide

## 🎯 Quick Deploy to Render

Your Student Compass application is now ready for Render deployment! Follow these steps:

### **📋 Prerequisites**
- GitHub repository with latest code ✅
- Render account (free at render.com) 
- Your API keys ready

### **🔧 Step 1: Prepare Repository**
All necessary files are already configured:
- ✅ `render.yaml` - Render configuration
- ✅ `Dockerfile` - Container configuration  
- ✅ Build scripts and environment files
- ✅ Production-ready API configuration

### **🚀 Step 2: Deploy Backend (FastAPI)**

1. **Go to Render Dashboard**
   - Visit [render.com](https://render.com)
   - Sign in and click "New +"
   - Select "Web Service"

2. **Connect Repository**
   - Connect your GitHub account
   - Select your `test` repository
   - Branch: `main`

3. **Configure Backend Service**
   ```
   Name: student-compass-api
   Environment: Python 3
   Build Command: cd Generative && pip install -r requirements.txt
   Start Command: cd Generative && uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

4. **Add Environment Variables**
   ```
   GROQ_API_KEY=your_actual_groq_api_key_here
   GOOGLE_GENAI_API_KEY=your_google_api_key_here
   ENVIRONMENT=production
   HOST=0.0.0.0
   PORT=$PORT
   ```

5. **Deploy Backend**
   - Click "Create Web Service"
   - Wait for deployment (3-5 minutes)
   - Note the backend URL (e.g., `https://student-compass-api.onrender.com`)

### **🎨 Step 3: Deploy Frontend (React)**

1. **Create Another Web Service**
   - Click "New +" → "Static Site"
   - Connect same GitHub repository

2. **Configure Frontend Service**
   ```
   Name: student-compass-frontend
   Build Command: cd Generative/frontend && npm ci && npm run build
   Publish Directory: Generative/frontend/build
   ```

3. **Add Environment Variable**
   ```
   REACT_APP_API_URL=https://student-compass-api.onrender.com
   ```
   *(Replace with your actual backend URL from Step 2)*

4. **Deploy Frontend**
   - Click "Create Static Site" 
   - Wait for deployment (2-3 minutes)
   - Get your live URL!

### **✅ Step 4: Verify Deployment**

1. **Test Backend**
   - Visit: `https://your-api.onrender.com/health`
   - Should return: `{"status": "healthy", "groq_available": true}`

2. **Test Frontend**
   - Visit your frontend URL
   - Try generating a roadmap
   - Should show real AI content (no demo data)

### **🔧 Alternative: One-Click Deploy**

You can also use the `render.yaml` file for automatic deployment:
1. In Render dashboard, click "New +"
2. Select "Blueprint"
3. Connect repository and deploy both services at once

### **💡 Pro Tips**

- **Free Tier**: Render's free tier is perfect for testing
- **Custom Domain**: Add your own domain in Render dashboard
- **Auto-Deploy**: Pushes to main branch will auto-deploy
- **Logs**: Check logs in Render dashboard for debugging
- **Scaling**: Easily scale up when you get more users

### **🆘 Troubleshooting**

**Build Fails?**
- Check that all files are committed and pushed
- Verify environment variables are set correctly

**API Not Working?**
- Ensure GROQ_API_KEY is set in backend environment
- Check backend logs in Render dashboard

**Frontend Can't Connect?**
- Verify REACT_APP_API_URL points to correct backend URL
- Check CORS settings in backend

### **🎉 You're Live!**

Once deployed, your Student Compass will be:
- ✅ **Globally accessible** via Render URLs
- ✅ **Auto-deploying** on code changes
- ✅ **Production-ready** with real AI content
- ✅ **Free to host** on Render's free tier

**Share your live application with the world! 🌍**