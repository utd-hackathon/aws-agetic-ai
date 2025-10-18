from typing import Dict, Any, List
import json
import re
from src.agents.base_agent import BaseAgent

class ProjectAdvisorAgent(BaseAgent):
    """
    Agent responsible for suggesting specific projects that bridge coursework
    to job requirements, recommending technologies and frameworks to learn,
    and providing portfolio development guidance.
    """

    def __init__(self):
        """Initialize the Project Advisor Agent"""
        super().__init__(
            name="Project Advisor Agent",
            description="Suggests projects and technologies to help build a portfolio aligned with career goals"
        )

    def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a project advisor request

        Args:
            request (Dict[str, Any]): Request with career goal, skills, and courses

        Returns:
            Dict[str, Any]: Project and technology recommendations
        """
        career_goal = request.get("career_goal", "")
        technical_skills = request.get("technical_skills", [])
        target_skills = request.get("target_skills", [])
        courses = request.get("courses", [])
        experience_level = request.get("experience_level", "beginner")

        if not career_goal:
            return {"error": "Career goal is required"}

        # Generate project recommendations
        project_recommendations = self.generate_projects(
            career_goal, technical_skills, target_skills, experience_level
        )

        # Recommend technologies and frameworks
        tech_recommendations = self.recommend_technologies(
            career_goal, technical_skills, target_skills
        )

        # Generate portfolio development guidance
        portfolio_guidance = self.generate_portfolio_guidance(
            career_goal, project_recommendations, tech_recommendations
        )

        # Link projects to courses
        course_project_links = self.link_projects_to_courses(
            project_recommendations, courses
        )

        return {
            "career_goal": career_goal,
            "projects": project_recommendations,
            "technologies": tech_recommendations,
            "portfolio_guidance": portfolio_guidance,
            "course_project_links": course_project_links
        }

    def generate_projects(
        self,
        career_goal: str,
        current_skills: List[str],
        target_skills: List[str],
        experience_level: str
    ) -> List[Dict[str, Any]]:
        """
        Generate project recommendations

        Args:
            career_goal (str): Career goal
            current_skills (List[str]): Current skills
            target_skills (List[str]): Target skills to learn
            experience_level (str): Experience level

        Returns:
            List[Dict[str, Any]]: Project recommendations
        """
        prompt = f"""
        You are a project advisor for UTD students pursuing a career in {career_goal}.
        Given the following information:
        
        Current skills: {', '.join(current_skills) if current_skills else 'None'}
        Target skills to learn: {', '.join(target_skills) if target_skills else 'None'}
        Experience level: {experience_level}
        
        Suggest 3-5 practical projects that would:
        1. Help the student build the target skills
        2. Demonstrate their abilities to potential employers
        3. Be appropriate for their experience level
        4. Be relevant to their career goal in {career_goal}
        
        For each project, include:
        1. Project title
        2. Brief description (1-2 sentences)
        3. Skills practiced/developed
        4. Estimated time to complete (in hours or weeks)
        5. Difficulty level (Beginner, Intermediate, Advanced)
        6. Key deliverables
        
        Format your response as a JSON array of objects with the fields above.
        """

        response = self.get_llm_response(prompt)

        # Parse the JSON response
        try:
            # Extract JSON from the response
            json_match = re.search(r'(\[.*\])', response.replace('\n', ' '))
            if json_match:
                projects = json.loads(json_match.group(1))
            else:
                projects = []
        except Exception as e:
            print(f"Error parsing project recommendations: {e}")
            projects = []

        return projects

    def recommend_technologies(
        self,
        career_goal: str,
        current_skills: List[str],
        target_skills: List[str]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Recommend technologies and frameworks

        Args:
            career_goal (str): Career goal
            current_skills (List[str]): Current skills
            target_skills (List[str]): Target skills to learn

        Returns:
            Dict[str, List[Dict[str, Any]]]: Technology recommendations by category
        """
        prompt = f"""
        You are a technology advisor for students pursuing a career in {career_goal}.
        Based on:
        
        Career goal: {career_goal}
        Current skills: {', '.join(current_skills) if current_skills else 'None'}
        Target skills: {', '.join(target_skills) if target_skills else 'None'}
        
        Recommend specific technologies, frameworks, and tools that the student should learn.
        Group your recommendations into categories like:
        
        - Programming Languages
        - Frameworks/Libraries
        - Databases
        - Cloud Services
        - Development Tools
        - Other Technologies
        
        For each technology, include:
        1. Name
        2. Brief description of why it's relevant
        3. Learning difficulty (Easy, Moderate, Challenging)
        4. Industry demand (High, Medium, Low)
        
        Format your response as a JSON object where keys are categories and values are arrays of technology objects.
        """

        response = self.get_llm_response(prompt)

        # Parse the JSON response
        try:
            # Clean up response and extract JSON
            cleaned_response = response.strip().replace("```json", "").replace("```", "")
            json_match = re.search(r'(\{.*\})', cleaned_response.replace('\n', ' '))
            if json_match:
                technologies = json.loads(json_match.group(1))
            else:
                technologies = {}
        except Exception as e:
            print(f"Error parsing technology recommendations: {e}")
            technologies = {}

        return technologies

    def generate_portfolio_guidance(
        self,
        career_goal: str,
        project_recommendations: List[Dict[str, Any]],
        tech_recommendations: Dict[str, List[Dict[str, Any]]]
    ) -> Dict[str, Any]:
        """
        Generate portfolio development guidance

        Args:
            career_goal (str): Career goal
            project_recommendations (List[Dict[str, Any]]): Project recommendations
            tech_recommendations (Dict[str, List[Dict[str, Any]]]): Technology recommendations

        Returns:
            Dict[str, Any]: Portfolio guidance
        """
        # Extract project titles
        project_titles = [p.get("project_title", "") for p in project_recommendations]

        # Extract top technologies
        top_techs = []
        for category, techs in tech_recommendations.items():
            for tech in techs[:2]:  # Get top 2 from each category
                if "name" in tech:
                    top_techs.append(tech["name"])

        prompt = f"""
        You are a portfolio development advisor for students pursuing a career in {career_goal}.
        Based on the following projects and technologies:
        
        Projects: {', '.join(project_titles)}
        Technologies: {', '.join(top_techs)}
        
        Provide comprehensive guidance on developing a strong portfolio that will appeal to employers.
        
        Include:
        1. Portfolio structure recommendations
        2. How to present the projects effectively
        3. What to emphasize for each project
        4. Additional portfolio elements beyond projects
        5. Online platforms to showcase the portfolio
        6. Tips for describing skills and technologies
        
        Format your response as a JSON object with these sections as keys and detailed guidance as values.
        """

        response = self.get_llm_response(prompt)

        # Parse the JSON response
        try:
            # Clean up response and extract JSON
            cleaned_response = response.strip().replace("```json", "").replace("```", "")
            json_match = re.search(r'(\{.*\})', cleaned_response.replace('\n', ' '))
            if json_match:
                guidance = json.loads(json_match.group(1))
            else:
                guidance = {}
        except Exception as e:
            print(f"Error parsing portfolio guidance: {e}")
            guidance = {}

        return guidance

    def link_projects_to_courses(
        self,
        projects: List[Dict[str, Any]],
        courses: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Link projects to relevant courses

        Args:
            projects (List[Dict[str, Any]]): Project recommendations
            courses (List[Dict[str, Any]]): Course information

        Returns:
            List[Dict[str, Any]]: Links between projects and courses
        """
        if not projects or not courses:
            return []

        # Extract project titles and skills
        project_info = [
            {
                "title": p.get("project_title", ""),
                "skills": p.get("skills", [])
            }
            for p in projects
        ]

        # Extract course codes and titles
        course_info = [
            {
                "code": c.get("course_code", ""),
                "title": c.get("course_title", ""),
                "description": c.get("course_description", "")
            }
            for c in courses
        ]

        prompt = f"""
        You are an academic advisor connecting projects to relevant courses.
        
        Projects: {json.dumps(project_info)}
        
        Courses: {json.dumps(course_info)}
        
        For each project, identify the most relevant courses that would help a student
        develop the necessary skills for that project. Explain why each course is relevant.
        
        Format your response as a JSON array where each object contains:
        1. "project_title": The project title
        2. "relevant_courses": Array of objects with:
           - "course_code": The course code
           - "relevance": Brief explanation of relevance to the project
        
        Only include meaningful connections between projects and courses.
        """

        response = self.get_llm_response(prompt)

        # Parse the JSON response
        try:
            # Extract JSON from the response
            json_match = re.search(r'(\[.*\])', response.replace('\n', ' '))
            if json_match:
                links = json.loads(json_match.group(1))
            else:
                links = []
        except Exception as e:
            print(f"Error parsing project-course links: {e}")
            links = []

        return links

    def get_capabilities(self) -> List[str]:
        """
        Get the capabilities of this agent

        Returns:
            List[str]: List of capability descriptions
        """
        return [
            "Suggest specific projects that align with career goals",
            "Recommend technologies and frameworks to learn",
            "Provide portfolio development guidance",
            "Link projects to relevant UTD courses",
            "Customize recommendations based on experience level"
        ]
