# src/gateway_main.py

import time

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .config import ATTACK_PROBABILITY, SIMULATION_STEPS, SLEEP_TIME_SECONDS
from .vehicle import Vehicle
from .attacker import maybe_generate_command, ATTACK
from .gateway import Gateway, GatewayDecision

console = Console()


def print_gateway_step(
    step: int,
    raw_cmd: dict,
    decision: GatewayDecision,
    vehicle: Vehicle,
) -> None:
    """
    Print a single step: top-to-bottom view for the gateway architecture.
    """

    # ----- Header -----
    if decision.ids_result.status == ATTACK:
        console.rule(f"[bold red]⚠ Gateway Step {step} – ATTACK DETECTED[/bold red]")
    else:
        console.rule(f"[bold cyan]Gateway Step {step}[/bold cyan]")

    # ----- 1) Incoming command + gateway decision -----
    incoming_table = Table(show_header=False, expand=True)
    incoming_table.add_row("Source ECU", decision.source)
    incoming_table.add_row("Subsystem", raw_cmd["subsystem"])
    incoming_table.add_row("Raw Value", f"{raw_cmd['value']:.3f}")
    incoming_table.add_row("IDS Status", decision.ids_result.status)
    incoming_table.add_row("Gateway Action", decision.action)
    incoming_table.add_row("Reason", decision.reason)

    incoming_panel = Panel(incoming_table, title="[bold cyan]Gateway View[/bold cyan]")
    console.print(incoming_panel)

    # ----- 2) Vehicle state after gateway decision -----
    vehicle_table = Table(show_header=False, expand=True)
    vehicle_table.add_row("Mode", vehicle.state.mode)
    vehicle_table.add_row("Speed (km/h)", f"{vehicle.state.speed:.1f}")
    vehicle_table.add_row("Steering (deg)", f"{vehicle.state.steering_angle:.1f}")

    if decision.forwarded_cmd is not None:
        fwd = decision.forwarded_cmd
        vehicle_table.add_row(
            "Applied Cmd",
            f"{fwd['subsystem']} value={fwd['value']:.3f}",
        )
    else:
        vehicle_table.add_row("Applied Cmd", "BLOCKED (no command applied)")

    vehicle_panel = Panel(vehicle_table, title="[bold magenta]Vehicle State[/bold magenta]")
    console.print(vehicle_panel)

    console.print()  # blank line


def main() -> None:
    console.print(
        "[bold green]Starting Safety Island / Gateway Firewall Simulation...[/bold green]"
    )

    vehicle = Vehicle()
    gateway = Gateway()

    step = 0

    try:
        while step < SIMULATION_STEPS:
            step += 1

            # 1) Generate a raw command (from some ECU / attacker)
            raw_cmd = maybe_generate_command(attack_probability=ATTACK_PROBABILITY)

            # Tag source based on is_attack (for simple demo)
            # In a richer system, you'd have multiple ECUs with IDs.
            if raw_cmd.get("is_attack", False):
                raw_cmd["source"] = "ATTACKER_ECU"
            else:
                raw_cmd["source"] = "CONTROL_ECU"

            # 2) Gateway inspects and decides
            decision: GatewayDecision = gateway.process_command(raw_cmd, vehicle.state)

            # 3) Apply forwarded command (if any) to vehicle
            if decision.forwarded_cmd is not None:
                vehicle.apply_command(decision.forwarded_cmd)

            # 4) Vehicle physics update
            vehicle.tick()

            # 5) Print step view
            print_gateway_step(step, raw_cmd, decision, vehicle)

            # 6) End early if we want a short demo
            # (Here, we keep going for SIMULATION_STEPS; you can change that.)

            # 7) Timing
            if decision.ids_result.status == ATTACK:
                time.sleep(2.0)
            else:
                time.sleep(SLEEP_TIME_SECONDS)

    except KeyboardInterrupt:
        console.print("[bold red]\nGateway simulation interrupted by user.[/bold red]")
    finally:
        console.print("[bold green]Gateway simulation finished.[/bold green]")


if __name__ == "__main__":
    main()
