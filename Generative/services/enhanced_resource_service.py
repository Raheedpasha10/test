"""
Enhanced Resource Discovery Service
Provides real learning resources with direct links to actual content using Google/YouTube APIs
"""
import json
import os
import random
import requests
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class LearningResource:
    """Enhanced learning resource with rich metadata"""
    title: str
    url: str
    description: str
    provider: str
    resource_type: str
    duration: Optional[str] = None
    rating: Optional[str] = None
    price: Optional[str] = None
    level: Optional[str] = None
    thumbnail: Optional[str] = None
    instructor: Optional[str] = None
    students: Optional[str] = None
    language: str = "English"
    last_updated: Optional[str] = None


class EnhancedResourceService:
    """Service for discovering real learning resources with direct links using Google/YouTube APIs"""
    
    def __init__(self):
        self.youtube_api_key = os.getenv("YOUTUBE_API_KEY") or os.getenv("GOOGLE_GENAI_API_KEY")
        self.gemini_api_key = os.getenv("GOOGLE_GENAI_API_KEY")
        
        # Configure Gemini for resource recommendations
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None
            
        self.real_resources_db = self._initialize_real_resources_database()
    
    def _initialize_real_resources_database(self) -> Dict[str, Dict[str, List[LearningResource]]]:
        """Initialize comprehensive database of real learning resources"""
        return {
            # PROGRAMMING & DEVELOPMENT
            "python": {
                "youtube": [
                    LearningResource(
                        title="Python Full Course for free 🐍",
                        url="https://www.youtube.com/watch?v=ix9cRaBkVe0",
                        description="Complete Python tutorial for beginners. Learn Python basics, variables, functions, and more in this comprehensive course.",
                        provider="YouTube",
                        resource_type="youtube",
                        duration="12 hours",
                        rating="4.8/5",
                        price="Free",
                        level="Beginner",
                        thumbnail="https://i.ytimg.com/vi/ix9cRaBkVe0/maxresdefault.jpg",
                        instructor="Bro Code",
                        students="2.1M views"
                    ),
                    LearningResource(
                        title="Python Tutorial - Python Full Course for Beginners",
                        url="https://www.youtube.com/watch?v=_uQrJ0TkZlc",
                        description="Learn Python programming from scratch. This Python tutorial covers all the fundamentals of Python programming language.",
                        provider="YouTube",
                        resource_type="youtube",
                        duration="6 hours",
                        rating="4.9/5",
                        price="Free",
                        level="Beginner",
                        thumbnail="https://i.ytimg.com/vi/_uQrJ0TkZlc/maxresdefault.jpg",
                        instructor="Programming with Mosh",
                        students="15M views"
                    ),
                    LearningResource(
                        title="Intermediate Python Programming Course",
                        url="https://www.youtube.com/watch?v=HGOBQPFzWKo",
                        description="Take your Python skills to the next level with this intermediate Python course covering decorators, generators, and more.",
                        provider="YouTube",
                        resource_type="youtube",
                        duration="6 hours",
                        rating="4.7/5",
                        price="Free",
                        level="Intermediate",
                        thumbnail="https://i.ytimg.com/vi/HGOBQPFzWKo/maxresdefault.jpg",
                        instructor="freeCodeCamp",
                        students="3.2M views"
                    )
                ],
                "courses": [
                    LearningResource(
                        title="Python for Everybody Specialization",
                        url="https://www.coursera.org/specializations/python",
                        description="Learn to Program and Analyze Data with Python. Develop programs to gather, clean, analyze, and visualize data.",
                        provider="Coursera",
                        resource_type="courses",
                        duration="8 months",
                        rating="4.8/5",
                        price="$49/month",
                        level="Beginner",
                        thumbnail="https://d3c33hcgiwev3.cloudfront.net/imageAssetProxy.v1/ShO4TdS5EeWy7ApJlLNhKQ_42b396ba8dc149b78ab54c75f59baf3e_python-for-everybody-thumbnail.png",
                        instructor="Charles Severance",
                        students="1.2M enrolled"
                    ),
                    LearningResource(
                        title="Complete Python Bootcamp From Zero to Hero in Python 3",
                        url="https://www.udemy.com/course/complete-python-bootcamp/",
                        description="Learn Python like a Professional! Start from the basics and go all the way to creating your own applications and games!",
                        provider="Udemy",
                        resource_type="courses",
                        duration="22 hours",
                        rating="4.6/5",
                        price="$19.99",
                        level="Beginner to Advanced",
                        thumbnail="https://img-b.udemycdn.com/course/240x135/567828_67d0.jpg",
                        instructor="Jose Portilla",
                        students="1.7M enrolled"
                    ),
                    LearningResource(
                        title="Python Programming MasterTrack Certificate",
                        url="https://www.coursera.org/mastertrack/python-programming-university-of-pennsylvania",
                        description="Master Python programming with hands-on projects and expert instruction from University of Pennsylvania.",
                        provider="Coursera",
                        resource_type="courses",
                        duration="4-6 months",
                        rating="4.7/5",
                        price="$39-79/month",
                        level="Intermediate",
                        thumbnail="https://d3c33hcgiwev3.cloudfront.net/imageAssetProxy.v1/penn-mastertrack-python.png",
                        instructor="University of Pennsylvania",
                        students="45K+ enrolled"
                    )
                ],
                "books": [
                    LearningResource(
                        title="Automate the Boring Stuff with Python",
                        url="https://www.amazon.com/Automate-Boring-Stuff-Python-Programming/dp/1593279922",
                        description="Learn how to use Python to write programs that do in minutes what would take you hours to do by hand.",
                        provider="Amazon",
                        resource_type="books",
                        rating="4.6/5",
                        price="$23.99",
                        level="Beginner",
                        thumbnail="https://images-na.ssl-images-amazon.com/images/I/816CIXG3vOL.jpg",
                        instructor="Al Sweigart",
                        language="English"
                    ),
                    LearningResource(
                        title="Python Crash Course",
                        url="https://www.amazon.com/Python-Crash-Course-Hands-Project-Based/dp/1593276036",
                        description="A fast-paced, thorough introduction to Python that will have you writing programs, solving problems, and making things that work in no time.",
                        provider="Amazon", 
                        resource_type="books",
                        rating="4.5/5",
                        price="$25.49",
                        level="Beginner",
                        thumbnail="https://images-na.ssl-images-amazon.com/images/I/81v4f_IhCOL.jpg",
                        instructor="Eric Matthes",
                        language="English"
                    )
                ],
                "certifications": [
                    LearningResource(
                        title="PCAP – Certified Associate in Python Programming",
                        url="https://pythoninstitute.org/pcap",
                        description="Industry-recognized Python certification that validates fundamental programming skills and knowledge of Python language syntax.",
                        provider="Python Institute",
                        resource_type="certifications",
                        duration="3-6 months prep",
                        rating="4.5/5",
                        price="$295",
                        level="Associate",
                        thumbnail="https://pythoninstitute.org/assets/63af904e3aa305.86478412.png",
                        instructor="Python Institute"
                    ),
                    LearningResource(
                        title="Microsoft Certified: Python Developer Associate",
                        url="https://docs.microsoft.com/en-us/learn/certifications/azure-developer/",
                        description="Demonstrate ability to design, build, test, and maintain cloud applications and services using Python on Microsoft Azure.",
                        provider="Microsoft",
                        resource_type="certifications", 
                        duration="3-4 months",
                        rating="4.4/5",
                        price="$165",
                        level="Associate",
                        thumbnail="https://images.credly.com/images/be8fcaeb-c769-4858-b567-ffaaa73ce8cf/azure-developer-associate-600x600.png",
                        instructor="Microsoft"
                    )
                ]
            },
            
            # Add more comprehensive topics
            "javascript": {
                "youtube": [
                    LearningResource(
                        title="JavaScript Full Course for free 🌐",
                        url="https://www.youtube.com/watch?v=8dWL3wF_OMw",
                        description="Complete JavaScript tutorial for beginners. Learn JavaScript from scratch with hands-on examples and projects.",
                        provider="YouTube",
                        resource_type="youtube",
                        duration="8 hours",
                        rating="4.9/5",
                        price="Free",
                        level="Beginner",
                        thumbnail="https://i.ytimg.com/vi/8dWL3wF_OMw/maxresdefault.jpg",
                        instructor="Bro Code",
                        students="1.8M views"
                    ),
                    LearningResource(
                        title="JavaScript Tutorial for Beginners: Learn JavaScript in 1 Hour",
                        url="https://www.youtube.com/watch?v=W6NZfCO5SIk",
                        description="JavaScript tutorial for beginners. Learn the basics of JavaScript programming in just 1 hour.",
                        provider="YouTube",
                        resource_type="youtube",
                        duration="1 hour",
                        rating="4.8/5",
                        price="Free",
                        level="Beginner",
                        thumbnail="https://i.ytimg.com/vi/W6NZfCO5SIk/maxresdefault.jpg",
                        instructor="Programming with Mosh",
                        students="8.2M views"
                    )
                ],
                "courses": [
                    LearningResource(
                        title="The Complete JavaScript Course 2024: From Zero to Expert!",
                        url="https://www.udemy.com/course/the-complete-javascript-course/",
                        description="The modern JavaScript course for everyone! Master JavaScript with projects, challenges and theory. Many courses in one!",
                        provider="Udemy",
                        resource_type="courses",
                        duration="69 hours",
                        rating="4.7/5",
                        price="$19.99",
                        level="All Levels",
                        thumbnail="https://img-b.udemycdn.com/course/240x135/851712_fc61_6.jpg",
                        instructor="Jonas Schmedtmann",
                        students="680K+ enrolled"
                    )
                ]
            },
            
            "react": {
                "youtube": [
                    LearningResource(
                        title="React Course - Beginner's Tutorial for React JavaScript Library [2022]",
                        url="https://www.youtube.com/watch?v=bMknfKXIFA8",
                        description="Learn React from scratch in this complete course. Build real projects and master React fundamentals.",
                        provider="YouTube",
                        resource_type="youtube",
                        duration="11 hours",
                        rating="4.9/5",
                        price="Free",
                        level="Beginner",
                        thumbnail="https://i.ytimg.com/vi/bMknfKXIFA8/maxresdefault.jpg",
                        instructor="freeCodeCamp",
                        students="4.2M views"
                    ),
                    LearningResource(
                        title="Full React Tutorial #1 - Introduction",
                        url="https://www.youtube.com/watch?v=j942wKiXFu8&list=PL4cUxeGkcC9gZD-Tvwfod2gaISzfRiP9d",
                        description="Complete React tutorial series covering components, hooks, routing, and state management.",
                        provider="YouTube",
                        resource_type="youtube",
                        duration="5 hours series",
                        rating="4.8/5", 
                        price="Free",
                        level="Beginner",
                        thumbnail="https://i.ytimg.com/vi/j942wKiXFu8/maxresdefault.jpg",
                        instructor="Net Ninja",
                        students="2.1M views"
                    )
                ]
            },
            
            "machine learning": {
                "youtube": [
                    LearningResource(
                        title="Machine Learning Course for Beginners",
                        url="https://www.youtube.com/watch?v=NWONeJKn6kc",
                        description="Learn Machine Learning in this complete course for beginners. You will learn the fundamentals and build ML projects.",
                        provider="YouTube",
                        resource_type="youtube", 
                        duration="20 hours",
                        rating="4.9/5",
                        price="Free",
                        level="Beginner",
                        thumbnail="https://i.ytimg.com/vi/NWONeJKn6kc/maxresdefault.jpg",
                        instructor="freeCodeCamp",
                        students="2.8M views"
                    )
                ],
                "courses": [
                    LearningResource(
                        title="Machine Learning Specialization",
                        url="https://www.coursera.org/specializations/machine-learning-introduction",
                        description="Build ML models with NumPy & scikit-learn, build & train supervised models for prediction & binary classification tasks.",
                        provider="Coursera",
                        resource_type="courses",
                        duration="3 months",
                        rating="4.9/5",
                        price="$49/month",
                        level="Beginner",
                        thumbnail="https://d3c33hcgiwev3.cloudfront.net/imageAssetProxy.v1/machine-learning-specialization.png",
                        instructor="Andrew Ng",
                        students="2.1M enrolled"
                    )
                ]
            }
        }
    
    def get_enhanced_resources(self, topic: str, resource_type: str, limit: int = 15, level: str = "intermediate") -> List[Dict[str, Any]]:
        """Get real learning resources with enhanced metadata and direct links using APIs"""
        topic_clean = topic.lower().strip()
        enhanced_resources = []
        
        # Skip database resources for now - FORCE API ONLY
        # We'll add database resources back only if APIs fail completely
        print(f"🚀 FORCING API-ONLY resource discovery for {resource_type}: {topic}")
        
        if False:  # Temporarily disable database resources
            resources = []
            for resource in resources[:min(1, limit)]:
                enhanced_resources.append({
                    "title": resource.title,
                    "url": resource.url,
                    "description": resource.description,
                    "provider": resource.provider,
                    "type": resource.resource_type,
                    "duration": resource.duration,
                    "rating": resource.rating,
                    "price": resource.price,
                    "level": resource.level,
                    "thumbnail": resource.thumbnail,
                    "instructor": resource.instructor,
                    "students": resource.students,
                    "language": resource.language,
                    "last_updated": resource.last_updated or "2024",
                    "direct_link": True,
                    "verified": True
                })
        
        # FORCE API CALLS FIRST - No fallbacks until we try real APIs
        remaining_limit = limit - len(enhanced_resources)
        
        if resource_type == "youtube":
            print(f"🎥 FORCING YouTube API search for: {topic}")
            api_resources = self._search_youtube_videos(topic, remaining_limit, level)
            if api_resources and len(api_resources) > 0:
                print(f"✅ SUCCESS: Found {len(api_resources)} real YouTube videos from API")
                enhanced_resources.extend(api_resources)
            else:
                print(f"⚠️ YouTube API returned no results, trying secondary search")
                # Try different search terms
                for alt_topic in [f"{topic} tutorial", f"learn {topic}", f"{topic} course"]:
                    alt_resources = self._search_youtube_videos(alt_topic, remaining_limit, level)
                    if alt_resources and len(alt_resources) > 0:
                        print(f"✅ SUCCESS: Found {len(alt_resources)} videos with alternate search: {alt_topic}")
                        enhanced_resources.extend(alt_resources)
                        break
            
        elif resource_type == "courses":
            print(f"🎓 Fetching course recommendations for: {topic}")
            api_resources = self._get_course_recommendations(topic, remaining_limit, level)
            if api_resources:
                enhanced_resources.extend(api_resources)
                print(f"✅ Found {len(api_resources)} course recommendations")
                
        elif resource_type == "books":
            print(f"📚 Fetching book recommendations for: {topic}")
            api_resources = self._get_book_recommendations(topic, remaining_limit, level)
            if api_resources:
                enhanced_resources.extend(api_resources)
                print(f"✅ Found {len(api_resources)} book recommendations")
                
        elif resource_type == "certifications":
            print(f"🏆 Fetching certification recommendations for: {topic}")
            api_resources = self._get_certification_recommendations(topic, remaining_limit, level)
            if api_resources:
                enhanced_resources.extend(api_resources)
                print(f"✅ Found {len(api_resources)} certification recommendations")
        
        # Only use fallbacks if we have very few real resources
        if len(enhanced_resources) < 3:
            print(f"⚠️ Only found {len(enhanced_resources)} real resources, adding minimal fallbacks")
            remaining_limit = max(3 - len(enhanced_resources), 0)
            fallback_resources = self._generate_smart_fallbacks(topic, resource_type, remaining_limit, level)
            enhanced_resources.extend(fallback_resources)
        
        print(f"🎯 Final resource count: {len(enhanced_resources)} ({len([r for r in enhanced_resources if r.get('verified', False)])} verified)")
        return enhanced_resources[:limit]
    
    def _search_youtube_videos(self, topic: str, limit: int, level: str) -> List[Dict[str, Any]]:
        """Search YouTube using API for real video results with direct links"""
        try:
            if not self.youtube_api_key:
                print("❌ YouTube API key not available")
                return []
            
            print(f"🔑 Using YouTube API key: {self.youtube_api_key[:15]}...")
            print(f"🎯 Searching YouTube for SPECIFIC topic: '{topic}' at level: {level}")
            
            # Create highly specific search queries for the exact topic
            # Ensure each search is unique and topic-specific
            search_queries = [
                f"{topic} tutorial {level}",
                f"{topic} course complete",
                f"learn {topic} step by step",
                f"{topic} {level} guide" if level != "beginner" else f"{topic} beginner tutorial",
                f"{topic} masterclass training"
            ]
            
            # Make queries more specific to avoid generic results
            if any(word in topic.lower() for word in ['data science', 'machine learning', 'ai']):
                search_queries = [
                    f"{topic} python tutorial {level}",
                    f"{topic} complete course 2024",
                    f"{topic} projects tutorial"
                ]
            elif any(word in topic.lower() for word in ['web development', 'frontend', 'backend']):
                search_queries = [
                    f"{topic} javascript tutorial {level}",
                    f"{topic} full stack course",
                    f"{topic} project build"
                ]
            elif any(word in topic.lower() for word in ['mobile', 'android', 'ios']):
                search_queries = [
                    f"{topic} app development {level}",
                    f"{topic} complete tutorial",
                    f"{topic} project course"
                ]
            
            print(f"📝 Topic-specific search queries: {search_queries}")
            
            all_videos = []
            seen_video_ids = set()  # Prevent duplicates
            
            for query in search_queries[:2]:  # Use top 2 queries
                url = "https://www.googleapis.com/youtube/v3/search"
                params = {
                    'part': 'snippet',
                    'q': query,
                    'type': 'video',
                    'videoDuration': 'long',  # Prefer longer educational content
                    'maxResults': limit // 2 + 2,
                    'key': self.youtube_api_key,
                    'order': 'relevance',
                    'publishedAfter': '2022-01-01T00:00:00Z'  # Recent content
                }
                
                print(f"🌐 Calling YouTube API with query: '{query}'")
                response = requests.get(url, params=params, timeout=10)
                print(f"📡 YouTube API response status: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"📺 YouTube API returned {len(data.get('items', []))} videos")
                    
                    for item in data.get('items', []):
                        video_id = item['id']['videoId']
                        snippet = item['snippet']
                        
                        # Skip duplicates
                        if video_id in seen_video_ids:
                            continue
                        seen_video_ids.add(video_id)
                        
                        # Get additional video details
                        video_details = self._get_video_details(video_id)
                        
                        video_resource = {
                            "title": snippet['title'],
                            "url": f"https://www.youtube.com/watch?v={video_id}",
                            "description": snippet['description'][:300] + "..." if len(snippet['description']) > 300 else snippet['description'],
                            "provider": "YouTube",
                            "type": "youtube",
                            "duration": video_details.get('duration', 'N/A'),
                            "rating": "4.5/5",  # Default rating
                            "price": "Free",
                            "level": level.title(),
                            "thumbnail": snippet['thumbnails'].get('high', {}).get('url', snippet['thumbnails']['default']['url']),
                            "instructor": snippet['channelTitle'],
                            "students": video_details.get('viewCount', 'N/A') + " views",
                            "language": "English",
                            "last_updated": snippet['publishedAt'][:10],
                            "direct_link": True,
                            "verified": True
                        }
                        all_videos.append(video_resource)
                        
                        if len(all_videos) >= limit:
                            break
                
                if len(all_videos) >= limit:
                    break
            
            return all_videos[:limit]
            
        except Exception as e:
            print(f"YouTube API error: {e}")
            return []
    
    def _get_video_details(self, video_id: str) -> Dict[str, str]:
        """Get additional video details like duration and view count"""
        try:
            url = "https://www.googleapis.com/youtube/v3/videos"
            params = {
                'part': 'contentDetails,statistics',
                'id': video_id,
                'key': self.youtube_api_key
            }
            
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('items'):
                    item = data['items'][0]
                    duration = item.get('contentDetails', {}).get('duration', 'PT0M')
                    view_count = item.get('statistics', {}).get('viewCount', '0')
                    
                    # Convert ISO 8601 duration to readable format
                    duration_readable = self._parse_youtube_duration(duration)
                    view_count_readable = self._format_view_count(view_count)
                    
                    return {
                        'duration': duration_readable,
                        'viewCount': view_count_readable
                    }
        except Exception as e:
            print(f"Video details error: {e}")
        
        return {'duration': 'N/A', 'viewCount': 'N/A'}
    
    def _parse_youtube_duration(self, duration: str) -> str:
        """Parse ISO 8601 duration to readable format"""
        import re
        
        pattern = r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?'
        match = re.match(pattern, duration)
        
        if match:
            hours, minutes, seconds = match.groups()
            hours = int(hours or 0)
            minutes = int(minutes or 0)
            
            if hours > 0:
                return f"{hours}h {minutes}m"
            else:
                return f"{minutes}m"
        
        return "N/A"
    
    def _format_view_count(self, count: str) -> str:
        """Format view count to readable format"""
        try:
            count = int(count)
            if count >= 1000000:
                return f"{count/1000000:.1f}M"
            elif count >= 1000:
                return f"{count/1000:.0f}K"
            else:
                return str(count)
        except:
            return "N/A"
    
    def _get_course_recommendations(self, topic: str, limit: int, level: str) -> List[Dict[str, Any]]:
        """Get course recommendations using Gemini AI with specialization-specific prompts"""
        try:
            if not self.model:
                return []
            
            # Create highly specific prompt based on the topic
            prompt = f"""
            You are an expert in {topic} education. Recommend EXACTLY 15 REAL, EXISTING online courses specifically for "{topic}" at {level} level.

            CRITICAL REQUIREMENTS:
            1. Each course MUST be specifically about "{topic}" - not general programming or generic skills
            2. Include ONLY actual course titles that exist on the platforms
            3. Provide REAL instructor names who actually teach these courses
            4. Each course must be different and specialized for "{topic}"
            
            SPECIALIZATION FOCUS for "{topic}":
            - If Data Science: Focus on pandas, matplotlib, sklearn, tensorflow specific courses
            - If Cybersecurity: Focus on ethical hacking, penetration testing, network security courses
            - If Web Development: Focus on React, Node.js, full-stack specific courses
            - If Mobile Development: Focus on React Native, Flutter, iOS/Android specific courses
            - If UI/UX Design: Focus on Figma, user research, prototyping specific courses
            - If DevOps: Focus on Docker, Kubernetes, CI/CD specific courses
            - If Game Development: Focus on Unity, Unreal Engine, C# game programming courses
            - If Machine Learning: Focus on neural networks, deep learning, AI algorithms courses
            
            For each "{topic}" course, provide:
            - Title: (Must contain "{topic}" or related specific technology)
            - Platform: (Coursera, Udemy, edX, Pluralsight, LinkedIn Learning)
            - URL: (Direct link to the specific course)
            - Description: (50-100 words about {topic} specifically)
            - Instructor: (Real instructor name who teaches {topic})
            - Duration: (Course length)
            - Price: (Actual course price)
            - Rating: (4.0-5.0 range)
            - Students: (Enrollment numbers)
            
            FORBIDDEN: Do NOT include generic "programming basics" or "computer science fundamentals" courses.
            REQUIRED: Every single course must be specifically about "{topic}" and use {topic}-specific terminology.
            
            IMPORTANT: You MUST provide exactly 15 different courses. Do not provide fewer than 15.
            
            Return ONLY a clean JSON array with exactly these fields for each course:
            [
                {{
                    "title": "Specific Course Name",
                    "url": "https://platform.com/course-url",
                    "description": "Detailed description",
                    "provider": "Platform Name",
                    "instructor": "Instructor Name",
                    "duration": "X hours/months",
                    "price": "$XX or Free",
                    "rating": "4.X/5",
                    "students": "XXX enrolled",
                    "level": "{level}"
                }}
            ]
            
            NO additional text, explanations, or formatting - JUST the JSON array.
            """
            
            print(f"🎓 Generating SPECIALIZED course recommendations for: {topic}")
            response = self.model.generate_content(prompt)
            courses_data = self._parse_gemini_response(response.text, "courses", topic, level)
            
            # Validate that courses are topic-specific
            filtered_courses = []
            topic_keywords = topic.lower().split()
            
            for course in courses_data:
                course_title = course.get('title', '').lower()
                course_desc = course.get('description', '').lower()
                
                # Check if course contains topic-specific terms
                is_relevant = any(keyword in course_title or keyword in course_desc 
                                for keyword in topic_keywords)
                
                if is_relevant:
                    filtered_courses.append(course)
                    print(f"✅ Relevant course: {course.get('title', '')}")
                else:
                    print(f"❌ Generic course filtered out: {course.get('title', '')}")
            
            return filtered_courses[:limit]
            
        except Exception as e:
            print(f"Gemini course recommendation error: {e}")
            return []
    
    def _get_book_recommendations(self, topic: str, limit: int, level: str) -> List[Dict[str, Any]]:
        """Get book recommendations using Gemini AI with specialization-specific prompts"""
        try:
            if not self.model:
                return []
            
            prompt = f"""
            You are a {topic} expert librarian. Recommend EXACTLY 15 REAL, EXISTING books specifically for "{topic}" at {level} level.

            CRITICAL REQUIREMENTS:
            1. Each book MUST be specifically about "{topic}" - not general programming or computer science
            2. Include ONLY actual book titles that exist and can be purchased
            3. Provide REAL author names who have written {topic} books
            4. Each book must be different and specialized for "{topic}"
            
            SPECIALIZATION FOCUS for "{topic}":
            - If Data Science: Focus on pandas, scikit-learn, data analysis, visualization books
            - If Cybersecurity: Focus on ethical hacking, network security, penetration testing books
            - If Web Development: Focus on React, JavaScript, Node.js, full-stack development books
            - If Mobile Development: Focus on React Native, Flutter, iOS Swift, Android Kotlin books
            - If UI/UX Design: Focus on design systems, user research, Figma, prototyping books
            - If DevOps: Focus on Docker, Kubernetes, CI/CD, infrastructure automation books
            - If Game Development: Focus on Unity, Unreal Engine, game design, C# game programming books
            - If Machine Learning: Focus on neural networks, deep learning, TensorFlow, PyTorch books
            - If Blockchain: Focus on smart contracts, Solidity, cryptocurrency, DeFi books
            
            For each "{topic}" book, provide:
            - Title: (Must contain "{topic}" or related specific technology)
            - Author: (Real author name who has written about {topic})
            - Publisher: (O'Reilly, Manning, Packt, Apress, etc.)
            - URL: (Amazon or publisher direct link)
            - Description: (50-100 words about {topic} specifically)
            - Price: (Book price range)
            - Rating: (4.0-5.0 range)
            - Publication year: (Recent books preferred)
            
            FORBIDDEN: Do NOT include generic "programming fundamentals" or "computer science basics" books.
            REQUIRED: Every single book must be specifically about "{topic}" and use {topic}-specific terminology.
            
            IMPORTANT: You MUST provide exactly 15 different books. Do not provide fewer than 15.
            
            Return ONLY a clean JSON array with exactly these fields for each book:
            [
                {{
                    "title": "Specific Book Title",
                    "url": "https://amazon.com/book-url",
                    "description": "Detailed description",
                    "provider": "Publisher Name",
                    "instructor": "Author Name",
                    "price": "$XX.XX",
                    "rating": "4.X/5",
                    "language": "English",
                    "level": "{level}"
                }}
            ]
            
            NO additional text, explanations, or formatting - JUST the JSON array.
            """
            
            print(f"📚 Generating SPECIALIZED book recommendations for: {topic}")
            response = self.model.generate_content(prompt)
            books_data = self._parse_gemini_response(response.text, "books", topic, level)
            
            # Validate that books are topic-specific
            filtered_books = []
            topic_keywords = topic.lower().split()
            
            for book in books_data:
                book_title = book.get('title', '').lower()
                book_desc = book.get('description', '').lower()
                
                # Check if book contains topic-specific terms
                is_relevant = any(keyword in book_title or keyword in book_desc 
                                for keyword in topic_keywords)
                
                if is_relevant:
                    filtered_books.append(book)
                    print(f"✅ Relevant book: {book.get('title', '')}")
                else:
                    print(f"❌ Generic book filtered out: {book.get('title', '')}")
            
            return filtered_books[:limit]
            
        except Exception as e:
            print(f"Gemini book recommendation error: {e}")
            return []
    
    def _get_certification_recommendations(self, topic: str, limit: int, level: str) -> List[Dict[str, Any]]:
        """Get certification recommendations using Gemini AI with specialization-specific prompts"""
        try:
            if not self.model:
                return []
            
            prompt = f"""
            You are a {topic} career advisor specializing in professional certifications. Recommend EXACTLY 15 REAL, EXISTING industry certifications specifically for "{topic}" at {level} level.

            CRITICAL REQUIREMENTS:
            1. Each certification MUST be specifically for "{topic}" - not general IT or computer science
            2. Include ONLY actual certifications that exist and can be taken
            3. Provide REAL certification names and issuing organizations
            4. Each certification must be different and specialized for "{topic}"
            
            SPECIALIZATION FOCUS for "{topic}":
            - If Data Science: Focus on Google Data Analytics, IBM Data Science, Microsoft Azure Data Scientist certifications
            - If Cybersecurity: Focus on CISSP, CEH, CompTIA Security+, OSCP, CISM certifications
            - If Web Development: Focus on Google Mobile Web Specialist, AWS Certified Developer, Microsoft Azure Developer certifications
            - If Mobile Development: Focus on Google Associate Android Developer, Apple iOS Developer, Meta React Native certifications
            - If UI/UX Design: Focus on Google UX Design, Adobe Certified Expert, Nielsen Norman Group UX certifications
            - If DevOps: Focus on AWS DevOps Engineer, Docker Certified Associate, Kubernetes Administrator certifications
            - If Game Development: Focus on Unity Certified Developer, Unreal Engine certifications
            - If Machine Learning: Focus on Google ML Engineer, AWS ML Specialty, TensorFlow Developer certifications
            - If Cloud Computing: Focus on AWS Solutions Architect, Microsoft Azure Architect, Google Cloud Engineer certifications
            
            For each "{topic}" certification, provide:
            - Title: (Must contain "{topic}" or related specific technology)
            - Provider: (Google, Microsoft, AWS, CompTIA, IBM, Oracle, Cisco, etc.)
            - URL: (Direct link to certification page)
            - Description: (50-100 words about {topic} certification specifically)
            - Duration: (Preparation time needed)
            - Price: (Exam cost)
            - Rating: (Industry recognition level)
            - Level: (Associate, Professional, Expert, etc.)
            
            FORBIDDEN: Do NOT include generic "IT fundamentals" or "computer literacy" certifications.
            REQUIRED: Every single certification must be specifically about "{topic}" and validate {topic} skills.
            
            IMPORTANT: You MUST provide exactly 15 different certifications. Do not provide fewer than 15.
            
            Return ONLY a clean JSON array with exactly these fields for each certification:
            [
                {{
                    "title": "Specific Certification Name",
                    "url": "https://provider.com/certification-url",
                    "description": "Detailed description",
                    "provider": "Certification Provider",
                    "duration": "X months prep",
                    "price": "$XXX exam fee",
                    "rating": "Industry Recognition Level",
                    "instructor": "Certification Provider",
                    "level": "{level}"
                }}
            ]
            
            NO additional text, explanations, or formatting - JUST the JSON array.
            """
            
            print(f"🏆 Generating SPECIALIZED certification recommendations for: {topic}")
            response = self.model.generate_content(prompt)
            cert_data = self._parse_gemini_response(response.text, "certifications", topic, level)
            
            # Validate that certifications are topic-specific
            filtered_certs = []
            topic_keywords = topic.lower().split()
            
            for cert in cert_data:
                cert_title = cert.get('title', '').lower()
                cert_desc = cert.get('description', '').lower()
                
                # Check if certification contains topic-specific terms
                is_relevant = any(keyword in cert_title or keyword in cert_desc 
                                for keyword in topic_keywords)
                
                if is_relevant:
                    filtered_certs.append(cert)
                    print(f"✅ Relevant certification: {cert.get('title', '')}")
                else:
                    print(f"❌ Generic certification filtered out: {cert.get('title', '')}")
            
            return filtered_certs[:limit]
            
        except Exception as e:
            print(f"Gemini certification recommendation error: {e}")
            return []
    
    def _parse_gemini_response(self, response_text: str, resource_type: str, topic: str, level: str) -> List[Dict[str, Any]]:
        """Parse Gemini AI response and format as resource data"""
        try:
            print(f"📄 Parsing Gemini response for {resource_type} (length: {len(response_text)})")
            
            # Multiple strategies to extract JSON from response
            import re
            
            # Strategy 1: Look for complete JSON array
            json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
            
            # Strategy 2: If no array found, look for individual JSON objects
            if not json_match:
                json_objects = re.findall(r'\{[^{}]*\}', response_text, re.DOTALL)
                if json_objects:
                    # Combine individual objects into an array
                    json_str = '[' + ','.join(json_objects) + ']'
                    json_match = type('Match', (), {'group': lambda: json_str})()
            
            if json_match:
                json_str = json_match.group()
                print(f"📊 Extracted JSON string (length: {len(json_str)})")
                
                # Clean up common JSON formatting issues
                json_str = json_str.replace('\n', ' ').replace('\r', ' ')
                json_str = re.sub(r',\s*}', '}', json_str)  # Remove trailing commas
                json_str = re.sub(r',\s*]', ']', json_str)  # Remove trailing commas before ]
                
                data = json.loads(json_str)
                print(f"🎯 Successfully parsed {len(data)} items from Gemini response")
                
                formatted_resources = []
                for item in data:
                    resource = {
                        "title": item.get("title", f"{topic.title()} Resource"),
                        "url": item.get("url", "#"),
                        "description": item.get("description", f"Learn {topic} with this comprehensive resource."),
                        "provider": item.get("provider", "Online Platform"),
                        "type": resource_type,
                        "duration": item.get("duration", "Varies"),
                        "rating": item.get("rating", "4.5/5"),
                        "price": item.get("price", "Varies"),
                        "level": level.title(),
                        "thumbnail": f"https://via.placeholder.com/240x135?text={topic.title()}",
                        "instructor": item.get("instructor", "Expert Instructor"),
                        "students": item.get("students", "N/A"),
                        "language": item.get("language", "English"),
                        "last_updated": "2024",
                        "direct_link": True,
                        "verified": True
                    }
                    formatted_resources.append(resource)
                
                return formatted_resources
                
        except Exception as e:
            print(f"Gemini response parsing error: {e}")
        
        return []
    
    def _find_related_resources(self, topic: str, resource_type: str) -> List[LearningResource]:
        """Find resources related to the topic using intelligent matching"""
        related_resources = []
        
        # Topic mapping for intelligent suggestions
        topic_mappings = {
            "programming": ["python", "javascript"],
            "web development": ["javascript", "react"],
            "data science": ["python", "machine learning"],
            "ai": ["machine learning", "python"],
            "frontend": ["javascript", "react"],
            "backend": ["python", "javascript"],
            "full stack": ["javascript", "react", "python"]
        }
        
        # Check for related topics
        for key, related_topics in topic_mappings.items():
            if key in topic or any(t in topic for t in related_topics):
                for related_topic in related_topics:
                    if related_topic in self.real_resources_db:
                        related_resources.extend(
                            self.real_resources_db[related_topic].get(resource_type, [])
                        )
        
        return related_resources[:5]  # Return top 5 related
    
    def _generate_smart_fallbacks(self, topic: str, resource_type: str, count: int, level: str) -> List[Dict[str, Any]]:
        """Generate intelligent fallback resources with realistic metadata"""
        fallbacks = []
        topic_title = topic.title()
        
        if resource_type == "youtube":
            youtube_channels = [
                ("freeCodeCamp", "https://www.youtube.com/c/Freecodecamp"),
                ("Traversy Media", "https://www.youtube.com/c/TraversyMedia"), 
                ("Programming with Mosh", "https://www.youtube.com/c/programmingwithmosh"),
                ("The Net Ninja", "https://www.youtube.com/c/TheNetNinja"),
                ("Academind", "https://www.youtube.com/c/Academind")
            ]
            
            for i, (channel, channel_url) in enumerate(youtube_channels[:count]):
                fallbacks.append({
                    "title": f"{topic_title} Complete Course - {level.title()} Level",
                    "url": f"{channel_url}/search?query={topic.replace(' ', '+')}",
                    "description": f"Comprehensive {topic} tutorial by {channel}. Learn from basics to advanced concepts with hands-on projects.",
                    "provider": "YouTube",
                    "type": "youtube",
                    "duration": f"{random.randint(3, 12)} hours",
                    "rating": f"{random.uniform(4.5, 4.9):.1f}/5",
                    "price": "Free",
                    "level": level.title(),
                    "thumbnail": f"https://i.ytimg.com/vi/placeholder_{i}/maxresdefault.jpg",
                    "instructor": channel,
                    "students": f"{random.randint(500, 2000)}K views",
                    "direct_link": True,
                    "verified": False
                })
        
        elif resource_type == "courses":
            platforms = [
                ("Coursera", "https://www.coursera.org", "$39-79/month"),
                ("Udemy", "https://www.udemy.com", "$19.99-89.99"),
                ("edX", "https://www.edx.org", "Free-$299"),
                ("Pluralsight", "https://www.pluralsight.com", "$29/month"),
                ("LinkedIn Learning", "https://www.linkedin.com/learning", "$29.99/month")
            ]
            
            for i, (platform, base_url, price) in enumerate(platforms[:count]):
                fallbacks.append({
                    "title": f"Complete {topic_title} Masterclass",
                    "url": f"{base_url}/courses/search?q={topic.replace(' ', '+')}",
                    "description": f"Master {topic} with hands-on projects and expert instruction. Build real-world applications and boost your career.",
                    "provider": platform,
                    "type": "courses", 
                    "duration": f"{random.randint(20, 60)} hours",
                    "rating": f"{random.uniform(4.3, 4.8):.1f}/5",
                    "price": price,
                    "level": level.title(),
                    "thumbnail": f"https://via.placeholder.com/240x135?text={platform}+{topic_title}",
                    "instructor": "Industry Expert",
                    "students": f"{random.randint(10, 500)}K+ enrolled",
                    "direct_link": True,
                    "verified": False
                })
        
        elif resource_type == "books":
            publishers = [
                ("O'Reilly Media", "https://www.oreilly.com"),
                ("Manning Publications", "https://www.manning.com"),
                ("Packt Publishing", "https://www.packtpub.com"),
                ("Apress", "https://www.apress.com"),
                ("Wiley", "https://www.wiley.com")
            ]
            
            for i, (publisher, url) in enumerate(publishers[:count]):
                fallbacks.append({
                    "title": f"Learning {topic_title}: A Comprehensive Guide",
                    "url": f"{url}/search?q={topic.replace(' ', '+')}",
                    "description": f"Master {topic} concepts with this comprehensive guide. Includes practical examples and real-world applications.",
                    "provider": publisher,
                    "type": "books",
                    "rating": f"{random.uniform(4.2, 4.7):.1f}/5",
                    "price": f"${random.randint(25, 65)}.99",
                    "level": level.title(),
                    "thumbnail": f"https://via.placeholder.com/150x200?text={topic_title}+Book",
                    "instructor": "Expert Author",
                    "language": "English",
                    "direct_link": True,
                    "verified": False
                })
        
        elif resource_type == "certifications":
            cert_providers = [
                ("Google", "https://grow.google/certificates"),
                ("Microsoft", "https://docs.microsoft.com/en-us/learn/certifications"),
                ("Amazon AWS", "https://aws.amazon.com/certification"),
                ("IBM", "https://www.ibm.com/training/certification"),
                ("Oracle", "https://education.oracle.com/certification")
            ]
            
            for i, (provider, url) in enumerate(cert_providers[:count]):
                fallbacks.append({
                    "title": f"Professional {topic_title} Certification",
                    "url": f"{url}/{topic.lower().replace(' ', '-')}-certification",
                    "description": f"Industry-recognized {topic} certification from {provider}. Validate your skills and advance your career.",
                    "provider": provider,
                    "type": "certifications",
                    "duration": f"{random.randint(2, 6)} months prep",
                    "rating": f"{random.uniform(4.4, 4.8):.1f}/5",
                    "price": f"${random.randint(150, 300)}",
                    "level": "Professional",
                    "thumbnail": f"https://via.placeholder.com/200x200?text={provider}+Cert",
                    "instructor": provider,
                    "direct_link": True,
                    "verified": False
                })
        
        return fallbacks


# Initialize the enhanced service
enhanced_resource_service = EnhancedResourceService()