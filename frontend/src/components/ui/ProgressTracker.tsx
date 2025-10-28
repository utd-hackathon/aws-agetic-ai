import React from 'react'
import { Check, Clock, ArrowRight } from 'lucide-react'

interface ProgressStep {
  id: string
  title: string
  description: string
  status: 'completed' | 'current' | 'pending'
  estimatedTime?: string
}

interface ProgressTrackerProps {
  steps: ProgressStep[]
  currentStep: string
  className?: string
}

const ProgressTracker: React.FC<ProgressTrackerProps> = ({ 
  steps, 
  currentStep, 
  className = '' 
}) => {
  const currentStepIndex = steps.findIndex(step => step.id === currentStep)

  return (
    <div className={`w-full ${className}`}>
      {/* Mobile Progress Bar */}
      <div className="md:hidden mb-6">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm font-medium text-secondary-700">
            Step {currentStepIndex + 1} of {steps.length}
          </span>
          <span className="text-sm text-secondary-500">
            {Math.round(((currentStepIndex + 1) / steps.length) * 100)}%
          </span>
        </div>
        <div className="progress-bar">
          <div 
            className="progress-fill"
            style={{ width: `${((currentStepIndex + 1) / steps.length) * 100}%` }}
          />
        </div>
        <div className="mt-2">
          <h3 className="font-medium text-secondary-900">
            {steps[currentStepIndex]?.title}
          </h3>
          <p className="text-sm text-secondary-600">
            {steps[currentStepIndex]?.description}
          </p>
        </div>
      </div>

      {/* Desktop Step Indicator */}
      <div className="hidden md:block">
        <nav aria-label="Progress">
          <ol className="flex items-center">
            {steps.map((step, stepIdx) => (
              <li key={step.id} className={`relative ${stepIdx !== steps.length - 1 ? 'pr-8 sm:pr-20' : ''}`}>
                {/* Connector Line */}
                {stepIdx !== steps.length - 1 && (
                  <div className="absolute inset-0 flex items-center" aria-hidden="true">
                    <div className={`h-0.5 w-full ${
                      step.status === 'completed' ? 'bg-primary-600' : 'bg-secondary-200'
                    }`} />
                  </div>
                )}

                {/* Step Circle */}
                <div className="relative flex items-center justify-center">
                  {step.status === 'completed' ? (
                    <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary-600 hover:bg-primary-700 transition-colors">
                      <Check className="h-5 w-5 text-white" aria-hidden="true" />
                    </div>
                  ) : step.status === 'current' ? (
                    <div className="flex h-8 w-8 items-center justify-center rounded-full border-2 border-primary-600 bg-white">
                      <div className="h-2.5 w-2.5 rounded-full bg-primary-600 animate-pulse" />
                    </div>
                  ) : (
                    <div className="flex h-8 w-8 items-center justify-center rounded-full border-2 border-secondary-300 bg-white group-hover:border-secondary-400 transition-colors">
                      <div className="h-2.5 w-2.5 rounded-full bg-transparent group-hover:bg-secondary-300 transition-colors" />
                    </div>
                  )}

                  {/* Step Content */}
                  <div className="absolute top-10 left-1/2 transform -translate-x-1/2 w-max max-w-xs">
                    <div className={`text-center ${
                      step.status === 'current' ? 'text-primary-600' : 
                      step.status === 'completed' ? 'text-secondary-700' : 'text-secondary-500'
                    }`}>
                      <div className={`text-sm font-medium ${
                        step.status === 'current' ? 'font-semibold' : ''
                      }`}>
                        {step.title}
                      </div>
                      <div className="text-xs mt-1">
                        {step.description}
                      </div>
                      {step.estimatedTime && step.status === 'current' && (
                        <div className="flex items-center justify-center mt-1 text-xs text-secondary-500">
                          <Clock className="h-3 w-3 mr-1" />
                          {step.estimatedTime}
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              </li>
            ))}
          </ol>
        </nav>
      </div>
    </div>
  )
}

export default ProgressTracker
