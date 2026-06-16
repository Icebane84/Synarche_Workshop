"""
artifact_anchor:
  id: CORE.GOVERNANCE_ENGINE.001
  version: v15.0 [OMEGA]
  provenance: '2026-06-09'
  domain: CORE
  celestial_class: STAR
  tier: GOVERNANCE
  state: ACTIVE
  ethos: SOVEREIGN_LOGIC_COMPONENT
  relations: []
"""

"""### **Block A: The Identification Lock (UIP-V15)**.

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID**     | `CSE-VAL-GOV-001`             | The Sovereign ID. |
| **Official Name**   | `governance_engine.py`        | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**             | The Standard.     |
| **Domain**          | `CSE-VAL`                     | The Subject.      |
| **Celestial Class** | `[STAR]`                      | The Weight.       |
| **Evolution**       | `PAD-SIP Layer C`             | The Maturity.     |
| **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**       | `IDENTITY: High Priestess`    | The Sovereign.    |
# Cognitive Load Cost: Medium

**The Spirit Bomb Axiom: Ethical Governance (Law 17)**
> Implemented from Blueprint `PAD-SIP.Layer.C.GovernanceDSL`.
> Ethos: Rules without enforcement are mere suggestions.
"""

import json
import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger("PhoenixLogger")

# ---------------------------------------------------------------------------
# §1  Rule dataclass
# ---------------------------------------------------------------------------

_OPERATORS = {
    "gt": lambda a, b: a > b,
    "gte": lambda a, b: a >= b,
    "lt": lambda a, b: a < b,
    "lte": lambda a, b: a <= b,
    "eq": lambda a, b: a == b,
    "neq": lambda a, b: a != b,
}


@dataclass
class GovernanceRule:
    """A single governance rule loaded from the JSON DSL.

    Attributes:
        rule_id     : stable identifier (e.g. "GOV-001").
        name        : machine-readable rule name.
        description : human-readable description.
        field       : the CognitiveState field this rule inspects.
        op          : comparison operator string (gt | gte | lt | lte | eq | neq).
        value       : threshold value to compare against.
        effect      : the effect string executed when the condition is true.
        priority    : higher priority rules are evaluated first.
        enabled     : if False the rule is skipped entirely.
    """

    rule_id: str
    name: str
    description: str
    field: str
    op: str
    value: Any
    effect: str
    priority: int = 50
    enabled: bool = True

    def evaluate(self, context: Dict[str, Any]) -> bool:
        """Return True if the rule condition is satisfied by the given context dict.

        Args:
            context: A flat dict of field-name → current value.

        Returns:
            bool: True if the condition fires (effect should be applied).
        """
        actual = context.get(self.field)
        if actual is None:
            return False
        comparator = _OPERATORS.get(self.op)
        if comparator is None:
            logger.warning(f"[GOV] Unknown operator '{self.op}' in rule {self.rule_id}")
            return False
        try:
            return comparator(actual, self.value)
        except TypeError:
            return False


# ---------------------------------------------------------------------------
# §2  GovernanceVerdict
# ---------------------------------------------------------------------------


@dataclass
class GovernanceVerdict:
    """Result object produced by GovernanceEngine.evaluate().

    Attributes:
        rule_id : the rule that fired.
        effect  : the prescribed effect to apply.
        field   : the field that triggered the rule.
        actual  : the actual observed field value.
        threshold: the threshold defined by the rule.
    """

    rule_id: str
    effect: str
    field: str
    actual: Any
    threshold: Any

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "effect": self.effect,
            "field": self.field,
            "actual": self.actual,
            "threshold": self.threshold,
        }


# ---------------------------------------------------------------------------
# §3  GovernanceEngine
# ---------------------------------------------------------------------------

# Default path resolution relative to this file → axion-core/data/
_DEFAULT_RULES_PATH = (
    Path(__file__).resolve().parent.parent.parent.parent / "data" / "governance_rules.json"
)


class GovernanceEngine:
    """Dynamic, JSON/DSL-driven governance evaluator for the Axion Cognitive OS.

    Implements PAD-SIP Layer C — it loads rules from a JSON file and exposes
    an `evaluate()` method that accepts a flat context dict and returns a list
    of GovernanceVerdicts for every rule whose condition fires.

    Rules can also be added at runtime via `register_rule()`, enabling programmatic
    governance policies on top of the file-based ones.

    Usage::

        engine = GovernanceEngine()
        verdicts = engine.evaluate(cognitive_state.to_dict())
        for v in verdicts:
            handler = engine.get_effect_handler(v.effect)
            if handler:
                handler(state)
    """

    def __init__(self, rules_path: Optional[str] = None) -> None:
        """Initialise the engine, loading rules from the governance_rules.json file.

        Args:
            rules_path: Absolute path to the rules JSON file.
                        Defaults to axion-core/data/governance_rules.json.
        """
        self._rules: List[GovernanceRule] = []
        self._effect_handlers: Dict[str, Any] = {}

        resolved = Path(rules_path) if rules_path else _DEFAULT_RULES_PATH
        self._load_rules(resolved)
        logger.info(f"[GOV] GovernanceEngine initialised with {len(self._rules)} rules from {resolved}")

    # ------------------------------------------------------------------
    # Rule loading
    # ------------------------------------------------------------------

    def _load_rules(self, path: Path) -> None:
        """Parse governance_rules.json and populate self._rules."""
        if not path.exists():
            logger.warning(f"[GOV] Rules file not found at {path}. Engine will have no rules.")
            return

        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            raw_rules = data.get("rules", [])
            for r in raw_rules:
                if not r.get("enabled", True):
                    continue
                cond = r.get("condition", {})
                rule = GovernanceRule(
                    rule_id=r["id"],
                    name=r["rule"],
                    description=r.get("description", ""),
                    field=cond["field"],
                    op=cond["op"],
                    value=cond["value"],
                    effect=r["effect"],
                    priority=r.get("priority", 50),
                    enabled=r.get("enabled", True),
                )
                self._rules.append(rule)
            # Sort descending by priority so high-priority rules fire first
            self._rules.sort(key=lambda x: x.priority, reverse=True)
        except Exception:
            logger.exception("[GOV] Failed to load governance rules")

    def reload_rules(self, rules_path: Optional[str] = None) -> int:
        """Hot-reload rules from disk without restarting the engine.

        Returns:
            int: Number of rules successfully loaded.
        """
        self._rules.clear()
        resolved = Path(rules_path) if rules_path else _DEFAULT_RULES_PATH
        self._load_rules(resolved)
        return len(self._rules)

    def register_rule(self, rule: GovernanceRule) -> None:
        """Add a governance rule programmatically at runtime.

        Args:
            rule: A GovernanceRule instance to append and re-sort.
        """
        self._rules.append(rule)
        self._rules.sort(key=lambda x: x.priority, reverse=True)
        logger.info(f"[GOV] Runtime rule registered: {rule.rule_id} ({rule.name})")

    # ------------------------------------------------------------------
    # Effect handler registry
    # ------------------------------------------------------------------

    def register_effect_handler(self, effect: str, handler: Any) -> None:
        """Bind a callable to an effect string.

        When a verdict with this effect is produced, callers can retrieve
        and invoke the handler via get_effect_handler().

        Args:
            effect  : the effect string defined in the rule (e.g. "trigger_maintenance_cycle").
            handler : any callable accepting a single argument (the CognitiveState).
        """
        self._effect_handlers[effect] = handler
        logger.debug(f"[GOV] Effect handler registered for '{effect}'")

    def get_effect_handler(self, effect: str) -> Optional[Any]:
        """Retrieve the callable bound to an effect string, or None.

        Args:
            effect: effect string from a GovernanceVerdict.

        Returns:
            callable or None.
        """
        return self._effect_handlers.get(effect)

    # ------------------------------------------------------------------
    # Core evaluation
    # ------------------------------------------------------------------

    def evaluate(self, context: Dict[str, Any]) -> List[GovernanceVerdict]:
        """Evaluate all enabled rules against a context dict.

        Args:
            context: A flat dict of field-name → current value.
                     Typically built from CognitiveState.to_dict() plus any
                     action-specific fields like "action_risk_score".

        Returns:
            List[GovernanceVerdict]: All verdicts for rules whose conditions fired,
            ordered by descending priority.
        """
        verdicts: List[GovernanceVerdict] = []
        for rule in self._rules:
            if not rule.enabled:
                continue
            if rule.evaluate(context):
                verdict = GovernanceVerdict(
                    rule_id=rule.rule_id,
                    effect=rule.effect,
                    field=rule.field,
                    actual=context.get(rule.field),
                    threshold=rule.value,
                )
                verdicts.append(verdict)
                logger.info(
                    f"[GOV] Rule fired | {rule.rule_id} '{rule.name}' "
                    f"→ effect='{rule.effect}' | {rule.field}={context.get(rule.field)}"
                )

        return verdicts

    def evaluate_single(self, rule_id: str, context: Dict[str, Any]) -> Optional[GovernanceVerdict]:
        """Evaluate a single rule by its ID.

        Args:
            rule_id : the rule's stable ID string.
            context : flat context dict.

        Returns:
            GovernanceVerdict if the rule fires, else None.
        """
        for rule in self._rules:
            if rule.rule_id == rule_id:
                if rule.evaluate(context):
                    return GovernanceVerdict(
                        rule_id=rule.rule_id,
                        effect=rule.effect,
                        field=rule.field,
                        actual=context.get(rule.field),
                        threshold=rule.value,
                    )
                return None
        logger.warning(f"[GOV] Rule ID '{rule_id}' not found")
        return None

    # ------------------------------------------------------------------
    # Introspection helpers
    # ------------------------------------------------------------------

    def list_rules(self) -> List[Dict[str, Any]]:
        """Return all loaded rules as plain dicts (for display / debugging)."""
        return [
            {
                "id": r.rule_id,
                "name": r.name,
                "field": r.field,
                "op": r.op,
                "value": r.value,
                "effect": r.effect,
                "priority": r.priority,
                "enabled": r.enabled,
            }
            for r in self._rules
        ]

    def __repr__(self) -> str:
        return f"<GovernanceEngine rules={len(self._rules)} handlers={len(self._effect_handlers)}>"
