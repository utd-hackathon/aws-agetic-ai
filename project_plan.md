# UTD Career Advisory AI System - Project Plan

## Project Overview
Building an agentic AI system to help UTD students make informed career decisions by connecting:
1. Job Market Data - Current employer requirements
2. UTD Course Catalog - Available courses and skills taught
3. Career Planning - Bridging education and employment

## System Architecture

### Agent Structure
1. **Job Market Agent**
   - Scrapes job postings from LinkedIn, Indeed, Glassdoor
   - Extracts skills, requirements, and salary information
   - Identifies trending skills by location

2. **Course Catalog Agent**
   - Gathers UTD course descriptions and prerequisites
   - Analyzes course content to extract taught skills
   - Maps relationships between courses and programs

3. **Career Matching Agent**
   - Coordinates with other agents
   - Analyzes job requirements vs. available coursework
   - Generates personalized course recommendations

4. **Project Advisor Agent**
   - Suggests projects to bridge coursework to job requirements
   - Recommends technologies and frameworks
   - Provides portfolio development guidance

### Agent Collaboration Flow
When a student asks "I want to become a data scientist":
1. Career Matching Agent receives the request
2. Job Market Agent scrapes current data scientist job postings
3. Course Catalog Agent analyzes relevant UTD courses
4. Project Advisor Agent suggests practical projects
5. All agents coordinate for a comprehensive response

## Technical Implementation
Using AWS Bedrock Agents to build autonomous systems that:
- Perform web scraping and data collection
- Process and analyze text data from job postings and course catalogs
- Make connections between market needs and educational offerings
- Provide conversational interfaces for students

## Development Plan

### Phase 1: Foundation Setup
- Set up AWS environment
- Configure AWS Bedrock
- Create basic agent frameworks

### Phase 2: Individual Agent Development
- Build and test Job Market Agent
  - Implement web scraping functionality
  - Create data extraction and analysis capabilities
- Build and test Course Catalog Agent
  - Create UTD course catalog database/access
  - Develop skill extraction algorithms
- Build and test Career Matching Agent
  - Develop matching algorithms
  - Create recommendation system
- Build and test Project Advisor Agent
  - Create project suggestion database
  - Develop context-aware recommendation logic

### Phase 3: Agent Integration
- Develop inter-agent communication protocols
- Implement orchestration logic
- Create unified API for frontend interaction

### Phase 4: User Interface
- Develop conversational interface
- Create dashboard for visualizing recommendations
- Implement user feedback mechanisms

### Phase 5: Testing and Refinement
- Conduct end-to-end system testing
- Gather user feedback
- Refine agent behavior and recommendations

## Success Criteria
- Autonomous agents working together without human intervention
- Relevant UTD course suggestions based on real job market analysis
- Clear agent specialization and coordination
- Agents can gather and process information independently
- System provides valuable career guidance to UTD students
