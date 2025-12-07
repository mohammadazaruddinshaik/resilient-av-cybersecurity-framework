# src/logger.py

import csv
import os
from datetime import datetime
from typing import Dict


class RunLogger:
    """
    Simple CSV logger for each simulation run.

    Each row = one simulation step:
        step, timestamp, speed, steering_angle,
        cmd_subsystem, cmd_value,
        ids_status, attack_type, safety_action, mode,
        engine_trust, steering_trust, brake_trust
    """

    def __init__(self) -> None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        os.makedirs("logs", exist_ok=True)
        self.filepath = f"logs/simulation_run_{timestamp}.csv"

        self.file = open(self.filepath, "w", newline="")
        self.writer = csv.writer(self.file)

        # CSV header
        self.writer.writerow(
            [
                "step",
                "timestamp",
                "speed",
                "steering_angle",
                "cmd_subsystem",
                "cmd_value",
                "ids_status",
                "attack_type",
                "safety_action",
                "mode",
                "engine_trust",
                "steering_trust",
                "brake_trust",
            ]
        )

    def log(
        self,
        step: int,
        vehicle,
        cmd: dict,
        ids_result,
        safety_action: str,
        trust_snapshot: Dict[str, float],
    ) -> None:
        """Log one simulation step."""
        self.writer.writerow(
            [
                step,
                datetime.now().isoformat(timespec="milliseconds"),
                f"{vehicle.state.speed:.3f}",
                f"{vehicle.state.steering_angle:.3f}",
                cmd["subsystem"],
                f"{cmd['value']:.4f}",
                ids_result.status,
                ids_result.attack_type or "",
                safety_action,
                vehicle.state.mode,
                f"{trust_snapshot.get('ENGINE', 0.0):.1f}",
                f"{trust_snapshot.get('STEERING', 0.0):.1f}",
                f"{trust_snapshot.get('BRAKE', 0.0):.1f}",
            ]
        )

    def close(self) -> None:
        """Close file when simulation ends."""
        self.file.close()
        print(f"[LOG] Saved run log to: {self.filepath}")
