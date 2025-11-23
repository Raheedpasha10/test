#!/bin/bash

# MARGDARSHAN - AI Career Guidance Platform
# Ultimate startup script to look like a pro! 😎

echo "🚀 MARGDARSHAN - AI Career Guidance Platform"
echo "================================================"
echo ""

# Colors for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}📍 Navigating to project directory...${NC}"
cd /Users/raheedpasha/Mini_Project/Generative

echo -e "${YELLOW}🐍 Activating Python virtual environment...${NC}"
source .venv/bin/activate

echo -e "${GREEN}⚡ Starting FastAPI backend server...${NC}"
python3 main.py &
BACKEND_PID=$!

echo -e "${BLUE}⏳ Waiting for backend to initialize...${NC}"
sleep 3

echo -e "${YELLOW}⚛️ Starting React frontend development server...${NC}"
cd frontend
npm start &
FRONTEND_PID=$!

echo ""
echo -e "${GREEN}✅ MARGDARSHAN is now running!${NC}"
echo "================================================"
echo -e "${BLUE}🌐 Frontend:${NC} http://localhost:3000"
echo -e "${BLUE}🔧 Backend:${NC}  http://localhost:8001"
echo -e "${BLUE}📖 API Docs:${NC} http://localhost:8001/docs"
echo ""
echo -e "${YELLOW}💡 To stop the servers, press Ctrl+C${NC}"
echo "================================================"

# Keep script running
wait