/**
 * artifact_anchor:
 * - id: App-component-start
 * - type: component
 */
import { useEffect, useRef, useState } from 'react';
import { CombatUI } from './components/CombatUI';
import { type BattleState, CombatEngine } from './engine/CombatEngine';
import { useCognitiveCore } from './store/useCognitiveCore';

export default function App() {
  const coreState = useCognitiveCore();
  const [battleState, setBattleState] = useState<BattleState | null>(null);
  const [activeTab, setActiveTab] = useState<'combat' | 'legacy'>('combat');
  const engineRef = useRef<CombatEngine | null>(null);

  // Initialize Combat Engine when the component mounts or talents change
  useEffect(() => {
    const engine = new CombatEngine((updatedState) => {
      setBattleState(updatedState);
      
      // Hook up achievements when criteria is met
      if (updatedState.victoryCount > 0) {
        // Complete "Oakhaven Purified" achievement on first win
        coreState.completeLegendaryAchievement('ach-1');
      }
      if (updatedState.isStunned && updatedState.innerFlame < 30) {
        // Complete "Sentinel's Gambit" if Garrett stun is triggered at low HP
        coreState.completeLegendaryAchievement('ach-2');
      }
      if (updatedState.innerFlame === 100 && updatedState.aegisShield >= 80) {
        // Complete "Inner Sanctuary" when flame is stabilized
        coreState.completeLegendaryAchievement('ach-3');
      }
    }, coreState.unlockedLegacyTalents);

    engineRef.current = engine;
    engine.start();

    return () => {
      engine.stop();
    };
  }, [coreState.unlockedLegacyTalents, coreState.completeLegendaryAchievement, coreState]);

  const handleTap = () => {
    engineRef.current?.triggerTap();
  };

  const handleGarrettSkill = () => {
    engineRef.current?.triggerGroundingCommand();
  };

  const handleSerafinaSkill = () => {
    engineRef.current?.triggerWhispersOfTheDawn();
  };

  const handleKaelenSkill = () => {
    engineRef.current?.triggerKaelenSkill();
  };

  const handleToggleDarkMode = () => {
    engineRef.current?.toggleDarkMode();
  };

  const handleResolveEvent = (choiceIndex: number) => {
    engineRef.current?.resolveEvent(choiceIndex);
  };

  const handleIgniteEcho = (talentId: string) => {
    const res = coreState.initiatePrestigeReset(talentId);
    alert(res.message);
    if (res.success) {
      // Re-initialize and restart the engine upon rebirth
      engineRef.current?.stop();
      const engine = new CombatEngine((updatedState) => {
        setBattleState(updatedState);
      }, coreState.unlockedLegacyTalents);
      engineRef.current = engine;
      engine.start();
    }
  };

  if (!battleState) {
    return <div className="loading">Igniting the spark...</div>;
  }

  const {
    victoryCount,
    activeEvent,
    innerFlame,
    hallucinationLevel
  } = battleState;

  // Determine atmospheric occlusion CSS property value
  const ambientOcclusionPct = 1 - (innerFlame / 100);


  return (
    <div
      className={`game-container hallucination-${hallucinationLevel.toLowerCase()}`}
      style={{ '--inner-flame': innerFlame } as React.CSSProperties}
    >
      {/* Atmospheric Occlusion Shadow Overlay */}
      <div
        className="vignette-overlay"
        style={{
          boxShadow: `inset 0 0 calc(100vw * ${ambientOcclusionPct * 0.8}) rgba(0, 0, 0, 0.95)`
        }}
      />

      <header className="game-header">
        <div className="title-group">
          <h1>Ashen Oath</h1>
          <span className="subtitle">Inner Flame Echoes (v15.0)</span>
        </div>
        <div className="stats-bar">
          <div className="stat-node">
            <span className="label">Victories:</span>
            <span className="val">{victoryCount}</span>
          </div>
          <div className="stat-node">
            <span className="label">Rebirths:</span>
            <span className="val">{coreState.unlockedLegacyTalents.length}</span>
          </div>
          <div className="stat-node">
            <span className="label">Prestige Points (PP):</span>
            <span className="val">{coreState.prestigeLevel}</span>
          </div>
        </div>
      </header>

      <nav className="tab-navigation">
        <button
          className={activeTab === 'combat' ? 'active' : ''}
          onClick={() => setActiveTab('combat')}
        >
          ⚔️ Combat Loop
        </button>
        <button
          className={activeTab === 'legacy' ? 'active' : ''}
          onClick={() => setActiveTab('legacy')}
        >
          🏺 Sanctuary of Memory ({coreState.unlockedLegacyTalents.length}/15)
        </button>
      </nav>

      <main className="game-content">
        {activeTab === 'combat' && (
          <CombatUI battleState={battleState} onTap={handleTap} onGarrettSkill={handleGarrettSkill} onSerafinaSkill={handleSerafinaSkill} onKaelenSkill={handleKaelenSkill} onToggleDarkMode={handleToggleDarkMode} />
        )}

        {activeTab === 'legacy' && (
          <div className="legacy-grid">
            <section className="card legacy-info-card">
              <h2>Sanctuary of Memory</h2>
              <p className="description">
                Earn Prestige Points (PP) by completing Legendary Achievements on the road to Oakhaven. 
                Use PP to ignite the cycle and unlock permanent, account-wide Legacy Talents.
              </p>
              <div className="prestige-banner">
                <span className="pp-balance">{coreState.prestigeLevel}</span>
                <span className="pp-label">Available Prestige Points (PP)</span>
              </div>
            </section>

            <section className="card achievements-card">
              <h2>Legendary Achievements</h2>
              <div className="achievements-list">
                {coreState.legendaryAchievements.map((ach) => {
                  const playerAch = coreState.playerAchievements.find((pa) => pa.achievementId === ach.id);
                  return (
                    <div key={ach.id} className={`ach-item ${playerAch?.isCompleted ? 'completed' : ''}`}>
                      <div className="ach-details">
                        <h3>{ach.name}</h3>
                        <p>{ach.description}</p>
                      </div>
                      <div className="ach-points">
                        +{ach.ppValue} PP
                        {playerAch?.isCompleted && <span className="check">✓</span>}
                      </div>
                    </div>
                  );
                })}
              </div>
            </section>

            <section className="card talents-card">
              <h2>Legacy Talents (Unlock via Rebirth)</h2>
              <div className="talents-list">
                {coreState.legacyTalents.map((talent) => {
                  const isUnlocked = coreState.unlockedLegacyTalents.includes(talent.id);
                  const canAfford = coreState.prestigeLevel >= talent.cost;

                  return (
                    <div
                      key={talent.id}
                      className={`talent-item ${isUnlocked ? 'unlocked' : ''}`}
                    >
                      <div className="talent-details">
                        <h3>{talent.name} <span className="tier-badge">{talent.tier}</span></h3>
                        <p>{talent.description}</p>
                      </div>
                      <div className="talent-action">
                        {isUnlocked ? (
                          <span className="status-label unlocked">UNLOCKED</span>
                        ) : (
                          <button
                            className="btn btn-unlock"
                            onClick={() => handleIgniteEcho(talent.id)}
                            type="button" // Explicitly set type to 'button'
                            disabled={!canAfford}
                          >
                            Rebirth ({talent.cost} PP)
                          </button>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>
            </section>
          </div>
        )}
        {/* Moral Dilemma Event Overlay Modal */}
        {activeEvent && (
          <div className="event-modal-backdrop" style={{ position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.85)', backdropFilter: 'blur(5px)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000 }}>
            <div className="event-modal-card" style={{ background: '#1c1c28', border: '1px solid #9b51e0', padding: '24px', borderRadius: '12px', maxWidth: '480px', width: '90%', textAlign: 'center', boxShadow: '0 0 25px rgba(155, 81, 224, 0.4)' }}>
              <h2 style={{ color: '#e0e0e0', marginTop: 0 }}>⚡ {activeEvent.title}</h2>
              <p style={{ color: '#a0a0b0', fontSize: '0.95rem', margin: '16px 0' }}>{activeEvent.text}</p>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                {activeEvent.choices.map((choice, idx) => (
                  <button
                    key={`${activeEvent.id}-${idx}`}
                    onClick={() => handleResolveEvent(idx)}
                    style={{ background: '#2a2a3c', border: '1px solid #4a4a60', color: '#fff', padding: '12px', borderRadius: '8px', cursor: 'pointer', textAlign: 'left', transition: 'all 0.2s' }}
                  >
                    <div style={{ fontWeight: 'bold' }}>{choice.text}</div>
                    <div style={{ fontSize: '0.8rem', color: '#4ac9a0', marginTop: '4px' }}>{choice.costLabel}</div>
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
