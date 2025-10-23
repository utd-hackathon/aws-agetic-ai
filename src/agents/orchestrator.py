from typing import Dict, Any, List

from src.agents.job_market_agent.job_market_agent import JobMarketAgent
from src.agents.course_catalog_agent.course_catalog_agent import CourseCatalogAgent
from src.agents.career_matching_agent.career_matching_agent import CareerMatchingAgent

class AgentOrchestrator:
    """
    Orchestrator that coordinates interactions between specialized agents
    to provide comprehensive career advisory services to UTD students.
    """

    def __init__(self):
        """Initialize the Agent Orchestrator with all specialized agents"""
        self.job_market_agent = JobMarketAgent()
        self.course_catalog_agent = CourseCatalogAgent()
        
        # Initialize Career Matching Agent with other agents for coordination
        self.career_matching_agent = CareerMatchingAgent(
            job_market_agent=self.job_market_agent,
            course_catalog_agent=self.course_catalog_agent
        )

    async def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a user request by coordinating between specialized agents

        Args:
            request (Dict[str, Any]): User request

        Returns:
            Dict[str, Any]: Comprehensive response
        """
        request_type = request.get("request_type", "career_advice")

        if request_type == "career_advice":
            return await self._process_career_advice_request(request)
        elif request_type == "job_market_analysis":
            return await self._process_job_market_request(request)
        elif request_type == "course_search":
            return self._process_course_search_request(request)
        else:
            return {"error": "Invalid request type"}

    async def _process_career_advice_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a comprehensive career advice request using the Career Matching Agent
        
        • Takes user career goals and coordinates with other agents
        • Analyzes job requirements vs. available coursework
        • Generates personalized course recommendations with explanations

        Args:
            request (Dict[str, Any]): Career advice request

        Returns:
            Dict[str, Any]: Comprehensive career advice response
        """
        print("🎯 Processing career advice request through Career Matching Agent...")
        
        # Use the Career Matching Agent to coordinate everything
        career_matching_response = await self.career_matching_agent.process_request(request)
        
        # If Career Matching Agent succeeded, return its comprehensive response
        if career_matching_response.get("success"):
            return {
                "success": True,
                "career_goal": career_matching_response.get("career_goal"),
                "location": career_matching_response.get("location"),
                
                # Job market insights
                "job_insights": [
                    f"Found {career_matching_response['job_market_analysis']['total_jobs']} job opportunities",
                    f"Average salary: ${career_matching_response['job_market_analysis']['salary_info'].get('overall_average', 0):,.0f}",
                    f"Top trending skills: {', '.join(career_matching_response['job_market_analysis']['trending_skills'][:3])}"
                ],
                
                # Skill gap analysis
                "skill_analysis": {
                    "current_coverage": f"{career_matching_response['skill_gap_analysis']['skill_coverage']:.1f}%",
                    "skills_to_develop": career_matching_response['skill_gap_analysis']['skills_to_develop'],
                    "missing_skills": [skill['skill'] for skill in career_matching_response['skill_gap_analysis']['missing_skills'][:5]]
                },
                
                # Course recommendations with explanations
                "course_recommendations": career_matching_response.get("course_recommendations", []),
                
                # Learning path
                "learning_path": career_matching_response.get("learning_path", {}),
                
                # Summary
                "summary": {
                    "total_courses_recommended": career_matching_response.get("total_recommended_courses", 0),
                    "estimated_completion": career_matching_response.get("estimated_completion_time", "Unknown"),
                    "next_steps": [
                        "Review the recommended courses and their explanations",
                        "Check prerequisites for your first semester courses", 
                        "Consider your current schedule and course load",
                        "Meet with an academic advisor to finalize your plan"
                    ]
                }
            }
        
        # Fallback if Career Matching Agent failed
        return {
            "success": False,
            "error": "Career matching analysis failed",
            "career_goal": request.get("career_goal", ""),
            "location": request.get("location", ""),
            "message": "Please try again or contact support"
        }

    async def _process_job_market_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a job market analysis request

        Args:
            request (Dict[str, Any]): Job market request

        Returns:
            Dict[str, Any]: Job market analysis
        """
        return await self.job_market_agent.process_request(request)

    def _process_course_search_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a course search request

        Args:
            request (Dict[str, Any]): Course search request

        Returns:
            Dict[str, Any]: Course search results
        """
        return self.course_catalog_agent.process_request(request)

    def get_agent_capabilities(self) -> Dict[str, List[str]]:
        """
        Get capabilities of all agents

        Returns:
            Dict[str, List[str]]: Dictionary mapping agent names to capabilities
        """
        return {
            "job_market_agent": self.job_market_agent.get_capabilities(),
            "course_catalog_agent": self.course_catalog_agent.get_capabilities(),
            "career_matching_agent": self.career_matching_agent.get_capabilities()
        }
