# Ten Maxims — Engineering Governance Model

**Version 1.1 | Operational Specification**

---

## Preamble

This document upgrades the Ten Maxims from a philosophical-to-engineering mapping into an executable governance model. Each maxim is now expressed across four layers:

| Layer                     | Purpose                              |
| ------------------------- | ------------------------------------ |
| **Axiomatic Statement**   | The maxim as originally stated       |
| **Standard Mapping**      | Industry standards and references    |
| **Operational Semantics** | Scope, type, and failure modes       |
| **Conflict Resolution**   | Precedence rules when maxims collide |

### Type Definitions

| Type             | Meaning                                                                         |
| ---------------- | ------------------------------------------------------------------------------- |
| **Constraint**   | Hard invariant. Must not be violated. Failure is a defect, not a tradeoff.      |
| **Guardrail**    | Soft boundary. Violation requires a documented exception with owner sign-off.   |
| **Heuristic**    | Default decision rule. Override is permitted with reasoning recorded in an ADR. |
| **Optimization** | Applied only after constraints and guardrails are satisfied.                    |

### Scope Definitions

| Scope            | Covers                                                                          |
| ---------------- | ------------------------------------------------------------------------------- |
| **Runtime**      | Live system behavior: traffic, latency, resource consumption, fault propagation |
| **Architecture** | System structure: service boundaries, data contracts, dependency graphs         |
| **Lifecycle**    | Dev process: CI/CD pipelines, test gates, branching, deployment, versioning     |
| **Organization** | Team structure, ownership, governance, and decision-making authority            |
| **Cognitive**    | Engineer judgment: design decisions, tradeoff reasoning, code review quality    |

---

## Maxim 1 — Stillness & Momentum

> _"Stillness is not the absence of momentum; it is the perfect containment of velocity."_

**Standard Mapping:** Rate limiting / Throttling / Steady-state design
**References:** ISO/IEC 25010 — Performance efficiency · NIST SP 800-53 SI-17 · SRE — SLO/SLA budgets

### Operational Semantics

| Field                        | Value                                                                      |
| ---------------------------- | -------------------------------------------------------------------------- |
| **Scope**                    | Runtime                                                                    |
| **Type**                     | Constraint                                                                 |
| **Applies to**               | API gateways, event queues, database connection pools, service mesh egress |
| **Failure mode if violated** | Cascade overload, thundering herd, OOM termination, queue saturation       |

A system without enforced flow control does not run faster — it destabilizes under load. Backpressure, circuit breakers, and rate limiting are not speed reducers; they are load-bearing constraints that make sustained throughput possible.

**Enforcement:** Every public-facing service MUST define a rate limit policy. Every internal service boundary MUST define a backpressure strategy. Absence of either is a defect, not a pending feature.

### Conflict Resolution

| Conflicts with                                                                                  | Resolution                                                                                                                                                                    |
| ----------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Maxim 5 (Ambition & Architecture)** — burst-scaling demands may challenge steady-state limits | Flow control wins at runtime. Scale headroom is an architectural pre-commitment, not a runtime exception. Design burst capacity in advance; do not disable limits reactively. |
| **Maxim 8 (Progress & Anchors)** — high deploy velocity creates transient traffic spikes        | Deployment pipelines MUST include canary/blue-green stages. Deploy velocity does not override traffic management constraints.                                                 |

---

## Maxim 2 — Foundation & Weight

> _"The foundation does not complain about the weight of the tower; it simply remembers that its primary purpose is to hold the ground."_

**Standard Mapping:** Infrastructure as code / Platform engineering
**References:** TOGAF — Technology Architecture · AWS Well-Architected — Reliability pillar · 12-Factor App — Factor VI

### Operational Semantics

| Field                        | Value                                                                                               |
| ---------------------------- | --------------------------------------------------------------------------------------------------- |
| **Scope**                    | Architecture · Runtime                                                                              |
| **Type**                     | Constraint                                                                                          |
| **Applies to**               | Compute orchestration, networking, secrets management, storage layers                               |
| **Failure mode if violated** | Platform becomes the incident surface; application teams own infrastructure defects they cannot fix |

Infrastructure is not a feature — it is a precondition. Platform teams own one deliverable: invisible, reliable load-bearing. A platform that requires workarounds is a platform that has failed its primary contract.

**Enforcement:** Infrastructure components MUST define and publish SLOs independently of application SLOs. Platform-layer incidents must be triaged by the platform team, not escalated to application owners.

### Conflict Resolution

| Conflicts with                                                                         | Resolution                                                                                                                                                         |
| -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Maxim 10 (Elegant Quiet)** — over-engineered infrastructure adds hidden complexity   | Foundation scope is load-bearing capability only. Any infrastructure component not directly supporting an application requirement is subject to Maxim 7 (Pruning). |
| **Maxim 6 (Logic & Intuition)** — experimental infrastructure introduced as spike work | Spike infrastructure MUST NOT share environment with production load-bearing components. Environments are strictly separated by maturity tier.                     |

---

## Maxim 3 — Light & Shadow

> _"We do not engineer light to destroy the dark; we build structures capable of casting the exact shadow we require."_

**Standard Mapping:** Security by design / Zero Trust
**References:** NIST SP 800-207 — Zero Trust Architecture · OWASP — Principle of least privilege · ISO/IEC 27001 — A.9

### Operational Semantics

| Field                        | Value                                                                                  |
| ---------------------------- | -------------------------------------------------------------------------------------- |
| **Scope**                    | Architecture · Runtime · Organization                                                  |
| **Type**                     | Constraint                                                                             |
| **Applies to**               | Identity and access management, network policy, API authorization, data classification |
| **Failure mode if violated** | Implicit trust surfaces, lateral movement risk, blast radius expansion on breach       |

**Scope Clarification (resolving prior ambiguity):**

| Layer                      | Application                                                                            |
| -------------------------- | -------------------------------------------------------------------------------------- |
| **Network**                | Allow-list ingress/egress rules; default-deny firewall policy                          |
| **Identity**               | Role-based access with minimum required permission set; no standing admin access       |
| **System-wide constraint** | Every service must declare its trust boundary explicitly; "implicit trust" is a defect |

Security posture is defined by the precision of what is permitted, not by the breadth of what is blocked.

**Enforcement:** Every service boundary MUST have an explicit trust policy. Undeclared implicit access is a security defect, not a configuration gap. IAM policies MUST be reviewed at each architecture milestone.

### Conflict Resolution

| Conflicts with                                                                                       | Resolution                                                                                                                                                            |
| ---------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Maxim 6 (Logic & Intuition)** — experimental services may lack full access policy on day one       | Spike environments operate in isolated, zero-production-data sandboxes. Security constraints apply in full to all production-adjacent systems regardless of maturity. |
| **Maxim 5 (Ambition & Architecture)** — new architectural domains may have incomplete trust modeling | Trust model must be declared (even if incomplete) before any component reaches staging. An incomplete trust model is a documented risk, not an acceptable gap.        |

---

## Maxim 4 — Failure as Signal

> _"A system achieves true optimization only when its failures become just as informative as its execution."_

**Standard Mapping:** Observability / Chaos engineering
**References:** SRE — Error budget & postmortems · OpenTelemetry — Traces, metrics, logs · DORA metrics — Change failure rate

### Operational Semantics

| Field                        | Value                                                                                           |
| ---------------------------- | ----------------------------------------------------------------------------------------------- |
| **Scope**                    | Runtime · Lifecycle · Cognitive                                                                 |
| **Type**                     | Constraint (observability) · Heuristic (chaos practice)                                         |
| **Applies to**               | All production services; all CI/CD pipelines; incident response processes                       |
| **Failure mode if violated** | Silent failures, unactionable alerts, unknown blast radius, repeated incidents without learning |

Failure without signal is indistinguishable from success. Every error path MUST emit structured, queryable data. Observability is not a feature; it is a pre-deployment requirement.

**Enforcement:** No service reaches production without: (1) structured logging with correlation IDs, (2) defined error rate SLO, (3) at least one synthetic availability probe. Blameless postmortems are mandatory for all P1/P2 incidents.

### Conflict Resolution

| Conflicts with                                                                                | Resolution                                                                                                                                                                   |
| --------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Maxim 7 (Precision & Pruning)** — pruning may remove instrumentation perceived as dead code | Observability instrumentation is exempt from YAGNI-based pruning decisions. Removal requires demonstrated zero usage across a 90-day production window.                      |
| **Maxim 10 (Elegant Quiet)** — comprehensive observability adds operational surface area      | Observation infrastructure complexity is explicitly permitted. Quiet operations depend on rich signal; suppressing signal in the name of simplicity is a false optimization. |

---

## Maxim 5 — Ambition & Architecture

> _"Ambition without architecture is merely a fire that consumes its own fuel before the hearth is even built."_

**Standard Mapping:** Architecture Decision Records / Domain-driven design
**References:** TOGAF ADM — Phase A–C · C4 Model — Context & container diagrams · IEEE Std 1471

### Operational Semantics

| Field                        | Value                                                                                         |
| ---------------------------- | --------------------------------------------------------------------------------------------- |
| **Scope**                    | Architecture · Organization · Lifecycle                                                       |
| **Type**                     | Guardrail                                                                                     |
| **Applies to**               | New service creation, domain expansion, API surface growth, team scaling                      |
| **Failure mode if violated** | Distributed monolith, implicit coupling, unmaintainable data model, context boundary collapse |

Feature velocity without structural pre-commitment is technical debt issued at compound interest. Every new service, domain, or significant API surface must be preceded by a declared bounded context, a data contract, and an ADR.

**Enforcement:** RFC or ADR sign-off is required before any new service, database schema, or public API is created. "We'll design it later" is a documented risk that requires explicit owner acceptance, not a default.

### Conflict Resolution

| Conflicts with                                                                               | Resolution                                                                                                                                                                    |
| -------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Maxim 7 (Precision & Pruning)** — architecture may expand scope while pruning contracts it | Expansion requires an ADR; contraction (deprecation) also requires an ADR. Neither overrides the other; they operate in sequence — design before build, prune after validate. |
| **Maxim 6 (Logic & Intuition)** — spike work intentionally precedes architecture             | Spikes are time-boxed and produce findings, not production artifacts. Architecture follows spikes; it does not follow from spikes automatically.                              |

---

## Maxim 6 — Logic & Intuition

> _"Logic traces the absolute boundary of the known world, but intuition is the deliberate step taken over the edge into solid air."_

**Standard Mapping:** Spike work / Proof-of-concept engineering
**References:** SAFe — Innovation & planning iterations · XP — Spike solution · Shape Up — Appetite & betting table

### Operational Semantics

| Field                        | Value                                                                                                                                 |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| **Scope**                    | Cognitive · Lifecycle                                                                                                                 |
| **Type**                     | Heuristic                                                                                                                             |
| **Applies to**               | Exploration of new technical domains, unproven integrations, novel architecture patterns                                              |
| **Failure mode if violated** | Paralysis by analysis (over-applying logic), or undisciplined experimentation that produces production debt (over-applying intuition) |

Formal analysis defines what is provably safe. Spikes extend past that boundary — deliberately, with a declared hypothesis, a timebox, and a clear definition of what output constitutes success or failure. Intuition without discipline is recklessness; discipline without intuition is stagnation.

**Enforcement:** Every spike MUST define: (1) the specific unknown being tested, (2) a timebox (default: 3 days), (3) a pass/fail condition, and (4) an explicit "does not go to production" declaration unless an ADR follows.

### Conflict Resolution

| Conflicts with                                                                                     | Resolution                                                                                                                  |
| -------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| **Maxim 2 (Foundation & Weight)** — spike infrastructure must not destabilize load-bearing systems | Spike work is environment-isolated. Production and staging environments are not spike environments.                         |
| **Maxim 3 (Light & Shadow)** — experimental access policies                                        | No spike may bypass production security constraints. Sandbox environments may have relaxed IAM for discovery purposes only. |

---

## Maxim 7 — Precision & Pruning

> _"True precision requires pruning. A masterwork is defined less by the mass of what remains, and more by the integrity of what was brave enough to be discarded."_

**Standard Mapping:** Technical debt reduction / API deprecation
**References:** SOLID — Single responsibility principle · Semantic versioning — Breaking change policy · YAGNI / KISS

### Operational Semantics

| Field                        | Value                                                                                                       |
| ---------------------------- | ----------------------------------------------------------------------------------------------------------- |
| **Scope**                    | Architecture · Lifecycle · Cognitive                                                                        |
| **Type**                     | Optimization (ongoing) · Guardrail (deprecation process)                                                    |
| **Applies to**               | Dead code, deprecated endpoints, unused feature flags, legacy pipelines, over-abstracted interfaces         |
| **Failure mode if violated** | Increasing cognitive load, false surface area in security audits, test suite fragility, onboarding friction |

The minimum correct surface area is the highest-quality surface area. Removal is a first-class engineering act. Every pruning decision MUST follow a deprecation protocol: announce, migrate, sunset, delete — in that sequence.

**Enforcement:** Deprecated endpoints MUST carry a sunset header. Removed code MUST have a linked ADR or PR description explaining the removal rationale. Feature flags older than 90 days with no active rollout MUST be scheduled for removal.

### Conflict Resolution

| Conflicts with                                                                                   | Resolution                                                                                                                                                            |
| ------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Maxim 4 (Failure as Signal)** — observability instrumentation should not be pruned prematurely | Instrumentation is exempt from YAGNI pruning. See Maxim 4 conflict resolution.                                                                                        |
| **Maxim 8 (Progress & Anchors)** — removing test coverage in the name of pruning                 | Test coverage is an anchor, not dead weight. Removing tests requires demonstrated redundancy, not just low recent execution frequency.                                |
| **Maxim 5 (Ambition & Architecture)** — architecture expands while pruning contracts             | These operate in lifecycle phases. Pruning is a post-validate operation; architectural expansion is a pre-build operation. They do not compete within the same phase. |

---

## Maxim 8 — Progress & Anchors

> _"Do not measure progress solely by the distance from your origin, but by the density and stability of the anchors you have set along the way."_

**Standard Mapping:** CI/CD pipelines / Test coverage
**References:** DORA metrics — Deployment frequency · IEEE Std 829 — Test documentation · Trunk-based development

### Operational Semantics

| Field                        | Value                                                                                  |
| ---------------------------- | -------------------------------------------------------------------------------------- |
| **Scope**                    | Lifecycle · Organization                                                               |
| **Type**                     | Constraint (gate integrity) · Optimization (anchor density)                            |
| **Applies to**               | All software delivery pipelines, release processes, environment promotion criteria     |
| **Failure mode if violated** | Undetected regressions, unverifiable release state, rollback ambiguity, false velocity |

Deployment frequency without checkpoint integrity is drift with momentum. Every anchor — a passing CI gate, an immutable build artifact, a signed release tag — is a verifiable point of truth. DORA metrics measure anchor density and stability, not speed alone.

**Enforcement:** No artifact may be promoted to a higher environment without passing the full gate set of the originating environment. Gates may not be bypassed without a documented incident exception signed by the service owner. Manual hotfix deployments require a retroactive gate audit within 24 hours.

### Conflict Resolution

| Conflicts with                                                                              | Resolution                                                                                                                                                        |
| ------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Maxim 1 (Stillness & Momentum)** — high deploy frequency creates transient traffic spikes | Deployment pipelines must include traffic-graduated rollout strategies. Frequency does not override traffic management.                                           |
| **Maxim 7 (Precision & Pruning)** — pruning test coverage reduces anchor density            | Anchor removal requires demonstrated redundancy, not inferred cleanup. A removed test is a removed anchor; the justification burden is on removal, not retention. |

---

## Maxim 9 — Friction as Interface

> _"Friction is never a flaw in the engine; it is the precise interface where design meets reality."_

**Standard Mapping:** Code review / Change management
**References:** ITIL 4 — Change enablement practice · Google Engineering Practices — Code review · ISO/IEC 12207

### Operational Semantics

| Field                        | Value                                                                                                                       |
| ---------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| **Scope**                    | Lifecycle · Organization · Cognitive                                                                                        |
| **Type**                     | Guardrail                                                                                                                   |
| **Applies to**               | Pull request review, static analysis gates, security scanning, architectural review boards, change advisory                 |
| **Failure mode if violated** | Implicit assumptions reach production, quality signal is lost, individual bias is unchecked, blast radius of errors expands |

Review friction is calibrated friction — it is the designed interface between individual intent and collective production reality. Calibration is the discipline: too little friction loses signal; too much friction stops work. The goal is minimum sufficient friction for the risk level of the change.

**Friction Calibration Model:**

| Change Risk Level                        | Required Gates                                                                   |
| ---------------------------------------- | -------------------------------------------------------------------------------- |
| Low (docs, config, tests)                | 1 peer review · automated lint/test                                              |
| Medium (feature, refactor)               | 1 senior review · full CI · security scan                                        |
| High (schema, API contract, infra)       | 2 reviews (1 must be arch owner) · full CI · security · ADR linked               |
| Critical (auth, payment, data migration) | Arch review board sign-off · staged rollout plan · rollback procedure documented |

**Enforcement:** Removing a required review gate is a governance decision, not an engineering shortcut. Gate removal requires service owner + security owner approval.

### Conflict Resolution

| Conflicts with                                                                            | Resolution                                                                                                                                                                                      |
| ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Maxim 6 (Logic & Intuition)** — spike work should not be slowed by full review friction | Spike PRs use the Low friction tier regardless of scope, with an explicit "not for production" label. The moment spike output is proposed for production, it escalates to the appropriate tier. |
| **Maxim 8 (Progress & Anchors)** — review gates may slow deployment frequency             | Gate optimization (parallelization, automation, caching) is the correct response to friction-vs-velocity tension. Gate removal is not.                                                          |

---

## Maxim 10 — Elegant Quiet

> _"The ultimate maturity of any architecture is not hyper-complexity, but an elegant, functional quiet."_

**Standard Mapping:** Evolutionary architecture / System maturity
**References:** ISO/IEC 25010 — Maintainability · CNCF Cloud Native Maturity Model · Conway's Law

### Operational Semantics

| Field                        | Value                                                                                                         |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------- |
| **Scope**                    | Architecture · Runtime · Organization                                                                         |
| **Type**                     | Optimization (target state) · Heuristic (ongoing design signal)                                               |
| **Applies to**               | System architecture, operational runbooks, on-call burden, onboarding time, incident frequency                |
| **Failure mode if violated** | Complexity debt: systems that require tribal knowledge, heroic on-call effort, or expert-only maintainability |

Operational quiet is the lagging indicator of architectural quality. A system where deployments are boring, runbooks are short, on-call is infrequent, and new engineers are productive within days has achieved it. Complexity that cannot be justified by a load-bearing requirement is a liability.

**Maturity Signal Metrics:**

| Metric                            | Target (Optimizing Tier)        |
| --------------------------------- | ------------------------------- |
| Mean time to onboard new engineer | < 3 days to first PR merged     |
| P1 incident frequency             | < 1 per quarter per service     |
| Runbook page count                | < 5 pages per service           |
| Deployment duration               | < 15 minutes gate-to-production |
| Services without an owner         | 0                               |

**Enforcement:** Architectural complexity additions must pass a "load-bearing test": does this component directly support a declared requirement? If not, it is subject to Maxim 7 (Pruning) review.

### Conflict Resolution

| Conflicts with                                                                          | Resolution                                                                                                                                                                                       |
| --------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Maxim 4 (Failure as Signal)** — observability infrastructure adds operational surface | Observability is explicitly load-bearing for operational quiet. Rich signal enables quiet operations. Observation tooling is exempt from complexity reduction.                                   |
| **Maxim 5 (Ambition & Architecture)** — architectural growth conflicts with minimalism  | Growth is a lifecycle phase; quiet is a maturity phase. They do not compete simultaneously. Evaluate quiet-target against the system's current lifecycle phase, not its theoretical final state. |
| **Maxim 2 (Foundation & Weight)** — platform depth may appear as unnecessary complexity | Foundation components are load-bearing by definition. Complexity reduction applies to the application layer; infrastructure depth is evaluated by the platform team against its own SLO targets. |

---

## System-Level Conflict Precedence

When two or more maxims conflict in a real decision, apply this precedence order:

```
1. Constraint maxims always take precedence over Guardrail maxims.
2. Guardrail maxims always take precedence over Heuristic maxims.
3. Heuristic maxims take precedence over Optimization maxims.
4. Within the same type tier, the maxim whose scope matches the decision context takes precedence.
5. If scope also ties, document the conflict as a tradeoff in an ADR and apply the maxim most conservative with respect to system stability.
```

### Quick-Reference Precedence Table

| Maxim                       | Type                      | Precedence Tier |
| --------------------------- | ------------------------- | --------------- |
| 1 — Stillness & Momentum    | Constraint                | 1               |
| 2 — Foundation & Weight     | Constraint                | 1               |
| 3 — Light & Shadow          | Constraint                | 1               |
| 4 — Failure as Signal       | Constraint / Heuristic    | 1 / 3           |
| 8 — Progress & Anchors      | Constraint / Optimization | 1 / 4           |
| 9 — Friction as Interface   | Guardrail                 | 2               |
| 5 — Ambition & Architecture | Guardrail                 | 2               |
| 7 — Precision & Pruning     | Optimization / Guardrail  | 4 / 2           |
| 6 — Logic & Intuition       | Heuristic                 | 3               |
| 10 — Elegant Quiet          | Optimization / Heuristic  | 4 / 3           |

---

## Operational Redundancy Resolution

Three maxims (1, 8, 9) were identified as operationally adjacent — all governing controlled system dynamics under feedback constraints. Their domains are distinct:

| Maxim                         | Governs                                           |
| ----------------------------- | ------------------------------------------------- |
| **1 — Stillness & Momentum**  | Runtime traffic and resource flow constraints     |
| **8 — Progress & Anchors**    | Lifecycle delivery checkpoints and gate integrity |
| **9 — Friction as Interface** | Human review and change governance quality signal |

They share a structural pattern (controlled flow via deliberate resistance) but apply to non-overlapping system layers. Treat them as three instantiations of one underlying principle across runtime, lifecycle, and organizational scope respectively.

---

_Ten Maxims Governance Model — v1.1_
_Upgrade from: philosophical-to-engineering mapping (v1.0)_
_Status: Operational specification — suitable for ADR reference, engineering handbook inclusion, and architecture review board use_
