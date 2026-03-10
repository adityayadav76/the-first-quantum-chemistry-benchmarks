# The First Quantum Chemistry Benchmarks
The First Quantum Chemistry Benchmarks ( Qrisp, ... )

![](https://automatski.com/wp-content/uploads/2025/05/Automatski-New-Logo.svg)

## About

TFQCB is a Quantum Chemistry Benchmark created by [Automatski](https://automatski.com). It is part of a larger suite of benchmarks used by Automatski to evaluate its quantum computers, which have not yet been released publicly. These benchmarks are used to validate correct operation after each engineering cycle, including changes and upgrades.

### Intellectual Property
All rights are reserved by Automatski for Automatski-authored components of this codebase. Rights to third-party or upstream components remain with their respective original authors and licensors.

## Installation

TFQCB requires Python v3.11+ on Linux to run.
Install dependencies:

```sh
pip install qiskit==1.4.2 qrisp pyscf requests
pip install openfermion
pip install openfermionpyscf
pip install scipy
```

Run the Benchmarks
```sh
cd Benchmarks\
python <program-name>.py
```

## Results

### vqe1.py

![](https://raw.githubusercontent.com/adityayadav76/the-first-quantum-chemistry-benchmarks/refs/heads/main/Runs/vqe1-console.png)

![](https://raw.githubusercontent.com/adityayadav76/the-first-quantum-chemistry-benchmarks/refs/heads/main/Runs/vqe1-plot.png)

### vqe2.py

![](https://raw.githubusercontent.com/adityayadav76/the-first-quantum-chemistry-benchmarks/refs/heads/main/Runs/vqe2-console.png)

![](https://raw.githubusercontent.com/adityayadav76/the-first-quantum-chemistry-benchmarks/refs/heads/main/Runs/vqe2-plot.png)



