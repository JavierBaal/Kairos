
import React from 'react';
import { cn } from '@/lib/utils';

interface StepProgressProps {
  steps: {
    id: number;
    label: string;
    isActive?: boolean;
    isCompleted?: boolean;
    variant?: 'default' | 'orange' | 'red';
  }[];
}

const StepProgress: React.FC<StepProgressProps> = ({ steps }) => {
  const getStepClasses = (step: StepProgressProps['steps'][0]) => {
    const variant = step.variant || 'default';
    
    if (step.isCompleted) {
      switch (variant) {
        case 'orange':
          return "border-orange/70 bg-orange/20 text-orange";
        case 'red':
          return "border-red/70 bg-red/20 text-red";
        default:
          return "border-primary/70 bg-primary/20 text-primary";
      }
    }
    
    if (step.isActive) {
      switch (variant) {
        case 'orange':
          return "border-orange bg-orange text-orange-foreground shadow-[0_0_15px_rgba(249,115,22,0.5)]";
        case 'red':
          return "border-red bg-red text-red-foreground shadow-[0_0_15px_rgba(234,56,76,0.5)]";
        default:
          return "border-primary bg-primary text-primary-foreground shadow-[0_0_15px_rgba(56,182,255,0.5)]";
      }
    }
    
    return "border-muted text-foreground/80";
  };
  
  const getTextClasses = (step: StepProgressProps['steps'][0]) => {
    const variant = step.variant || 'default';
    
    if (step.isActive) {
      switch (variant) {
        case 'orange':
          return "text-orange";
        case 'red':
          return "text-red";
        default:
          return "text-primary";
      }
    }
    
    if (step.isCompleted) {
      return "text-foreground";
    }
    
    return "text-muted-foreground";
  };

  return (
    <div className="flex justify-center items-center space-x-6 md:space-x-12 py-8">
      {steps.map((step, index) => (
        <div key={step.id} className="flex flex-col items-center">
          <div 
            className={cn(
              "step-indicator animate-fade-in",
              getStepClasses(step)
            )}
            style={{ animationDelay: `${index * 100}ms` }}
          >
            {step.id}
          </div>
          <span 
            className={cn(
              "mt-2 text-sm font-medium animate-fade-in",
              getTextClasses(step)
            )}
            style={{ animationDelay: `${(index * 100) + 100}ms` }}
          >
            {step.label}
          </span>
          
          {index < steps.length - 1 && (
            <div className="absolute hidden md:block left-0 right-0 h-0.5 bg-muted top-6" style={{
              width: '100px',
              transform: 'translateX(50%)',
              zIndex: -1
            }}></div>
          )}
        </div>
      ))}
    </div>
  );
};

export default StepProgress;
