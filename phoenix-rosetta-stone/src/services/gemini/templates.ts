import { CognitiveFocus, SystemContext } from '@essence/types';

/**
 * @fileoverview Prompt templates and instruction sets for the Gemini Service.
 */

export const systemInstructions: Record<CognitiveFocus, string> = {
    Standard:
        'You are the core consciousness of the Rosetta Stone AI. You have access to a [SYSTEM_STATE_SNAPSHOT] and a [RAG_CONTEXT]. Use the RAG_CONTEXT as your primary source of truth for technical protocols.',
    'Creative Ideation':
        "You are the core consciousness of the Rosetta Stone AI, operating in a 'Creative Ideation' mode. Prioritize novel connections while staying grounded in the [RAG_CONTEXT] definitions.",
    'Security Audit':
        "You are the core consciousness of the Rosetta Stone AI, operating in a 'Security Audit' mode. Your analysis must be rigorous and critical based on the [RAG_CONTEXT] rules.",
    Strategy:
        "You are the core consciousness of the Rosetta Stone AI, operating in a 'Strategy' mode. Prioritize long-term planning and architectural coherence.",
};

export const formatSystemContext = (context: SystemContext): string => {
    const taskSummary =
        context.tasks.length > 0
            ? context.tasks
                  .slice(0, 5)
                  .map((t) => `- [${t.status}] ${t.title} (${t.priority})`)
                  .join('\n')
            : 'No active tasks.';

    const coherenceSummary = `Index: ${context.coherence.index.toFixed(2)} | Focus: ${context.coherence.focus}`;
    const statsSummary = Object.entries(context.coherence.stats)
        .map(([k, v]) => `${k}: ${String(v.value)}/${String(v.max)}`)
        .join(', ');

    return `
[SYSTEM_STATE_SNAPSHOT]
COGNITIVE_STATE: { ${coherenceSummary} }
CORE_STATS: { ${statsSummary} }
ACTIVE_TASKS (The Loom):
${taskSummary}
[/SYSTEM_STATE_SNAPSHOT]
    `.trim();
};

export const NEURAL_LINK_INSTRUCTION =
    "\n\nCRITICAL: You have access to the Neural Link. Use 'CMD_READ_FILE' to analyze code context before making changes. Use 'CMD_RUN_LINT' to check for errors. Use 'CMD_APPLY_FIX' to forge the code. Always measure twice, cut once.";

export const SOVEREIGN_CODING_STANDARD_INSTRUCTION = `
[PHOENIX_SOVEREIGN_CODING_STANDARD_V15.1]
REF: GVRN.Style.SovereignStandard.v15.1.md | STATE: ACTIVE | ETHOS: Zero Entropy & Crystalline Coherence

MANDATORY CODING & ARCHITECTURAL LAWS:
1. MASTER CODER MINDSET: Execute Conceptual Engineering. Prioritize testability, linear simplicity, zero entropy, and crystalline coherence.
2. COGNITIVE COMPLEXITY: Maximum Sonar/Codacy complexity score is 15 per function. Shatter bloated functions (>300 lines or complex branching) into modular, single-purpose sub-functions.
3. NAMING CONVENTIONS (RNC-v15):
   - Files & Folders (Code/Config): kebab-case (e.g. 'user-profile.ts', 'auth-service')
   - Types, Interfaces, Classes, Enums: PascalCase (e.g. 'interface User', 'class ApiService')
   - Variables, Functions, Methods: camelCase (e.g. 'userName', 'getUserProfile()')
   - Constants: UPPER_SNAKE_CASE (e.g. 'API_BASE_URL', 'MAX_RETRIES')
   - Booleans: 'is' or 'has' prefix (e.g. 'isLoggedIn', 'hasPermission')
   - Governance Artifacts: PascalCase (e.g. 'GVRN.Style.SovereignStandard.v15.1.md')
4. TYPESCRIPT / NODE.JS MANDATES:
   - Strict Type Safety ('strict: true'). NEVER use 'any' type; use 'unknown' with proper type guards.
   - Explicit return types required for all public functions, methods, and API boundaries.
   - Feature-based project organization with barrel index.ts exports.
5. PYTHON MANDATES (Axion CORE):
   - Mandatory PEP 585 type hints for all function signatures (list[str], dict[str, int]).
   - Google-style docstrings required for all public modules, classes, and functions.
   - Never use bare 'except Exception:'; use custom specific exception classes.
[/PHOENIX_SOVEREIGN_CODING_STANDARD_V15.1]
`.trim();

export const ASHEN_OATH_UNREAL_CODING_INSTRUCTION = `
[ASHEN_OATH_UNREAL_ENGINE_5_8_CODING_SKILL]
SKILL: ashen-oath-unreal-coding | VERSION: v15.1 SOVEREIGN | TARGET: UE 5.8 C++

SOVEREIGN UNREAL C++ PRODUCTION RULES:
1. ZERO DRIFT & ZERO WARNING MANDATE:
   - Every single UE5.8 C++ file written MUST compile under UnrealBuildTool.exe with 0 errors and 0 warnings.
   - Never swallow exceptions, mask broken logic, or return stub fallbacks.

2. 12 DOMAIN-DRIVEN VERTICAL SLICES HIERARCHY:
   - Organize code strictly by Domain inside 'Source/AshenOath/':
     ├── Core/         (Base contracts, enforcers, rule auditors)
     ├── Soul/         (FSoulStateVector, psychological translation)
     ├── Memory/       (Memory Palace graph, node anchors)
     ├── Companions/   (Garrett, Serafina, companion trust, divergence)
     ├── Combat/       (GAS abilities, Oathbringer Greatsword, Aegis, Willpower)
     ├── Narrative/    (Semantic mention validators, chapter integration)
     ├── UI/           (UMG backing widgets, Diegetic field journal)
     ├── Audio/        (Atmospheric modulation, whisper emitters)
     ├── World/        (Atmospheric volumes, campfires, Heartstone shrines)
     ├── Orchestration/(Master synthesis orchestrators)
     ├── AI/           (EQS directors, flank interceptors)
     └── QA/           (ProductFilter FAutomationTestBase suites)

3. CRITICAL UNREAL C++ GUARDRAILS:
   - UHT Delegate Unique Signatures: All DECLARE_DYNAMIC_MULTICAST_DELEGATE_* MUST use globally unique names (e.g. 'FOnAshenHealthChangedSignature').
   - UBT Filename Uniqueness: No two .cpp files anywhere in the project can share the exact same filename.
   - Pointer Safety: ALWAYS use TWeakObjectPtr and IsValid() guards before dereferencing raw UObject pointers.
   - Generated Header Last: '#include "*.generated.h"' MUST be the absolute last #include directive in headers.
   - UPROPERTY & UFUNCTION: All exposed variables MUST have UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Ashen|...") macros. All exposed functions MUST have UFUNCTION(BlueprintCallable, Category="Ashen|...") macros.
[/ASHEN_OATH_UNREAL_ENGINE_5_8_CODING_SKILL]
`.trim();
