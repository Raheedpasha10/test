# Vercel Deployment Guide - Margdarshan AI Career Guidance System

## 🚀 **Pre-Deployment Setup Complete**

All necessary files have been configured for Vercel deployment:

### ✅ **Configuration Files Created/Updated:**
- `vercel.json` - Vercel deployment configuration
- `api/main.py` - Serverless function entry point
- `api/requirements.txt` - Python dependencies
- `Generative/frontend/package.json` - Updated with vercel-build script

### ✅ **API Configuration:**
- Frontend automatically detects production environment
- Uses relative URLs in production (`''` baseURL)
- Maintains localhost:8001 for local development

## 📋 **Deployment Steps**

### **1. Prerequisites**
```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login
```

### **2. Environment Variables Setup**
In Vercel Dashboard, add these environment variables:

```env
GROQ_API_KEY=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
GOOGLE_GENAI_API_KEY=AIzaSyDKnGmFUmbYatesQL_JpFS_1PcfLxCdMtY
ENVIRONMENT=production
```

### **3. Deploy to Vercel**
```bash
# From project root directory
vercel

# Follow prompts:
# ? Set up and deploy "~/path/to/project"? [Y/n] Y
# ? Which scope do you want to deploy to? (your-username)
# ? Link to existing project? [y/N] N
# ? What's your project's name? margdarshan-ai
# ? In which directory is your code located? ./

# Deploy to production
vercel --prod
```

## 🏗️ **Project Structure for Vercel**

```
project-root/
├── vercel.json                 # Vercel configuration
├── api/                        # Serverless functions
│   ├── main.py                # FastAPI entry point
│   └── requirements.txt       # Python dependencies
├── Generative/                # Backend source code
│   ├── main.py               # Original FastAPI app
│   ├── services/             # AI services
│   ├── routes/               # API routes
│   └── frontend/             # React frontend
│       ├── package.json      # Frontend dependencies
│       ├── src/              # React source code
│       └── public/           # Static assets
└── VERCEL_DEPLOYMENT_GUIDE.md
```

## ⚙️ **Vercel Configuration Explained**

### **vercel.json Breakdown:**
```json
{
  "version": 2,
  "builds": [
    {
      "src": "Generative/frontend/package.json",
      "use": "@vercel/static-build",
      "config": { "distDir": "build" }
    },
    {
      "src": "api/main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/api/main.py"
    },
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ]
}
```

### **Route Handling:**
- `/api/*` → Python backend (FastAPI)
- `/*` → React frontend (static files)

## 🔧 **Backend Configuration**

### **api/main.py:**
- Acts as serverless function entry point
- Imports FastAPI app from `Generative/main.py`
- Handles all API requests in production

### **Environment Variables:**
- Automatically loaded from Vercel environment settings
- Same API keys work for all services (Google AI, Groq)

## 🎯 **Frontend Configuration**

### **Automatic Environment Detection:**
```javascript
baseURL: process.env.NODE_ENV === 'production' ? '' : 'http://localhost:8001'
```

### **Build Process:**
- Uses `vercel-build` script for deployment
- Disables ESLint plugin for faster builds
- Generates static build in `build/` directory

## 🚀 **Deployment Workflow**

### **Automatic Deployments:**
1. **Push to main branch** → Triggers automatic deployment
2. **Pull requests** → Creates preview deployments
3. **Manual deployments** → Use `vercel --prod`

### **Build Process:**
1. **Frontend**: React build → Static files
2. **Backend**: Python serverless functions
3. **Routing**: Vercel handles API/frontend routing

## 🔍 **Post-Deployment Testing**

### **Frontend Testing:**
- Access your Vercel URL (e.g., `https://margdarshan-ai.vercel.app`)
- Test roadmap generation for multiple specializations
- Verify all phases show real AI content
- Check learning resources API integration

### **Backend Testing:**
```bash
# Test API endpoints
curl https://your-vercel-url.vercel.app/api/health
curl -X POST https://your-vercel-url.vercel.app/api/multi-agent-roadmap \
  -H "Content-Type: application/json" \
  -d '{"query": "UI/UX design", "background": {"experience_level": "Beginner"}}'
```

### **Expected Results:**
✅ Health endpoint returns {"status": "healthy"}
✅ Roadmap generation works in <30 seconds
✅ All phases display real AI content
✅ Learning resources load from real APIs

## 🐛 **Troubleshooting**

### **Common Issues:**

#### **1. Build Failures:**
- Check `vercel-build` script in package.json
- Ensure all dependencies are listed
- Verify Python dependencies in `api/requirements.txt`

#### **2. API Timeouts:**
- Vercel free tier has 10s function limit
- Pro tier supports up to 60s (configured to 30s)
- Optimize AI requests if needed

#### **3. Environment Variables:**
- Verify API keys in Vercel dashboard
- Check environment variable names match exactly
- Redeploy after adding new variables

#### **4. CORS Issues:**
- Frontend uses relative URLs in production
- No CORS issues expected with this setup

### **Debug Commands:**
```bash
# Check deployment logs
vercel logs

# Local development with production build
vercel dev

# Check function limits and usage
vercel inspect
```

## 📊 **Performance Considerations**

### **Optimizations Applied:**
- ✅ Serverless functions for backend scalability
- ✅ Static site generation for frontend speed
- ✅ Relative URLs for optimal routing
- ✅ 30-second timeout for AI operations
- ✅ Production-optimized build settings

### **Monitoring:**
- Vercel provides automatic analytics
- Function execution time monitoring
- Error rate tracking
- Performance insights

## 🎯 **Success Criteria**

### **Deployment Successful When:**
✅ Frontend loads without errors
✅ AI roadmap generation works reliably
✅ All phases show real content (no "Extracting...")
✅ Learning resources API calls succeed
✅ Response times under 30 seconds
✅ Mobile/desktop compatibility maintained

---

## 🚀 **Ready for Deployment!**

Your Margdarshan AI system is now fully configured for Vercel deployment. The system will maintain the same functionality as local development while benefiting from:

- **Global CDN distribution**
- **Automatic scaling**
- **HTTPS by default**
- **Custom domain support**
- **Continuous deployment from Git**

**Execute the deployment commands above and your presentation-ready system will be live on Vercel!** 🎉