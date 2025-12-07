# src/experiment_runner.py

"""
Experiment runner for the AV cyber-resilience framework.

Purpose:
    - Run multiple simulations programmatically (no console UI).
    - Vary attack probability.
    - Collect metrics such as:
        * number of attack commands
        * number of detected attacks
        * number of safety actions
        * fraction of runs that reach SAFE_STOP after an attack
    - Save a CSV summary to reports/experiment_results.csv

Run from project root:

    python -m src.experiment_runner
"""

import csv
import os
from dataclasses import dataclass
from typing import List

from .vehicle import Vehicle
from .attacker import maybe_generate_command, ATTACK
from .ids_rule import detect_attack_rule
from .trust_model import TrustManager
from .safety_controller import decide_safety_action
from .config import SIMULATION_STEPS


@dataclass
class RunMetrics:
    attack_probability: float
    steps: int
    attack_commands: int
    detected_attacks: int
    emergency_brakes: int
    cut_engine_actions: int
    safe_stop_reached: bool


def run_single_simulation(attack_probability: float) -> RunMetrics:
    """
    Run one simulation (no rich UI, no logging to CSV),
    only collect metrics.
    """
    vehicle = Vehicle()
    trust_manager = TrustManager()

    steps = 0
    attack_commands = 0
    detected_attacks = 0
    emergency_brakes = 0
    cut_engine_actions = 0
    safe_stop_reached = False

    while steps < SIMULATION_STEPS:
        steps += 1

        cmd = maybe_generate_command(attack_probability=attack_probability)
        ids_result = detect_attack_rule(cmd, vehicle.state)

        is_attack = ids_result.status == ATTACK
        if is_attack:
            attack_commands += 1

        # Update trust
        trust_manager.update(cmd["subsystem"], is_attack=is_attack)
        trust_snapshot = trust_manager.get_trust_snapshot()

        # Safety decision
        safety_action = decide_safety_action(ids_result, trust_snapshot)

        if safety_action == "EMERGENCY_BRAKE":
            emergency_brakes += 1
        if safety_action == "CUT_ENGINE":
            cut_engine_actions += 1

        if is_attack:
            detected_attacks += 1  # since IDS is rule-based and deterministic here

        # Apply safety & command
        vehicle.apply_safety_override(safety_action)

        if not (vehicle.state.mode == "SAFE_STOP" and is_attack):
            vehicle.apply_command(cmd)

        vehicle.tick()

        # Check if we reached SAFE_STOP after attack
        if vehicle.state.mode == "SAFE_STOP" and is_attack:
            safe_stop_reached = True
            break

    return RunMetrics(
        attack_probability=attack_probability,
        steps=steps,
        attack_commands=attack_commands,
        detected_attacks=detected_attacks,
        emergency_brakes=emergency_brakes,
        cut_engine_actions=cut_engine_actions,
        safe_stop_reached=safe_stop_reached,
    )


def aggregate_metrics(metrics_list: List[RunMetrics]) -> dict:
    """
    Aggregate a list of RunMetrics into averages and rates.
    """
    n = len(metrics_list)
    if n == 0:
        return {}

    total_attacks = sum(m.attack_commands for m in metrics_list)
    total_detected = sum(m.detected_attacks for m in metrics_list)
    total_em_brakes = sum(m.emergency_brakes for m in metrics_list)
    total_cut_engine = sum(m.cut_engine_actions for m in metrics_list)
    safe_stop_runs = sum(1 for m in metrics_list if m.safe_stop_reached)

    avg_attacks_per_run = total_attacks / n
    avg_em_brakes_per_run = total_em_brakes / n

    detection_rate = (
        total_detected / total_attacks if total_attacks > 0 else 0.0
    )
    safe_stop_rate = safe_stop_runs / n

    return {
        "num_runs": n,
        "total_attacks": total_attacks,
        "total_detected": total_detected,
        "total_emergency_brakes": total_em_brakes,
        "total_cut_engine": total_cut_engine,
        "avg_attacks_per_run": avg_attacks_per_run,
        "avg_em_brakes_per_run": avg_em_brakes_per_run,
        "detection_rate": detection_rate,
        "safe_stop_rate": safe_stop_rate,
    }


def main() -> None:
    # You can tune these to create multiple experiment settings
    attack_probs = [0.1, 0.3, 0.5]
    runs_per_setting = 5

    os.makedirs("reports", exist_ok=True)
    out_csv = "reports/experiment_results.csv"

    print("[*] Running experiments...")
    print(f"    Attack probabilities: {attack_probs}")
    print(f"    Runs per setting    : {runs_per_setting}")
    print(f"    Simulation steps/run: {SIMULATION_STEPS}")

    rows = []
    header = [
        "attack_probability",
        "num_runs",
        "total_attacks",
        "total_detected",
        "total_emergency_brakes",
        "total_cut_engine",
        "avg_attacks_per_run",
        "avg_em_brakes_per_run",
        "detection_rate",
        "safe_stop_rate",
    ]

    for p in attack_probs:
        print(f"\n--- Attack Probability = {p} ---")
        run_metrics_list: List[RunMetrics] = []

        for i in range(runs_per_setting):
            rm = run_single_simulation(attack_probability=p)
            run_metrics_list.append(rm)
            print(
                f"Run {i+1}/{runs_per_setting}: "
                f"attacks={rm.attack_commands}, "
                f"EM_brakes={rm.emergency_brakes}, "
                f"SAFE_STOP={rm.safe_stop_reached}"
            )

        agg = aggregate_metrics(run_metrics_list)
        print(
            f"Summary for p={p}: "
            f"detection_rate={agg['detection_rate']:.3f}, "
            f"safe_stop_rate={agg['safe_stop_rate']:.3f}, "
            f"avg_attacks/run={agg['avg_attacks_per_run']:.2f}"
        )

        row = [p] + [agg[k] for k in header[1:]]
        rows.append(row)

    # Save CSV
    with open(out_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

    print(f"\n[+] Saved experiment summary to: {out_csv}")


if __name__ == "__main__":
    main()
