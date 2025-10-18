from typing import Dict, Any, List
import requests
import json
import re
import os
from dotenv import load_dotenv
from src.agents.base_agent import BaseAgent

# Load environment variables
load_dotenv()

class CourseCatalogAgent(BaseAgent):
    """
    Agent responsible for gathering UTD course descriptions and prerequisites,
    analyzing course content to extract taught skills, and mapping relationships
    between courses.
    """

    def __init__(self):
        """Initialize the Course Catalog Agent"""
        super().__init__(
            name="Course Catalog Agent",
            description="Analyzes UTD course offerings to extract skills and course relationships"
        )
        self.utd_api_url = os.getenv("UTD_COURSE_API_URL", "")
        self.utd_api_key = os.getenv("UTD_COURSE_API_KEY", "")

        # Cache for course data
        self.course_cache = {}

    def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a course catalog request

        Args:
            request (Dict[str, Any]): Request containing search parameters

        Returns:
            Dict[str, Any]: Course catalog data
        """
        search_term = request.get("search_term", "")
        department = request.get("department", "")
        skill = request.get("skill", "")

        # Get course data based on request parameters
        if search_term:
            courses = self.search_courses(search_term)
        elif department:
            courses = self.get_courses_by_department(department)
        elif skill:
            courses = self.get_courses_by_skill(skill)
        else:
            return {"error": "No search criteria provided"}

        # Extract skills from courses
        if courses:
            course_skills = self.extract_course_skills(courses)

            # Map relationships between courses
            course_relationships = self.map_course_relationships(courses)

            return {
                "courses": courses,
                "skills": course_skills,
                "relationships": course_relationships
            }
        else:
            return {"error": "No courses found matching the criteria"}

    def get_all_courses(self) -> List[Dict[str, Any]]:
        """
        Get all courses from the UTD course catalog

        Returns:
            List[Dict[str, Any]]: List of courses
        """
        # In a real implementation, this would use an API or web scraping
        # to get actual course data. For demonstration, we'll simulate with LLM.

        if self.course_cache:
            return list(self.course_cache.values())

        prompt = """
        You are a UTD course catalog expert. Generate a comprehensive list of 30 realistic UTD courses
        across different departments including Computer Science, Data Science, Business, and Engineering.
        
        For each course, include:
        1. Course code (e.g., CS 6301)
        2. Course title
        3. Department
        4. Course description
        5. Prerequisites (if any)
        6. Credit hours
        
        Format your response as a JSON array of objects with the fields above.
        """

        response = self.get_llm_response(prompt)

        # Parse the JSON response
        try:
            # Extract JSON from the response
            json_match = re.search(r'(\[.*\])', response.replace('\n', ''))
            if json_match:
                courses = json.loads(json_match.group(1))
            else:
                courses = []

            # Update cache
            for course in courses:
                course_code = course.get("course_code")
                if course_code:
                    self.course_cache[course_code] = course

        except Exception as e:
            print(f"Error parsing course data: {e}")
            courses = []

        return courses

    def search_courses(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Search for courses by term

        Args:
            search_term (str): Term to search for

        Returns:
            List[Dict[str, Any]]: List of matching courses
        """
        all_courses = self.get_all_courses()
        search_term = search_term.lower()

        # Filter courses by search term
        matching_courses = [
            course for course in all_courses
            if search_term in course.get("course_title", "").lower() or
               search_term in course.get("course_description", "").lower() or
               search_term in course.get("course_code", "").lower()
        ]

        return matching_courses

    def get_courses_by_department(self, department: str) -> List[Dict[str, Any]]:
        """
        Get courses by department

        Args:
            department (str): Department name

        Returns:
            List[Dict[str, Any]]: List of courses in the department
        """
        all_courses = self.get_all_courses()
        department = department.lower()

        # Filter courses by department
        matching_courses = [
            course for course in all_courses
            if department in course.get("department", "").lower()
        ]

        return matching_courses

    def get_courses_by_skill(self, skill: str) -> List[Dict[str, Any]]:
        """
        Get courses that teach a specific skill

        Args:
            skill (str): Skill name

        Returns:
            List[Dict[str, Any]]: List of courses teaching the skill
        """
        all_courses = self.get_all_courses()
        courses_with_skills = []
        skill = skill.lower()

        for course in all_courses:
            # Extract skills for this course
            course_skills = self.extract_skills_from_course(course)

            # Check if the target skill is among them
            for course_skill in course_skills:
                if skill in course_skill.lower():
                    courses_with_skills.append(course)
                    break

        return courses_with_skills

    def extract_skills_from_course(self, course: Dict[str, Any]) -> List[str]:
        """
        Extract skills taught in a course

        Args:
            course (Dict[str, Any]): Course information

        Returns:
            List[str]: List of skills taught in the course
        """
        course_description = course.get("course_description", "")
        course_title = course.get("course_title", "")

        prompt = f"""
        You are a curriculum analysis expert. Extract a list of specific skills and competencies
        that students would learn from this course:
        
        Course: {course_title}
        Description: {course_description}
        
        Return only a JSON array of skill strings, with no additional text.
        """

        response = self.get_llm_response(prompt)

        # Parse the JSON response
        try:
            # Extract JSON from the response
            json_match = re.search(r'(\[.*\])', response.replace('\n', ''))
            if json_match:
                skills = json.loads(json_match.group(1))
            else:
                skills = []
        except Exception as e:
            print(f"Error parsing skills for course {course_title}: {e}")
            skills = []

        return skills

    def extract_course_skills(self, courses: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """
        Extract skills from a list of courses

        Args:
            courses (List[Dict[str, Any]]): List of courses

        Returns:
            Dict[str, List[str]]: Dictionary mapping course codes to skills
        """
        course_skills = {}

        for course in courses:
            course_code = course.get("course_code")
            if course_code:
                skills = self.extract_skills_from_course(course)
                course_skills[course_code] = skills

        return course_skills

    def map_course_relationships(self, courses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Map relationships between courses

        Args:
            courses (List[Dict[str, Any]]): List of courses

        Returns:
            List[Dict[str, Any]]: List of course relationships
        """
        relationships = []

        # Extract prerequisites
        for course in courses:
            course_code = course.get("course_code")
            prerequisites = course.get("prerequisites", "")

            if not prerequisites or not course_code:
                continue

            # Extract course codes from prerequisites
            prereq_codes = re.findall(r'([A-Z]{2,4}\s+\d{4}[A-Z]*)', prerequisites)

            for prereq_code in prereq_codes:
                relationships.append({
                    "course": course_code,
                    "prerequisite": prereq_code.strip(),
                    "type": "prerequisite"
                })

        # Add skill-based relationships
        course_skills = self.extract_course_skills(courses)

        for i, course1 in enumerate(courses):
            code1 = course1.get("course_code")
            if not code1 or code1 not in course_skills:
                continue

            skills1 = set(course_skills[code1])

            for j, course2 in enumerate(courses[i+1:], i+1):
                code2 = course2.get("course_code")
                if not code2 or code2 not in course_skills:
                    continue

                skills2 = set(course_skills[code2])

                # Find common skills
                common_skills = skills1.intersection(skills2)

                if len(common_skills) > 2:  # At least 3 skills in common
                    relationships.append({
                        "course1": code1,
                        "course2": code2,
                        "common_skills": list(common_skills),
                        "type": "related"
                    })

        return relationships

    def get_capabilities(self) -> List[str]:
        """
        Get the capabilities of this agent

        Returns:
            List[str]: List of capability descriptions
        """
        return [
            "Gather UTD course descriptions and prerequisites",
            "Analyze course content to extract taught skills",
            "Search courses by term, department, or skill",
            "Map relationships between different courses"
        ]
