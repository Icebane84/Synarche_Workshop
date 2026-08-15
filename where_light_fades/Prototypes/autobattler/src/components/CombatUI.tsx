/**
 * artifact_anchor:
 * - id:
 * - type:
 */
import type React from "react";
import type { BattleState } from "../engine/CombatEngine";

interface CombatUiProps {
  battleState: BattleState;
  onTap: () => void;
  onGarrettSkill: () => void;
  onSerafinaSkill: () => void;
  onKaelenSkill: () => void;
  onToggleDarkMode: () => void;
}

export const CombatUI: React.FC<CombatUiProps> = ({
  battleState,
  onTap,
  onGarrettSkill,
  onSerafinaSkill,
  onKaelenSkill,
  onToggleDarkMode,
}) => {
  const {
    enemyName,
    enemyCategory,
    enemyDescription,
    enemyHealth,
    enemyMaxHealth,
    isStunned,
    exposedStacks,
    innerFlame,
    aegisShield,
    resonanceDrift,
    darkModeActive,
    combatLog,
  } = battleState;

  const enemyHealthPct = Math.max(0, (enemyHealth / enemyMaxHealth) * 100);

  return (
    <div className="combat-layout">
      {/* 4. Enemy Information (Top-Center Bar) */}
      <section className="card combat-layout-top">
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <div>
            <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
              <h2 style={{ margin: 0 }}>{enemyName}</h2>
              {enemyCategory && (
                <span
                  style={{
                    fontSize: "0.75rem",
                    color: "#9b51e0",
                    border: "1px solid #9b51e0",
                    padding: "2px 6px",
                    borderRadius: "4px",
                  }}
                >
                  {enemyCategory}
                </span>
              )}
              {isStunned && <span className="stun-badge">STUNNED</span>}
            </div>
            {enemyDescription && (
              <p style={{ fontSize: "0.8rem", color: "#8a8a9e", fontStyle: "italic", margin: "4px 0 0 0" }}>
                {enemyDescription}
              </p>
            )}
          </div>
          {exposedStacks > 0 && (
            <span className="badge exposed">
              🎯 Exposed x{exposedStacks} (+{exposedStacks * 40}% damage)
            </span>
          )}
        </div>

        <div className="progress-group" style={{ marginTop: "10px", marginBottom: 0 }}>
          <div className="bar-label">
            <span>Adversary Health</span>
            <span>
              {enemyHealth} / {enemyMaxHealth}
            </span>
          </div>
          <div className="progress-bar-bg">
            <div className="progress-bar-fill red" style={{ width: `${enemyHealthPct}%` }} />
          </div>
        </div>
      </section>

      {/* Main Grid: Left Vertical Log + Center Unified Flame & Action Bar */}
      <div className="combat-grid">
        {/* 5. Combat Log (Left Side, Vertical) */}
        <section className="card logs-card-vertical" style={{ height: "100%", minHeight: "360px" }}>
          <h2>Vigil Log</h2>
          <div
            className="logs-container-vertical"
            style={{
              height: "300px",
              overflowY: "auto",
              display: "flex",
              flexDirection: "column",
              gap: "6px",
              opacity: Math.max(0.3, innerFlame / 100),
              transition: "opacity 0.5s ease",
            }}
          >
            {combatLog.map((log, index) => (
              <div
                key={`log-${log.slice(0, 10)}-${index}`}
                className="log-line"
                style={{
                  fontSize: "0.8rem",
                  color: index === 0 ? "var(--color-gold)" : "#8a8a9e",
                  borderLeft: index === 0 ? "2px solid var(--color-gold)" : "2px solid rgba(255,255,255,0.1)",
                  paddingLeft: "6px",
                }}
              >
                {log}
              </div>
            ))}
          </div>
        </section>

        {/* Center Panel: Unified Health Bar & Action Bar */}
        <div style={{ display: "flex", flexDirection: "column", gap: "1.5rem" }}>
          {/* 2. Unified Health Bar: Inner Flame Gauge */}
          <section className="card flame-card" style={{ alignItems: "center", textAlign: "center" }}>
            <h2>The Unified Flame</h2>
            <div className="flame-visualization">
              {/* Serafina Aegis Silver Ring */}
              <div
                className="shield-ring"
                style={{
                  opacity: aegisShield / 100,
                  transform: `scale(${1 + aegisShield / 200})`,
                  borderWidth: `${Math.max(1, Math.floor(aegisShield / 15))}px`,
                }}
              />
              {/* Glowing Core Flame */}
              <div
                className={`core-flame ${innerFlame < 30 ? "critical" : ""}`}
                style={{
                  boxShadow: darkModeActive ? "0 0 35px rgba(155, 81, 224, 0.8)" : undefined,
                }}
              />
            </div>

            <div className="progress-group" style={{ width: "90%" }}>
              <div className="bar-label">
                <span>Inner Flame Intensity (Sanity/HP)</span>
                <span>{innerFlame}%</span>
              </div>
              <div className="progress-bar-bg">
                <div className="progress-bar-fill gold" style={{ width: `${innerFlame}%` }} />
              </div>
            </div>

            <div className="progress-group" style={{ width: "90%" }}>
              <div className="bar-label">
                <span>Aegis of Grace (Serafina Shield)</span>
                <span>{aegisShield}%</span>
              </div>
              <div className="progress-bar-bg">
                <div className="progress-bar-fill silver" style={{ width: `${aegisShield}%` }} />
              </div>
            </div>

            {/* Resonance Drift Aura */}
            <div className="progress-group" style={{ width: "90%", marginTop: "8px" }}>
              <div className="bar-label">
                <span>
                  Cosmic Balance:{" "}
                  {resonanceDrift < 40
                    ? "🌑 Nyx Dominant"
                    : resonanceDrift > 60
                      ? "☀️ White Flame Dominant"
                      : "⚖️ Equilibrium"}
                </span>
                <span>{resonanceDrift}%</span>
              </div>
              <div
                className="progress-bar-bg"
                style={{ background: "linear-gradient(90deg, #110022 0%, #444444 50%, #fff8cc 100%)" }}
              >
                <div
                  className="progress-bar-fill"
                  style={{
                    width: "12px",
                    marginLeft: `calc(${resonanceDrift}% - 6px)`,
                    backgroundColor:
                      resonanceDrift < 40 ? "#9b51e0" : resonanceDrift > 60 ? "#f2c94c" : "#ffffff",
                    boxShadow: "0 0 10px #fff",
                  }}
                />
              </div>
            </div>

            <button
              className="btn btn-tap"
              onClick={onTap}
              disabled={innerFlame <= 0}
              type="button"
              style={{ width: "90%", marginTop: "1rem" }}
            >
              🔥 Feed Spark (Click to kindle)
            </button>
          </section>

          {/* 3. Character Action Bar (Bottom-Center, Horizontal) */}
          <div className="action-bar-grid">
            {/* Kaelen */}
            <div className="squad-member-card kaelen-card">
              <div className="squad-member-header">
                <span className="unit-name">Kaelen</span>
                <span className="unit-role">Vanguard</span>
              </div>
              <div className={`passive-indicator ${innerFlame < 40 ? "active-oath" : ""}`}>
                🛡️ Weight of the Oath: {innerFlame < 40 ? "ACTIVE (Recoil x1.8)" : "Inactive"}
              </div>
              <button
                className="btn skill-btn kaelen"
                onClick={onKaelenSkill}
                disabled={innerFlame < 50}
                type="button"
              >
                ⚡ Inward Inquisition
              </button>
              <button
                className={`btn stance-btn ${darkModeActive ? "active-dark" : ""}`}
                onClick={onToggleDarkMode}
                type="button"
                style={{
                  background: darkModeActive ? "#5c0632" : "#2a2a3c",
                  borderColor: darkModeActive ? "#ff2a6d" : "#4a4a60",
                }}
              >
                {darkModeActive ? "🔥 Return Light Stance" : "🌑 Enter Dark Stance"}
              </button>
            </div>

            {/* Serafina */}
            <div className="squad-member-card serafina-card">
              <div className="squad-member-header">
                <span className="unit-name">Serafina</span>
                <span className="unit-role">Anchor</span>
              </div>
              <div className="passive-indicator">
                🛡️ Aegis Shielding (+5/tick)
              </div>
              <button
                className="btn skill-btn serafina"
                onClick={onSerafinaSkill}
                disabled={innerFlame <= 0}
                type="button"

              >
                ☀️ Whispers of Dawn (Restore 100%)
              </button>
            </div>

            {/* Garrett */}
            <div className="squad-member-card garrett-card">
              <div className="squad-member-header">
                <span className="unit-name">Garrett</span>
                <span className="unit-role">Pragmatist</span>
              </div>
              <div className="passive-indicator">
                🎯 Piercing Insight (+Exposed)
              </div>
              <button
                className="btn skill-btn garrett"
                onClick={onGarrettSkill}
                disabled={innerFlame <= 0 || isStunned}
                type="button"

              >
                ❄️ Grounding Command (Stun / Recoil Pause)
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

