# src/trust_model.py

"""
Simple trust model for vehicle subsystems.

Each subsystem (ENGINE, STEERING, BRAKE) has a trust score in [0, 100].
- Starts at 100 (fully trusted).
- Drops sharply when an attack is detected on that subsystem.
- Recovers slowly over time when no attacks are happening.

This is not ML; it's a transparent, rule-based trust mechanism that makes
the framework look more like a real "cyber-resilience" system.
"""

from dataclasses import dataclass, field
from typing import Dict, Iterable


DEFAULT_SUBSYSTEMS = ("ENGINE", "STEERING", "BRAKE")


@dataclass
class TrustManager:
    """
    Track and update trust scores for each subsystem.

    Usage:
        tm = TrustManager()
        tm.update("ENGINE", is_attack=True)
        snapshot = tm.get_trust_snapshot()
    """

    subsystems: Iterable[str] = field(default_factory=lambda: DEFAULT_SUBSYSTEMS)
    initial_trust: float = 100.0
    attack_drop: float = 25.0      # how much to drop on each attack
    recovery_step: float = 1.0     # how much to recover per clean step

    trust: Dict[str, float] = field(init=False)

    def __post_init__(self) -> None:
        self.trust = {name: float(self.initial_trust) for name in self.subsystems}

    def update(self, subsystem: str, is_attack: bool) -> None:
        """
        Update trust scores given the current step.

        - If attack on subsystem S: trust[S] -= attack_drop (min 0).
        - If no attack: all subsystems slowly recover by recovery_step (max 100).
        """
        if is_attack and subsystem in self.trust:
            self.trust[subsystem] = max(0.0, self.trust[subsystem] - self.attack_drop)
        else:
            # small recovery for all subsystems
            for name in self.trust:
                self.trust[name] = min(100.0, self.trust[name] + self.recovery_step)

    def get_trust_snapshot(self) -> Dict[str, float]:
        """
        Return a copy of the current trust state for logging / display.
        """
        return dict(self.trust)
