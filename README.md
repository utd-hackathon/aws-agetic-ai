# UTD Career Advisory AI System

This project builds an agentic AI system to help UTD students make informed career decisions by connecting job market data, UTD course offerings, and career planning through autonomous agents built on AWS Bedrock.

## Project Structure

- `agents/`: Core agent implementations
  - `job_market_agent/`: Scrapes and analyzes job postings
  - `course_catalog_agent/`: Processes UTD course information
  - `career_matching_agent/`: Matches careers to courses
  - `project_advisor_agent/`: Recommends projects and skills

- `core/`: Shared functionality
  - `aws/`: AWS configuration and utilities
  - `data/`: Data models and database access
  - `utils/`: Utility functions

- `api/`: API interfaces for agent communication
- `ui/`: User interface components
- `scripts/`: Utility scripts for setup and maintenance
- `tests/`: Test cases

## Setup

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Configure AWS credentials (see `Configuration` section below)
4. Run the development server:
   ```
   python -m api.app
   ```

## Configuration

Create a `.env` file in the project root with the following variables:

```
# AWS Configuration
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1

# AWS Bedrock Configuration
BEDROCK_MODEL_ID=anthropic.claude-v2

# Database Configuration
MONGODB_URI=mongodb://localhost:27017
DATABASE_NAME=utd_career_advisor

# API Keys for Job Sites (as needed)
LINKEDIN_API_KEY=your_linkedin_api_key
INDEED_API_KEY=your_indeed_api_key
GLASSDOOR_API_KEY=your_glassdoor_api_key
```

## Development

See `project_plan.md` for detailed development phases and implementation strategy.
