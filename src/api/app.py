from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uvicorn
from src.agents.orchestrator import AgentOrchestrator

# Initialize FastAPI app
app = FastAPI(
    title="UTD Career Advisory AI System",
    description="API for UTD Career Advisory AI System that helps students make informed career decisions",
    version="0.1.0"
)

# Initialize agent orchestrator
orchestrator = AgentOrchestrator()

# Define request models
class CareerAdviceRequest(BaseModel):
    career_goal: str
    location: Optional[str] = ""
    current_skills: Optional[List[str]] = []
    completed_courses: Optional[List[str]] = []
    experience_level: Optional[str] = "beginner"

class JobMarketRequest(BaseModel):
    job_title: str
    location: Optional[str] = ""
    limit: Optional[int] = 10

class CourseSearchRequest(BaseModel):
    search_term: Optional[str] = None
    department: Optional[str] = None
    skill: Optional[str] = None

class ProjectRequest(BaseModel):
    career_goal: str
    technical_skills: Optional[List[str]] = []
    target_skills: Optional[List[str]] = []
    courses: Optional[List[Dict[str, Any]]] = []
    experience_level: Optional[str] = "beginner"

# API endpoints
@app.get("/")
async def root():
    """Welcome to the UTD Career Advisory AI System API"""
    return {
        "message": "Welcome to the UTD Career Advisory AI System API",
        "version": "0.1.0",
        "endpoints": [
            "/career-advice",
            "/job-market",
            "/course-search",
            "/project-recommendations",
            "/agent-capabilities"
        ]
    }

@app.post("/career-advice")
async def get_career_advice(request: CareerAdviceRequest):
    """Get comprehensive career advice based on career goals"""
    try:
        orchestrator_request = {
            "request_type": "career_advice",
            **request.dict()
        }
        response = orchestrator.process_request(orchestrator_request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.post("/job-market")
async def get_job_market_analysis(request: JobMarketRequest):
    """Get job market analysis for a specific job title"""
    try:
        orchestrator_request = {
            "request_type": "job_market_analysis",
            **request.dict()
        }
        response = orchestrator.process_request(orchestrator_request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.post("/course-search")
async def search_courses(request: CourseSearchRequest):
    """Search for UTD courses by term, department, or skill"""
    try:
        if not request.search_term and not request.department and not request.skill:
            raise HTTPException(status_code=400, detail="At least one search parameter is required")

        orchestrator_request = {
            "request_type": "course_search",
            **request.dict()
        }
        response = orchestrator.process_request(orchestrator_request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.post("/project-recommendations")
async def get_project_recommendations(request: ProjectRequest):
    """Get project and technology recommendations based on career goals"""
    try:
        orchestrator_request = {
            "request_type": "project_recommendations",
            **request.dict()
        }
        response = orchestrator.process_request(orchestrator_request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.get("/agent-capabilities")
async def get_agent_capabilities():
    """Get capabilities of all agents in the system"""
    return orchestrator.get_agent_capabilities()

if __name__ == "__main__":
    uvicorn.run("api.app:app", host="0.0.0.0", port=8000, reload=True)
