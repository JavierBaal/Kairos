
import React from 'react';
import { cn } from '@/lib/utils';

interface AgentCardProps {
  name: string;
  description: string;
  variant?: 'default' | 'orange' | 'red';
}

const AgentCard: React.FC<AgentCardProps> = ({ 
  name, 
  description, 
  variant = 'default' 
}) => {
  const getVariantClasses = () => {
    switch (variant) {
      case 'orange':
        return {
          card: 'agent-card-orange',
          outerCircle: 'bg-orange/20 group-hover:bg-orange/30',
          innerCircle: 'bg-orange',
          text: 'text-orange-foreground'
        };
      case 'red':
        return {
          card: 'agent-card-red',
          outerCircle: 'bg-red/20 group-hover:bg-red/30',
          innerCircle: 'bg-red',
          text: 'text-red-foreground'
        };
      default:
        return {
          card: 'agent-card',
          outerCircle: 'bg-primary/20 group-hover:bg-primary/30',
          innerCircle: 'bg-primary',
          text: 'text-primary-foreground'
        };
    }
  };

  const variantClasses = getVariantClasses();

  return (
    <div className={cn("group animate-scale-in", variantClasses.card)}>
      <div className={cn("w-16 h-16 mb-4 rounded-full flex items-center justify-center transition-all", variantClasses.outerCircle)}>
        <div className={cn("w-10 h-10 rounded-full flex items-center justify-center", variantClasses.innerCircle)}>
          <span className={cn("font-semibold", variantClasses.text)}>
            {name.charAt(0)}
          </span>
        </div>
      </div>
      
      <h3 className="text-foreground font-medium mb-2">{name}</h3>
      
      <p className="text-sm text-muted-foreground">{description}</p>
    </div>
  );
};

export default AgentCard;
