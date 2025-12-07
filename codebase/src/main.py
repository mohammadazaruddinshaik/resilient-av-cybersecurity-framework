# src/main.py

import time

from rich.console import Console
from rich.table import Table

from .config import (
    ATTACK_PROBABILITY,
    SIMULATION_STEPS,
    SLEEP_TIME_SECONDS,
)
from .vehicle import Vehicle
from .attacker import maybe_generate_command, ATTACK
from .ids_rule import detect_attack_rule, IDSResult
from .safety_controller import decide_safety_action
from .logger import RunLogger
from .trust_model import TrustManager

console = Console()


def render_step(
    step: int,
    vehicle: Vehicle,
    cmd: dict,
    ids_result: IDSResult,
    safety_action: str,
    trust_snapshot: dict,
) -> None:
    """
    Pretty-print one simulation step to the console, including trust levels.
    """

    title = f"Simulation Step {step}"
    if ids_result.status == ATTACK:
        title = f"[bold red]⚠ {title} – ATTACK DETECTED[/bold red]"

    table = Table(title=title, show_header=False)

    # Vehicle state
    table.add_row("Vehicle Mode", vehicle.state.mode)
    table.add_row("Speed (km/h)", f"{vehicle.state.speed:.1f}")
    table.add_row("Steering (deg)", f"{vehicle.state.steering_angle:.1f}")

    # Trust levels
    table.add_row("ENGINE trust", f"{trust_snapshot.get('ENGINE', 0.0):.1f}")
    table.add_row("STEERING trust", f"{trust_snapshot.get('STEERING', 0.0):.1f}")
    table.add_row("BRAKE trust", f"{trust_snapshot.get('BRAKE', 0.0):.1f}")

    # Command + IDS results
    if cmd is not None:
        table.add_row("Incoming Cmd", f"{cmd['subsystem']} value={cmd['value']:.2f}")
        table.add_row("Traffic Status", ids_result.status)

        if ids_result.status == ATTACK:
            table.add_row("Attack Type", ids_result.attack_type or "-")
            table.add_row("Subsystem", ids_result.subsystem or "-")
            table.add_row("Reason", ids_result.reason or "-")
            table.add_row("Safety Action", safety_action)
        else:
            table.add_row("Attack Type", "-")
            table.add_row("Subsystem", "-")
            table.add_row("Safety Action", "NONE")

    console.print(table)


def main() -> None:
    vehicle = Vehicle()
    step = 0

    console.print(
        "[bold yellow]Running with Rule-based IDS + Trust Model[/bold yellow]"
    )

    # Create run logger
    logger = RunLogger()

    # Create trust manager (ENGINE, STEERING, BRAKE)
    trust_manager = TrustManager()

    try:
        while step < SIMULATION_STEPS:
            step += 1

            # 1) Generate command (sometimes attack)
            cmd = maybe_generate_command(attack_probability=ATTACK_PROBABILITY)

            # 2) IDS: rule-based
            ids_result = detect_attack_rule(cmd, vehicle.state)

            # 3) Update trust based on IDS outcome
            is_attack = ids_result.status == ATTACK
            trust_manager.update(cmd["subsystem"], is_attack=is_attack)
            trust_snapshot = trust_manager.get_trust_snapshot()

            # 4) Safety controller decides action (trust-aware)
            safety_action = decide_safety_action(ids_result, trust_snapshot)

            # 5) Apply safety override first
            vehicle.apply_safety_override(safety_action)

            # 6) Apply normal command ONLY if not fully stopped due to attack
            if not (vehicle.state.mode == "SAFE_STOP" and ids_result.status == ATTACK):
                vehicle.apply_command(cmd)

            # 7) Natural physics step
            vehicle.tick()

            # 8) Print status for demo
            if step == 1:
                console.clear()
            render_step(step, vehicle, cmd, ids_result, safety_action, trust_snapshot)

            # 9) Log this step to CSV (including trust)
            logger.log(step, vehicle, cmd, ids_result, safety_action, trust_snapshot)

            # 10) If vehicle reached safe stop because of an attack, end demo
            if vehicle.state.mode == "SAFE_STOP" and ids_result.status == ATTACK:
                console.print(
                    "[bold green]\nVehicle reached SAFE_STOP after attack – ending demo.[/bold green]"
                )
                break

            # 11) Demo pacing
            if ids_result.status == ATTACK:
                console.print(
                    "[bold red]ATTACK detected – pausing for explanation...[/bold red]"
                )
                time.sleep(3.0)
            else:
                time.sleep(SLEEP_TIME_SECONDS)

    except KeyboardInterrupt:
        console.print("[bold red]\nSimulation interrupted by user.[/bold red]")

    finally:
        logger.close()


if __name__ == "__main__":
    main()
