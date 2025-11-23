#!/bin/bash

# Margdarshan Vercel Deployment Script
# This script automates the deployment process to Vercel

echo "🚀 Margdarshan AI - Vercel Deployment Script"
echo "============================================="

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI is not installed."
    echo "📦 Installing Vercel CLI..."
    npm install -g vercel
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install Vercel CLI. Please install manually:"
        echo "   npm install -g vercel"
        exit 1
    fi
fi

echo "✅ Vercel CLI is available"

# Check if user is logged in to Vercel
echo "🔐 Checking Vercel authentication..."
if ! vercel whoami &> /dev/null; then
    echo "❌ Not logged in to Vercel"
    echo "🔑 Please login to Vercel:"
    vercel login
    if [ $? -ne 0 ]; then
        echo "❌ Vercel login failed. Please try again."
        exit 1
    fi
fi

echo "✅ Vercel authentication successful"

# Verify project structure
echo "📁 Verifying project structure..."
required_files=("vercel.json" "api/main.py" "api/requirements.txt" "Generative/frontend/package.json")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Required file missing: $file"
        exit 1
    fi
done
echo "✅ All required files present"

# Build frontend locally to check for errors
echo "🏗️ Testing frontend build..."
cd Generative/frontend
npm install
if [ $? -ne 0 ]; then
    echo "❌ Frontend dependency installation failed"
    exit 1
fi

npm run build
if [ $? -ne 0 ]; then
    echo "❌ Frontend build failed. Please fix build errors before deploying."
    exit 1
fi
echo "✅ Frontend builds successfully"

cd ../..

# Check API dependencies
echo "🐍 Checking Python dependencies..."
pip install -r api/requirements.txt --dry-run > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "⚠️  Some Python dependencies may not be available"
    echo "   This is normal - Vercel will handle dependencies"
fi

# Environment variables reminder
echo ""
echo "🔑 IMPORTANT: Ensure these environment variables are set in Vercel:"
echo "   GROQ_API_KEY=your_working_groq_api_key_here"
echo "   GOOGLE_GENAI_API_KEY=your_working_google_api_key_here"
echo "   ENVIRONMENT=production"
echo ""

read -p "🤔 Have you set the environment variables in Vercel Dashboard? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "⚠️  Please set environment variables first:"
    echo "   1. Go to vercel.com/dashboard"
    echo "   2. Select your project"
    echo "   3. Go to Settings → Environment Variables"
    echo "   4. Add the API keys listed above"
    echo "   5. Run this script again"
    exit 1
fi

# Deploy to Vercel
echo "🚀 Deploying to Vercel..."
echo ""

# First deployment (creates project)
echo "📤 Starting deployment..."
vercel --prod

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Deployment Successful!"
    echo "================================================"
    echo "✅ Your Margdarshan AI system is now live!"
    echo ""
    echo "🔗 Next steps:"
    echo "   1. Check your Vercel dashboard for the live URL"
    echo "   2. Test roadmap generation on the live site"
    echo "   3. Verify all phases show real AI content"
    echo "   4. Test learning resources functionality"
    echo ""
    echo "💡 Useful commands:"
    echo "   vercel --prod     # Deploy to production"
    echo "   vercel            # Deploy to preview"
    echo "   vercel logs       # View deployment logs"
    echo "   vercel inspect    # Check function details"
    echo ""
    echo "🎯 Your presentation-ready system is deployed!"
else
    echo ""
    echo "❌ Deployment failed!"
    echo "======================"
    echo "🔧 Troubleshooting steps:"
    echo "   1. Check vercel logs for error details"
    echo "   2. Verify environment variables are set"
    echo "   3. Ensure API keys are valid"
    echo "   4. Check the VERCEL_DEPLOYMENT_GUIDE.md for help"
    echo ""
    echo "📞 Get deployment logs:"
    echo "   vercel logs"
fi