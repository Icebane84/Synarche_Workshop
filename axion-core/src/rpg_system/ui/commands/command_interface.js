/**
 * GUCA-VEC-003: VEC Command & Control Interface
 * Defines the syntax for dispatching Sovereign-level tasks.
 */

// --- DEPENDENCY: The Tarot-Specialist Hierarchy ---
const TAROT_MASKS = {
  HIEROPHANT: "The Hierophant",
  JUDGEMENT: "Judgement",
  EMPEROR: "The Emperor",
};

/**
 * Dispatches a command to a specialized system layer.
 * @param {object} command - The command object to execute.
 * @param {string} command.tarot_mask - The Sovereign personality authorizing the action.
 * @param {string} command.objective - A high-level description of the goal.
 * @param {string} command.target_layer - The PRS-001 layer to be modified.
 * @param {object} command.payload - The specific data or files for the operation.
 * @returns {boolean} - Returns true if the command is valid and dispatched.
 */
function dispatchCommand(command) {
  // Parameter Validation (Sentinel Protocol)
  if (!command.tarot_mask || !Object.values(TAROT_MASKS).includes(command.tarot_mask)) {
    console.error("COMMAND REJECTED: Invalid or missing Tarot Mask.");
    return false;
  }
  if (!command.target_layer || !command.target_layer.startsWith("@")) {
    console.error("COMMAND REJECTED: Target layer must be a valid PRS-001 path.");
    return false;
  }
  if (!command.objective || !command.payload) {
    console.error("COMMAND REJECTED: Objective and Payload are mandatory.");
    return false;
  }

  console.log(`COMMAND ACCEPTED: [${command.tarot_mask}] is executing objective: "${command.objective}" on layer [${command.target_layer}].`);
  // In a real system, this would trigger a process (e.g., call a service, run a script)
  // executeSystemTask(command.payload);
  return true;
}

// --- EXAMPLE USAGE (Simulating Directive from PRS-ENFORCE-001) ---
const populateSecurityDirective = {
  tarot_mask: TAROT_MASKS.HIEROPHANT,
  objective: "Populate foundational security services.",
  target_layer: "@shield",
  payload: {
    files_to_create: [
      "Authentication.service.ts",
      "Auth.essence.ts"
    ],
    template: "standard_service_v1"
  }
};

dispatchCommand(populateSecurityDirective);