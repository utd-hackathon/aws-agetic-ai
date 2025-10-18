import requests
from typing import Dict, Any, List
from bs4 import BeautifulSoup
from src.agents.base_agent import BaseAgent
import json
import re
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class JobMarketAgent(BaseAgent):
    """
    Agent responsible for scraping job postings and extracting skills,
    requirements, and salary information from job sites.
    """

    def __init__(self):
        """Initialize the Job Market Agent"""
        super().__init__(
            name="Job Market Agent",
            description="Scrapes and analyzes job postings to extract skills, requirements, and trends"
        )
        self.job_sites = {
            "linkedin": {
                "base_url": "https://www.linkedin.com/jobs/search",
                "api_key": os.getenv("LINKEDIN_API_KEY")
            },
            "indeed": {
                "base_url": "https://www.indeed.com/jobs",
                "api_key": os.getenv("INDEED_API_KEY")
            },
            "glassdoor": {
                "base_url": "https://www.glassdoor.com/Job",
                "api_key": os.getenv("GLASSDOOR_API_KEY")
            }
        }

    def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a job market data request

        Args:
            request (Dict[str, Any]): Request with job title and location

        Returns:
            Dict[str, Any]: Job market data
        """
        job_title = request.get("job_title", "")
        location = request.get("location", "")
        limit = request.get("limit", 10)

        if not job_title:
            return {"error": "Job title is required"}

        # Scrape job postings
        job_postings = self.scrape_job_postings(job_title, location, limit)

        # Extract skills and requirements
        skills_data = self.extract_skills(job_postings)

        # Extract salary information
        salary_data = self.extract_salary_info(job_postings)

        # Identify trends
        trends = self.identify_trends(skills_data)

        return {
            "job_title": job_title,
            "location": location,
            "job_count": len(job_postings),
            "skills": skills_data,
            "salaries": salary_data,
            "trends": trends
        }

    def scrape_job_postings(self, job_title: str, location: str = "", limit: int = 10) -> List[Dict[str, Any]]:
        """
        Scrape job postings from various job sites

        Args:
            job_title (str): Job title to search for
            location (str): Location to search in
            limit (int): Maximum number of postings to retrieve

        Returns:
            List[Dict[str, Any]]: List of job postings
        """
        # In a real implementation, this would use Selenium or a similar tool
        # to scrape actual job listings. For demonstration, we'll simulate with LLM.

        prompt = f"""
        You are a job market data expert. Generate {limit} realistic job postings for the job title 
        "{job_title}" in {location if location else 'any location'}. Include:
        
        1. Job title
        2. Company name
        3. Location
        4. Job description (with required skills and qualifications)
        5. Salary range (if available)
        
        Format your response as a JSON array of objects with the fields above.
        """

        response = self.get_llm_response(prompt)

        # Parse the JSON response
        try:
            # Extract JSON from the response (handling possible text before/after JSON)
            json_match = re.search(r'(\[.*\])', response.replace('\n', ''))
            if json_match:
                job_postings = json.loads(json_match.group(1))
            else:
                job_postings = []
        except Exception as e:
            print(f"Error parsing job postings: {e}")
            job_postings = []

        return job_postings

    def extract_skills(self, job_postings: List[Dict[str, Any]]) -> Dict[str, int]:
        """
        Extract skills from job postings

        Args:
            job_postings (List[Dict[str, Any]]): List of job postings

        Returns:
            Dict[str, int]: Dictionary of skills with counts
        """
        all_job_descriptions = "\n\n".join(posting.get("job_description", "") for posting in job_postings)

        prompt = f"""
        You are a skills extraction expert. Extract all technical and non-technical skills 
        from the following job descriptions. Return the results as a JSON object where the keys
        are the skills and the values are the count of how many times each skill appears.
        
        Job Descriptions:
        {all_job_descriptions[:4000]}  # Limiting to 4000 chars to avoid token limits
        """

        response = self.get_llm_response(prompt)

        # Parse the JSON response
        try:
            # Extract JSON from the response
            json_match = re.search(r'(\{.*\})', response.replace('\n', ''))
            if json_match:
                skills_data = json.loads(json_match.group(1))
            else:
                skills_data = {}
        except Exception as e:
            print(f"Error parsing skills data: {e}")
            skills_data = {}

        return skills_data

    def extract_salary_info(self, job_postings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Extract salary information from job postings

        Args:
            job_postings (List[Dict[str, Any]]): List of job postings

        Returns:
            Dict[str, Any]: Salary statistics
        """
        salaries = []

        for posting in job_postings:
            salary_range = posting.get("salary_range", "")
            if not salary_range:
                continue

            # Extract numeric values from salary strings (e.g. "$60,000 - $80,000")
            values = re.findall(r'[\$£€]?([0-9,.]+)[kK]?', salary_range)

            if len(values) >= 2:
                try:
                    min_val = float(values[0].replace(",", ""))
                    max_val = float(values[1].replace(",", ""))

                    # Check if salary is in thousands
                    if "k" in salary_range.lower():
                        min_val *= 1000
                        max_val *= 1000

                    salaries.append({"min": min_val, "max": max_val})
                except ValueError:
                    pass

        if not salaries:
            return {"count": 0, "average_min": 0, "average_max": 0, "overall_average": 0}

        # Calculate statistics
        avg_min = sum(s["min"] for s in salaries) / len(salaries)
        avg_max = sum(s["max"] for s in salaries) / len(salaries)
        overall_avg = (avg_min + avg_max) / 2

        return {
            "count": len(salaries),
            "average_min": avg_min,
            "average_max": avg_max,
            "overall_average": overall_avg
        }

    def identify_trends(self, skills_data: Dict[str, int]) -> List[Dict[str, Any]]:
        """
        Identify trends in skills data

        Args:
            skills_data (Dict[str, int]): Dictionary of skills with counts

        Returns:
            List[Dict[str, Any]]: List of trending skills with scores
        """
        # Sort skills by count
        sorted_skills = sorted(skills_data.items(), key=lambda x: x[1], reverse=True)

        # Return top skills as trends
        trends = [
            {"skill": skill, "count": count, "score": min(10, count)}
            for skill, count in sorted_skills[:10]
        ]

        return trends

    def get_capabilities(self) -> List[str]:
        """
        Get the capabilities of this agent

        Returns:
            List[str]: List of capability descriptions
        """
        return [
            "Scrape job postings from LinkedIn, Indeed, and Glassdoor",
            "Extract skills and requirements from job descriptions",
            "Extract salary information from job postings",
            "Identify trending skills by job title and location"
        ]
