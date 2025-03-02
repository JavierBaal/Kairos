
import React, { useState } from 'react';
import { cn } from '@/lib/utils';

const CollaborationControls = () => {
  const [selectedOption, setSelectedOption] = useState<'step' | 'strategic' | 'custom'>('strategic');
  const [teamObjective, setTeamObjective] = useState("Descubrir oportunidades de mercado y desarrollar estrategias competitivas");

  return (
    <div className="glass-panel rounded-xl p-6 animate-fade-in" style={{ animationDelay: '300ms' }}>
      <h2 className="text-lg font-medium text-foreground mb-5">Personalización de Flujo de Trabajo</h2>
      
      <div className="space-y-4">
        <div>
          <label className="block text-muted-foreground mb-2">Tipo de Colaboración:</label>
          <div className="flex flex-wrap gap-4">
            <div className="radio-option" onClick={() => setSelectedOption('step')}>
              <div className={cn("radio-circle", selectedOption === 'step' && "border-red")}>
                {selectedOption === 'step' && <div className="radio-selected-red" />}
              </div>
              <span className={cn("text-sm", selectedOption === 'step' ? "text-red" : "text-muted-foreground")}>
                Paso a paso
              </span>
            </div>
            
            <div className="radio-option" onClick={() => setSelectedOption('strategic')}>
              <div className={cn("radio-circle", selectedOption === 'strategic' && "border-primary")}>
                {selectedOption === 'strategic' && <div className="radio-selected" />}
              </div>
              <span className={cn("text-sm", selectedOption === 'strategic' ? "text-foreground" : "text-muted-foreground")}>
                Estratégica
              </span>
            </div>
            
            <div className="radio-option" onClick={() => setSelectedOption('custom')}>
              <div className={cn("radio-circle", selectedOption === 'custom' && "border-orange")}>
                {selectedOption === 'custom' && <div className="radio-selected-orange" />}
              </div>
              <span className={cn("text-sm", selectedOption === 'custom' ? "text-orange" : "text-muted-foreground")}>
                Personalizada
              </span>
            </div>
          </div>
        </div>
        
        <div>
          <label htmlFor="teamObjective" className="block text-muted-foreground mb-2">
            Objetivo del Equipo:
          </label>
          <input
            id="teamObjective"
            value={teamObjective}
            onChange={(e) => setTeamObjective(e.target.value)}
            className="input-field w-full"
            placeholder="Describe el objetivo principal de tu equipo..."
          />
        </div>
        
        <div className="pt-4 grid grid-cols-1 md:grid-cols-3 gap-4">
          <button className="button-secondary">
            Guardar Configuración
          </button>
          <button className="button-orange">
            Previsualizar
          </button>
          <button className="button-red">
            Activar Equipo de Inteligencia
          </button>
        </div>
      </div>
    </div>
  );
};

export default CollaborationControls;
