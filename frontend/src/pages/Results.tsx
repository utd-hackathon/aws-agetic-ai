import React, { useState } from 'react'
import { useCareerGuidance } from '../context/CareerGuidanceContext'
import { useNavigate } from 'react-router-dom'
import CourseCard from '../components/ui/CourseCard'
import ProjectCard from '../components/ui/ProjectCard'
import { 
  ArrowLeft, 
  Download, 
  Share2, 
  BookOpen, 
  Briefcase, 
  Code, 
  TrendingUp,
  Target,
  Calendar,
  CheckCircle,
  Star
} from 'lucide-react'

const Results: React.FC = () => {
  const navigate = useNavigate()
  const { userProfile, guidanceResult } = useCareerGuidance()
  const [activeTab, setActiveTab] = useState<'overview' | 'courses' | 'jobs' | 'projects' | 'roadmap'>('overview')
  const [selectedCourses, setSelectedCourses] = useState<any[]>([])
  const [selectedProjects, setSelectedProjects] = useState<any[]>([])
  const [toast, setToast] = useState<{ message: string; type: 'success' | 'info' | 'error' } | null>(null)

  if (!guidanceResult || !userProfile) {
    return (
      <div className="max-w-4xl mx-auto text-center py-16">
        <div className="bg-warning-50 border border-warning-200 rounded-lg p-6">
          <h2 className="text-xl font-semibold text-warning-800 mb-2">No Results Found</h2>
          <p className="text-warning-700 mb-4">
            It looks like you haven't completed the career guidance process yet.
          </p>
          <button
            onClick={() => navigate('/')}
            className="btn-primary"
          >
            Start Career Guidance
          </button>
        </div>
      </div>
    )
  }

  // Helper function to get unique course identifier
  const getCourseId = (course: any): string => {
    return course.course_code || course.id || course.course_name || JSON.stringify(course)
  }

  // Helper function to check if course is in plan
  const isCourseInPlan = (course: any): boolean => {
    const courseId = getCourseId(course)
    return selectedCourses.some(c => getCourseId(c) === courseId)
  }

  const showToast = (message: string, type: 'success' | 'info' | 'error' = 'success') => {
    setToast({ message, type })
    setTimeout(() => setToast(null), 3000)
  }

  const handleCourseSelect = (course: any) => {
    console.log('Course clicked:', course)
    const courseId = getCourseId(course)
    console.log('Course ID:', courseId)
    const isAdding = !selectedCourses.find(c => getCourseId(c) === courseId)
    console.log('Is adding:', isAdding)
    console.log('Selected courses before:', selectedCourses.map(c => getCourseId(c)))
    
    setSelectedCourses(prev => {
      const found = prev.find(c => getCourseId(c) === courseId)
      
      if (found) {
        // Remove from selection
        return prev.filter(c => getCourseId(c) !== courseId)
      } else {
        // Add to selection
        return [...prev, course]
      }
    })
    
    if (isAdding) {
      showToast(`✓ ${course.title || course.course_name} added to your plan!`)
    }
  }

  const handleProjectSelect = (project: any) => {
    const isAdding = !selectedProjects.find(p => p.title === project.title)
    setSelectedProjects(prev => 
      prev.find(p => p.title === project.title)
        ? prev.filter(p => p.title !== project.title)
        : [...prev, project]
    )
    if (isAdding) {
      showToast(`✓ ${project.title} added to your roadmap!`)
    }
  }

  const handleShare = async () => {
    const shareData = {
      title: 'My Career Roadmap - UTD Career Guidance',
      text: `My personalized career roadmap for ${guidanceResult.career_goal}`,
      url: window.location.href
    }

    try {
      if (navigator.share) {
        await navigator.share(shareData)
        showToast('✓ Shared successfully!')
      } else {
        // Fallback: Copy link to clipboard
        await navigator.clipboard.writeText(window.location.href)
        showToast('✓ Link copied to clipboard!', 'info')
      }
    } catch (error) {
      if ((error as Error).name !== 'AbortError') {
        console.error('Error sharing:', error)
        showToast('Failed to share. Please try again.', 'error')
      }
    }
  }

  const handleExportPDF = () => {
    // Create a simple text summary for now
    const summary = `
=== UTD Career Guidance Report ===
Career Goal: ${guidanceResult.career_goal}
Location: ${guidanceResult.location}

=== Course Recommendations ===
${guidanceResult.course_recommendations?.map((course: any, index: number) => 
  `${index + 1}. ${course.title} (${course.course_code})
   Priority: ${course.priority}
   Skills: ${course.skills_addressed?.join(', ') || 'N/A'}
   Explanation: ${course.explanation}
`).join('\n') || 'No courses available'}

=== Project Recommendations ===
${guidanceResult.project_recommendations?.map((project: any, index: number) => 
  `${index + 1}. ${project.title}
   Difficulty: ${project.difficulty}
   Duration: ${project.duration_weeks} weeks
   Skills: ${project.skills_practiced?.join(', ') || 'N/A'}
`).join('\n') || 'No projects available'}

=== Learning Path ===
Total Semesters: ${guidanceResult.learning_path?.total_semesters || 'N/A'}
Total Credits: ${guidanceResult.learning_path?.total_credit_hours || 'N/A'}
Completion: ${guidanceResult.learning_path?.completion_timeline || 'N/A'}

Generated on: ${new Date().toLocaleDateString()}
    `.trim()

    // Create a blob and download
    const blob = new Blob([summary], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `career-roadmap-${guidanceResult.career_goal?.replace(/\s+/g, '-').toLowerCase()}.txt`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)
    
    showToast('✓ Report downloaded successfully!')
  }

  const tabs = [
    { id: 'overview', label: 'Overview', icon: Target },
    { id: 'courses', label: 'Courses', icon: BookOpen },
    { id: 'jobs', label: 'Job Market', icon: Briefcase },
    { id: 'projects', label: 'Projects', icon: Code },
    { id: 'roadmap', label: 'Roadmap', icon: Calendar }
  ]

  const renderOverview = () => (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-4xl font-bold text-secondary-900 mb-4">
          Your Career Roadmap
        </h1>
        <p className="text-xl text-secondary-600 mb-6">
          Personalized guidance for becoming a {guidanceResult.career_goal}
        </p>
        
        {/* Quick Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-2xl mx-auto">
          <div className="bg-primary-50 rounded-lg p-4">
            <div className="text-2xl font-bold text-primary-600">
              {guidanceResult.course_recommendations?.length || 0}
            </div>
            <div className="text-sm text-primary-700">Recommended Courses</div>
          </div>
          <div className="bg-blue-50 rounded-lg p-4">
            <div className="text-2xl font-bold text-blue-600">
              {guidanceResult.project_recommendations?.length || 0}
            </div>
            <div className="text-sm text-blue-700">Project Ideas</div>
          </div>
          <div className="bg-success-50 rounded-lg p-4">
            <div className="text-2xl font-bold text-success-600">
              {guidanceResult.skill_analysis?.current_coverage || '0%'}
            </div>
            <div className="text-sm text-success-700">Skill Coverage</div>
          </div>
          <div className="bg-warning-50 rounded-lg p-4">
            <div className="text-2xl font-bold text-warning-600">
              {guidanceResult.learning_path?.completion_timeline || 'N/A'}
            </div>
            <div className="text-sm text-warning-700">Est. Completion</div>
          </div>
        </div>
      </div>

      {/* Key Insights */}
      <div className="grid md:grid-cols-2 gap-8">
        {/* Skill Analysis */}
        <div className="card">
          <div className="flex items-center space-x-3 mb-4">
            <div className="w-10 h-10 bg-success-100 rounded-lg flex items-center justify-center">
              <TrendingUp className="h-5 w-5 text-success-600" />
            </div>
            <h3 className="text-lg font-semibold text-secondary-900">Skill Analysis</h3>
          </div>
          
          {guidanceResult.skill_analysis && (
            <div className="space-y-4">
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-secondary-600">Current Coverage</span>
                  <span className="font-medium">{guidanceResult.skill_analysis.current_coverage}</span>
                </div>
                <div className="progress-bar">
                  <div 
                    className="progress-fill"
                    style={{ width: `${parseFloat(guidanceResult.skill_analysis.current_coverage) || 0}%` }}
                  />
                </div>
              </div>
              
              <div>
                <h4 className="text-sm font-medium text-secondary-700 mb-2">Skills to Develop:</h4>
                <div className="flex flex-wrap gap-1">
                  {guidanceResult.skill_analysis.missing_skills?.slice(0, 5).map((skill: string, index: number) => (
                    <span key={index} className="badge-warning text-xs">
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Job Market Insights */}
        <div className="card">
          <div className="flex items-center space-x-3 mb-4">
            <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
              <Briefcase className="h-5 w-5 text-blue-600" />
            </div>
            <h3 className="text-lg font-semibold text-secondary-900">Job Market</h3>
          </div>
          
          {guidanceResult.job_insights && (
            <div className="space-y-3">
              {guidanceResult.job_insights.slice(0, 3).map((insight: string, index: number) => (
                <div key={index} className="flex items-start space-x-2">
                  <CheckCircle className="h-4 w-4 text-success-600 mt-0.5 flex-shrink-0" />
                  <span className="text-sm text-secondary-600">{insight}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Top Recommendations Preview */}
      <div className="space-y-6">
        <h3 className="text-2xl font-semibold text-secondary-900">Top Recommendations</h3>
        
        <div className="grid md:grid-cols-2 gap-6">
          {/* Top Course */}
          {guidanceResult.course_recommendations?.[0] && (
            <div>
              <h4 className="text-lg font-medium text-secondary-800 mb-3 flex items-center">
                <BookOpen className="h-5 w-5 mr-2 text-primary-600" />
                Priority Course
              </h4>
              <CourseCard
                course={guidanceResult.course_recommendations[0]}
                onAddToPlan={handleCourseSelect}
                isInPlan={guidanceResult.course_recommendations[0] ? isCourseInPlan(guidanceResult.course_recommendations[0]) : false}
                showActions={false}
              />
            </div>
          )}

          {/* Top Project */}
          {guidanceResult.project_recommendations?.[0] && (
            <div>
              <h4 className="text-lg font-medium text-secondary-800 mb-3 flex items-center">
                <Code className="h-5 w-5 mr-2 text-success-600" />
                Recommended Project
              </h4>
              <ProjectCard
                project={guidanceResult.project_recommendations[0]}
                onAddToRoadmap={handleProjectSelect}
                isInRoadmap={selectedProjects.some(p => p.title === guidanceResult.project_recommendations?.[0]?.title)}
              />
            </div>
          )}
        </div>
      </div>
    </div>
  )

  const renderCourses = () => (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-semibold text-secondary-900">Course Recommendations</h2>
        <div className="text-sm text-secondary-500">
          {selectedCourses.length} of {guidanceResult.course_recommendations?.length || 0} selected
        </div>
      </div>
      
      {guidanceResult.course_recommendations && guidanceResult.course_recommendations.length > 0 ? (
        <div className="grid gap-6">
          {guidanceResult.course_recommendations.map((course: any, index: number) => (
            <CourseCard
              key={index}
              course={course}
              isSelected={isCourseInPlan(course)}
              onAddToPlan={handleCourseSelect}
              isInPlan={isCourseInPlan(course)}
            />
          ))}
        </div>
      ) : (
        <div className="card text-center py-12">
          <div className="text-secondary-400 mb-4">
            <BookOpen className="h-16 w-16 mx-auto" />
          </div>
          <h3 className="text-lg font-medium text-secondary-700 mb-2">
            No Course Recommendations Available
          </h3>
          <p className="text-secondary-600">
            Course recommendations will be generated based on your career goals and skills.
          </p>
        </div>
      )}
    </div>
  )

  const renderJobs = () => (
    <div className="space-y-6">
      <h2 className="text-2xl font-semibold text-secondary-900">Job Market Insights</h2>
      
      {/* Market Summary */}
      {guidanceResult.market_insights && (
        <div className="card bg-gradient-to-r from-blue-50 to-primary-50">
          <h3 className="text-lg font-semibold text-secondary-900 mb-4">Market Summary</h3>
          <div className="grid md:grid-cols-3 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">
                {guidanceResult.market_insights.total_opportunities || 'N/A'}
              </div>
              <div className="text-sm text-blue-700">Available Jobs</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-success-600">
                ${guidanceResult.market_insights.salary_insights?.average?.toLocaleString() || 'N/A'}
              </div>
              <div className="text-sm text-success-700">Average Salary</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-primary-600">
                {guidanceResult.market_insights.market_health || 'Healthy'}
              </div>
              <div className="text-sm text-primary-700">Market Health</div>
            </div>
          </div>
          
          {/* Market Summary Text */}
          {guidanceResult.market_insights.market_summary && (
            <div className="mt-4 pt-4 border-t border-blue-100">
              <p className="text-sm text-secondary-700">{guidanceResult.market_insights.market_summary}</p>
            </div>
          )}
        </div>
      )}

      {/* Hot Skills */}
      {guidanceResult.market_insights?.hot_skills && guidanceResult.market_insights.hot_skills.length > 0 && (
        <div className="card">
          <h3 className="text-lg font-semibold text-secondary-900 mb-4">🔥 In-Demand Skills</h3>
          <div className="grid md:grid-cols-2 gap-4">
            {guidanceResult.market_insights.hot_skills.slice(0, 10).map((skillInfo: any, index: number) => (
              <div key={index} className="flex items-center justify-between p-3 bg-secondary-50 rounded-lg">
                <span className="font-medium text-secondary-900">{skillInfo.skill}</span>
                <span className="text-sm text-secondary-600">
                  {skillInfo.frequency} {skillInfo.frequency === 1 ? 'job' : 'jobs'}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Emerging vs Established Skills */}
      {(guidanceResult.market_insights?.emerging_skills || guidanceResult.market_insights?.established_skills) && (
        <div className="grid md:grid-cols-2 gap-6">
          {guidanceResult.market_insights.emerging_skills && guidanceResult.market_insights.emerging_skills.length > 0 && (
            <div className="card">
              <h3 className="text-lg font-semibold text-secondary-900 mb-4">🚀 Emerging Skills</h3>
              <div className="space-y-2">
                {guidanceResult.market_insights.emerging_skills.map((skill: string, index: number) => (
                  <div key={index} className="badge-success">
                    {skill}
                  </div>
                ))}
              </div>
            </div>
          )}
          
          {guidanceResult.market_insights.established_skills && guidanceResult.market_insights.established_skills.length > 0 && (
            <div className="card">
              <h3 className="text-lg font-semibold text-secondary-900 mb-4">📚 Established Skills</h3>
              <div className="space-y-2">
                {guidanceResult.market_insights.established_skills.map((skill: string, index: number) => (
                  <div key={index} className="badge-primary">
                    {skill}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )

  const renderProjects = () => (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-semibold text-secondary-900">Project Recommendations</h2>
        <div className="text-sm text-secondary-500">
          {selectedProjects.length} of {guidanceResult.project_recommendations?.length || 0} selected
        </div>
      </div>
      
      {guidanceResult.project_recommendations && guidanceResult.project_recommendations.length > 0 ? (
        <div className="grid gap-6">
          {guidanceResult.project_recommendations.map((project: any, index: number) => (
            <ProjectCard
              key={index}
              project={project}
              onAddToRoadmap={handleProjectSelect}
              isInRoadmap={selectedProjects.some(p => p.title === project.title)}
            />
          ))}
        </div>
      ) : (
        <div className="card text-center py-12">
          <div className="text-secondary-400 mb-4">
            <Code className="h-16 w-16 mx-auto" />
          </div>
          <h3 className="text-lg font-medium text-secondary-700 mb-2">
            No Project Recommendations Yet
          </h3>
          <p className="text-secondary-600">
            Project recommendations will be generated based on your course selections and career goals.
          </p>
        </div>
      )}
    </div>
  )

  const renderRoadmap = () => (
    <div className="space-y-6">
      <h2 className="text-2xl font-semibold text-secondary-900">Learning Roadmap</h2>
      
      {guidanceResult.learning_path && (
        <div className="space-y-6">
          {/* Timeline Overview */}
          <div className="card bg-gradient-to-r from-primary-50 to-success-50">
            <h3 className="text-lg font-semibold text-secondary-900 mb-4">Timeline Overview</h3>
            <div className="grid md:grid-cols-3 gap-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-primary-600">
                  {guidanceResult.learning_path.total_semesters || 'N/A'}
                </div>
                <div className="text-sm text-primary-700">Semesters</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-success-600">
                  {guidanceResult.learning_path.total_credit_hours || guidanceResult.learning_path.total_credits || 'N/A'}
                </div>
                <div className="text-sm text-success-700">Credit Hours</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-warning-600">
                  {guidanceResult.learning_path.completion_timeline || guidanceResult.learning_path.estimated_completion || 'N/A'}
                </div>
                <div className="text-sm text-warning-700">Completion</div>
              </div>
            </div>
            
            {/* Rationale */}
            {guidanceResult.learning_path.rationale && (
              <div className="mt-4 pt-4 border-t border-primary-100">
                <h4 className="font-medium text-secondary-900 mb-2">Learning Strategy:</h4>
                <p className="text-sm text-secondary-700 whitespace-pre-line">{guidanceResult.learning_path.rationale}</p>
              </div>
            )}
          </div>

          {/* Milestones */}
          {guidanceResult.learning_path.milestones && guidanceResult.learning_path.milestones.length > 0 && (
            <div className="card">
              <h3 className="text-lg font-semibold text-secondary-900 mb-4">Learning Milestones</h3>
              <div className="space-y-3">
                {guidanceResult.learning_path.milestones.map((milestone: any, index: number) => (
                  <div key={index} className="flex items-start space-x-3 p-3 bg-secondary-50 rounded-lg">
                    <div className="flex-shrink-0 w-8 h-8 bg-primary-600 text-white rounded-full flex items-center justify-center font-bold">
                      {index + 1}
                    </div>
                    <div className="flex-1">
                      <h4 className="font-medium text-secondary-900">{milestone.name}</h4>
                      <p className="text-sm text-secondary-600 mt-1">{milestone.description}</p>
                      <div className="text-xs text-secondary-500 mt-1">
                        Semesters: {milestone.semesters?.join(', ')}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Semester Breakdown */}
          {guidanceResult.learning_path.semesters && guidanceResult.learning_path.semesters.length > 0 && (
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-secondary-900">Semester Plan</h3>
              {guidanceResult.learning_path.semesters.map((semester: any, index: number) => (
                <div key={index} className="card">
                  <div className="flex items-center justify-between mb-4">
                    <div>
                      <h4 className="text-lg font-medium text-secondary-900">
                        {semester.semester_name || semester.name || `Semester ${index + 1}`}
                      </h4>
                      {semester.focus_area && (
                        <p className="text-sm text-secondary-600 mt-1">Focus: {semester.focus_area}</p>
                      )}
                    </div>
                    <span className="badge-primary">
                      {semester.total_credits || semester.credits || 0} credits
                    </span>
                  </div>
                  
                  <div className="grid md:grid-cols-2 gap-4">
                    {semester.courses?.map((course: any, courseIndex: number) => (
                      <div key={courseIndex} className="flex items-start space-x-3 p-3 bg-secondary-50 rounded-lg hover:bg-secondary-100 transition-colors">
                        <BookOpen className="h-5 w-5 text-primary-600 mt-0.5 flex-shrink-0" />
                        <div className="flex-1 min-w-0">
                          <div className="font-medium text-secondary-900 line-clamp-1">
                            {course.title || course.name || 'Untitled Course'}
                          </div>
                          <div className="text-sm text-secondary-600">
                            {course.course_code || course.code} • {course.credit_hours || course.credits || 3} credits
                          </div>
                          {course.priority && (
                            <span className={`inline-block mt-1 text-xs px-2 py-0.5 rounded-full ${
                              course.priority === 'high' || course.priority === 'critical' 
                                ? 'bg-error-100 text-error-700' 
                                : course.priority === 'medium' 
                                ? 'bg-warning-100 text-warning-700' 
                                : 'bg-success-100 text-success-700'
                            }`}>
                              {course.priority} priority
                            </span>
                          )}
                          {course.skills_gained && course.skills_gained.length > 0 && (
                            <div className="mt-2 flex flex-wrap gap-1">
                              {course.skills_gained.slice(0, 2).map((skill: string, skillIdx: number) => (
                                <span key={skillIdx} className="text-xs badge-primary">
                                  {skill}
                                </span>
                              ))}
                            </div>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  )

  const renderTabContent = () => {
    switch (activeTab) {
      case 'overview':
        return renderOverview()
      case 'courses':
        return renderCourses()
      case 'jobs':
        return renderJobs()
      case 'projects':
        return renderProjects()
      case 'roadmap':
        return renderRoadmap()
      default:
        return renderOverview()
    }
  }

  return (
    <div className="max-w-6xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <button
          onClick={() => navigate('/')}
          className="btn-ghost flex items-center space-x-2"
        >
          <ArrowLeft className="h-4 w-4" />
          <span>Back to Home</span>
        </button>

        <div className="flex items-center space-x-3">
          <button 
            onClick={handleShare}
            className="btn-outline btn-sm flex items-center space-x-2"
          >
            <Share2 className="h-4 w-4" />
            <span>Share</span>
          </button>
          <button 
            onClick={handleExportPDF}
            className="btn-primary btn-sm flex items-center space-x-2"
          >
            <Download className="h-4 w-4" />
            <span>Export Report</span>
          </button>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="border-b border-secondary-200 mb-8">
        <nav className="flex space-x-8 overflow-x-auto">
          {tabs.map((tab) => {
            const Icon = tab.icon
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`flex items-center space-x-2 py-4 px-1 border-b-2 font-medium text-sm whitespace-nowrap transition-colors ${
                  activeTab === tab.id
                    ? 'border-primary-600 text-primary-600'
                    : 'border-transparent text-secondary-500 hover:text-secondary-700 hover:border-secondary-300'
                }`}
              >
                <Icon className="h-4 w-4" />
                <span>{tab.label}</span>
              </button>
            )
          })}
        </nav>
      </div>

      {/* Tab Content */}
      <div className="animate-fade-in">
        {renderTabContent()}
      </div>

      {/* Toast Notification */}
      {toast && (
        <div className="fixed bottom-4 right-4 z-50 animate-slide-up">
          <div className={`
            px-6 py-4 rounded-lg shadow-lg flex items-center space-x-3
            ${toast.type === 'success' ? 'bg-success-600 text-white' : 
              toast.type === 'error' ? 'bg-error-600 text-white' : 
              'bg-primary-600 text-white'}
          `}>
            {toast.type === 'success' && <CheckCircle className="h-5 w-5" />}
            {toast.type === 'error' && <Star className="h-5 w-5" />}
            {toast.type === 'info' && <Star className="h-5 w-5" />}
            <span className="font-medium">{toast.message}</span>
          </div>
        </div>
      )}
    </div>
  )
}

export default Results