from typing import Dict, Any, List

from src.agents.job_market_agent.job_market_agent import JobMarketAgent
from src.agents.course_catalog_agent.course_catalog_agent import CourseCatalogAgent
from src.agents.career_matching_agent.career_matching_agent import CareerMatchingAgent
from src.agents.project_advisor_agent.project_advisor_agent import ProjectAdvisorAgent

class AgentOrchestrator:
    """
    Orchestrator that coordinates interactions between specialized agents
    to provide comprehensive career advisory services to UTD students.
    """

    def __init__(self):
        """Initialize the Agent Orchestrator with all specialized agents"""
        self.job_market_agent = JobMarketAgent()
        self.course_catalog_agent = CourseCatalogAgent()
        self.career_matching_agent = CareerMatchingAgent()
        self.project_advisor_agent = ProjectAdvisorAgent()

    def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a user request by coordinating between specialized agents

        Args:
            request (Dict[str, Any]): User request

        Returns:
            Dict[str, Any]: Comprehensive response
        """
        request_type = request.get("request_type", "career_advice")

        if request_type == "career_advice":
            return self._process_career_advice_request(request)
        elif request_type == "job_market_analysis":
            return self._process_job_market_request(request)
        elif request_type == "course_search":
            return self._process_course_search_request(request)
        elif request_type == "project_recommendations":
            return self._process_project_request(request)
        else:
            return {"error": "Invalid request type"}

    def _process_career_advice_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a comprehensive career advice request

        Args:
            request (Dict[str, Any]): Career advice request

        Returns:
            Dict[str, Any]: Comprehensive career advice response
        """
        career_goal = request.get("career_goal", "")
        location = request.get("location", "")
        current_skills = request.get("current_skills", [])
        completed_courses = request.get("completed_courses", [])
        experience_level = request.get("experience_level", "beginner")

        # Step 1: Get job market data
        job_market_request = {
            "job_title": career_goal,
            "location": location,
            "limit": 10
        }
        job_market_data = self.job_market_agent.process_request(job_market_request)

        # Extract required skills from job market data
        required_skills = []
        if "skills" in job_market_data:
            # Sort skills by count and take top 15
            required_skills = [
                skill for skill, count in sorted(
                    job_market_data["skills"].items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:15]
            ]

        # Step 2: Get course recommendations
        career_matching_request = {
            "career_goal": career_goal,
            "location": location,
            "current_skills": current_skills,
            "completed_courses": completed_courses
        }
        career_advice = self.career_matching_agent.process_request(career_matching_request)

        # Step 3: Get course details for recommended courses
        recommended_courses = career_advice.get("course_recommendations", [])
        course_codes = [course.get("course_code") for course in recommended_courses if "course_code" in course]

        courses_detail = []
        for code in course_codes:
            course_search_request = {
                "search_term": code
            }
            course_results = self.course_catalog_agent.process_request(course_search_request)
            if "courses" in course_results and course_results["courses"]:
                courses_detail.extend(course_results["courses"])

        # Step 4: Get project recommendations
        target_skills = [
            skill for skill in required_skills
            if skill not in current_skills
        ]

        project_request = {
            "career_goal": career_goal,
            "technical_skills": current_skills,
            "target_skills": target_skills,
            "courses": courses_detail,
            "experience_level": experience_level
        }
        project_advice = self.project_advisor_agent.process_request(project_request)

        # Step 5: Compile comprehensive response
        return {
            "career_goal": career_goal,
            "job_market_analysis": {
                "required_skills": required_skills,
                "salary_information": job_market_data.get("salaries", {}),
                "trends": job_market_data.get("trends", [])
            },
            "course_recommendations": career_advice.get("course_recommendations", []),
            "learning_path": career_advice.get("learning_path", {}),
            "project_recommendations": project_advice.get("projects", []),
            "technology_recommendations": project_advice.get("technologies", {}),
            "portfolio_guidance": project_advice.get("portfolio_guidance", {})
        }

    def _process_job_market_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a job market analysis request

        Args:
            request (Dict[str, Any]): Job market request

        Returns:
            Dict[str, Any]: Job market analysis
        """
        return self.job_market_agent.process_request(request)

    def _process_course_search_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a course search request

        Args:
            request (Dict[str, Any]): Course search request

        Returns:
            Dict[str, Any]: Course search results
        """
        return self.course_catalog_agent.process_request(request)

    def _process_project_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a project recommendation request

        Args:
            request (Dict[str, Any]): Project recommendation request

        Returns:
            Dict[str, Any]: Project recommendations
        """
        return self.project_advisor_agent.process_request(request)

    def get_agent_capabilities(self) -> Dict[str, List[str]]:
        """
        Get capabilities of all agents

        Returns:
            Dict[str, List[str]]: Dictionary mapping agent names to capabilities
        """
        return {
            "job_market_agent": self.job_market_agent.get_capabilities(),
            "course_catalog_agent": self.course_catalog_agent.get_capabilities(),
            "career_matching_agent": self.career_matching_agent.get_capabilities(),
            "project_advisor_agent": self.project_advisor_agent.get_capabilities()
        }
