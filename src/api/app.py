from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime
import uvicorn
from src.agents.orchestrator import AgentOrchestrator
from src.auth.linkedin_auth import require_linkedin_auth, linkedin_auth

# Initialize FastAPI app
app = FastAPI(
    title="UTD Career Guidance AI System",
    description="Autonomous agent system for data-driven career guidance",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agent orchestrator
orchestrator = AgentOrchestrator()

# Define request models
class CareerQueryRequest(BaseModel):
    query: str
    location: Optional[str] = "Dallas, TX"

class CareerQueryResponse(BaseModel):
    success: bool
    career_goal: Optional[str] = None
    job_market: Optional[Dict] = None
    course_recommendations: Optional[list] = None
    insights: Optional[Dict] = None
    next_steps: Optional[list] = None
    error: Optional[str] = None
    processing_time_seconds: Optional[float] = None

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
    """Welcome to the UTD Career Guidance AI System API"""
    return {
        "service": "UTD Career Guidance AI",
        "status": "operational",
        "version": "1.0.0",
        "linkedin_auth_required": True,
        "timestamp": datetime.utcnow().isoformat(),
        "endpoints": [
            "/auth/linkedin",
            "/auth/status", 
            "/auth/logout",
            "/api/career-guidance",
            "/career-advice",
            "/job-market",
            "/course-search",
            "/agent-capabilities",
            "/health",
            "/api/stats"
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "bedrock": "connected",
        "timestamp": datetime.utcnow().isoformat()
    }

# Authentication endpoints
@app.post("/auth/linkedin")
async def authenticate_linkedin():
    """Authenticate with LinkedIn - required before using the system"""
    try:
        success = await require_linkedin_auth()
        if success:
            return {
                "success": True,
                "message": "LinkedIn authentication successful",
                "status": "authenticated"
            }
        else:
            return {
                "success": False,
                "message": "LinkedIn authentication failed",
                "status": "not_authenticated"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Authentication error: {str(e)}")

@app.get("/auth/status")
async def get_auth_status():
    """Get current LinkedIn authentication status"""
    try:
        status = linkedin_auth.get_auth_status()
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Status check error: {str(e)}")

@app.post("/auth/logout")
async def logout_linkedin():
    """Logout and clear LinkedIn session"""
    try:
        success = linkedin_auth.logout()
        return {
            "success": success,
            "message": "LinkedIn session cleared" if success else "Logout failed"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Logout error: {str(e)}")

@app.post("/api/career-guidance", response_model=CareerQueryResponse)
async def get_career_guidance(request: CareerQueryRequest):
    """
    Main endpoint: Process career query and return guidance.
    Requires LinkedIn authentication for real job market data.
    
    Example request:
    {
        "query": "I want to become a data scientist",
        "location": "Dallas, TX"
    }
    """
    # Check LinkedIn authentication first
    if not linkedin_auth.is_authenticated():
        raise HTTPException(
            status_code=401, 
            detail="LinkedIn authentication required. Please authenticate first using /auth/linkedin"
        )
    
    start_time = datetime.utcnow()
    
    try:
        # Call orchestrator agent
        result = await orchestrator.process_request({
            "request_type": "career_advice",
            "career_goal": request.query,
            "location": request.location
        })
        
        # Calculate processing time
        end_time = datetime.utcnow()
        processing_time = (end_time - start_time).total_seconds()
        
        return CareerQueryResponse(
            success=True,
            career_goal=result.get('career_goal'),
            job_market=result.get('job_market_analysis'),
            course_recommendations=result.get('course_recommendations'),
            insights=result.get('learning_path'),
            next_steps=result.get('project_recommendations'),
            processing_time_seconds=round(processing_time, 2)
        )
        
    except Exception as e:
        print(f"Error processing query: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process career query: {str(e)}"
        )

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
    """Get job market analysis for a specific job title - requires LinkedIn authentication"""
    # Check LinkedIn authentication first
    if not linkedin_auth.is_authenticated():
        raise HTTPException(
            status_code=401, 
            detail="LinkedIn authentication required for real job market data. Please authenticate first using /auth/linkedin"
        )
    
    try:
        orchestrator_request = {
            "request_type": "job_market_analysis",
            **request.dict()
        }
        response = await orchestrator.process_request(orchestrator_request)
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
        response = await orchestrator.process_request(orchestrator_request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.get("/api/agents/status")
async def get_agent_status():
    """Check status of all agents"""
    return {
        "career_matching_agent": "operational",
        "job_market_agent": "operational", 
        "course_catalog_agent": "operational",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/api/stats")
async def get_system_stats():
    """Get system statistics for demo"""
    # In production, fetch from DynamoDB
    return {
        "total_queries_processed": 0,
        "total_jobs_scraped": 0,
        "total_courses_analyzed": 0,
        "avg_response_time_seconds": 0,
        "last_job_scrape": None,
        "last_catalog_update": None
    }

@app.get("/agent-capabilities")
async def get_agent_capabilities():
    """Get capabilities of all agents in the system"""
    return orchestrator.get_agent_capabilities()

if __name__ == "__main__":
    uvicorn.run("api.app:app", host="0.0.0.0", port=8000, reload=True)
