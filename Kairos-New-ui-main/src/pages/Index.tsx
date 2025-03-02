
import React, { useState } from 'react';
import Header from '@/components/Layout/Header';
import StepProgress from '@/components/StepProgress/StepProgress';
import AgentCard from '@/components/Agents/AgentCard';
import CollaborationControls from '@/components/Workflow/CollaborationControls';

const Index = () => {
  const [currentStep] = useState(2);
  
  const steps = [
    { id: 1, label: 'FORMAR', isCompleted: currentStep > 1 },
    { id: 2, label: 'DEFINIR', isActive: currentStep === 2 },
    { id: 3, label: 'CONECTAR', isActive: currentStep === 3 },
    { id: 4, label: 'ACTIVAR', isActive: currentStep === 4 },
    { id: 5, label: 'RESULTADOS', isActive: currentStep === 5 },
  ];
  
  const specialists = [
    {
      id: 1,
      name: 'Analista de Mercado',
      description: 'Experto en análisis de tendencias y oportunidades de mercado'
    },
    {
      id: 2,
      name: 'Cazador de Oportunidades',
      description: 'Especialista en identificar gaps de mercado y oportunidades'
    },
    {
      id: 3,
      name: 'Estratega Competitivo',
      description: 'Desarrolla planes estratégicos basados en análisis de competencia'
    }
  ];
  
  return (
    <div className="min-h-screen bg-background text-foreground">
      <Header />
      
      <main className="container pt-20 pb-10 px-4 md:px-6">
        <StepProgress steps={steps} />
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
          <div className="md:col-span-1">
            <h2 className="text-lg font-medium text-foreground mb-5 animate-fade-in">ESPECIALISTAS</h2>
            <div className="grid grid-cols-1 gap-4">
              {specialists.map((specialist, index) => (
                <AgentCard 
                  key={specialist.id} 
                  name={specialist.name} 
                  description={specialist.description} 
                />
              ))}
            </div>
          </div>
          
          <div className="md:col-span-2">
            <h2 className="text-lg font-medium text-foreground mb-5 animate-fade-in">DEFINIR EQUIPO</h2>
            <div className="glass-panel rounded-xl p-6 h-80 mb-8 animate-fade-in">
              <div className="flex items-center justify-center h-full text-muted-foreground">
                <div className="text-center">
                  <div className="w-16 h-16 rounded-full border-2 border-dashed border-muted-foreground/30 flex items-center justify-center mx-auto mb-4">
                    <svg className="w-6 h-6 text-muted-foreground/70" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 4v16m8-8H4" />
                    </svg>
                  </div>
                  <p>Arrastra especialistas aquí para crear tu equipo</p>
                </div>
              </div>
            </div>
            
            <div className="h-12"></div>
          </div>
        </div>
        
        <CollaborationControls />
      </main>
    </div>
  );
};

export default Index;
