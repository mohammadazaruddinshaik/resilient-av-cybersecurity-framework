# src/attacker.py
import random
from typing import Literal, TypedDict

NORMAL = "NORMAL"
ATTACK = "ATTACK"

ENGINE = "ENGINE"
STEERING = "STEERING"
BRAKE = "BRAKE"

Subsystem = Literal["ENGINE", "STEERING", "BRAKE"]

class Command(TypedDict, total=False):
    subsystem: Subsystem
    value: float
    label: str
    attack_type: str

def generate_normal_command() -> Command:
    subsystem: Subsystem = random.choice([ENGINE, STEERING, BRAKE])

    if subsystem == ENGINE:
        value = random.uniform(-0.1, 0.2)
    elif subsystem == STEERING:
        value = random.uniform(-0.2, 0.2)
    else:  # BRAKE
        value = random.uniform(0.0, 0.3)

    return {"subsystem": subsystem, "value": value, "label": NORMAL}

def generate_attack_command() -> Command:
    attack_type = random.choice(["ENGINE_ATTACK", "STEERING_ATTACK", "BRAKE_ATTACK"])

    if attack_type == "ENGINE_ATTACK":
        cmd: Command = {"subsystem": ENGINE, "value": 1.0}
    elif attack_type == "STEERING_ATTACK":
        cmd = {"subsystem": STEERING, "value": 3.0}
    else:
        cmd = {"subsystem": BRAKE, "value": 0.0}

    cmd["label"] = ATTACK
    cmd["attack_type"] = attack_type
    return cmd

def maybe_generate_command(attack_probability: float = 0.2) -> Command:
    if random.random() < attack_probability:
        return generate_attack_command()
    return generate_normal_command()
