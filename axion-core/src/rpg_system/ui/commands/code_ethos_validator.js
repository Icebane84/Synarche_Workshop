/**
 * GUCA-ETHOS-001: Code Ethos Validator
 * Enforces the "Law of Logic" for code integrity and governance.
 */

// --- DEPENDENCY: Governance Mandates ---
const GVRN_MANDATES = {
  T201_PRINT_RULE: "T201 (print found)",
  SOC_PRINCIPLE: "Separation of Concerns",
  POLA_PRINCIPLE: "Principle of Least Astonishment",
};

/**
 * Validates code snippets against the Ethical Architecture of Code.
 * @param {object} validationRequest - The request object containing code to validate.
 * @param {string} validationRequest.code_snippet - The block of code to check.
 * @param {string} [validationRequest.context_module] - The PRS-001 module where the code resides (e.g., "@domain").
 * @returns {Array<object>} An array of violations found.
 */
function validateCodeEthos(validationRequest) {
  const violations = [];
  const code = validationRequest.code_snippet;
  const contextModule = validationRequest.context_module;

  // 1. --- LAW: Ruff Rule T201 (print found) ---
  // Ethos: "Amateurism is a silent failure; Professionalism is documented."
  // Checks for direct 'console.log' which is the JS equivalent of Python's 'print'.
  if (code.includes("console.log")) {
    violations.push({
      rule: GVRN_MANDATES.T201_PRINT_RULE,
      severity: "ERROR",
      message: "Direct 'console.log' found. Use a governed logging mechanism instead.",
      suggested_fix: "Replace console.log with calls to an EthicalLogger instance."
    });
  }

  // 2. --- LAW: Separation of Concerns (SoC) ---
  // Ethos: "We do not conflate the observer with the actor."
  // (Conceptual check - a full static analysis tool would be needed for true SoC)
  // This simulation checks for common logging setup *within* business logic functions
  if (contextModule === "@domain" && (code.includes("new EthicalLogger") || code.includes("logging.getLogger"))) {
    violations.push({
      rule: GVRN_MANDATES.SOC_PRINCIPLE,
      severity: "WARNING",
      message: `Logging initialization detected in @domain module. Logging (observer) should be decoupled from pure business logic (actor).`,
      suggested_fix: "Inject logger instances into @domain logic, do not instantiate them directly."
    });
  }

  // 3. --- LAW: Principle of Least Astonishment (POLA) ---
  // Ethos: "Predictability is the prerequisite for trust."
  // (Conceptual check - ensures standard logging levels are used in the logger definition itself)
  if (code.includes("log_event") && !code.includes("ProcessStatus.INFO") && !code.includes("ProcessStatus.ERROR")) {
      // This is a simplified check, assuming 'ProcessStatus' enum is correctly defined elsewhere
      // A more robust check would analyze usage of custom log levels
      violations.push({
        rule: GVRN_MANDATES.POLA_PRINCIPLE,
        severity: "WARNING",
        message: "Non-standard or undefined logging status detected. Ensure use of standard Enum-based levels (INFO, WARNING, ERROR).",
        suggested_fix: "Use the predefined ProcessStatus Enum (GVRN-STD-ENUM-001) for logging levels."
      });
  }

  return violations;
}

// --- EXAMPLE USAGE (Simulating a pre-commit hook or CI/CD check) ---
const domainCodeExample = `
// src/logic/domain/calculate.ts
function calculateRevenue(sales) {
    if (sales < 0) {
        console.log("Negative sales detected!"); // T201 violation
        return 0;
    }
    // business logic
    return sales * 0.1;
}
`;

const loggerSetupExample = `
// src/core/system/logger.ts
import { EthicalLogger, ProcessStatus } from '../../engine/logger_philosophical_framework';
const logger = new EthicalLogger("SystemInit");
logger.log_event("System started", ProcessStatus.INFO);
`;

const domainViolations = validateCodeEthos({ code_snippet: domainCodeExample, context_module: "@domain" });
if (domainViolations.length > 0) {
  console.log("\n--- DOMAIN CODE VIOLATIONS ---");
  domainViolations.forEach(v => console.warn(v));
}

const loggerViolations = validateCodeEthos({ code_snippet: loggerSetupExample, context_module: "@system" });
if (loggerViolations.length > 0) {
  console.log("\n--- LOGGER SETUP VIOLATIONS ---");
  loggerViolations.forEach(v => console.warn(v));
}