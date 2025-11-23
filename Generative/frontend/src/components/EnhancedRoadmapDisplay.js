import React, { useState } from 'react';
import LinearCard from './LinearCard';

const EnhancedRoadmapDisplay = ({ phases, currentSkills }) => {
  const [expandedPhases, setExpandedPhases] = useState(new Set());

  // Debug logging to see what data we're getting
  console.log('🔍 EnhancedRoadmapDisplay received phases:', phases);
  console.log('🔍 EnhancedRoadmapDisplay currentSkills:', currentSkills);

  // Safety check for empty phases - provide fallback
  const safePhasesData = phases && phases.length > 0 ? phases : [
    {
      phase: 'Foundation & Setup',
      duration: '4-6 weeks',
      topics: ['Set up development environment', 'Learn core fundamentals', 'Practice basic concepts', 'Build first project'],
      projects: ['Hello World application', 'Basic portfolio site'],
      tools: ['Code Editor', 'Version Control', 'Browser DevTools']
    },
    {
      phase: 'Intermediate Development',
      duration: '6-8 weeks', 
      topics: ['Advanced concepts', 'Framework fundamentals', 'API integration', 'Testing basics'],
      projects: ['Interactive web app', 'API-connected project'],
      tools: ['Framework libraries', 'API tools', 'Testing frameworks']
    },
    {
      phase: 'Advanced & Professional',
      duration: '8-10 weeks',
      topics: ['Production deployment', 'Performance optimization', 'Security best practices', 'Team collaboration'],
      projects: ['Full-stack application', 'Production-ready project'],
      tools: ['Cloud platforms', 'CI/CD tools', 'Monitoring systems']
    }
  ];

  const togglePhaseExpansion = (index) => {
    const newExpanded = new Set(expandedPhases);
    if (newExpanded.has(index)) {
      newExpanded.delete(index);
    } else {
      newExpanded.add(index);
    }
    setExpandedPhases(newExpanded);
  };

  const getPhaseIcon = (index) => {
    const icons = ['💡', '🚀', '⭐', '👑', '💎', '🏆'];
    return icons[index] || '📍';
  };

  const getPhaseColor = (index) => {
    const colors = [
      'from-blue-500/10 to-blue-600/5 border-blue-500/20',
      'from-purple-500/10 to-purple-600/5 border-purple-500/20', 
      'from-green-500/10 to-green-600/5 border-green-500/20',
      'from-orange-500/10 to-orange-600/5 border-orange-500/20',
      'from-red-500/10 to-red-600/5 border-red-500/20',
      'from-indigo-500/10 to-indigo-600/5 border-indigo-500/20'
    ];
    return colors[index] || 'from-gray-500/10 to-gray-600/5 border-gray-500/20';
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center mb-8">
        <div className="inline-flex items-center gap-2 px-3 py-1 bg-accent/5 border border-accent/10 rounded-full mb-4 opacity-70 hover:opacity-100 transition-opacity">
          <span className="text-accent text-xs">✨</span>
          <span className="text-xs font-medium text-accent">Powered by AI</span>
        </div>
        <h2 className="text-title-3 font-semibold text-text-primary mb-2">
          Your {currentSkills} Learning Journey
        </h2>
        <p className="text-large text-text-secondary">
          Structured progression designed for {currentSkills} mastery
        </p>
      </div>

      {/* Timeline Progress */}
      <div className="relative">
        <div className="flex items-center justify-between mb-8">
          {safePhasesData.map((_, index) => (
            <div key={index} className="flex flex-col items-center">
              <div className={`w-10 h-10 rounded-full bg-gradient-to-br ${getPhaseColor(index)} 
                border-2 flex items-center justify-center text-lg font-semibold transition-all duration-300`}>
                {getPhaseIcon(index)}
              </div>
              <span className="text-micro text-text-tertiary mt-2">Phase {index + 1}</span>
            </div>
          ))}
        </div>
        {/* Connection Line */}
        <div className="absolute top-5 left-5 right-5 h-0.5 bg-gradient-to-r from-accent/30 via-accent/50 to-accent/30 -z-10"></div>
      </div>

      {/* Phases */}
      <div className="space-y-6">
        {safePhasesData.map((phase, index) => (
          <div key={index} className="group">
            <LinearCard className={`bg-gradient-to-br ${getPhaseColor(index)} border hover:shadow-lg transition-all duration-300`}>
              <div className="p-8">
                {/* Phase Header */}
                <div className="flex items-start gap-6 mb-6">
                  <div className={`flex items-center justify-center w-14 h-14 rounded-full bg-gradient-to-br ${getPhaseColor(index)} 
                    border-2 text-xl font-bold shadow-lg`}>
                    {getPhaseIcon(index)}
                  </div>
                  <div className="flex-1">
                    <div className="flex items-start justify-between mb-3">
                      <div>
                        <h3 className="text-title-5 font-semibold text-text-primary leading-tight mb-2">
                          {phase.phase}
                        </h3>
                        <div className="flex items-center gap-4 text-text-secondary">
                          <span className="flex items-center gap-1">
                            <span>⏱️</span>
                            <span className="text-small font-medium">{phase.duration}</span>
                          </span>
                          <span className="flex items-center gap-1">
                            <span>🎯</span>
                            <span className="text-small font-medium">{phase.topics?.length || 0} objectives</span>
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Key Topics - Clean List Style */}
                <div className="mb-6">
                  <h4 className="text-large font-semibold text-text-primary mb-4 flex items-center gap-2">
                    <span>📚</span>
                    <span>Learning Objectives</span>
                  </h4>
                  <div className="grid gap-3">
                    {(phase.topics || []).slice(0, 4).map((topic, topicIndex) => (
                      <div key={topicIndex} className="flex items-start gap-3 group/item">
                        <div className="flex items-center justify-center w-6 h-6 rounded-full bg-accent/20 text-accent text-micro font-bold mt-1 group-hover/item:bg-accent group-hover/item:text-white transition-all">
                          {topicIndex + 1}
                        </div>
                        <p className="text-small text-text-primary leading-relaxed flex-1 group-hover/item:text-text-primary transition-colors">
                          {topic}
                        </p>
                      </div>
                    ))}
                    {(phase.topics || []).length > 4 && !expandedPhases.has(index) && (
                      <p className="text-micro text-text-tertiary ml-9 italic">
                        +{(phase.topics || []).length - 4} more learning objectives
                      </p>
                    )}
                  </div>
                </div>

                {/* Projects & Tools Tags */}
                <div className="flex items-center gap-3 mb-4">
                  {phase.projects && phase.projects.length > 0 && (
                    <div className="flex items-center gap-2 px-3 py-2 bg-blue-500/10 border border-blue-500/20 rounded-full">
                      <span className="text-blue-600">🛠️</span>
                      <span className="text-small font-medium text-blue-700">
                        {phase.projects.length} Project{phase.projects.length !== 1 ? 's' : ''}
                      </span>
                    </div>
                  )}
                  {phase.tools && phase.tools.length > 0 && (
                    <div className="flex items-center gap-2 px-3 py-2 bg-green-500/10 border border-green-500/20 rounded-full">
                      <span className="text-green-600">⚡</span>
                      <span className="text-small font-medium text-green-700">
                        {phase.tools.length} Tool{phase.tools.length !== 1 ? 's' : ''}
                      </span>
                    </div>
                  )}
                </div>

                {/* Expand/Collapse Button */}
                {((phase.topics || []).length > 4 || (phase.projects || []).length > 0 || (phase.tools || []).length > 0) && (
                  <button
                    onClick={() => togglePhaseExpansion(index)}
                    className="flex items-center gap-2 px-4 py-2 bg-accent/10 hover:bg-accent/20 text-accent rounded-8 transition-all duration-200 font-medium"
                  >
                    <span className="text-small">
                      {expandedPhases.has(index) ? 'Show Less' : 'View Details'}
                    </span>
                    <span className="transform transition-transform duration-200" style={{
                      transform: expandedPhases.has(index) ? 'rotate(180deg)' : 'rotate(0deg)'
                    }}>
                      ▼
                    </span>
                  </button>
                )}

                {/* Expanded Content */}
                {expandedPhases.has(index) && (
                  <div className="mt-6 pt-6 border-t border-border-primary space-y-6 animate-in slide-in-from-top duration-300">
                    {/* Additional Topics */}
                    {(phase.topics || []).length > 4 && (
                      <div>
                        <h5 className="text-small font-semibold text-text-secondary mb-3 flex items-center gap-2">
                          <span>📋</span>
                          <span>Additional Learning Objectives</span>
                        </h5>
                        <div className="grid gap-2">
                          {(phase.topics || []).slice(4).map((topic, topicIndex) => (
                            <div key={topicIndex + 4} className="flex items-start gap-3">
                              <div className="flex items-center justify-center w-5 h-5 rounded-full bg-gray-200 text-gray-600 text-micro font-bold mt-1">
                                {topicIndex + 5}
                              </div>
                              <p className="text-small text-text-secondary leading-relaxed">{topic}</p>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Projects */}
                    {phase.projects && phase.projects.length > 0 && (
                      <div>
                        <h5 className="text-small font-semibold text-text-secondary mb-3 flex items-center gap-2">
                          <span>🚀</span>
                          <span>Hands-on Projects</span>
                        </h5>
                        <div className="space-y-3">
                          {phase.projects.map((project, projectIndex) => (
                            <div key={projectIndex} className="p-4 bg-gradient-to-r from-blue-500/5 to-blue-600/5 border border-blue-500/10 rounded-8 hover:from-blue-500/10 hover:to-blue-600/10 transition-all">
                              <div className="flex items-start gap-3">
                                <div className="flex items-center justify-center w-8 h-8 rounded-full bg-blue-500/20 text-blue-600 text-small font-bold">
                                  {projectIndex + 1}
                                </div>
                                <p className="text-small text-text-primary leading-relaxed font-medium">{project}</p>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Tools */}
                    {phase.tools && phase.tools.length > 0 && (
                      <div>
                        <h5 className="text-small font-semibold text-text-secondary mb-3 flex items-center gap-2">
                          <span>⚡</span>
                          <span>Tools & Technologies</span>
                        </h5>
                        <div className="flex flex-wrap gap-2">
                          {phase.tools.map((tool, toolIndex) => (
                            <span 
                              key={toolIndex}
                              className="inline-flex items-center px-3 py-1 bg-green-500/10 border border-green-500/20 text-small font-medium text-green-700 rounded-full hover:bg-green-500/20 transition-colors"
                            >
                              {tool}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </LinearCard>
          </div>
        ))}
      </div>
    </div>
  );
};

export default EnhancedRoadmapDisplay;