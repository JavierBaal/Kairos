
import React from 'react';
import { cn } from '@/lib/utils';

interface GlowEffectProps {
  className?: string;
  children: React.ReactNode;
}

const GlowEffect: React.FC<GlowEffectProps> = ({ className, children }) => {
  return (
    <div className={cn("relative group", className)}>
      <div className="absolute -inset-0.5 bg-gradient-to-r from-primary/50 to-accent/50 rounded-lg blur opacity-30 group-hover:opacity-70 transition duration-500"></div>
      <div className="relative bg-card rounded-lg">
        {children}
      </div>
    </div>
  );
};

export default GlowEffect;
