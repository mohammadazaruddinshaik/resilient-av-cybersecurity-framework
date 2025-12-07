# src/vehicle.py
from dataclasses import dataclass

@dataclass
class VehicleState:
    speed: float = 0.0
    steering_angle: float = 0.0
    mode: str = "AUTO"   # AUTO, SAFE_ENGINE, SAFE_STOP

class Vehicle:
    def __init__(self) -> None:
        self.state = VehicleState(speed=40.0, steering_angle=0.0, mode="AUTO")

    def apply_command(self, cmd: dict) -> None:
        if self.state.mode == "SAFE_STOP":
            return

        subsystem = cmd["subsystem"]
        value = float(cmd["value"])

        if subsystem == "ENGINE":
            self.state.speed = max(0.0, self.state.speed + value * 5)
        elif subsystem == "STEERING":
            new_angle = self.state.steering_angle + value * 10
            self.state.steering_angle = max(-30.0, min(30.0, new_angle))
        elif subsystem == "BRAKE":
            self.state.speed = max(0.0, self.state.speed - value * 10)

    def apply_safety_override(self, action: str) -> None:
        if action == "NONE":
            return
        if action == "EMERGENCY_BRAKE":
            self.state.mode = "SAFE_STOP"
            self.state.speed = max(0.0, self.state.speed - 20.0)
        elif action == "CUT_ENGINE":
            self.state.mode = "SAFE_ENGINE"
            self.state.speed = max(0.0, self.state.speed - 5.0)

    def tick(self) -> None:
        if self.state.mode in ("AUTO", "SAFE_ENGINE") and self.state.speed > 0:
            self.state.speed = max(0.0, self.state.speed - 0.5)
