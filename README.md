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

## 📁 Project Structure

```
src/
├── main.py                  # Main simulation entry point
├── gateway_main.py          # Gateway-based simulation entrypoint
├── vehicle.py               # Vehicle digital twin simulator
├── attacker.py              # Threat generator & attack models
├── ids_rule.py              # Rule-based intrusion detection
├── safety_controller.py      # Safety monitoring & emergency response
├── gateway.py               # Firewall / safety island ECU
├── trust_model.py           # Trust computation algorithms
├── config.py                # Tunable parameters & configuration
├── logger.py                # Logging utilities
├── analyze_logs.py          # Post-simulation log analysis
├── analyze_trust.py         # Trust metrics evaluation & plotting
├── experiment_runner.py      # Batch experiment execution
├── dashboard_main.py        # Visualization dashboard
├── __init__.py              # Package initialization
└── __pycache__/             # Python cache

logs/
├── simulation_run_*.csv     # Timestamped simulation outputs

reports/
├── experiment_results.csv   # Aggregated experiment reports

data/
└── models/                  # Pre-trained models (if applicable)
```

---

## 🚀 Running the Simulation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### 1️⃣ Setup Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2️⃣ Run Main Simulation

```bash
cd codebase
python src/main.py
```

### 3️⃣ Run Gateway-Based Simulation

```bash
python src/gateway_main.py
```

### 4️⃣ Run Batch Experiments

```bash
python src/experiment_runner.py
```

### 5️⃣ Analyze Results

```bash
# Analyze simulation logs
python src/analyze_logs.py

# Analyze trust metrics and generate plots
python src/analyze_trust.py
```

### 6️⃣ Launch Dashboard (Optional)

```bash
python src/dashboard_main.py
```

---

## ⚙️ Configuration

Edit `src/config.py` to customize:

- Number of simulation steps
- Vehicle parameters (speed, steering limits)
- Attack scenarios and intensity
- Trust thresholds
- IDS sensitivity levels
- Gateway filtering policies

---

## 📊 Outputs

**Simulation Logs** (`logs/`)
- CSV files with timestamped vehicle states, commands, and trust values
- Attack detection events and gateway actions

**Reports** (`reports/`)
- Aggregated experiment results
- Performance metrics and statistics

**Visualizations**
- Trust evolution plots
- Attack timeline analysis
- Safety metric dashboards

---

## 🔍 Core Modules

### Vehicle Module (`vehicle.py`)
Simulates vehicle dynamics:
- Speed and acceleration control
- Steering angle management
- State monitoring

### Attacker Module (`attacker.py`)
Generates attack scenarios:
- Malicious command injection
- Parameter manipulation
- Coordinated attacks

### IDS Module (`ids_rule.py`)
Detects anomalies using rules:
- Threshold violations
- Rate-of-change analysis
- Command validation

### Trust Model (`trust_model.py`)
Computes vehicle confidence:
- Trust decay during attacks
- Recovery mechanisms
- ECU-source reputation

### Safety Controller (`safety_controller.py`)
Enforces safe operation:
- Emergency braking
- Actuator limiting
- State stabilization

### Gateway ECU (`gateway.py`)
Filters and sanitizes commands:
- Command validation
- Policy enforcement
- Attack mitigation

---

## 🎯 Research Applications

- Autonomous vehicle cybersecurity analysis
- Trust-based resilience evaluation
- IDS performance benchmarking
- Attack scenario modeling
- Safety mechanism validation
- ECU communication security

---

## 📝 Requirements

See `requirements.txt` for full dependency list. Core libraries:

- NumPy - Numerical computations
- Pandas - Data manipulation and logging
- Matplotlib - Visualization
- scikit-learn - Machine learning utilities (if applicable)

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/enhancement`)
3. Commit changes (`git commit -m 'Add enhancement'`)
4. Push to branch (`git push origin feature/enhancement`)
5. Open a Pull Request

---

## 📄 License

[MIT](https://choosealicense.com/licenses/mit/)

---

## 👤 Authors

- [@shaikmohammadazaruddin](https://github.com/shaikmohammadazaruddin)

---

## 📧 Contact & Support

For questions, issues, or collaboration:
- Open an issue in the repository
- Contact the author directly

---

##  Acknowledgments

This framework is developed as part of a major research initiative on resilient autonomous vehicle cybersecurity architecture.