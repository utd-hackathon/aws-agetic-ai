from typing import Dict, Any, List
import json
from src.agents.base_agent import BaseAgent

class CareerMatchingAgent(BaseAgent):
    """
    Agent responsible for taking user career goals, coordinating with other agents,
    analyzing job requirements vs. available coursework, and generating personalized
    course recommendations with explanations.
    """

    def __init__(self):
        """Initialize the Career Matching Agent"""
        super().__init__(
            name="Career Matching Agent",
            description="Matches career goals with courses and provides personalized recommendations"
        )

    def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a career matching request

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

        # This agent doesn't directly implement the job market or course catalog functionality
        # but would coordinate with those agents in a real implementation.
        # For demonstration, we'll simulate the coordinated response using LLM.

        # 1. Generate job requirements for the career goal
        job_requirements = self.get_job_requirements(career_goal, location)

        # 2. Generate course recommendations based on job requirements
        course_recommendations = self.get_course_recommendations(
            job_requirements, current_skills, completed_courses
        )

        # 3. Generate a personalized learning path
        learning_path = self.generate_learning_path(course_recommendations, current_skills)

        return {
            "career_goal": career_goal,
            "job_requirements": job_requirements,
            "course_recommendations": course_recommendations,
            "learning_path": learning_path
        }

    def get_job_requirements(self, career_goal: str, location: str = "") -> Dict[str, Any]:
        """
        Get job requirements for a career goal

        Args:
            career_goal (str): Career goal
            location (str): Preferred location

        Returns:
            Dict[str, Any]: Job requirements
        """
        prompt = f"""
        You are a career analysis expert. For the career goal of "{career_goal}"
        {f'in {location}' if location else ''}, provide a detailed analysis of:
        
        1. Essential technical skills required
        2. Important soft skills needed
        3. Typical educational requirements
        4. Experience level expectations
        5. Industry certifications that would be valuable
        
        Format your response as a JSON object with these categories as keys,
        and arrays of specific items as values.
        """

        response = self.get_llm_response(prompt)

        # Parse the JSON response
        try:
            requirements_match = response.strip().replace("```json", "").replace("```", "")
            requirements = json.loads(requirements_match)
        except Exception as e:
            print(f"Error parsing job requirements: {e}")
            requirements = {
                "technical_skills": [],
                "soft_skills": [],
                "education": [],
                "experience": [],
                "certifications": []
            }

        return requirements

    def get_course_recommendations(
        self,
        job_requirements: Dict[str, Any],
        current_skills: List[str],
        completed_courses: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Get course recommendations based on job requirements and user background

        Args:
            job_requirements (Dict[str, Any]): Job requirements
            current_skills (List[str]): User's current skills
            completed_courses (List[str]): User's completed courses

        Returns:
            List[Dict[str, Any]]: Course recommendations
        """
        # Extract technical skills from job requirements
        technical_skills = job_requirements.get("technical_skills", [])

        # Create a list of missing skills (skills required but not in current_skills)
        missing_skills = [skill for skill in technical_skills if skill not in current_skills]

        prompt = f"""
        You are a UTD course recommendation expert. Based on the following information:
        
        1. Missing skills the student needs to acquire: {missing_skills}
        2. Courses the student has already completed: {completed_courses}
        
        Recommend 5-8 UTD courses that would help the student gain the missing skills.
        
        For each course, include:
        1. Course code (e.g., CS 6301)
        2. Course title
        3. Primary skills addressed from the missing skills list
        4. Brief justification for the recommendation
        
        Format your response as a JSON array of objects with the fields above.
        """

        response = self.get_llm_response(prompt)

        # Parse the JSON response
        try:
            recommendations_match = response.strip().replace("```json", "").replace("```", "")
            # Extract JSON array using regex
            import re
            json_match = re.search(r'(\[.*\])', recommendations_match.replace('\n', ' '))
            if json_match:
                recommendations = json.loads(json_match.group(1))
            else:
                recommendations = []
        except Exception as e:
            print(f"Error parsing course recommendations: {e}")
            recommendations = []

        return recommendations

    def generate_learning_path(
        self,
        course_recommendations: List[Dict[str, Any]],
        current_skills: List[str]
    ) -> Dict[str, Any]:
        """
        Generate a personalized learning path

        Args:
            course_recommendations (List[Dict[str, Any]]): Course recommendations
            current_skills (List[str]): User's current skills

        Returns:
            Dict[str, Any]: Learning path
        """
        # Extract course codes and titles
        courses = [
            {
                "code": course.get("course_code", ""),
                "title": course.get("course_title", "")
            }
            for course in course_recommendations
        ]

        prompt = f"""
        You are an educational planning expert. Based on these recommended courses:
        
        {json.dumps(courses, indent=2)}
        
        And the student's current skills:
        {current_skills}
        
        Create a semester-by-semester learning path that organizes these courses
        in a logical sequence, considering prerequisites and skill-building progression.
        
        Organize your response as a JSON object with:
        1. "semesters": an array of semester objects, each containing:
           - "semester_name" (e.g., "Fall 2025")
           - "courses": array of course codes to take that semester
        2. "rationale": brief explanation of the overall path design
        
        Assume a standard load of 2-3 courses per semester.
        """

        response = self.get_llm_response(prompt)

        # Parse the JSON response
        try:
            path_match = response.strip().replace("```json", "").replace("```", "")
            # Extract JSON object using regex
            import re
            json_match = re.search(r'(\{.*\})', path_match.replace('\n', ' '))
            if json_match:
                learning_path = json.loads(json_match.group(1))
            else:
                learning_path = {"semesters": [], "rationale": ""}
        except Exception as e:
            print(f"Error parsing learning path: {e}")
            learning_path = {"semesters": [], "rationale": ""}

        return learning_path

    def get_capabilities(self) -> List[str]:
        """
        Get the capabilities of this agent

        Returns:
            List[str]: List of capability descriptions
        """
        return [
            "Analyze job requirements for specific career goals",
            "Match job requirements with UTD courses",
            "Generate personalized course recommendations",
            "Create semester-by-semester learning paths",
            "Coordinate with Job Market and Course Catalog agents"
        ]
