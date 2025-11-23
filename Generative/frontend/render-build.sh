#!/bin/bash

# Render build script for Student Compass frontend
echo "🚀 Starting Student Compass Frontend Build..."

# Install dependencies
echo "📦 Installing Node.js dependencies..."
npm ci

# Set backend API URL for production
echo "🔧 Configuring production API URL..."
if [ -n "$REACT_APP_API_URL" ]; then
    echo "API URL: $REACT_APP_API_URL"
else
    echo "⚠️  REACT_APP_API_URL not set, using default"
fi

# Build the React application
echo "🏗️  Building React application..."
npm run build

echo "✅ Frontend build completed successfully!"