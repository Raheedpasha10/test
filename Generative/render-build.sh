#!/bin/bash

# Render build script for Student Compass backend
echo "🚀 Starting Student Compass Backend Build..."

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Set up environment
echo "🔧 Setting up environment..."
export ENVIRONMENT=production

echo "✅ Backend build completed successfully!"