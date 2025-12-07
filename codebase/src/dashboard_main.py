# src/dashboard_main.py

import time
from typing import Dict

from rich.console import Console, Group
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .config import ATTACK_PROBABILITY, SIMULATION_STEPS, SLEEP_TIME_SECONDS
from .vehicle import Vehicle
from .attacker import maybe_generate_command, ATTACK
from .ids_rule import detect_attack_rule, IDSResult
from .safety_controller import decide_safety_action
from .logger import RunLogger
from .trust_model import TrustManager

console = Console()


def make_vehicle_panel(step: int, vehicle: Vehicle, cmd: dict, ids_result: IDSResult, safety_action: str) -> Panel:
    table = Table(show_header=False, box=None, expand=True)

    title = f"Step {step}"
    if ids_result.status == ATTACK:
        title = f"[red]⚠ Step {step} – ATTACK DETECTED[/red]"

    table.add_row("Mode", vehicle.state.mode)
    table.add_row("Speed (km/h)", f"{vehicle.state.speed:.1f}")
    table.add_row("Steering (deg)", f"{vehicle.state.steering_angle:.1f}")

    if cmd is not None:
        table.add_row("Incoming Cmd", f"{cmd['subsystem']} value={cmd['value']:.2f}")
        table.add_row("IDS Status", ids_result.status)
        if ids_result.status == ATTACK:
            table.add_row("Attack Type", ids_result.attack_type or "-")
            table.add_row("Subsystem", ids_result.subsystem or "-")
            table.add_row("Reason", ids_result.reason or "-")
            table.add_row("Safety Action", safety_action)
        else:
            table.add_row("Attack Type", "-")
            table.add_row("Subsystem", "-")
            table.add_row("Safety Action", "NONE")

    return Panel(table, title=f"[bold cyan]Vehicle State – {title}[/bold cyan]", border_style="cyan")


def bar(value: float, max_value: float = 100.0, width: int = 20) -> str:
    """
    Simple text progress bar for trust display.
    """
    value = max(0.0, min(max_value, value))
    filled = int((value / max_value) * width)
    empty = width - filled
    return "█" * filled + "░" * empty


def make_trust_panel(trust_snapshot: Dict[str, float]) -> Panel:
    table = Table(show_header=True, header_style="bold magenta", expand=True)
    table.add_column("Subsystem")
    table.add_column("Trust")
    table.add_column("Bar")

    for subsystem in ("ENGINE", "STEERING", "BRAKE"):
        t = trust_snapshot.get(subsystem, 0.0)
        table.add_row(
            subsystem,
            f"{t:.1f}",
            bar(t),
        )

    return Panel(table, title="[bold magenta]Subsystem Trust[/bold magenta]", border_style="magenta")


def make_status_panel(last_attack_type: str | None, last_safety_action: str | None) -> Panel:
    if last_attack_type:
        text = Text()
        text.append("Last Attack: ", style="bold red")
        text.append(last_attack_type + "\n", style="red")
        text.append("Last Safety Action: ", style="bold yellow")
        text.append(last_safety_action or "NONE", style="yellow")
    else:
        text = Text("No attacks detected yet.", style="green")

    return Panel(text, title="[bold yellow]Events[/bold yellow]", border_style="yellow")


def build_layout(
    step: int,
    vehicle: Vehicle,
    cmd: dict,
    ids_result: IDSResult,
    safety_action: str,
    trust_snapshot: Dict[str, float],
    last_attack_type: str | None,
    last_safety_action: str | None,
) -> Panel:
    """
    Build a combined dashboard view as a single Panel.
    """
    vehicle_panel = make_vehicle_panel(step, vehicle, cmd, ids_result, safety_action)
    trust_panel = make_trust_panel(trust_snapshot)
    status_panel = make_status_panel(last_attack_type, last_safety_action)

    group = Group(vehicle_panel, trust_panel, status_panel)
    return Panel(group, title="[bold white]AV Cybersecurity Dashboard[/bold white]", border_style="white")


def main() -> None:
    vehicle = Vehicle()
    trust_manager = TrustManager()
    logger = RunLogger()

    step = 0
    last_attack_type: str | None = None
    last_safety_action: str | None = None

    console.print("[bold green]Starting AV Cybersecurity Dashboard (console UI)...[/bold green]")

    with Live(refresh_per_second=4, console=console) as live:
        try:
            while step < SIMULATION_STEPS:
                step += 1

                # 1) Generate command
                cmd = maybe_generate_command(attack_probability=ATTACK_PROBABILITY)

                # 2) IDS
                ids_result = detect_attack_rule(cmd, vehicle.state)

                # 3) Trust update
                is_attack = ids_result.status == ATTACK
                trust_manager.update(cmd["subsystem"], is_attack=is_attack)
                trust_snapshot = trust_manager.get_trust_snapshot()

                # 4) Safety action
                safety_action = decide_safety_action(ids_result, trust_snapshot)

                # update last attack info (for status panel)
                if is_attack:
                    last_attack_type = ids_result.attack_type or "UNKNOWN"
                    last_safety_action = safety_action

                # 5) Apply safety override
                vehicle.apply_safety_override(safety_action)

                # 6) Apply command if not fully stopped due to attack
                if not (vehicle.state.mode == "SAFE_STOP" and ids_result.status == ATTACK):
                    vehicle.apply_command(cmd)

                # 7) Physics tick
                vehicle.tick()

                # 8) Log
                logger.log(step, vehicle, cmd, ids_result, safety_action, trust_snapshot)

                # 9) Update dashboard
                layout_panel = build_layout(
                    step,
                    vehicle,
                    cmd,
                    ids_result,
                    safety_action,
                    trust_snapshot,
                    last_attack_type,
                    last_safety_action,
                )
                live.update(layout_panel)

                # 10) End if safe stop after attack
                if vehicle.state.mode == "SAFE_STOP" and ids_result.status == ATTACK:
                    time.sleep(2.0)
                    break

                # Slower step for readability
                if ids_result.status == ATTACK:
                    time.sleep(2.0)
                else:
                    time.sleep(SLEEP_TIME_SECONDS)

        except KeyboardInterrupt:
            console.print("[bold red]\nDashboard interrupted by user.[/bold red]")

        finally:
            logger.close()
            console.print("[bold green]Simulation finished. Logs saved in ./logs[/bold green]")


if __name__ == "__main__":
    main()
