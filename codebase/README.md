# 🔐 Resilient Autonomous Vehicle Cybersecurity Framework

A modular simulation-based framework for detecting cyberattacks, enforcing safety, and modeling trust in autonomous vehicle systems.

---

## 📌 Overview

Autonomous vehicles depend on networked ECUs for motion control.  
A compromised ECU can manipulate acceleration, steering, or braking — creating unsafe conditions.

This project implements a **cybersecurity-integrated resilience architecture**, including:

- Intrusion Detection
- Safety enforcement logic
- Trust confidence modeling
- Gateway firewall ECU simulation
- Logging and visualization for evaluation

The framework demonstrates how a vehicle can **detect attacks, neutralize threats, and stabilize safely**.

---

## 🏗 System Architecture

### Implemented Components

1. **Vehicle Digital Twin**
   - Simulated speed, steering, and operational states

2. **Threat Injection Engine**
   - Generates legitimate and malicious control commands

3. **Rule-Based Intrusion Detection System**
   - Detects anomalous subsystem values
   - Labels attack type

4. **Safety Controller**
   - Emergency braking and safe-stop logic

5. **Trust Model**
   - Confidence decay during attacks
   - Gradual recovery under stable operation

6. **Gateway Firewall / Safety Island ECU**
   - Filters commands before actuators
   - Actions:
     - `ALLOW`
     - `BLOCK`
     - `SANITIZE`

7. **Monitoring & Visualization Layer**
   - Runtime step-by-step console-based simulation
   - CSV logs for offline evaluation

---

## ✨ Key Features

- Real-time attack detection  
- Automatic safety override  
- ECU-source filtering  
- Trust-based resilience modeling  
- Gateway firewall simulation  
- Research-ready logging & analytics

This architecture reflects **OEM-style automotive cybersecurity concepts**.

---

## 📂 Project Structure

src/
├── attacker.py # Threat generator
├── vehicle.py # Vehicle simulator
├── ids_rule.py # Rule-based intrusion detection
├── safety_controller.py # Safe-stop logic
├── gateway.py # Firewall / safety island ECU
├── gateway_main.py # Simulation entrypoint
├── analyze_trust.py # Evaluation and plotting
├── config.py # Tunable parameters 


---

## 🚀 Running the Simulation

### 1️⃣ Setup Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
 

 