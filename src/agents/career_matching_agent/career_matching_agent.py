from typing import Dict, Any, List
import json
import asyncio
from src.agents.base_agent import BaseAgent
from src.core.llm.career_llm_service import career_llm_service

class CareerMatchingAgent(BaseAgent):
    """
    Agent responsible for taking user career goals, coordinating with other agents,
    analyzing job requirements vs. available coursework, and generating personalized
    course recommendations with explanations.
    
    This agent:
    • Takes user career goals and coordinates with other agents
    • Analyzes job requirements vs. available coursework  
    • Generates personalized course recommendations with explanations
    """

    def __init__(self, job_market_agent=None, course_catalog_agent=None):
        """Initialize the Career Matching Agent"""
        super().__init__(
            name="Career Matching Agent",
            description="Matches career goals with courses and provides personalized recommendations"
        )
        self.job_market_agent = job_market_agent
        self.course_catalog_agent = course_catalog_agent

    async def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a career matching request by coordinating with other agents
        
        • Takes user career goals and coordinates with other agents
        • Analyzes job requirements vs. available coursework
        • Generates personalized course recommendations with explanations

        Args:
            request (Dict[str, Any]): Request with career goal and user info

        Returns:
            Dict[str, Any]: Career matching recommendations
        """
        career_goal = request.get("career_goal", "")
        location = request.get("location", "")
        current_skills = request.get("current_skills", [])
        completed_courses = request.get("completed_courses", [])

        if not career_goal:
            return {"error": "Career goal is required"}

        print(f"🎯 Career Matching Agent processing: {career_goal}")
        
        # Store career goal for LLM context
        self._current_career_goal = career_goal
        
        # Step 1: Coordinate with Job Market Agent to get real job requirements
        print("📊 Coordinating with Job Market Agent...")
        job_market_data = await self._get_job_market_requirements(career_goal, location)
        
        # Step 2: Coordinate with Course Catalog Agent to get available courses
        print("📚 Coordinating with Course Catalog Agent...")
        available_courses = await self._get_available_courses()
        
        # Step 3: Analyze job requirements vs. available coursework
        print("🔍 Analyzing job requirements vs. available coursework...")
        skill_gap_analysis = self._analyze_skill_gaps(job_market_data, current_skills)
        
        # Step 4: Generate personalized course recommendations with explanations
        print("💡 Generating personalized course recommendations...")
        course_recommendations = self._generate_course_recommendations(
            skill_gap_analysis, available_courses, completed_courses
        )
        
        # Step 5: Create learning path
        print("🗺️ Creating personalized learning path...")
        learning_path = self._create_learning_path(course_recommendations, current_skills)

        return {
            "success": True,
            "career_goal": career_goal,
            "location": location,
            "job_market_analysis": {
                "total_jobs": job_market_data.get("job_count", 0),
                "required_skills": job_market_data.get("skills", {}),
                "salary_info": job_market_data.get("salaries", {}),
                "trending_skills": list(job_market_data.get("skills", {}).keys())[:10]
            },
            "skill_gap_analysis": skill_gap_analysis,
            "course_recommendations": course_recommendations,
            "learning_path": learning_path,
            "total_recommended_courses": len(course_recommendations),
            "estimated_completion_time": f"{len(course_recommendations) // 2 + 1} semesters"
        }

    async def _get_job_market_requirements(self, career_goal: str, location: str) -> Dict[str, Any]:
        """
        Coordinate with Job Market Agent to get real job requirements
        
        Args:
            career_goal (str): Career goal
            location (str): Preferred location
            
        Returns:
            Dict[str, Any]: Job market data with requirements
        """
        if not self.job_market_agent:
            print("⚠️ Job Market Agent not available, using fallback data")
            return self._get_fallback_job_requirements(career_goal)
        
        try:
            # Call Job Market Agent to get real job data (optimized for top 2 jobs)
            job_request = {
                "job_title": career_goal,
                "location": location,
                "limit": 2  # Optimized to only get top 2 jobs for efficiency
            }
            job_data = await self.job_market_agent.process_request(job_request)
            return job_data
        except Exception as e:
            print(f"❌ Error coordinating with Job Market Agent: {e}")
            return self._get_fallback_job_requirements(career_goal)
    
    def _get_fallback_job_requirements(self, career_goal: str) -> Dict[str, Any]:
        """Fallback job requirements when Job Market Agent is unavailable"""
        # Common skills for different career goals
        skill_mapping = {
            "data scientist": ["Python", "Machine Learning", "SQL", "Statistics", "Pandas", "NumPy"],
            "software engineer": ["Python", "JavaScript", "Git", "SQL", "React", "Node.js"],
            "devops engineer": ["AWS", "Docker", "Kubernetes", "Linux", "Python", "Jenkins"],
            "data engineer": ["Python", "SQL", "Apache Spark", "AWS", "ETL", "Kafka"],
            "machine learning engineer": ["Python", "TensorFlow", "PyTorch", "MLOps", "Docker", "AWS"]
        }
        
        # Get skills for the career goal (case insensitive)
        goal_lower = career_goal.lower()
        skills = {}
        for key, skill_list in skill_mapping.items():
            if key in goal_lower:
                for skill in skill_list:
                    skills[skill] = 3  # Mock frequency
                break
        
        if not skills:
            # Default skills for any technical role
            skills = {"Python": 3, "SQL": 2, "Git": 2, "Problem Solving": 3}
        
        return {
            "job_count": 5,
            "skills": skills,
            "salaries": {"count": 3, "average_min": 70000, "average_max": 120000, "overall_average": 95000},
            "trends": ["Remote work", "Cloud computing", "AI/ML"]
        }

    async def _get_available_courses(self) -> List[Dict[str, Any]]:
        """
        Coordinate with Course Catalog Agent to get available courses
        
        Returns:
            List[Dict[str, Any]]: Available courses
        """
        if not self.course_catalog_agent:
            print("⚠️ Course Catalog Agent not available, using fallback data")
            return self._get_fallback_courses()
        
        try:
            # Get all available courses directly from Course Catalog Agent
            # Use direct access to courses instead of process_request for getting all courses
            return self.course_catalog_agent.courses
        except Exception as e:
            print(f"❌ Error coordinating with Course Catalog Agent: {e}")
            return self._get_fallback_courses()
    
    def _get_fallback_courses(self) -> List[Dict[str, Any]]:
        """Fallback course data when Course Catalog Agent is unavailable"""
        return [
            {
                "course_code": "CS 1336",
                "title": "Programming Fundamentals",
                "description": "Introduction to programming concepts using Java",
                "skills": ["Java", "Programming", "Problem Solving"],
                "prerequisites": "None"
            },
            {
                "course_code": "CS 2336",
                "title": "Computer Science II",
                "description": "Object-oriented programming and data structures",
                "skills": ["Java", "Data Structures", "OOP"],
                "prerequisites": "CS 1336"
            },
            {
                "course_code": "CS 3345",
                "title": "Data Structures and Introduction to Algorithmic Analysis",
                "description": "Advanced data structures and algorithm analysis",
                "skills": ["Algorithms", "Data Structures", "Analysis"],
                "prerequisites": "CS 2336"
            },
            {
                "course_code": "CS 4349",
                "title": "Advanced Algorithm Design and Analysis",
                "description": "Design and analysis of efficient algorithms",
                "skills": ["Algorithms", "Complexity Analysis", "Problem Solving"],
                "prerequisites": "CS 3345"
            },
            {
                "course_code": "CS 4337",
                "title": "Organization of Programming Languages",
                "description": "Study of programming language concepts and paradigms",
                "skills": ["Programming Languages", "Compilers", "Language Design"],
                "prerequisites": "CS 3345"
            },
            {
                "course_code": "CS 4348",
                "title": "Operating Systems Concepts",
                "description": "Operating system design and implementation",
                "skills": ["Operating Systems", "System Programming", "Concurrency"],
                "prerequisites": "CS 3345"
            },
            {
                "course_code": "CS 4375",
                "title": "Introduction to Machine Learning",
                "description": "Fundamentals of machine learning algorithms and applications",
                "skills": ["Machine Learning", "Python", "Statistics", "Data Analysis"],
                "prerequisites": "CS 3345"
            },
            {
                "course_code": "CS 4395",
                "title": "Human Language Technologies",
                "description": "Natural language processing and computational linguistics",
                "skills": ["NLP", "Python", "Machine Learning", "Text Processing"],
                "prerequisites": "CS 3345"
            }
        ]
    
    def _analyze_skill_gaps(self, job_market_data: Dict[str, Any], current_skills: List[str]) -> Dict[str, Any]:
        """
        Analyze skill gaps between job requirements and current skills
        
        Args:
            job_market_data (Dict[str, Any]): Job market data with required skills
            current_skills (List[str]): User's current skills
            
        Returns:
            Dict[str, Any]: Skill gap analysis
        """
        required_skills = job_market_data.get("skills", {})
        
        # Convert current_skills to lowercase for comparison
        current_skills_lower = [skill.lower() for skill in current_skills]
        
        # Identify missing skills
        missing_skills = []
        existing_skills = []
        
        for skill, frequency in required_skills.items():
            if skill.lower() in current_skills_lower:
                existing_skills.append({
                    "skill": skill,
                    "frequency": frequency,
                    "status": "already_have"
                })
            else:
                missing_skills.append({
                    "skill": skill,
                    "frequency": frequency,
                    "priority": "high" if frequency >= 3 else "medium" if frequency >= 2 else "low"
                })
        
        # Sort missing skills by frequency (priority)
        missing_skills.sort(key=lambda x: x["frequency"], reverse=True)
        
        return {
            "missing_skills": missing_skills,
            "existing_skills": existing_skills,
            "skill_coverage": len(existing_skills) / (len(existing_skills) + len(missing_skills)) * 100 if (existing_skills or missing_skills) else 0,
            "total_required_skills": len(required_skills),
            "skills_to_develop": len(missing_skills)
        }

    def _generate_course_recommendations(
        self,
        skill_gap_analysis: Dict[str, Any],
        available_courses: List[Dict[str, Any]],
        completed_courses: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Generate personalized course recommendations using LLM for relevance
        
        Args:
            skill_gap_analysis (Dict[str, Any]): Skill gap analysis
            available_courses (List[Dict[str, Any]]): Available courses
            completed_courses (List[str]): User's completed courses
            
        Returns:
            List[Dict[str, Any]]: Course recommendations with explanations
        """
        print("🤖 Using LLM to generate relevant course recommendations...")
        
        # Get career goal from the analysis context
        career_goal = getattr(self, '_current_career_goal', 'General Career')
        
        # Get job requirements from skill gap analysis
        job_requirements = {
            'skills': {skill['skill']: skill['priority'] for skill in skill_gap_analysis.get('missing_skills', [])}
        }
        
        # Use LLM service to get relevant recommendations
        llm_analysis = career_llm_service.analyze_career_skills_match(
            career_goal=career_goal,
            available_courses=available_courses,
            job_requirements=job_requirements
        )
        
        if not llm_analysis.get('success'):
            print("⚠️ LLM analysis failed, using fallback recommendations")
            return self._fallback_course_recommendations(skill_gap_analysis, available_courses, completed_courses)
        
        # Convert LLM recommendations to our format
        recommendations = []
        completed_course_codes = set([course.lower() for course in completed_courses])
        llm_recommendations = llm_analysis.get('llm_recommendations', [])
        
        print(f"🎯 LLM found {len(llm_recommendations)} relevant courses for {career_goal}")
        print(f"🔍 LLM analysis success: {llm_analysis.get('success')}")
        print(f"🔍 Available courses: {len(available_courses)}")
        
        for llm_rec in llm_recommendations:
            course_code = llm_rec.get('course_code', '')
            
            if course_code.lower() in completed_course_codes:
                continue
            
            # Find the full course details
            course_details = None
            for course in available_courses:
                if course.get('course_code') == course_code:
                    course_details = course
                    break
            
            if course_details:
                # Map LLM priority to our priority system
                relevance_score = llm_rec.get('relevance_score', 5)
                if relevance_score >= 8:
                    priority = 'high'
                elif relevance_score >= 6:
                    priority = 'medium'
                else:
                    priority = 'low'
                
                recommendations.append({
                    "course_code": course_code,
                    "title": course_details.get("title", llm_rec.get("title", "Course Title")),
                    "description": course_details.get("description", "Course description not available"),
                    "skills_addressed": llm_rec.get("skills_gained", course_details.get("skills", [])[:3]),
                    "priority": priority,
                    "explanation": llm_rec.get("explanation", f"This course is relevant for your {career_goal} career goal."),
                    "prerequisites": course_details.get("prerequisites", "None listed"),
                    "semester_credit_hours": course_details.get("semester_credit_hours", "3"),
                    "relevance_score": relevance_score,
                    "llm_recommended": True
                })
        
        # If LLM didn't find enough courses, supplement with skill-based matching
        if len(recommendations) < 3:
            print("🔄 Supplementing with skill-based recommendations...")
            fallback_recs = self._fallback_course_recommendations(skill_gap_analysis, available_courses, completed_courses)
            
            # Add fallback recommendations that aren't already included
            existing_codes = {rec["course_code"] for rec in recommendations}
            for fallback_rec in fallback_recs:
                if fallback_rec["course_code"] not in existing_codes and len(recommendations) < 6:
                    fallback_rec["llm_recommended"] = False
                    recommendations.append(fallback_rec)
        
        print(f"✅ Generated {len(recommendations)} relevant course recommendations")
        return recommendations[:6]  # Limit to 6 recommendations
    
    def _fallback_course_recommendations(
        self,
        skill_gap_analysis: Dict[str, Any],
        available_courses: List[Dict[str, Any]],
        completed_courses: List[str]
    ) -> List[Dict[str, Any]]:
        """Fallback course recommendations when LLM is unavailable"""
        missing_skills = skill_gap_analysis.get("missing_skills", [])
        recommendations = []
        
        # Convert completed courses to lowercase for comparison
        completed_lower = [course.lower() for course in completed_courses]
        
        for skill_info in missing_skills:
            skill = skill_info["skill"]
            priority = skill_info["priority"]
            
            # Find courses that teach this skill
            matching_courses = []
            for course in available_courses:
                course_skills = course.get("skills", [])
                course_code = course.get("course_code", "")
                
                # Skip if already completed
                if course_code.lower() in completed_lower:
                    continue
                
                # Check if course teaches the required skill
                if any(skill.lower() in course_skill.lower() for course_skill in course_skills):
                    matching_courses.append(course)
            
            # Add best matching course for this skill
            if matching_courses:
                best_course = matching_courses[0]  # Take first match
                
                recommendation = {
                    "course_code": best_course.get("course_code", ""),
                    "title": best_course.get("title", ""),
                    "description": best_course.get("description", ""),
                    "skills_addressed": [skill],
                    "priority": priority,
                    "explanation": f"This course will help you develop {skill} skills, which are {priority} priority for your career goal.",
                    "prerequisites": best_course.get("prerequisites", ""),
                    "semester_credit_hours": best_course.get("semester_credit_hours", "3")
                }
                
                # Avoid duplicates
                if not any(rec["course_code"] == recommendation["course_code"] for rec in recommendations):
                    recommendations.append(recommendation)
        
        # Sort by priority (high -> medium -> low)
        priority_order = {"high": 0, "medium": 1, "low": 2}
        recommendations.sort(key=lambda x: priority_order.get(x["priority"], 3))
        
        return recommendations[:6]  # Limit to 6 recommendations
    
    def _create_learning_path(
        self,
        course_recommendations: List[Dict[str, Any]],
        current_skills: List[str]
    ) -> Dict[str, Any]:
        """
        Create a personalized learning path with semester-by-semester progression
        
        Args:
            course_recommendations (List[Dict[str, Any]]): Course recommendations
            current_skills (List[str]): User's current skills
            
        Returns:
            Dict[str, Any]: Learning path with semesters and rationale
        """
        if not course_recommendations:
            return {
                "semesters": [],
                "rationale": "No course recommendations available to create a learning path."
            }
        
        # Group courses by priority
        high_priority = [c for c in course_recommendations if c.get("priority") == "high"]
        medium_priority = [c for c in course_recommendations if c.get("priority") == "medium"]
        low_priority = [c for c in course_recommendations if c.get("priority") == "low"]
        
        semesters = []
        semester_count = 1
        courses_per_semester = 2
        
        # Create semesters starting with high priority courses
        all_courses = high_priority + medium_priority + low_priority
        
        for i in range(0, len(all_courses), courses_per_semester):
            semester_courses = all_courses[i:i + courses_per_semester]
            
            if semester_courses:
                semester_name = f"Semester {semester_count}"
                semesters.append({
                    "semester_name": semester_name,
                    "courses": [
                        {
                            "course_code": course["course_code"],
                            "title": course["title"],
                            "priority": course["priority"]
                        }
                        for course in semester_courses
                    ]
                })
                semester_count += 1
        
        rationale = f"""
        This learning path is designed to systematically address your skill gaps:
        
        • High priority skills are addressed first ({len(high_priority)} courses)
        • Medium priority skills follow ({len(medium_priority)} courses)  
        • Low priority skills are covered last ({len(low_priority)} courses)
        • Each semester includes {courses_per_semester} courses for manageable workload
        • Total completion time: {len(semesters)} semesters
        
        This progression ensures you develop the most critical skills for your career goal first.
        """
        
        return {
            "semesters": semesters,
            "rationale": rationale.strip(),
            "total_semesters": len(semesters),
            "total_courses": len(course_recommendations)
        }

    def get_capabilities(self) -> List[str]:
        """
        Get the capabilities of this agent

        Returns:
            List[str]: List of capability descriptions
        """
        return [
            "Takes user career goals and coordinates with other agents",
            "Analyzes job requirements vs. available coursework",
            "Generates personalized course recommendations with explanations",
            "Creates skill gap analysis based on real job market data",
            "Develops semester-by-semester learning paths",
            "Coordinates with Job Market Agent for real job requirements",
            "Coordinates with Course Catalog Agent for available courses",
            "Provides priority-based course sequencing",
            "Estimates completion time and workload"
        ]
