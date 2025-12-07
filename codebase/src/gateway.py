# src/gateway.py

"""
Gateway / Safety Island module.

Acts as a firewall ECU between other ECUs (including attacker)
and the actual actuators (Vehicle).

Responsibilities:
  - Inspect every incoming command
  - Run rule-based IDS
  - Check source (CONTROL_ECU vs ATTACKER_ECU)
  - Decide whether to:
      * ALLOW  : forward as-is
      * BLOCK  : drop completely
      * SANITIZE: forward a safe/clamped version

This is an alternative architecture to "IDS inside vehicle":
here, the gateway is the brain in the middle of the network.
"""

from dataclasses import dataclass
from typing import Optional, Dict

from .ids_rule import detect_attack_rule, IDSResult
from .attacker import ATTACK, ENGINE, STEERING, BRAKE


@dataclass
class GatewayDecision:
    forwarded_cmd: Optional[dict]  # command after filtering (or None if blocked)
    action: str                    # "ALLOW" | "BLOCK" | "SANITIZE"
    ids_result: IDSResult
    reason: str
    source: str                    # which ECU sent it


class Gateway:
    """
    Simple gateway / safety island.

    For now, policy is:
      - If IDS says ATTACK and source is ATTACKER_ECU -> BLOCK
      - If IDS says ATTACK but source is CONTROL_ECU -> SANITIZE (clamp value)
      - Otherwise -> ALLOW
    """

    def __init__(self) -> None:
        # could hold policy tables, trust per source, etc.
        pass

    def sanitize_value(self, subsystem: str, value: float) -> float:
        """
        Clamp values into safe ranges for each subsystem.

        This is the "firewall cleaning" stage.
        """
        if subsystem == ENGINE:
            # allow only gentle accel/decel
            return max(-0.3, min(0.3, value))
        if subsystem == STEERING:
            # limit steering angle change
            return max(-0.4, min(0.4, value))
        if subsystem == BRAKE:
            # avoid extreme brake spikes
            return max(0.0, min(0.6, value))
        return value

    def process_command(self, cmd: dict, vehicle_state) -> GatewayDecision:
        """
        Inspect and decide how to handle the incoming command.

        cmd must contain:
          - subsystem: ENGINE/STEERING/BRAKE
          - value: float
          - is_attack: bool (from attacker)
          - attack_type: optional str
          - source: "CONTROL_ECU" | "ATTACKER_ECU" | something else
        """
        source = cmd.get("source", "UNKNOWN")
        ids_result = detect_attack_rule(cmd, vehicle_state)
        is_attack = ids_result.status == ATTACK
        subsystem = cmd["subsystem"]
        value = cmd["value"]

        # CASE 1: Attack from known attacker source -> BLOCK
        if is_attack and source == "ATTACKER_ECU":
            return GatewayDecision(
                forwarded_cmd=None,
                action="BLOCK",
                ids_result=ids_result,
                reason="Malicious command from ATTACKER_ECU blocked at gateway.",
                source=source,
            )

        # CASE 2: Attack from a nominal ECU -> SANITIZE
        if is_attack:
            safe_value = self.sanitize_value(subsystem, value)
            safe_cmd = dict(cmd)
            safe_cmd["value"] = safe_value
            return GatewayDecision(
                forwarded_cmd=safe_cmd,
                action="SANITIZE",
                ids_result=ids_result,
                reason="Malicious value sanitized to safe range by gateway.",
                source=source,
            )

        # CASE 3: No attack -> ALLOW
        return GatewayDecision(
            forwarded_cmd=cmd,
            action="ALLOW",
            ids_result=ids_result,
            reason="Command considered safe by IDS.",
            source=source,
        )
