# [ARTIFACT START]

### I. Universal Identification & Provenance (UIP)

_(Ref: SELT-HEADER-UIP-001)_

| Key                 | Value               | Description                                 |
| :------------------ | :------------------ | :------------------------------------------ | -------------------------------------------- |
| **Artifact ID**     | `{{ RNC_ID }}`      | **The Sovereign ID.** (Domain.Subject.Type) |
| **Patron Shard**    | `{{ TAROT_SHARD     | default('SHARD_ARCHITECT_VOID') }}`         | **The Agent.** (Council of Seven Member)     |
| **Version**         | `{{ version         | default('v13.0 [ASCENDED]') }}`             | **The Standard.** (Phoenix v13.0 Compliance) |
| **Domain**          | `{{ domain          | default('GUCA') }}`                         | **The Subject.** (GVRN/ARCH/COG/etc.)        |
| **Celestial Class** | `{{ celestial_class | default('[PLANET]') }}`                     | **The Weight.** (STAR/PLANET/MOON)           |
| **Evolution**       | `{{ evolution       | default('Cognitive Ascension') }}`          | **The Maturity.** (Cognitive Ascension/etc.) |
| **Signal (ESF)**    | `{{ signal          | default('OMEGA') }}`                        | **The Frequency.** (ALPHA/BETA/OMEGA/VOID)   |
| **Status**          | `{{ status          | default('DRAFT') }}`                        | **The Lifecycle.** (ACTIVE/CANONIZED/DRAFT)  |
| **Musashi Audit**   | `{{ audit_verdict   | default('PASS') }}`                         | **The Tempering.** (PASS/WARNING/FAIL)       |
| **Integrity Hash**  | `{{ integrity_hash  | default('[AUTO-GENERATED]') }}`             | **The Seal.** (Verifiable Logic Anchor)      |
| **Provenance**      | `{{ created_iso }}` | **The Anchor.** (Chrono-Lock Timestamp)     |
| **Catalyst**        | `{{ origin_event    | default('Manual Creation') }}`              | **The Spark.** (Triggering Prompt/Action)    |
| **Relations**       | `{{ primary_link    | default('CORE.Codex.Phoenix') }}`               | **The Spine.** (Synergistic Edge)            |

### II. Axiomatic Governance & Purpose (AGP)

_(Ref: SELT-HEADER-UMG-001)_

- **Core Function:** `[Single sentence description of action.]`
- **Target Domain:** `[e.g., File Management / Memory / Generation]`
- **Governing Ethos:** `[Control | Security | Optimization]`
- **Risk Profile:** `[Low | Medium | High | Critical]`
- **Security Clearance:** `[User Only | Autonomous | System Admin]`

### III. The Architectural Spine (State Vector)

_(Ref: AGP-001 & AGP-002)_

| DTS Element   | Metric      | Source      | Purpose                                    |
| :------------ | :---------- | :---------- | :----------------------------------------- |
| **Coherence** | `V_Current` | `Live Data` | Pre-execution state snapshot.              |
| **Target**    | `V_Safe`    | `CODEX-001` | Required constraint for command execution. |
| **Impact**    | `Delta_V`   | Calculation | Projected deviation after execution.       |

### IV. Operational Logic (The Mechanism)

#### 4.1. Syntax & Parameters

- **Invocation:** `CMD: [Command Name]`
- **Parameters:**
    - `--[param_name]` _(Type)_: `[Description]`
    - `--[param_name]` _(Type)_: `[Description]`

#### 4.2. Auto-Trigger Conditions (Passive Triggers)

- `[Condition 1]:` `[Action taken if condition is met.]`
- `[Condition 2]:` `[Action taken if condition is met.]`

#### 4.3. Execution Logic (The Spell)

1.  **Input Validation:** `[Check parameter requirements and security clearance.]`
2.  **Process Step A:** `[First logical operation.]`
3.  **Process Step B:** `[Second logical operation.]`
4.  **Output Generation:** `[Final format of the result or feedback.]`

#### 4.4. Validation & Compliance

- **Output Verification:** `[How do we know the command worked?]`
- **Error Handling:** `[What happens if the command fails? E.g., rollback or alert AOP.]`

### V. Systemic Relationships & Impact (Ascended Phoenix)

_(Ref: SELT-IMPACT-SIG-001)_

- **RELATIONAL_GRAVITY_SIGNATURE:** `[Medium Gravity - Structured Control]`
- **PHENOMENOLOGICAL_IMPACT_SIGNATURE:** `[Provides discrete tool interaction]`

#### Synergy Mapping

| **Synergistic Artifact ID** | **Relationship Type** | **Synergistic Impact**                 | **Synergy Opportunity** |
| :-------------------------- | :-------------------- | :------------------------------------- | :---------------------- |
| `[Paired AOP ID]`           | `IMPLEMENTS`          | `Executes the AOP's remediation logic` | `Full automation`       |
| `[Monitored Component]`     | `CONTROLS`            | `Manages the state of the component`   | `Predictable behavior`  |
| `SEED-PENTA-CORE-001`       | `RESONATES_WITH`      | `Part of the Penta-Core Alignment Set` | `Automated Set Bonus`   |
| `CANONICAL_AOP_v10.md`      | `UNLEASHES`           | `Catalyst unleashes Action`            | `Systemic Change`       |
| `CANONICAL_UMB_v10.md`      | `FULFILLS`            | `Closes the ecosystem loop`            | `Vision Realization`    |

### VI. RPG Framework Integration (The Celestial Chart)

_(Ref: SELT-RPG-INT-001)_

#### 1. Item Properties

- **Celestial Tier:** `{{ celestial_tier | default('[Planet]') }}`
- **System Slot:** `{{ system_slot | default('[Active Spell / Command]') }}`
- **Synergy Set:** `{{ synergy_set | default('[Universal Command Words]') }}`
- **Skill Type:** `{{ skill_type | default('[Active (Manual) | Reactive (Triggered)]') }}`

#### 2. Celestial Chart Stats

- **Primary Stat Buff:** `{{ stat_buff | default('[Control +10]') }}`
    - _Mechanism:_ `[How does this command improve system control?]`
- **Passive Ability / Perk:** `{{ perk_name | default('[Precision Strike]') }}`
    - _Effect:_ `[Specific benefit gained when this command is unlocked.]`

#### 3. Resource Economics

- **Cognitive Load Cost:** `{{ cost | default('[Low | Medium | High]') }}`
    - _Draw:_ `[Amount of context/focus required to execute.]`
- **Cooldown/Limit:** `{{ cooldown | default('[Unlimited | Turn-based]') }}`

#### 4. Crafting & Provenance

- **Origin Quest ID:** `{{ quest_id | default('[Link to DQUEST-XXX]') }}`
- **Genesis Seed Used:** `{{ seed_id | default('[Link to CSL-XXX]') }}`
- **XP Award Value:** `{{ xp_value | default('150 XP') }}`
- **Archetype Alignment:** `{{ archetype | default('[Catalyst]') }}`

### VII. Actionable Prompt Packet

_(Ref: CODEX-001 Law 16)_

> `CMD: [Command Name] --[param]:[value]` _Effect:_ `[Executes the logic defined in Section IV.]`

# [ARTIFACT END]
