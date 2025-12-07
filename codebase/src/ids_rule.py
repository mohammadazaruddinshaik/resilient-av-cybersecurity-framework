# ids_rule.py

from .attacker import ENGINE, STEERING, BRAKE, NORMAL, ATTACK

class IDSResult:
    def __init__(self, status, attack_type=None, subsystem=None, reason=None):
        self.status = status
        self.attack_type = attack_type
        self.subsystem = subsystem
        self.reason = reason

def detect_attack_rule(cmd, vehicle_state):
    subsystem = cmd["subsystem"]
    value = cmd["value"]
    speed = vehicle_state.speed

    # default normal
    result = IDSResult(status=NORMAL)

    # ENGINE attack: strong throttle OR throttle at moderately high speed
    if subsystem == ENGINE:
        if value > 0.8 or (value > 0.5 and speed > 40):
            return IDSResult(
                status=ATTACK,
                attack_type="ENGINE_ATTACK",
                subsystem=ENGINE,
                reason=f"Suspicious engine command {value:.2f} at speed {speed:.1f}",
            )

    # STEERING attack: large steering jump
    if subsystem == STEERING:
        if abs(value) > 1.5:
            return IDSResult(
                status=ATTACK,
                attack_type="STEERING_ATTACK",
                subsystem=STEERING,
                reason=f"Abnormal steering command {value:.2f}",
            )

    # BRAKE attack: brake fully released when moving at moderate speed
    if subsystem == BRAKE:
        if value == 0.0 and speed > 30:
            return IDSResult(
                status=ATTACK,
                attack_type="BRAKE_ATTACK",
                subsystem=BRAKE,
                reason=f"Brake release at speed {speed:.1f}",
            )

    return result
