
import React from 'react';
import { cn } from '@/lib/utils';

interface FadeInProps {
  delay?: number;
  duration?: number;
  className?: string;
  children: React.ReactNode;
}

const FadeIn: React.FC<FadeInProps> = ({ 
  delay = 0, 
  duration = 500,
  className,
  children 
}) => {
  return (
    <div 
      className={cn("animate-fade-in", className)}
      style={{ 
        animationDelay: `${delay}ms`,
        animationDuration: `${duration}ms`
      }}
    >
      {children}
    </div>
  );
};

export default FadeIn;
