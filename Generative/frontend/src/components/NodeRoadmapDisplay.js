import React, { useState } from 'react';

const NodeRoadmapDisplay = ({ roadmapData, currentSkills = "Your Career" }) => {
  const [selectedNode, setSelectedNode] = useState(null);

  // Create fallback phases when no data is available
  const createFallbackPhases = () => {
    return [
      { 
        phase: 'Foundation Phase', 
        duration: '4-6 weeks', 
        content: 'Learn the fundamentals and core concepts',
        goals: ['Master basic concepts', 'Build foundation skills', 'Understand core principles'],
        topics: ['Core principles', 'Essential tools', 'Basic concepts'],
        projects: ['Starter project', 'Basic implementation'],
        tools: ['VS Code', 'Git', 'Command Line'],
        resources: ['Documentation', 'Beginner tutorials', 'Practice exercises'],
        difficulty: 'Beginner'
      },
      { 
        phase: 'Growth Phase', 
        duration: '6-8 weeks', 
        content: 'Build practical skills and apply knowledge',
        goals: ['Apply knowledge', 'Create projects', 'Build real applications'],
        topics: ['Advanced concepts', 'Real-world application', 'Best practices'],
        projects: ['Portfolio project', 'Practical application'],
        tools: ['Advanced frameworks', 'Development tools'],
        resources: ['Advanced tutorials', 'Project examples', 'Code repositories'],
        difficulty: 'Intermediate'
      },
      { 
        phase: 'Mastery Phase', 
        duration: '8-12 weeks', 
        content: 'Master expert concepts and techniques',
        goals: ['Expert proficiency', 'Industry readiness', 'Advanced problem solving'],
        topics: ['Expert techniques', 'System design', 'Optimization'],
        projects: ['Capstone project', 'Complex system'],
        tools: ['Professional tools', 'Enterprise technologies'],
        resources: ['Professional documentation', 'Industry publications', 'Expert courses'],
        difficulty: 'Advanced'
      }
    ];
  };

  // Parse and structure phase data from real multi-agent content
  const parsePhases = (data) => {
    console.log('🔍 NodeRoadmapDisplay received data:', data);
    
    if (!data || (typeof data !== 'string' && typeof data !== 'object')) {
      console.log('⚠️ No valid data provided, using fallback phases');
      return createFallbackPhases();
    }

    // Handle case where data is an object with final_roadmap property
    let textData = '';
    if (typeof data === 'object') {
      textData = data.final_roadmap || data.content || JSON.stringify(data);
    } else {
      textData = data;
    }

    console.log('📝 Processing text data:', textData.substring(0, 200) + '...');

    const phases = [];
    
    // Enhanced parsing for better structure extraction from multi-agent content
    // Handle multiple formats:
    // 1. ### **Phase 1: Name** (duration) - Backend format
    // 2. ## Phase 1: Name - Alternative format  
    // 3. **Phase 1: Name** - Bold format
    // Split by phase markers first, then process each phase
    const phaseMarkers = [
      /###\s*\*\*Phase\s*\d+/gi,  // ### **Phase 1
      /##\s*Phase\s*\d+/gi,        // ## Phase 1
      /\*\*Phase\s*\d+/gi          // **Phase 1
    ];
    
    // Find all phase start positions
    const phaseStarts = [];
    for (const marker of phaseMarkers) {
      let match;
      while ((match = marker.exec(textData)) !== null) {
        phaseStarts.push({ index: match.index, text: match[0] });
      }
    }
    
    // Sort by position and extract phases
    phaseStarts.sort((a, b) => a.index - b.index);
    const matches = [];
    
    for (let i = 0; i < phaseStarts.length; i++) {
      const start = phaseStarts[i].index;
      const end = i < phaseStarts.length - 1 ? phaseStarts[i + 1].index : textData.length;
      const phaseContent = textData.substring(start, end);
      matches.push([phaseContent, phaseContent]); // [full match, group 1] format for compatibility
    }
    
    if (matches.length > 0) {
      console.log('✅ Found phase matches:', matches.length);
      matches.forEach((match, index) => {
        const phaseContent = match[0];
        let title = `Phase ${index + 1}`;
        
        // Smart title extraction based on actual content analysis
        console.log('📝 Phase content sample:', phaseContent.substring(0, 300));
        
        // Method 1: Look for explicit phase headers in various formats
        // Backend format: ### **Phase 1: Name** (duration)
        const phasePatterns = [
          /###\s*\*\*Phase\s*\d+[:\s]*([^*]+?)\*\*/i,  // ### **Phase 1: Name**
          /##\s*\*\*Phase\s*\d+[:\s]*([^*]+?)\*\*/i,   // ## **Phase 1: Name**
          /Phase\s*\d+[:\s]*([^(\n*]+)/i,               // Phase 1: Name
          /##\s*Phase\s*\d+[:\s]*([^(\n*]+)/i,          // ## Phase 1: Name
          /\*\*Phase\s*\d+[:\s]*([^*\n(]+)\*\*/i        // **Phase 1: Name**
        ];
        
        for (const pattern of phasePatterns) {
          const titleMatch = phaseContent.match(pattern);
          if (titleMatch && titleMatch[1] && !titleMatch[1].toLowerCase().includes('learning goals')) {
            title = titleMatch[1].replace(/\*/g, '').trim();
            // Remove duration if present: "Name (4-6 weeks)" -> "Name"
            title = title.replace(/\s*\([^)]*\)\s*$/, '').trim();
            console.log(`✅ Extracted title: "${title}" using pattern: ${pattern}`);
            break;
          }
        }
        
        // Method 2: Intelligent content analysis for better title inference
        if (!title || title.includes('Learning Goals') || title.trim().length < 5) {
          const contentLower = phaseContent.toLowerCase();
          
          // Analyze content to determine phase focus
          if (contentLower.includes('syntax') && contentLower.includes('variables') && contentLower.includes('functions')) {
            title = 'Programming Fundamentals';
          } else if (contentLower.includes('algorithms') && (contentLower.includes('arrays') || contentLower.includes('trees'))) {
            title = 'Data Structures & Algorithms';
          } else if (contentLower.includes('html') || contentLower.includes('css') || contentLower.includes('dom')) {
            title = 'Frontend Development';
          } else if (contentLower.includes('api') || contentLower.includes('backend') || contentLower.includes('server')) {
            title = 'Backend Development';
          } else if (contentLower.includes('react') || contentLower.includes('components') || contentLower.includes('state')) {
            title = 'React Development';
          } else if (contentLower.includes('database') || contentLower.includes('sql') || contentLower.includes('mongodb')) {
            title = 'Database Management';
          } else if (contentLower.includes('deployment') || contentLower.includes('docker') || contentLower.includes('cloud')) {
            title = 'DevOps & Deployment';
          } else if (contentLower.includes('testing') || contentLower.includes('debugging') || contentLower.includes('quality')) {
            title = 'Testing & QA';
          } else if (contentLower.includes('authentication') || contentLower.includes('security') || contentLower.includes('encryption')) {
            title = 'Security & Authentication';
          } else if (contentLower.includes('performance') || contentLower.includes('optimization') || contentLower.includes('scaling')) {
            title = 'Performance Optimization';
          } else {
            // Smart fallback based on phase progression
            const progressionTitles = [
              'Foundation Building',
              'Core Development',
              'Advanced Concepts',
              'System Design',
              'Professional Skills',
              'Specialization'
            ];
            title = progressionTitles[index] || `Phase ${index + 1}`;
          }
          
          console.log(`🎯 Inferred title from content analysis: "${title}"`);
        }
        
        // Extract different sections with improved extraction
        const goals = extractSection(phaseContent, ['learning goals', 'goals', 'objectives']);
        const topics = extractSection(phaseContent, ['key topics', 'topics', 'concepts', 'skills']);
        const projects = extractSection(phaseContent, ['hands-on projects', 'projects', 'practice', 'build']);
        const tools = extractSection(phaseContent, ['tools & technologies', 'tools', 'technologies']);
        const resources = extractSection(phaseContent, ['resources', 'learning resources', 'materials']);
        
        const durationMatch = phaseContent.match(/(\d+[-–]\d+\s*(?:weeks?|months?))/i);
        const duration = durationMatch ? durationMatch[1] : `${4 + index * 2}-${6 + index * 2} weeks`;
        
        console.log(`📋 Phase ${index + 1}: "${title}" - Goals: ${goals.length}, Topics: ${topics.length}, Projects: ${projects.length}`);
        
        phases.push({
          phase: title,
          duration: duration,
          content: phaseContent,
          goals: goals,
          topics: topics,
          projects: projects,
          tools: tools,
          resources: resources,
          difficulty: index === 0 ? 'Beginner' : index === 1 ? 'Intermediate' : 'Advanced'
        });
      });
    } else {
      console.log('⚠️ No phase matches found, trying alternative parsing methods');
      
      // Try splitting by common delimiters
      const sections = textData.split(/(?=Phase|Step|Stage|\*\*Phase|\*\*Step)/gi).filter(s => s.trim().length > 50);
      
      if (sections.length > 1) {
        console.log('✅ Found sections via delimiter splitting:', sections.length);
        sections.forEach((section, index) => {
          if (index < 6) { // Max 6 phases
            const title = extractTitle(section, index);
            const goals = extractSection(section, ['goals', 'objectives', 'learn', 'master']);
            const topics = extractSection(section, ['topics', 'skills', 'concepts']);
            const projects = extractSection(section, ['projects', 'build', 'create', 'practice']);
            const tools = extractSection(section, ['tools', 'technologies', 'use']);
            const resources = extractSection(section, ['resources', 'materials', 'links']);
            
            const durationMatch = section.match(/(\d+[-–]\d+\s*(?:weeks?|months?))/i);
            const duration = durationMatch ? durationMatch[1] : `${4 + index * 2}-${6 + index * 2} weeks`;
            
            phases.push({
              phase: title,
              duration: duration,
              content: section,
              goals: goals.slice(0, 4),
              topics: topics.slice(0, 5),
              projects: projects.slice(0, 3),
              tools: tools.slice(0, 6),
              resources: resources.slice(0, 5),
              difficulty: index === 0 ? 'Beginner' : index === 1 ? 'Intermediate' : 'Advanced'
            });
          }
        });
      }
    }

    console.log('📊 Parsed phases:', phases.length, phases);
    return phases.length > 0 ? phases.slice(0, 6) : createFallbackPhases();
  };

  // Helper function to extract title from section
  const extractTitle = (section, index) => {
    // Try to find a title in the first few lines
    const lines = section.split('\n').slice(0, 3);
    for (const line of lines) {
      const cleaned = line.replace(/[#*-]+/g, '').trim();
      if (cleaned.length > 5 && cleaned.length < 50 && !cleaned.toLowerCase().includes('week')) {
        return cleaned;
      }
    }
    return `Phase ${index + 1}`;
  };

  // Enhanced extraction logic to get more comprehensive content
  const extractSection = (text, keywords) => {
    console.log('🔍 Extracting section for keywords:', keywords);
    
    const items = [];
    const lines = text.split('\n');
    let inSection = false;
    let sectionStarted = false;
    
    // Helper function to check if header matches keywords (bidirectional matching)
    const headerMatchesKeywords = (headerText, keywordList) => {
      const headerLower = headerText.toLowerCase().replace(/:/g, '').trim();
      return keywordList.some(keyword => {
        const keywordLower = keyword.toLowerCase();
        // Check if header contains keyword OR keyword contains header (for partial matches)
        // Also handle "Learning Goals" matching "goals" keyword
        return headerLower.includes(keywordLower) || 
               keywordLower.includes(headerLower) ||
               (headerLower.includes('learning') && keywordLower.includes('goal')) ||
               (headerLower.includes('goal') && keywordLower.includes('learning'));
      });
    };
    
    for (let i = 0; i < lines.length; i++) {
      const cleanLine = lines[i].trim();
      
      // Check for multiple header formats:
      // 1. **Learning Goals:** (bold text with colon - what backend generates)
      // 2. **Key Topics:** (bold text with colon)
      // 3. ### Goals (markdown header - alternative format)
      // 4. ## Goals (markdown header)
      const headerPatterns = [
        /^\*\*(.+?):\*\*/i,         // **Learning Goals:**
        /^\*\*(.+?)\*\*/i,          // **Goals** (without colon)
        /^###\s+(.+)$/i,            // ### Goals
        /^##\s+(.+)$/i,             // ## Goals
        /^#\s+(.+)$/i               // # Goals
      ];
      
      let headerMatch = null;
      let headerText = '';
      
      for (const pattern of headerPatterns) {
        const match = cleanLine.match(pattern);
        if (match && match[1]) {
          headerMatch = match;
          headerText = match[1].trim();
          break;
        }
      }
      
      if (headerMatch) {
        const wasInSection = inSection;
        inSection = headerMatchesKeywords(headerText, keywords);
        
        if (wasInSection && !inSection) {
          console.log('🛑 Hit new section, stopping extraction');
          break;
        }
        
        if (inSection) {
          sectionStarted = true;
          console.log(`📋 Found section "${headerText}" for keywords: ${keywords}`);
        }
        continue;
      }
      
      // If we're in a section, extract content
      if (inSection && sectionStarted) {
        // Stop if we hit another header (different section)
        if (cleanLine.match(/^\*\*/) || cleanLine.match(/^#{1,3}\s+/)) {
          // Check if it's still our section or a different one
          const nextHeaderMatch = cleanLine.match(/^\*\*(.+?):\*\*/i) || 
                                  cleanLine.match(/^#{1,3}\s+(.+)$/i);
          if (nextHeaderMatch) {
            const nextHeaderText = nextHeaderMatch[1].trim();
            const isStillOurSection = headerMatchesKeywords(nextHeaderText, keywords);
            if (!isStillOurSection) {
              console.log('🛑 Hit different section, stopping extraction');
              break;
            }
          }
        }
        
        // Extract bullet points, numbered items, and descriptive text
        if (cleanLine.startsWith('-') || cleanLine.startsWith('•') || cleanLine.startsWith('*') || 
            cleanLine.match(/^\d+\./)) {
          
          let item = cleanLine
            .replace(/^[-•*]\s*/, '')
            .replace(/^\d+\.\s*/, '')
            .replace(/\*\*/g, '')
            .replace(/\[(.*?)\]/g, '$1')
            .trim();
          
          // Clean up common prefixes but preserve meaningful content
          // Only remove if it's a generic verb prefix, not if it's part of the actual content
          if (item.match(/^(Learn|Master|Understand|Build|Create|Develop|Practice)\s+/i) && 
              item.length < 50) {
            item = item.replace(/^(Learn|Master|Understand|Build|Create|Develop|Practice)\s+/i, '');
          }
          
          // Filter out generic/placeholder items and ensure meaningful content
          if (item.length > 5 && item.length < 200 && 
              !item.includes('Phase') && 
              !item.toLowerCase().match(/^(list|include|add|use)\s+/i) &&
              !item.match(/^\[.*\]$/) && // Not just a placeholder like [item]
              item !== 'basics' && item !== 'core concepts' && item !== 'skills') {
            items.push(item);
            console.log('✅ Extracted item:', item);
          }
        }
      }
    }
    
    // If we didn't find items with keywords, try extracting from raw content as fallback
    if (items.length === 0) {
      console.log('⚠️ No items found with keywords, trying raw extraction');
      const rawItems = text.split('\n')
        .filter(line => {
          const trimmed = line.trim();
          return (trimmed.startsWith('-') || trimmed.startsWith('•')) && 
                 trimmed.length > 10 && // Must be meaningful length
                 !trimmed.toLowerCase().includes('phase') &&
                 !trimmed.match(/^\*\*/); // Not a header
        })
        .map(line => {
          let item = line.replace(/^[-•*]\s*/, '').replace(/\*\*/g, '').trim();
          // Remove generic prefixes only if very short
          if (item.length < 50) {
            item = item.replace(/^(Learn|Master|Understand|Build|Create|Develop|Practice)\s+/i, '');
          }
          return item;
        })
        .filter(item => 
          item.length > 5 && 
          item.length < 200 &&
          item !== 'basics' && 
          item !== 'core concepts' && 
          item !== 'skills'
        );
      
      items.push(...rawItems.slice(0, 8));
    }
    
    console.log('📊 Final extracted items:', items);
    return items.slice(0, 10); // More items for better content
  };

  const safePhases = parsePhases(roadmapData);

  const handleNodeClick = (index) => {
    setSelectedNode(selectedNode === index ? null : index);
  };

  const cleanTitle = (title) => {
    if (!title || title.includes('Learning Goals')) {
      return 'Learning Phase'; // Generic fallback
    }
    
    let cleanedTitle = title;
    
    // Remove common prefixes and clean up
    cleanedTitle = cleanedTitle.replace(/^Phase\s*\d+:\s*/gi, '');
    cleanedTitle = cleanedTitle.replace(/I Want To Learn|And Become Proficient In This Field|Foundation Excellence/g, '');
    cleanedTitle = cleanedTitle.replace(/\*+/g, ''); // Remove asterisks
    cleanedTitle = cleanedTitle.replace(/\s*\([^)]*\)\s*/g, ''); // Remove parentheses content
    cleanedTitle = cleanedTitle.replace(/\s+/g, ' ').trim();
    
    // Capitalize first letter of each word for consistency
    cleanedTitle = cleanedTitle.replace(/\b\w/g, l => l.toUpperCase());
    
    return cleanedTitle || 'Learning Phase';
  };

  const getDifficultyColor = (difficulty) => {
    switch (difficulty.toLowerCase()) {
      case 'beginner': return 'border-gray-600/50 bg-gray-800/40';
      case 'intermediate': return 'border-gray-600/50 bg-gray-800/60';
      case 'advanced': return 'border-gray-600/50 bg-gray-800/80';
      default: return 'border-gray-600/50 bg-gray-800/50';
    }
  };

  const getDifficultyBadge = (difficulty) => {
    switch (difficulty.toLowerCase()) {
      case 'beginner': return 'bg-green-500/20 text-green-300 border-green-500/30';
      case 'intermediate': return 'bg-yellow-500/20 text-yellow-300 border-yellow-500/30';
      case 'advanced': return 'bg-red-500/20 text-red-300 border-red-500/30';
      default: return 'bg-gray-500/20 text-gray-300 border-gray-500/30';
    }
  };

  return (
    <div className="min-h-screen" style={{ backgroundColor: '#08090a', color: '#f7f8f8' }}>
      {/* Enhanced Header with Progress */}
      <div className="relative px-8 py-8">
        <div className="max-w-7xl mx-auto">

          {/* Progress Indicator */}
          {selectedNode !== null && (
            <div className="flex items-center justify-center gap-2 mb-8">
              {safePhases.map((_, index) => (
                <div
                  key={index}
                  className={`w-3 h-3 rounded-full transition-all duration-300 ${
                    index === selectedNode
                      ? 'bg-white scale-125'
                      : index < selectedNode
                      ? 'bg-green-500'
                      : 'bg-gray-600'
                  }`}
                />
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Main Content */}
      {selectedNode === null ? (
        /* SIMPLE CLEAN ROADMAP DISPLAY - DIRECTLY SHOWING AGENT CONTENT */
        <div className="w-full px-4 pb-16">
          <div className="max-w-6xl mx-auto">
            <div className="space-y-8">
              {safePhases.map((phase, index) => (
                <div 
                  key={index} 
                  onClick={() => handleNodeClick(index)}
                  className="bg-gray-800/50 border border-gray-700 rounded-xl p-6 cursor-pointer hover:bg-gray-800/70 transition-all duration-200"
                >
                  {/* Simple Phase Header */}
                  <div className="flex items-center gap-4 mb-6">
                    <div className="w-12 h-12 rounded-lg bg-white/10 flex items-center justify-center">
                      <span className="text-xl font-bold text-white">{index + 1}</span>
                    </div>
                    <div className="flex-1">
                      <h3 className="text-2xl font-bold text-white mb-1">
                        {cleanTitle(phase.phase)}
                      </h3>
                      <div className="flex items-center gap-4 text-sm text-gray-400">
                        <span>📅 {phase.duration}</span>
                        <span className={`px-2 py-1 rounded border text-xs ${getDifficultyBadge(phase.difficulty)}`}>
                          {phase.difficulty}
                        </span>
                      </div>
                    </div>
                  </div>

                  {/* Content Preview - Direct from Agent */}
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    {/* Learning Goals */}
                    <div>
                      <h4 className="text-white font-semibold mb-3 flex items-center gap-2">
                        Learning Goals
                        <span className="text-xs bg-gray-700 px-2 py-1 rounded">
                          {(phase.goals || []).length || 'Extracting...'}
                        </span>
                      </h4>
                      <div className="space-y-2">
                        {(phase.goals || []).length > 0 ? (
                          (phase.goals || []).slice(0, 3).map((goal, i) => (
                            <div key={i} className="text-sm text-gray-300 flex items-start gap-2">
                              <span className="text-gray-500">•</span>
                              <span>{goal.charAt(0).toUpperCase() + goal.slice(1)}</span>
                            </div>
                          ))
                        ) : (
                          <div className="text-sm text-gray-500">No goals extracted</div>
                        )}
                      </div>
                    </div>

                    {/* Key Topics */}
                    <div>
                      <h4 className="text-white font-semibold mb-3 flex items-center gap-2">
                        Key Topics
                        <span className="text-xs bg-gray-700 px-2 py-1 rounded">
                          {(phase.topics || []).length || 'Extracting...'}
                        </span>
                      </h4>
                      <div className="space-y-1">
                        {(phase.topics || []).length > 0 ? (
                          (phase.topics || []).slice(0, 4).map((topic, i) => (
                            <div key={i} className="text-sm px-2 py-1 bg-gray-700/50 rounded text-gray-300">
                              {topic.charAt(0).toUpperCase() + topic.slice(1)}
                            </div>
                          ))
                        ) : (
                          <div className="text-sm text-gray-500">No topics extracted</div>
                        )}
                      </div>
                    </div>

                    {/* Projects */}
                    <div>
                      <h4 className="text-white font-semibold mb-3 flex items-center gap-2">
                        Projects
                        <span className="text-xs bg-gray-700 px-2 py-1 rounded">
                          {(phase.projects || []).length}
                        </span>
                      </h4>
                      <div className="space-y-2">
                        {(phase.projects || []).length > 0 ? (
                          (phase.projects || []).slice(0, 2).map((project, i) => (
                            <div key={i} className="text-sm text-gray-300">
                              <span className="font-medium">#{i + 1}</span> {project}
                            </div>
                          ))
                        ) : (
                          <div className="text-sm text-gray-500">No projects extracted</div>
                        )}
                        
                        {/* Tools */}
                        {(phase.tools || []).length > 0 && (
                          <div className="pt-2">
                            <div className="text-xs text-gray-400 mb-1">Tools:</div>
                            <div className="flex flex-wrap gap-1">
                              {(phase.tools || []).slice(0, 3).map((tool, i) => (
                                <span key={i} className="text-xs px-2 py-1 bg-gray-600 rounded text-gray-300">
                                  {tool.charAt(0).toUpperCase() + tool.slice(1)}
                                </span>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>

                  {/* Quick Action */}
                  <div className="mt-6 pt-4 border-t border-gray-600/50 flex items-center justify-between">
                    <span className="text-sm text-gray-400">Click for detailed breakdown</span>
                    <span className="text-sm text-gray-300">Explore →</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      ) : (
        /* PROFESSIONAL PHASE DETAIL VIEW - FULL WIDTH */
        <div className="w-full px-4 pb-16">
          <div className="max-w-[1600px] mx-auto">
            {/* Professional Header */}
            <div className="flex items-center gap-4 mb-8">
              <button
                onClick={() => setSelectedNode(null)}
                className="w-10 h-10 rounded-lg bg-gray-800 border border-gray-700 
                           flex items-center justify-center text-white hover:bg-gray-700 transition-colors"
              >
                ←
              </button>
              <div className="flex-1">
                <div className="flex items-center gap-3 mb-1">
                  <h1 className="text-2xl font-bold text-white">
                    {cleanTitle(safePhases[selectedNode]?.phase)}
                  </h1>
                  <div className={`px-2 py-1 rounded text-xs border ${getDifficultyBadge(safePhases[selectedNode]?.difficulty)}`}>
                    {safePhases[selectedNode]?.difficulty}
                  </div>
                </div>
                <div className="flex items-center gap-4 text-sm text-gray-400">
                  <span>📅 {safePhases[selectedNode]?.duration}</span>
                  <span>🎯 {safePhases[selectedNode]?.goals?.length || 0} Goals</span>
                  <span>🚀 {safePhases[selectedNode]?.projects?.length || 0} Projects</span>
                  <span>🛠️ {safePhases[selectedNode]?.tools?.length || 0} Tools</span>
                  <span>📚 {safePhases[selectedNode]?.resources?.length || 0} Resources</span>
                </div>
              </div>
              <div className="text-sm text-gray-400">
                Phase {selectedNode + 1} of {safePhases.length}
              </div>
            </div>

            {/* Enhanced Content Grid - Showcasing Rich Multi-Agent Content */}
            <div className="space-y-6">
              {/* Main Content Row */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Learning Goals - Enhanced */}
                <div className="bg-gray-800/50 backdrop-blur rounded-xl p-6 border border-gray-700">
                  <div className="flex items-center gap-3 mb-4">
                    <div className="w-8 h-8 rounded-lg bg-gray-700 flex items-center justify-center">
                      <span className="text-white text-sm font-bold">G</span>
                    </div>
                    <div>
                      <h3 className="text-xl font-bold text-white">Learning Goals</h3>
                      <p className="text-xs text-gray-400">What you'll achieve in this phase</p>
                    </div>
                  </div>
                  <div className="grid grid-cols-1 gap-3">
                    {(safePhases[selectedNode]?.goals || []).length > 0 ? (
                      (safePhases[selectedNode]?.goals || []).map((goal, i) => (
                        <div key={i} className="flex items-start gap-3 p-3 bg-black/20 rounded-lg border border-gray-600/30">
                          <div className="w-6 h-6 bg-gray-700 rounded-full flex items-center justify-center text-xs font-bold text-white mt-0.5 flex-shrink-0">
                            {i + 1}
                          </div>
                          <span className="text-gray-200 text-sm leading-relaxed">{goal}</span>
                        </div>
                      ))
                    ) : (
                      <div className="p-4 bg-gray-900/40 rounded-lg border border-gray-600/30">
                        <div className="text-gray-400 text-sm mb-2">No extracted goals yet. Raw content:</div>
                        <div className="text-xs text-gray-500 max-h-32 overflow-y-auto">
                          {safePhases[selectedNode]?.content || 'No content available'}
                        </div>
                      </div>
                    )}
                  </div>
                </div>

                {/* Key Topics - Enhanced */}
                <div className="bg-gray-800/50 backdrop-blur rounded-xl p-6 border border-gray-700">
                  <div className="flex items-center gap-3 mb-4">
                    <div className="w-8 h-8 rounded-lg bg-gray-700 flex items-center justify-center">
                      <span className="text-white text-sm font-bold">T</span>
                    </div>
                    <div>
                      <h3 className="text-xl font-bold text-white">Key Topics</h3>
                      <p className="text-xs text-gray-400">Core concepts you'll master</p>
                    </div>
                  </div>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                    {(safePhases[selectedNode]?.topics || []).length > 0 ? (
                      (safePhases[selectedNode]?.topics || []).map((topic, i) => (
                        <div key={i} className="p-3 bg-gray-700/30 border border-gray-600/30 rounded-lg hover:bg-gray-700/50 transition-colors">
                          <span className="text-gray-200 text-sm font-medium">{topic}</span>
                        </div>
                      ))
                    ) : (
                      <div className="p-4 bg-gray-900/40 rounded-lg border border-gray-600/30 col-span-full">
                        <div className="text-gray-400 text-sm">No topics extracted yet from AI content.</div>
                      </div>
                    )}
                  </div>
                </div>
              </div>

              {/* Projects & Tools Row */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Hands-on Projects - Enhanced */}
                <div className="bg-gray-800/50 backdrop-blur rounded-xl p-6 border border-gray-700">
                  <div className="flex items-center gap-3 mb-4">
                    <div className="w-8 h-8 rounded-lg bg-gray-700 flex items-center justify-center">
                      <span className="text-white text-sm font-bold">P</span>
                    </div>
                    <div>
                      <h3 className="text-xl font-bold text-white">Hands-on Projects</h3>
                      <p className="text-xs text-gray-400">Build real applications to showcase skills</p>
                    </div>
                  </div>
                  <div className="space-y-3">
                    {(safePhases[selectedNode]?.projects || []).length > 0 ? (
                      (safePhases[selectedNode]?.projects || []).map((project, i) => (
                        <div key={i} className="p-4 bg-gray-700/30 border border-gray-600/30 rounded-lg">
                          <div className="flex items-start gap-3">
                            <div className="w-8 h-8 bg-gray-600 rounded-lg flex items-center justify-center text-sm font-bold text-white flex-shrink-0">
                              {i + 1}
                            </div>
                            <div>
                              <h4 className="text-white font-medium mb-1">Project {i + 1}</h4>
                              <p className="text-gray-300 text-sm">{project}</p>
                            </div>
                          </div>
                        </div>
                      ))
                    ) : (
                      <div className="p-4 bg-gray-900/40 rounded-lg border border-gray-600/30">
                        <div className="text-gray-400 text-sm">No projects extracted yet from AI-generated content.</div>
                      </div>
                    )}
                  </div>
                </div>

                {/* Tools & Technologies - Enhanced */}
                <div className="bg-gray-800/50 backdrop-blur rounded-xl p-6 border border-gray-700">
                  <div className="flex items-center gap-3 mb-4">
                    <div className="w-8 h-8 rounded-lg bg-gray-700 flex items-center justify-center">
                      <span className="text-white text-sm font-bold">T</span>
                    </div>
                    <div>
                      <h3 className="text-xl font-bold text-white">Tools & Technologies</h3>
                      <p className="text-xs text-gray-400">Essential tech stack for this phase</p>
                    </div>
                  </div>
                  <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
                    {(safePhases[selectedNode]?.tools || []).length > 0 ? (
                      (safePhases[selectedNode]?.tools || []).map((tool, i) => (
                        <div key={i} className="p-2 bg-gray-700/30 border border-gray-600/30 rounded-lg text-center">
                          <span className="text-gray-200 text-sm font-medium">{tool}</span>
                        </div>
                      ))
                    ) : (
                      <div className="p-4 bg-gray-900/40 rounded-lg border border-gray-600/30 col-span-full">
                        <div className="text-gray-400 text-sm">No tools extracted yet from AI content.</div>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>

            {/* Learning Resources Section - Enhanced */}
            <div className="mt-8">
              <div className="bg-gray-800/50 backdrop-blur rounded-xl p-6 border border-gray-700">
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-8 h-8 rounded-lg bg-gray-700 flex items-center justify-center">
                    <span className="text-white text-sm font-bold">R</span>
                  </div>
                  <h3 className="text-xl font-bold text-white">Learning Resources</h3>
                  <div className="text-sm text-gray-400">
                    Curated materials for this phase
                  </div>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {(safePhases[selectedNode]?.resources || []).length > 0 ? (
                    (safePhases[selectedNode]?.resources || []).map((resource, i) => (
                      <div key={i} className="p-4 bg-gray-900/60 rounded-lg border border-gray-600">
                        <div className="flex items-start gap-2">
                          <div className="w-2 h-2 bg-blue-400 rounded-full mt-2 flex-shrink-0"></div>
                          <div>
                            <span className="text-gray-300 font-medium">
                              {resource.charAt(0).toUpperCase() + resource.slice(1)}
                            </span>
                          </div>
                        </div>
                      </div>
                    ))
                  ) : (
                    // Generate smart resources based on phase content
                    (() => {
                      const currentPhase = safePhases[selectedNode];
                      const smartResources = [];
                      
                      if (currentPhase?.topics) {
                        currentPhase.topics.forEach(topic => {
                          const topicLower = topic.toLowerCase();
                          if (topicLower.includes('variables') || topicLower.includes('syntax')) {
                            smartResources.push('Programming syntax tutorial');
                            smartResources.push('Variables and data types guide');
                          } else if (topicLower.includes('functions')) {
                            smartResources.push('Functions tutorial');
                            smartResources.push('Function examples and exercises');
                          } else if (topicLower.includes('algorithms')) {
                            smartResources.push('Algorithm visualization tools');
                            smartResources.push('Algorithm practice problems');
                          } else if (topicLower.includes('arrays')) {
                            smartResources.push('Array methods documentation');
                            smartResources.push('Array manipulation exercises');
                          }
                        });
                      }
                      
                      // Add some general resources
                      smartResources.push('Official documentation');
                      smartResources.push('Interactive coding platform');
                      smartResources.push('Video tutorial series');
                      
                      // Remove duplicates and limit
                      const uniqueResources = [...new Set(smartResources)].slice(0, 5);
                      
                      return uniqueResources.map((resource, i) => (
                        <div key={i} className="p-4 bg-gray-900/60 rounded-lg border border-gray-600">
                          <div className="flex items-start gap-2">
                            <div className="w-2 h-2 bg-blue-400 rounded-full mt-2 flex-shrink-0"></div>
                            <div>
                              <span className="text-gray-300 font-medium">{resource}</span>
                            </div>
                          </div>
                        </div>
                      ));
                    })()
                  )}
                </div>
              </div>
            </div>

            {/* Navigation */}
            <div className="mt-8 flex justify-between">
              <button
                onClick={() => selectedNode > 0 && setSelectedNode(selectedNode - 1)}
                disabled={selectedNode === 0}
                className={`px-6 py-3 rounded-lg font-medium transition-colors ${
                  selectedNode === 0
                    ? 'bg-gray-800 text-gray-500 cursor-not-allowed border border-gray-700'
                    : 'bg-gray-700 text-white hover:bg-gray-600 border border-gray-600'
                }`}
              >
                ← Previous Phase
              </button>
              <button
                onClick={() => selectedNode < safePhases.length - 1 && setSelectedNode(selectedNode + 1)}
                disabled={selectedNode === safePhases.length - 1}
                className={`px-6 py-3 rounded-lg font-medium transition-colors ${
                  selectedNode === safePhases.length - 1
                    ? 'bg-gray-800 text-gray-500 cursor-not-allowed border border-gray-700'
                    : 'bg-white text-black hover:bg-gray-200'
                }`}
              >
                Next Phase →
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default NodeRoadmapDisplay;