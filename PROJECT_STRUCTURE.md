# Project Structure

```
aws-agetic-ai/
├── README.md                          # Main documentation
├── requirements.txt                   # Python dependencies
├── start_server.py                   # Server startup script
├── LICENSE                           # MIT License
│
├── src/                              # Source code
│   ├── agents/                       # AI Agents
│   │   ├── base_agent.py            # Base agent class
│   │   ├── orchestrator.py          # Agent orchestrator
│   │   ├── career_matching_agent/   # Career matching logic
│   │   │   └── career_matching_agent.py
│   │   ├── job_market_agent/         # Job market analysis
│   │   │   └── job_market_agent.py
│   │   ├── course_catalog_agent/    # Course catalog management
│   │   │   └── course_catalog_agent.py
│   │   └── project_advisor_agent/   # Project recommendations
│   │       └── project_advisor_agent.py
│   │
│   ├── api/                         # API layer
│   │   ├── app.py                   # FastAPI application
│   │   └── user_onboarding.py       # User onboarding models
│   │
│   ├── auth/                        # Authentication
│   │   ├── __init__.py
│   │   └── linkedin_auth.py         # LinkedIn authentication
│   │
│   ├── config/                      # Configuration
│   │   └── config.py                # AWS and system config
│   │
│   ├── core/                        # Core services
│   │   ├── aws/
│   │   │   └── bedrock_service.py   # AWS Bedrock integration
│   │   └── llm/
│   │       └── career_llm_service.py # LLM service for career guidance
│   │
│   └── scrapers/                    # Web scrapers
│       ├── __init__.py
│       ├── utd_course_selenium.py   # UTD course scraper
│       └── linkedin_selenium_scraper.py # LinkedIn job scraper
│
├── frontend/                        # React frontend
│   ├── package.json                 # Node.js dependencies
│   ├── vite.config.ts              # Vite configuration
│   ├── tailwind.config.js          # TailwindCSS config
│   ├── tsconfig.json               # TypeScript config
│   └── src/
│       ├── App.tsx                  # Main app component
│       ├── main.tsx                # Entry point
│       ├── components/             # React components
│       │   ├── Header.tsx
│       │   ├── QuickStartForm.tsx
│       │   ├── ComprehensiveForm.tsx
│       │   ├── Results.tsx
│       │   ├── CourseCard.tsx
│       │   ├── JobInsights.tsx
│       │   ├── ProjectCard.tsx
│       │   ├── LoadingSpinner.tsx
│       │   ├── ErrorMessage.tsx
│       │   └── SkillAnalysis.tsx
│       ├── pages/                   # Page components
│       │   ├── Home.tsx
│       │   └── Results.tsx
│       ├── context/                # React context
│       │   └── CareerGuidanceContext.tsx
│       └── services/                # API services
│           └── api.ts
│
├── data/                           # Data storage
│   ├── utd_courses.json           # UTD course database (2,470+ courses)
│   ├── linkedin_session.json     # LinkedIn session data
│   └── job_cache/                # Cached job data (auto-generated)
│
└── docs/                          # Documentation (if needed)
    └── API.md                     # API documentation
```

## Key Components

### Backend Architecture
- **FastAPI**: Modern, fast web framework for building APIs
- **AWS Bedrock**: LLM integration with Claude 3.5 Sonnet
- **Selenium**: Web scraping for LinkedIn and UTD courses
- **Pydantic**: Data validation and serialization

### Frontend Architecture
- **React 18**: Modern React with hooks and context
- **TypeScript**: Type-safe JavaScript
- **TailwindCSS**: Utility-first CSS framework
- **Vite**: Fast build tool and dev server

### AI Agents
1. **Career Matching Agent**: Orchestrates all other agents
2. **Job Market Intelligence Agent**: LinkedIn scraping and analysis
3. **Course Catalog Agent**: UTD course database management
4. **Project Advisor Agent**: LLM-powered project recommendations

### Data Flow
1. User input → Frontend → API
2. API → Agent Orchestrator → Specialized Agents
3. Agents → AWS Bedrock → LLM Analysis
4. Results → Frontend → User Display

### Security & Performance
- **LinkedIn Authentication**: Secure session management
- **Anti-bot Measures**: Stealth scraping with delays
- **Caching**: Intelligent data caching
- **Error Handling**: Robust fallback systems
