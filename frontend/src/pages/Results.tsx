import React from 'react'
import { useCareerGuidance } from '../context/CareerGuidanceContext'
import { ArrowLeft, TrendingUp, BookOpen, Target, Briefcase, Lightbulb } from 'lucide-react'
import { Link } from 'react-router-dom'
import JobMarketInsights from '../components/JobMarketInsights'
import CourseRecommendations from '../components/CourseRecommendations'
import ProjectRecommendations from '../components/ProjectRecommendations'
import LearningPath from '../components/LearningPath'
import SkillAnalysis from '../components/SkillAnalysis'
import LoadingSpinner from '../components/LoadingSpinner'
import ErrorMessage from '../components/ErrorMessage'

const Results: React.FC = () => {
  const { userProfile, guidanceResult, loading, error } = useCareerGuidance()

  if (loading) {
    return <LoadingSpinner message="Analyzing your career path..." />
  }

  if (error) {
    return (
      <div className="max-w-4xl mx-auto">
        <ErrorMessage message={error} />
        <Link to="/" className="btn-primary inline-flex items-center">
          <ArrowLeft className="h-4 w-4 mr-2" />
          Try Again
        </Link>
      </div>
    )
  }

  if (!guidanceResult || !userProfile) {
    return (
      <div className="max-w-4xl mx-auto text-center">
        <h2 className="text-2xl font-bold text-secondary-900 mb-4">No Results Found</h2>
        <p className="text-secondary-600 mb-6">
          It looks like you haven't gotten career guidance yet.
        </p>
        <Link to="/" className="btn-primary inline-flex items-center">
          <ArrowLeft className="h-4 w-4 mr-2" />
          Get Career Guidance
        </Link>
      </div>
    )
  }

  return (
    <div className="max-w-6xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <Link to="/" className="inline-flex items-center text-primary-600 hover:text-primary-700 mb-4">
          <ArrowLeft className="h-4 w-4 mr-2" />
          Back to Home
        </Link>
        
        <div className="bg-gradient-to-r from-primary-600 to-primary-700 rounded-xl p-8 text-white">
          <h1 className="text-3xl font-bold mb-2">
            Your Career Guidance for {guidanceResult.career_goal}
          </h1>
          <p className="text-primary-100 text-lg">
            {guidanceResult.location} • {userProfile.academic_year} • {userProfile.skill_level}
          </p>
          {guidanceResult.quick_start && (
            <div className="mt-4 inline-flex items-center px-3 py-1 bg-primary-500 rounded-full text-sm">
              <Lightbulb className="h-4 w-4 mr-2" />
              Quick Start Results
            </div>
          )}
        </div>
      </div>

      {/* Job Market Insights */}
      <section className="mb-8">
        <div className="flex items-center mb-4">
          <TrendingUp className="h-6 w-6 text-primary-600 mr-3" />
          <h2 className="text-2xl font-bold text-secondary-900">Job Market Insights</h2>
        </div>
        <JobMarketInsights 
          jobInsights={guidanceResult.job_insights}
          marketInsights={guidanceResult.market_insights}
        />
      </section>

      {/* Skill Analysis */}
      <section className="mb-8">
        <div className="flex items-center mb-4">
          <Target className="h-6 w-6 text-primary-600 mr-3" />
          <h2 className="text-2xl font-bold text-secondary-900">Skill Analysis</h2>
        </div>
        <SkillAnalysis skillAnalysis={guidanceResult.skill_analysis} />
      </section>

      {/* Course Recommendations */}
      <section className="mb-8">
        <div className="flex items-center mb-4">
          <BookOpen className="h-6 w-6 text-primary-600 mr-3" />
          <h2 className="text-2xl font-bold text-secondary-900">Course Recommendations</h2>
        </div>
        <CourseRecommendations 
          courses={guidanceResult.course_recommendations}
          curriculumComparison={guidanceResult.curriculum_comparison}
        />
      </section>

      {/* Learning Path */}
      <section className="mb-8">
        <div className="flex items-center mb-4">
          <Briefcase className="h-6 w-6 text-primary-600 mr-3" />
          <h2 className="text-2xl font-bold text-secondary-900">Learning Path</h2>
        </div>
        <LearningPath learningPath={guidanceResult.learning_path} />
      </section>

      {/* Project Recommendations */}
      {guidanceResult.projects && guidanceResult.projects.length > 0 && (
        <section className="mb-8">
          <div className="flex items-center mb-4">
            <Lightbulb className="h-6 w-6 text-primary-600 mr-3" />
            <h2 className="text-2xl font-bold text-secondary-900">Project Ideas</h2>
          </div>
          <ProjectRecommendations projects={guidanceResult.projects} />
        </section>
      )}

      {/* Summary */}
      {guidanceResult.summary && (
        <section className="mb-8">
          <div className="card">
            <h3 className="text-xl font-semibold text-secondary-900 mb-4">Summary</h3>
            <div className="space-y-2">
              <p className="text-secondary-700">
                <strong>Total Courses Recommended:</strong> {guidanceResult.summary.total_courses_recommended}
              </p>
              <p className="text-secondary-700">
                <strong>Estimated Completion:</strong> {guidanceResult.summary.estimated_completion}
              </p>
              {guidanceResult.summary.next_steps && (
                <div>
                  <strong className="text-secondary-700">Next Steps:</strong>
                  <ul className="list-disc list-inside mt-2 space-y-1">
                    {guidanceResult.summary.next_steps.map((step: string, index: number) => (
                      <li key={index} className="text-secondary-600">{step}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        </section>
      )}
    </div>
  )
}

export default Results
