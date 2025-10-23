# 🎓 UTD Career Guidance AI System

An intelligent, autonomous AI career guidance system that helps UTD students plan their academic journey based on career goals, real-time job market data, and available coursework.

## 🚀 Quick Start

```bash
# 1. Install dependencies
cd aws-agetic-ai
pip install -r requirements.txt

# 2. Start the server
python start_server.py

# 3. Test the system
python test_system.py
```

**Server**: http://127.0.0.1:8000  
**API Docs**: http://127.0.0.1:8000/docs

## ✨ Features

### Core Capabilities

✅ **Career-Specific Course Recommendations**
- Analyzes career goals and recommends relevant UTD courses
- Provides personalized explanations for each recommendation
- Supports 12+ career paths (Financial Analyst, Data Scientist, Neuroscientist, etc.)
- Generates semester-by-semester learning paths

✅ **Real-Time Job Market Intelligence**
- LinkedIn job data scraping (Selenium-based)
- Skills analysis and trending skills identification
- Salary insights and market trends
- Location-based job availability

✅ **Comprehensive Course Catalog**
- 70 UTD courses across 18 departments
- Intelligent course search and filtering
- Prerequisite tracking
- Skills-based matching

✅ **Intelligent Fallback Systems**
- Works without AWS Bedrock credentials
- Works without LinkedIn credentials
- Optimized for speed and reliability

## 📊 System Architecture

```
FastAPI Application (API Layer)
        ↓
Agent Orchestrator (Coordinator)
        ↓
   ┌────┴────┬───────┐
   ↓         ↓       ↓
Career    Job     Course
Matching  Market  Catalog
Agent     Agent   Agent
   ↓
LinkedIn Scraper + Mock Data
```

## 📁 Project Structure

```
aws-agetic-ai/
├── src/
│   ├── agents/              # AI Agents
│   │   ├── career_matching_agent/
│   │   ├── job_market_agent/
│   │   ├── course_catalog_agent/
│   │   └── orchestrator.py
│   ├── api/app.py          # FastAPI application
│   ├── auth/               # LinkedIn authentication
│   ├── config/             # Configuration
│   ├── core/
│   │   ├── aws/            # AWS Bedrock integration
│   │   └── llm/            # LLM recommendation service
│   └── scrapers/           # Web scrapers
├── data/
│   ├── utd_courses.json    # 70 UTD courses
│   └── job_cache/          # Cached job data
├── start_server.py         # Server startup
├── test_system.py          # System test
├── SETUP.md               # Detailed setup
└── PROJECT_SUMMARY.md     # Technical summary
```

## 🔌 API Endpoints

### Primary Endpoint

**POST /api/career-guidance**
```json
{
  "query": "I want to become a Data Scientist",
  "location": "Dallas, TX"
}
```

**Response includes:**
- Career goal analysis
- Job market insights (skills, salaries, trending skills)
- Personalized course recommendations with explanations
- Semester-by-semester learning path
- Estimated completion time

### Additional Endpoints

- **POST /job-market** - Job market analysis
- **POST /course-search** - Search UTD courses
- **GET /health** - System health check
- **GET /docs** - Interactive API documentation

## 💡 Example Usage

### Career Guidance Request

```python
import requests

response = requests.post(
    "http://127.0.0.1:8000/api/career-guidance",
    json={
        "query": "I want to become a Financial Analyst",
        "location": "Dallas, TX"
    }
)

data = response.json()
print(f"Recommended Courses: {len(data['course_recommendations'])}")
print(f"Job Market Insights: {data['job_market_analysis']}")
print(f"Learning Path: {data['learning_path']}")
```

### Example Output

For "Financial Analyst":
1. **STAT 4351**: Probability and Statistics (High Priority)
2. **FIN 3320**: Business Finance (High Priority)
3. **ACCT 2301**: Introduction to Financial Accounting (High Priority)
4. **ECON 2301**: Principles of Macroeconomics (High Priority)

**Job Market**: 2 jobs, $95K avg salary, trending skills: Financial Analysis, Excel, Financial Modeling

## 🎯 Supported Career Paths

- Financial Analyst, Investment Analyst
- Data Scientist, Data Engineer
- Software Engineer, DevOps Engineer
- Neuroscientist, Behavioral Neuroscientist
- Marketing Analyst, Business Analyst
- Operations Manager, Management Consultant
- And more...

## 📚 Course Database

**Total**: 70 courses  
**Departments**: 18 (CS, FIN, ACCT, ECON, BA, NSC, BIOL, PSYC, CHEM, PHYS, MATH, STAT, etc.)

### Course Categories:
- **Computer Science**: 21 courses
- **Business & Finance**: 23 courses (FIN, ACCT, ECON, BA, MGMT, MKTG, MIS, OPRE)
- **Neuroscience & Psychology**: 9 courses (NSC, PSYC)
- **Biology & Chemistry**: 5 courses
- **Mathematics & Statistics**: 8 courses
- **Engineering & Systems**: 4 courses

## ⚙️ Configuration (Optional)

Create a `.env` file for optional features:

```env
# AWS Bedrock (Optional - uses fallback if not provided)
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=us-east-1

# LinkedIn (Optional - uses mock data if not provided)
LINKEDIN_EMAIL=your_email
LINKEDIN_PASSWORD=your_password
```

**Note**: System works fully without these credentials using intelligent fallbacks.

## 🧪 Testing

```bash
# Quick system test
python test_system.py

# Manual API testing
curl http://127.0.0.1:8000/health
curl -X POST http://127.0.0.1:8000/api/career-guidance \
  -H "Content-Type: application/json" \
  -d '{"query": "I want to become a Data Scientist", "location": "Dallas, TX"}'
```

## 📖 Documentation

- **SETUP.md** - Detailed setup instructions
- **PROJECT_SUMMARY.md** - Technical architecture and implementation details
- **API Docs** - http://127.0.0.1:8000/docs (when server is running)

## 🔧 Technology Stack

- **Backend**: FastAPI, Python 3.11+
- **Web Scraping**: Selenium WebDriver
- **AI/LLM**: AWS Bedrock Claude Haiku (with intelligent fallback)
- **Data Storage**: JSON files (local development)
- **Authentication**: LinkedIn OAuth flow

## 📈 Performance

- **Career Recommendations**: < 1 second (with caching)
- **Job Market Analysis**: 2-5 seconds
- **Course Search**: < 100ms
- **Total Response Time**: ~1-3 seconds typical

## 🎓 Academic Context

This system was developed as part of the UTD Career Guidance AI Challenge, focusing on:
- Autonomous agentic AI architecture
- AWS Bedrock integration
- Real-time job market analysis
- Personalized academic path planning
- Student-centric career guidance

## 📝 License

See LICENSE file for details.

## 🤝 Contributing

This is an academic project. For questions or feedback, please refer to the project documentation.
