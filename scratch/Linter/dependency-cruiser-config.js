/**
 * OMEGA-V15 PROTOCOL: Architectural Boundary Sentinel
 * 
 * Enforces the "One-Way Flow" of dependency gravity and prevents Epistemic Entropy
 * by blocking prohibited import paths across OGLN Sovereign Folders.
 * 
 * Target Mappings:
 * - 0_GOVERNANCE/  -> @system, @shield, @atlas
 * - 1_BLUEPRINTS/  -> @domain, @essence
 * - 2_PROTOCOLS/   -> @nexus
 * - 3_COMMANDS/    -> @fabric
 * - 4_LOGS/        -> @pulse, @archive
 */

module.exports = {
  forbidden: [
    {
      name: 'P0-circular-dependency-violation',
      comment: 'Strict Prohibition: The Platonic Blueprint (@domain) must never import from the State Nexus (@nexus).',
      severity: 'error',
      from: { path: '^1_BLUEPRINTS' },
      to: { path: '^2_PROTOCOLS' }
    },
    {
      name: 'P1-archive-leakage-protection',
      comment: 'Strict Prohibition: The Core System (@system) must not depend on historical logs or testing tools (@archive).',
      severity: 'error',
      from: { path: '^0_GOVERNANCE' },
      to: { path: '^4_LOGS' }
    },
    {
      name: 'P2-boundary-bypass-shield',
      comment: 'Boundary Violation: The UI presentation layer (@fabric) cannot bypass the State Nexus (@nexus) to touch Law directly.',
      severity: 'error',
      from: { path: '^3_COMMANDS' },
      to: { path: '^0_GOVERNANCE' }
    },
    {
      name: 'P2-ethics-bypass-detection',
      comment: 'Integrity Breach: The State Nexus (@nexus) cannot bypass Noetic Immune System (@shield) validation logic.',
      severity: 'error',
      from: { path: '^2_PROTOCOLS' },
      to: { path: '!^0_GOVERNANCE/security' }
    }
  ],
  options: {
    doNotFollow: { path: 'node_modules' },
    tsPreCompilationDeps: true,
    alias: {
      "@system": "0_GOVERNANCE",
      "@domain": "1_BLUEPRINTS",
      "@nexus": "2_PROTOCOLS",
      "@fabric": "3_COMMANDS",
      "@shield": "0_GOVERNANCE/security",
      "@archive": "4_LOGS"
    }
  }
};
