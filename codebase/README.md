# Vehicular Ad-hoc Network (VANET) Security Simulation

A comprehensive simulation framework for analyzing trust-based security mechanisms in Vehicular Ad-hoc Networks (VANETs) with integrated Intrusion Detection Systems (IDS).

## Overview

This project simulates a VANET environment to study vehicle communication security, trust management, and attack detection mechanisms. It provides tools for analyzing vehicle behavior, detecting malicious actors, and evaluating trust propagation in dynamic vehicular networks.

## Features

- **Trust-Based Security Model**: Dynamic trust computation and propagation between vehicles
- **Attack Simulation**: Configurable attacker models for security testing
- **Intrusion Detection System (IDS)**: Rule-based anomaly detection
- **Safety Controller**: Real-time monitoring and response to security threats
- **Comprehensive Logging**: Detailed simulation logs for analysis
- **Trust Analysis Tools**: Visualization and statistical analysis of trust metrics
- **Log Analysis**: Post-simulation data processing and insights

## Tech Stack

**Language:** Python 3.x

**Core Libraries:**
- NumPy - Numerical computations
- Pandas - Data analysis and logging
- Matplotlib/Seaborn - Visualization (if applicable)

## Project Structure

```
codebase/
├── src/
│   ├── main.py              # Entry point for simulation
│   ├── vehicle.py           # Vehicle entity implementation
│   ├── attacker.py          # Attack models and behaviors
│   ├── trust_model.py       # Trust computation algorithms
│   ├── ids_rule.py          # IDS rule definitions
│   ├── safety_controller.py # Safety monitoring system
│   ├── logger.py            # Logging utilities
│   ├── config.py            # Configuration settings
│   ├── analyze_logs.py      # Log analysis tools
│   └── analyze_trust.py     # Trust metric analysis
├── logs/                    # Simulation output logs
├── reports/                 # Generated reports
├── requirements.txt         # Python dependencies
└── README.md
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

```bash
# Clone the repository
git clone <repository-url>

# Navigate to project directory
cd "Major Project"

# Create virtual environment (recommended)
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

Edit `src/config.py` to customize simulation parameters:

- Number of vehicles
- Simulation duration
- Attack scenarios
- Trust thresholds
- IDS sensitivity
- Network topology

## Usage

### Run Simulation

```bash
# Navigate to source directory
cd codebase

# Run the main simulation
python src/main.py
```

### Analyze Results

```bash
# Analyze simulation logs
python src/analyze_logs.py

# Analyze trust metrics
python src/analyze_trust.py
```

## Simulation Outputs

- **Logs**: Timestamped CSV files in `logs/` directory containing vehicle interactions and trust values
- **Reports**: Generated analysis reports in `reports/` directory
- **Metrics**: Trust evolution, attack detection rates, and network behavior statistics

## Key Components

### Trust Model
Implements reputation-based trust computation using:
- Direct observations
- Indirect recommendations
- Historical behavior analysis

### Intrusion Detection System
Rule-based detection for:
- Message tampering
- Sybil attacks
- False information dissemination
- Abnormal behavior patterns

### Safety Controller
Monitors and responds to:
- Trust threshold violations
- Detected attacks
- Network anomalies

## Research Applications

This framework is suitable for:
- VANET security research
- Trust management algorithm evaluation
- IDS performance testing
- Attack scenario modeling
- Network behavior analysis

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Authors

- [@shaikmohammadazaruddin](https://github.com/shaikmohammadazaruddin)

## Acknowledgments

This project is developed as part of a major research project on vehicular network security.

## Contact

For questions or collaboration opportunities, please open an issue or contact the author.