# 🧭 Student Compass - AI-Powered Career Guidance Platform

> **Intelligent career navigation with AI-powered roadmaps, personalized learning paths, and real-time progress tracking**

## 🌟 Overview

Student Compass is a cutting-edge AI-powered platform that revolutionizes career guidance for students and professionals. Using advanced multi-agent AI systems, it provides personalized learning roadmaps, skill assessments, and intelligent career recommendations to help users transition seamlessly from academic learning to professional success.

## ✨ Core Features

### 🤖 Advanced AI Systems
- **Multi-Agent Roadmap Generation**: Specialized AI agents working together for comprehensive career planning
- **Real-Time Content Generation**: Dynamic, personalized roadmaps using Groq and Google AI
- **Intelligent Skill Matching**: AI-driven analysis of current skills vs. career requirements
- **Smart Progress Adaptation**: Learning paths that evolve based on user progress and market trends

### 🎯 Personalized Learning Experience
- **Dynamic Career Assessment**: Comprehensive evaluation of skills, interests, and goals
- **Visual Learning Paths**: Interactive roadmaps with detailed phase breakdowns
- **Project-Based Learning**: Real-world projects aligned with industry requirements
- **Tool & Resource Recommendations**: Curated lists of industry-standard tools and platforms

### 📊 Professional Analytics
- **Progress Dashboard**: Real-time tracking of learning milestones and achievements
- **Career Market Insights**: Live job market data and industry trend analysis
- **Skill Gap Identification**: Precise analysis of areas needing development
- **Performance Metrics**: Detailed analytics on learning efficiency and progress velocity

## 🏗 Architecture & Technology

### Frontend Stack
- **React 18** - Modern component architecture with hooks
- **Tailwind CSS** - Utility-first styling with custom design system
- **Framer Motion** - Smooth animations and micro-interactions
- **React Router** - Seamless single-page application navigation
- **Context API** - Efficient state management

### Backend Infrastructure
- **FastAPI** - High-performance async Python web framework
- **Multi-Agent AI System** - Specialized AI agents for different career domains
- **RESTful API Design** - Clean, intuitive API endpoints
- **Real-time Processing** - Async operations for fast response times

### AI Integration
- **Groq API** - Ultra-fast LLM inference for real-time content generation
- **Google Generative AI** - Advanced language models for comprehensive analysis
- **Custom AI Services** - Specialized agents for technical, market, and strategic analysis
- **Intelligent Fallback System** - Ensures consistent service availability

## 🚀 Quick Start Guide

### Prerequisites
- **Python 3.9+** with virtual environment support
- **Node.js 16+** with npm or yarn
- **API Keys**: Groq API key (required), Google AI key (optional)

### Installation & Setup

1. **Clone and Navigate**
   ```bash
   git clone https://github.com/your-username/student-compass.git
   cd student-compass
   ```

2. **Backend Configuration**
   ```bash
   cd Generative
   
   # Create and activate virtual environment
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Configure environment
   cp .env.example .env
   # Add your API keys to .env file
   ```

3. **Frontend Setup**
   ```bash
   cd Generative/frontend
   npm install
   ```

4. **Launch Application**
   ```bash
   # Start backend (Terminal 1)
   cd Generative
   source .venv/bin/activate
   python main.py
   
   # Start frontend (Terminal 2)
   cd Generative/frontend
   npm start
   ```

5. **Access Points**
   - **Main Application**: http://localhost:3000
   - **API Backend**: http://localhost:8001
   - **API Documentation**: http://localhost:8001/docs

## 📂 Project Architecture

```
student-compass/
├── 🔧 Generative/                    # Core Backend System
│   ├── 📁 config/                   # Environment & settings management
│   ├── 📁 models/                   # Data models & database schemas
│   ├── 📁 routes/                   # API endpoint definitions
│   │   ├── multi_agent_roadmap.py  # Multi-agent system endpoints
│   │   ├── auth.py                 # Authentication routes
│   │   └── resources.py            # Resource management
│   ├── 📁 services/                # Core business logic
│   │   ├── ai_service.py           # AI integration layer
│   │   ├── multi_agent_service.py  # Multi-agent orchestration
│   │   ├── enhanced_multi_agent_service.py  # Advanced AI features
│   │   └── user_service.py         # User management
│   ├── 📁 tests/                   # Comprehensive test suite
│   ├── 🚀 main.py                  # FastAPI application entry
│   └── 📋 requirements.txt         # Python dependencies
│
├── 🎨 Generative/frontend/          # Modern React Frontend
│   ├── 📁 src/
│   │   ├── 🧩 components/          # Reusable UI components
│   │   │   ├── EnhancedRoadmapDisplay.js
│   │   │   ├── AgentInterface.js
│   │   │   └── LoadingScreen.js
│   │   ├── 📄 pages/               # Main application pages
│   │   │   ├── Landing.js          # Landing page
│   │   │   ├── UltimateRoadmap.js  # Roadmap visualization
│   │   │   └── CareerPath.js       # Career exploration
│   │   ├── 🔗 services/            # API communication layer
│   │   └── 📊 constants/           # Application data & config
│   ├── 📦 package.json             # Frontend dependencies
│   └── 🎨 tailwind.config.js       # Design system configuration
│
└── 📚 Documentation & Config        # Project management files
```

## 🔥 Key Features in Action

### 🎯 Smart Career Matching
Our AI analyzes your skills, interests, and goals to suggest the most suitable career paths, helping you discover opportunities you might not have considered.

### 🗺 Dynamic Learning Roadmaps
Get step-by-step learning plans with:
- **Phase-based progression** with clear milestones
- **Real-world projects** to build your portfolio
- **Industry-standard tools** recommendations
- **Flexible timelines** that adapt to your pace

### 🤖 Multi-Agent AI System
Our sophisticated AI system uses multiple specialized agents:
- **Technical Analysis Agent** - Evaluates technical requirements
- **Market Research Agent** - Analyzes industry trends
- **Strategic Planning Agent** - Creates comprehensive roadmaps

### 📈 Progress Tracking
Monitor your journey with:
- **Visual progress indicators** showing completion status
- **Achievement milestones** to keep you motivated
- **Skill gap analysis** highlighting areas for improvement
- **Performance analytics** tracking your learning velocity

## 🎨 Design Philosophy

Student Compass follows modern UI/UX principles with:
- **Clean, minimalist interface** focusing on usability
- **Responsive design** working seamlessly across all devices
- **Accessibility-first** approach ensuring inclusive experience
- **Performance optimization** for fast, smooth interactions

## 🔮 Future Roadmap

- **Advanced AI Tutoring** - Personalized learning assistance
- **Community Features** - Connect with peers and mentors
- **Industry Partnerships** - Direct pathways to job opportunities
- **Certification Tracking** - Monitor and validate your achievements
- **Mobile Application** - Native iOS and Android apps

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines and feel free to submit issues and pull requests.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🌟 Support

If you find Student Compass helpful, please consider:
- ⭐ Starring this repository
- 🐛 Reporting bugs and issues
- 💡 Suggesting new features
- 📢 Sharing with fellow students and developers

---

**Built with ❤️ for the next generation of professionals**