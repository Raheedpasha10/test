import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const InnovativeRoadmapDisplay = ({ phases, currentSkills }) => {
  const [activePhase, setActivePhase] = useState(0);
  const [selectedTab, setSelectedTab] = useState('overview');

  const tabsConfig = [
    { id: 'overview', label: 'Overview', icon: '📋' },
    { id: 'skills', label: 'Skills & Topics', icon: '🎯' },
    { id: 'projects', label: 'Projects', icon: '🚀' },
    { id: 'resources', label: 'Resources', icon: '📚' },
    { id: 'timeline', label: 'Timeline', icon: '⏱️' }
  ];

  const getPhaseIcon = (index) => {
    const icons = ['🌱', '🔥', '⭐', '👑', '🚀', '💎'];
    return icons[index] || '📍';
  };

  const getSkillLevel = (phase, index) => {
    const levels = ['Foundation', 'Intermediate', 'Advanced', 'Expert', 'Master', 'Elite'];
    return levels[index] || 'Specialized';
  };

  return (
    <div className="innovative-roadmap bg-bg-primary">
      {/* Phase Progress Bar */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-title-3 font-semibold">Your {currentSkills} Journey</h2>
          <span className="text-small text-text-tertiary">
            Phase {activePhase + 1} of {phases.length}
          </span>
        </div>
        
        <div className="flex items-center gap-2 mb-4">
          {phases.map((phase, index) => (
            <motion.div
              key={index}
              className={`flex-1 h-2 rounded-full cursor-pointer transition-all duration-300 ${
                index <= activePhase ? 'bg-accent' : 'bg-bg-tertiary'
              }`}
              onClick={() => setActivePhase(index)}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            />
          ))}
        </div>

        <div className="flex items-center gap-4 overflow-x-auto pb-2">
          {phases.map((phase, index) => (
            <motion.button
              key={index}
              onClick={() => setActivePhase(index)}
              className={`flex items-center gap-2 px-4 py-2 rounded-8 whitespace-nowrap transition-all ${
                index === activePhase 
                  ? 'bg-accent text-white' 
                  : 'bg-bg-secondary text-text-secondary hover:bg-bg-tertiary'
              }`}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              <span className="text-lg">{getPhaseIcon(index)}</span>
              <span className="text-small font-medium">{getSkillLevel(phase, index)}</span>
            </motion.button>
          ))}
        </div>
      </div>

      {/* Current Phase Display */}
      <AnimatePresence mode="wait">
        <motion.div
          key={activePhase}
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: -20 }}
          transition={{ duration: 0.3 }}
          className="bg-bg-secondary rounded-12 p-6 mb-6"
        >
          <div className="flex items-start gap-4 mb-6">
            <div className="flex items-center justify-center w-12 h-12 rounded-12 bg-accent text-white text-xl">
              {getPhaseIcon(activePhase)}
            </div>
            <div className="flex-1">
              <h3 className="text-title-4 font-semibold text-text-primary mb-2">
                {phases[activePhase]?.phase || `Phase ${activePhase + 1}`}
              </h3>
              <p className="text-large text-text-secondary mb-3">
                Duration: {phases[activePhase]?.duration || '4-6 weeks'}
              </p>
              <div className="flex items-center gap-2">
                <span className="px-3 py-1 bg-accent/10 text-accent rounded-6 text-small font-medium">
                  {getSkillLevel(phases[activePhase], activePhase)}
                </span>
                <span className="px-3 py-1 bg-green-100 text-green-700 rounded-6 text-small font-medium">
                  {phases[activePhase]?.topics?.length || 0} Learning Objectives
                </span>
              </div>
            </div>
          </div>

          {/* Tab Navigation */}
          <div className="flex items-center gap-1 mb-6 overflow-x-auto">
            {tabsConfig.map((tab) => (
              <motion.button
                key={tab.id}
                onClick={() => setSelectedTab(tab.id)}
                className={`flex items-center gap-2 px-4 py-2 rounded-8 text-small font-medium whitespace-nowrap transition-all ${
                  selectedTab === tab.id
                    ? 'bg-accent text-white'
                    : 'text-text-secondary hover:bg-bg-tertiary hover:text-text-primary'
                }`}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                <span>{tab.icon}</span>
                <span>{tab.label}</span>
              </motion.button>
            ))}
          </div>

          {/* Tab Content */}
          <AnimatePresence mode="wait">
            <motion.div
              key={selectedTab}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.2 }}
            >
              {selectedTab === 'overview' && (
                <div className="space-y-4">
                  <div className="bg-bg-primary rounded-8 p-4">
                    <h4 className="text-large font-medium text-text-primary mb-2">Phase Overview</h4>
                    <p className="text-text-secondary">
                      Master the fundamentals of {currentSkills} with hands-on projects and industry-standard practices.
                      Build a strong foundation that will serve as the bedrock for your professional development.
                    </p>
                  </div>
                  
                  <div className="grid grid-cols-2 gap-4">
                    <div className="bg-blue-50 border border-blue-200 rounded-8 p-4">
                      <div className="flex items-center gap-2 mb-2">
                        <span className="text-blue-600">🎯</span>
                        <span className="text-small font-medium text-blue-800">Learning Focus</span>
                      </div>
                      <p className="text-small text-blue-700">Core concepts & practical application</p>
                    </div>
                    
                    <div className="bg-green-50 border border-green-200 rounded-8 p-4">
                      <div className="flex items-center gap-2 mb-2">
                        <span className="text-green-600">📈</span>
                        <span className="text-small font-medium text-green-800">Skill Level</span>
                      </div>
                      <p className="text-small text-green-700">{getSkillLevel(phases[activePhase], activePhase)}</p>
                    </div>
                  </div>
                </div>
              )}

              {selectedTab === 'skills' && (
                <div className="space-y-4">
                  <h4 className="text-large font-medium text-text-primary mb-3">Skills & Learning Objectives</h4>
                  <div className="grid gap-3">
                    {(phases[activePhase]?.topics || []).map((topic, index) => (
                      <motion.div
                        key={index}
                        initial={{ opacity: 0, x: -10 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: index * 0.1 }}
                        className="flex items-start gap-3 p-3 bg-bg-primary rounded-8 hover:bg-bg-tertiary transition-colors"
                      >
                        <div className="flex items-center justify-center w-6 h-6 rounded-full bg-accent/20 text-accent text-small font-bold mt-0.5">
                          {index + 1}
                        </div>
                        <div className="flex-1">
                          <p className="text-small font-medium text-text-primary">{topic}</p>
                        </div>
                      </motion.div>
                    ))}
                  </div>
                </div>
              )}

              {selectedTab === 'projects' && (
                <div className="space-y-4">
                  <h4 className="text-large font-medium text-text-primary mb-3">Hands-on Projects</h4>
                  {(phases[activePhase]?.projects || []).length > 0 ? (
                    <div className="grid gap-4">
                      {phases[activePhase].projects.map((project, index) => (
                        <motion.div
                          key={index}
                          initial={{ opacity: 0, y: 10 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ delay: index * 0.1 }}
                          className="p-4 bg-gradient-to-r from-accent/5 to-accent/10 border border-accent/20 rounded-8"
                        >
                          <div className="flex items-center gap-2 mb-2">
                            <span className="text-accent">🚀</span>
                            <span className="text-small font-medium text-accent">Project {index + 1}</span>
                          </div>
                          <p className="text-small text-text-primary">{project}</p>
                        </motion.div>
                      ))}
                    </div>
                  ) : (
                    <div className="text-center py-8 text-text-tertiary">
                      <span className="text-4xl mb-2 block">🛠️</span>
                      <p>Projects will be added based on your learning progress</p>
                    </div>
                  )}
                </div>
              )}

              {selectedTab === 'resources' && (
                <div className="space-y-4">
                  <h4 className="text-large font-medium text-text-primary mb-3">Learning Resources</h4>
                  <div className="grid gap-3">
                    {['📚 Comprehensive Course Materials', '🎥 Video Tutorials & Walkthroughs', '📝 Practice Exercises & Challenges', '🌐 Community & Support Forums'].map((resource, index) => (
                      <motion.div
                        key={index}
                        initial={{ opacity: 0, x: -10 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: index * 0.1 }}
                        className="flex items-center gap-3 p-3 bg-bg-primary rounded-8 hover:bg-bg-tertiary transition-colors"
                      >
                        <div className="text-lg">{resource.split(' ')[0]}</div>
                        <span className="text-small text-text-primary">{resource.substring(2)}</span>
                      </motion.div>
                    ))}
                  </div>
                </div>
              )}

              {selectedTab === 'timeline' && (
                <div className="space-y-4">
                  <h4 className="text-large font-medium text-text-primary mb-3">Learning Timeline</h4>
                  <div className="space-y-3">
                    {['Week 1-2: Foundation & Setup', 'Week 3-4: Core Concepts', 'Week 5-6: Practical Projects', 'Week 7+: Advanced Topics'].map((milestone, index) => (
                      <motion.div
                        key={index}
                        initial={{ opacity: 0, x: -10 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: index * 0.1 }}
                        className="flex items-center gap-4 p-3 bg-bg-primary rounded-8"
                      >
                        <div className="w-8 h-8 rounded-full bg-accent/20 flex items-center justify-center text-accent text-small font-bold">
                          {index + 1}
                        </div>
                        <span className="text-small text-text-primary">{milestone}</span>
                      </motion.div>
                    ))}
                  </div>
                </div>
              )}
            </motion.div>
          </AnimatePresence>
        </motion.div>
      </AnimatePresence>

      {/* Navigation */}
      <div className="flex items-center justify-between">
        <motion.button
          onClick={() => setActivePhase(Math.max(0, activePhase - 1))}
          disabled={activePhase === 0}
          className="flex items-center gap-2 px-4 py-2 rounded-8 bg-bg-secondary text-text-secondary disabled:opacity-50 disabled:cursor-not-allowed hover:bg-bg-tertiary transition-colors"
          whileHover={{ scale: activePhase > 0 ? 1.02 : 1 }}
          whileTap={{ scale: activePhase > 0 ? 0.98 : 1 }}
        >
          <span>←</span>
          <span className="text-small font-medium">Previous Phase</span>
        </motion.button>

        <div className="flex items-center gap-2">
          <span className="text-small text-text-tertiary">
            Phase {activePhase + 1} of {phases.length}
          </span>
        </div>

        <motion.button
          onClick={() => setActivePhase(Math.min(phases.length - 1, activePhase + 1))}
          disabled={activePhase === phases.length - 1}
          className="flex items-center gap-2 px-4 py-2 rounded-8 bg-accent text-white disabled:opacity-50 disabled:cursor-not-allowed hover:bg-accent-hover transition-colors"
          whileHover={{ scale: activePhase < phases.length - 1 ? 1.02 : 1 }}
          whileTap={{ scale: activePhase < phases.length - 1 ? 0.98 : 1 }}
        >
          <span className="text-small font-medium">Next Phase</span>
          <span>→</span>
        </motion.button>
      </div>
    </div>
  );
};

export default InnovativeRoadmapDisplay;