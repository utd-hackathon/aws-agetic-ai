import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useCareerGuidance } from '../context/CareerGuidanceContext'
import { careerGuidanceAPI, OnboardingOptions } from '../services/api'
import QuickStartForm from '../components/QuickStartForm'
import ComprehensiveForm from '../components/ComprehensiveForm'
import LoadingSpinner from '../components/LoadingSpinner'
import ErrorMessage from '../components/ErrorMessage'

const Home: React.FC = () => {
  const navigate = useNavigate()
  const { setUserProfile, setGuidanceResult, setLoading, setError, loading, error } = useCareerGuidance()
  const [onboardingOptions, setOnboardingOptions] = useState<OnboardingOptions | null>(null)
  const [formType, setFormType] = useState<'quick' | 'comprehensive'>('quick')

  useEffect(() => {
    loadOnboardingOptions()
  }, [])

  const loadOnboardingOptions = async () => {
    try {
      const options = await careerGuidanceAPI.getOnboardingOptions()
      setOnboardingOptions(options)
    } catch (err) {
      setError('Failed to load form options')
    }
  }

  const handleQuickStart = async (profile: any) => {
    setLoading(true)
    setError(null)
    
    try {
      const result = await careerGuidanceAPI.quickStart(profile)
      setUserProfile(profile)
      setGuidanceResult(result)
      navigate('/results')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to get career guidance')
    } finally {
      setLoading(false)
    }
  }

  const handleComprehensive = async (profile: any) => {
    setLoading(true)
    setError(null)
    
    try {
      const result = await careerGuidanceAPI.comprehensiveGuidance(profile)
      setUserProfile(profile)
      setGuidanceResult(result)
      navigate('/results')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to get career guidance')
    } finally {
      setLoading(false)
    }
  }

  if (!onboardingOptions) {
    return <LoadingSpinner message="Loading form options..." />
  }

  return (
    <div className="max-w-4xl mx-auto">
      {/* Hero Section */}
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-secondary-900 mb-4">
          AI-Powered Career Guidance
        </h1>
        <p className="text-xl text-secondary-600 mb-8">
          Get personalized course recommendations, job market insights, and project ideas 
          tailored to your career goals.
        </p>
        
        {/* Form Type Toggle */}
        <div className="flex justify-center mb-8">
          <div className="bg-secondary-100 rounded-lg p-1">
            <button
              onClick={() => setFormType('quick')}
              className={`px-6 py-2 rounded-md transition-colors ${
                formType === 'quick'
                  ? 'bg-white text-primary-600 shadow-sm'
                  : 'text-secondary-600 hover:text-primary-600'
              }`}
            >
              Quick Start (30 seconds)
            </button>
            <button
              onClick={() => setFormType('comprehensive')}
              className={`px-6 py-2 rounded-md transition-colors ${
                formType === 'comprehensive'
                  ? 'bg-white text-primary-600 shadow-sm'
                  : 'text-secondary-600 hover:text-primary-600'
              }`}
            >
              Comprehensive (5 minutes)
            </button>
          </div>
        </div>
      </div>

      {/* Error Message */}
      {error && <ErrorMessage message={error} />}

      {/* Forms */}
      {formType === 'quick' ? (
        <QuickStartForm
          options={onboardingOptions}
          onSubmit={handleQuickStart}
          loading={loading}
        />
      ) : (
        <ComprehensiveForm
          options={onboardingOptions}
          onSubmit={handleComprehensive}
          loading={loading}
        />
      )}

      {/* Features Section */}
      <div className="mt-16 grid md:grid-cols-3 gap-8">
        <div className="card text-center">
          <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mx-auto mb-4">
            <span className="text-2xl">🎯</span>
          </div>
          <h3 className="text-lg font-semibold text-secondary-900 mb-2">
            Personalized Recommendations
          </h3>
          <p className="text-secondary-600">
            Get course suggestions tailored to your career goals and current skills
          </p>
        </div>

        <div className="card text-center">
          <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mx-auto mb-4">
            <span className="text-2xl">📊</span>
          </div>
          <h3 className="text-lg font-semibold text-secondary-900 mb-2">
            Real Job Market Data
          </h3>
          <p className="text-secondary-600">
            Based on actual LinkedIn job postings and market trends
          </p>
        </div>

        <div className="card text-center">
          <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mx-auto mb-4">
            <span className="text-2xl">🚀</span>
          </div>
          <h3 className="text-lg font-semibold text-secondary-900 mb-2">
            Project Ideas
          </h3>
          <p className="text-secondary-600">
            Build your portfolio with practical project recommendations
          </p>
        </div>
      </div>
    </div>
  )
}

export default Home
