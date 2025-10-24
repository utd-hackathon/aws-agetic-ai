import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import { GraduationCap, Brain, Target } from 'lucide-react'

const Header: React.FC = () => {
  const location = useLocation()

  return (
    <header className="bg-white shadow-sm border-b border-secondary-200">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Link to="/" className="flex items-center space-x-3">
            <div className="flex items-center space-x-2">
              <GraduationCap className="h-8 w-8 text-primary-600" />
              <div>
                <h1 className="text-xl font-bold text-secondary-900">
                  UTD Career Guidance AI
                </h1>
                <p className="text-sm text-secondary-600">
                  Autonomous AI Career Advisor
                </p>
              </div>
            </div>
          </Link>

          <nav className="flex items-center space-x-6">
            <Link
              to="/"
              className={`flex items-center space-x-2 px-3 py-2 rounded-lg transition-colors ${
                location.pathname === '/'
                  ? 'bg-primary-100 text-primary-700'
                  : 'text-secondary-600 hover:text-primary-600 hover:bg-primary-50'
              }`}
            >
              <Brain className="h-4 w-4" />
              <span>Career Guidance</span>
            </Link>
            
            <Link
              to="/results"
              className={`flex items-center space-x-2 px-3 py-2 rounded-lg transition-colors ${
                location.pathname === '/results'
                  ? 'bg-primary-100 text-primary-700'
                  : 'text-secondary-600 hover:text-primary-600 hover:bg-primary-50'
              }`}
            >
              <Target className="h-4 w-4" />
              <span>My Results</span>
            </Link>
          </nav>
        </div>
      </div>
    </header>
  )
}

export default Header
