#!/bin/bash
set -e

echo "🐍 Installing Python dependencies..."
cd Generative
pip install --upgrade pip
pip install -r requirements.txt

echo "📦 Installing Node.js dependencies..."
cd frontend
npm ci

echo "🏗️ Building React frontend..."
npm run build

echo "✅ Build complete!"