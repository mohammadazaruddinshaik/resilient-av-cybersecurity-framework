# src/safety_controller.py

"""
Safety controller for the autonomous vehicle.

Takes:
    - IDSResult (rule-based IDS decision)
    - trust_snapshot (per-subsystem trust scores)

Returns:
    - safety_action: string describing what the vehicle should do.

Actions used by Vehicle.apply_safety_override():
    - "NONE"            : no additional safety action
    - "CUT_ENGINE"      : cut engine power
    - "EMERGENCY_BRAKE" : brake hard and go to SAFE_STOP
"""

from dataclasses import dataclass
from typing import Dict

from .attacker import ATTACK


@dataclass
class SafetyConfig:
    # Trust thresholds for stronger actions
    low_trust_threshold: float = 50.0  # below this = low trust
    very_low_trust_threshold: float = 25.0  # optional, for more aggressive response


def decide_safety_action(ids_result, trust_snapshot: Dict[str, float], config: SafetyConfig | None = None) -> str:
    """
    Decide what safety action to take based on IDS result and trust levels.

    Basic idea:
      - If no attack: return "NONE".
      - If attack:
          - ENGINE_ATTACK:
               high trust   -> CUT_ENGINE (mild)
               low trust    -> EMERGENCY_BRAKE (aggressive)
          - STEERING_ATTACK:
               always EMERGENCY_BRAKE (steering is critical)
          - BRAKE_ATTACK:
               always EMERGENCY_BRAKE
          - default:
               EMERGENCY_BRAKE (fail-safe)
    """
    if config is None:
        config = SafetyConfig()

    # no attack → no safety action
    if ids_result.status != ATTACK:
        return "NONE"

    subsystem = ids_result.subsystem or ""
    attack_type = ids_result.attack_type or ""
    trust = float(trust_snapshot.get(subsystem, 100.0))

    # --- Steering & brake are very safety-critical ---
    if "STEERING" in attack_type:
        # Any steering attack → hard stop
        return "EMERGENCY_BRAKE"

    if "BRAKE" in attack_type:
        # Brake spoofing → hard stop
        return "EMERGENCY_BRAKE"

    # --- Engine attacks: severity depends on trust ---
    if "ENGINE" in attack_type:
        if trust < config.low_trust_threshold:
            # We already distrust this subsystem → go aggressive
            return "EMERGENCY_BRAKE"
        else:
            # First or rare engine anomaly → try CUT_ENGINE first
            return "CUT_ENGINE"

    # --- Fallback: unknown attack type → safe side ---
    return "EMERGENCY_BRAKE"
