#!/bin/bash

# Enhanced MARGDARSHAN - AI Career Guidance Platform with 3D UI
# Ultimate startup script to run both backend and frontend servers

echo "🚀 Enhanced MARGDARSHAN - AI Career Guidance Platform with 3D UI"
echo "==============================================================="
echo ""

# Colors for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to cleanup processes on exit
cleanup() {
    echo -e "\n${YELLOW}🛑 Shutting down servers...${NC}"
    if [[ -n $BACKEND_PID ]]; then
        kill $BACKEND_PID 2>/dev/null
        echo -e "${GREEN}✅ Backend server stopped${NC}"
    fi
    if [[ -n $FRONTEND_PID ]]; then
        kill $FRONTEND_PID 2>/dev/null
        echo -e "${GREEN}✅ Frontend server stopped${NC}"
    fi
    exit 0
}

# Trap Ctrl+C and call cleanup
trap cleanup INT TERM

echo -e "${BLUE}📍 Navigating to project directory...${NC}"
cd /Users/raheedpasha/Mini_Project/Generative

echo -e "${YELLOW}🐍 Checking Python virtual environment...${NC}"
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}🔧 Creating Python virtual environment...${NC}"
    python3 -m venv .venv
fi

echo -e "${YELLOW}🐍 Activating Python virtual environment...${NC}"
source .venv/bin/activate

echo -e "${GREEN}⚡ Starting FastAPI backend server...${NC}"
python3 main.py &
BACKEND_PID=$!

echo -e "${BLUE}⏳ Waiting for backend to initialize...${NC}"
sleep 3

# Check if backend started successfully
if ps -p $BACKEND_PID > /dev/null; then
    echo -e "${GREEN}✅ Backend server is running (PID: $BACKEND_PID)${NC}"
else
    echo -e "${RED}❌ Backend server failed to start${NC}"
    exit 1
fi

echo -e "${YELLOW}⚛️ Starting React frontend development server...${NC}"
cd frontend

# Check if node_modules exists, if not install dependencies
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}📦 Installing frontend dependencies...${NC}"
    npm install
    
    # Install additional UI enhancement packages
    echo -e "${YELLOW}✨ Installing UI enhancement packages...${NC}"
    npm install framer-motion react-intersection-observer
fi

# Start frontend server
npm start &
FRONTEND_PID=$!

echo ""
echo -e "${GREEN}✅ Enhanced MARGDARSHAN is now running!${NC}"
echo "================================================================"
echo -e "${BLUE}🌐 Frontend:${NC} http://localhost:3000"
echo -e "${BLUE}🎯 Ultimate Roadmap:${NC} http://localhost:3000/ultimate-roadmap"
echo -e "${BLUE}🎨 Enhanced Roadmap:${NC} http://localhost:3000/enhanced-roadmap"
echo -e "${BLUE}🔧 Backend:${NC}  http://localhost:8001"
echo -e "${BLUE}📖 API Docs:${NC} http://localhost:8001/docs"
echo ""
echo -e "${PURPLE}💡 Enhanced UI Features:${NC}"
echo -e "   • 3D tilt effects on cards and buttons"
echo -e "   • Advanced animations with Framer Motion"
echo -e "   • Dynamic glow effects"
echo -e "   • Smooth transitions and micro-interactions"
echo -e "   • Scroll-triggered animations"
echo ""
echo -e "${CYAN}📝 Documentation:${NC}"
echo -e "   • UI Enhancements Summary: UI_ENHANCEMENTS_SUMMARY.md"
echo -e "   • Enhanced README: ENHANCED_README.md"
echo ""
echo -e "${YELLOW}🛑 To stop the servers, press Ctrl+C${NC}"
echo "================================================================"

# Keep script running and wait for processes
wait