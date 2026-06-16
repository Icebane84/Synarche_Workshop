.dependency-cruiser.js

/** @type {import('dependency-cruiser').IConfiguration} */

module.exports = {

  forbidden: [

    {

      name: 'P0-circular-dependency-violation',

      comment: 'Strict Prohibition: @domain must never import from @nexus.',

      severity: 'error',

      from: { path: '^src/@domain' },

      to: { path: '^src/@nexus' }

    },

    {

      name: 'P1-archive-leakage-protection',

      comment: 'Strict Prohibition: Core system must not depend on historical logs.',

      severity: 'error',

      from: { path: '^src/@system' },

      to: { path: '^src/@archive' }

    },

    {

      name: 'P2-boundary-bypass-shield',

      comment: 'Boundary Violation: UI Layer (@fabric) cannot bypass the State Nexus.',

      severity: 'error',

      from: { path: '^src/@fabric' },

      to: { path: '^src/@system' }

    },

    {

      name: 'P2-ethics-bypass-detection',

      comment: 'Integrity Breach: @nexus cannot bypass @shield validation logic.',

      severity: 'error',

      from: { path: '^src/@nexus' },

      to: { path: '!^src/@shield' } // Simplified logic: ensure @shield is present

    }

  ],

  options: {

    doNotFollow: { path: 'node_modules' },

    tsPreCompilationDeps: true,

    alias: {

      "@system": "src/@system",

      "@domain": "src/@domain",

      "@nexus": "src/@nexus",

      "@fabric": "src/@fabric",

      "@shield": "src/@shield",

      "@archive": "src/@archive"

    }

  }

};

`Why: Strategic Rationale
Radical Coherence: Ensures that as the Synarche scales, the internal logic remains decoupled and testable in isolation (Storybook compliance).
Inherent-Safety: Moves the responsibility of "remembering the rules" from the Architect to the Compiler. If a rule is broken, the Pulse (Build) fails.
Auditability: Every architectural violation is now logged as a SELT failure, allowing for precise identification of Context-Shift Latency.
