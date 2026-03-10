'''
pip install qrisp
pip install pyscf
pip install openfermion
pip install openfermionpyscf
pip install scipy
'''

###############################################################
# 56-Qubit Qrisp VQE Example
# Ferrocene Active Space Simulation
###############################################################

import sys
import numpy as np

from pyscf import gto, scf
from scipy.optimize import minimize

from qrisp import QuantumVariable
from qrisp.operators import exp_pauli
from qrisp.measurement import measure_expectation

from openfermion import MolecularData, get_fermion_operator
from openfermion.transforms import jordan_wigner
from openfermion.utils import count_qubits
from openfermion.measurements import group_into_tensor_product_basis_sets
from openfermionpyscf import run_pyscf

###############################################################
# Automatski Backend
###############################################################

sys.path.append('../../python/')

from AutomatskiKomencoQiskit import AutomatskiKomencoQiskit
from AutomatskiBackendQrisp import *

backend = AutomatskiKomencoQiskit(
    host="XXX.XXX.XXX.XXX",
    port=XX
)

automatski_backend = AutomatskiBackend(backend=backend)

###############################################################
# Ferrocene Geometry (simplified)
###############################################################

geometry = [
("Fe",(0.0,0.0,0.0)),

("C",(1.4,0.0,1.6)),
("C",(0.4,1.3,1.6)),
("C",(-1.1,0.8,1.6)),
("C",(-1.1,-0.8,1.6)),
("C",(0.4,-1.3,1.6)),

("C",(1.4,0.0,-1.6)),
("C",(0.4,1.3,-1.6)),
("C",(-1.1,0.8,-1.6)),
("C",(-1.1,-0.8,-1.6)),
("C",(0.4,-1.3,-1.6))
]

###############################################################
# Hartree-Fock Calculation
###############################################################

print("Running Hartree-Fock...")

mol = gto.M(
    atom=geometry,
    basis="sto-3g",
    charge=0,
    spin=0
)

mf = scf.RHF(mol)
mf.kernel()

print("HF Energy:", mf.e_tot)

###############################################################
# Build OpenFermion Molecule
###############################################################

molecule = run_pyscf(
    MolecularData(
        geometry,
        basis="sto-3g",
        multiplicity=1,
        charge=0
    ),
    run_scf=True
)

###############################################################
# Active Space Selection
###############################################################

active_orbitals = 28
frozen_core = 10

hamiltonian = molecule.get_molecular_hamiltonian(
    occupied_indices=range(frozen_core),
    active_indices=range(frozen_core, frozen_core + active_orbitals)
)

fermion_hamiltonian = get_fermion_operator(hamiltonian)

###############################################################
# Fermion → Qubit Mapping
###############################################################

qubit_hamiltonian = jordan_wigner(fermion_hamiltonian)

n_qubits = count_qubits(qubit_hamiltonian)

print("Number of qubits:", n_qubits)

###############################################################
# Measurement Reduction
###############################################################

print("Grouping Pauli operators...")

groups = group_into_tensor_product_basis_sets(qubit_hamiltonian)

print("Measurement groups:", len(groups))

###############################################################
# Quantum Register
###############################################################

qv = QuantumVariable(n_qubits)

###############################################################
# Operator Pool
###############################################################

operator_pool = list(qubit_hamiltonian.terms.keys())[:30]

ansatz_ops = []
parameters = []

###############################################################
# Build Ansatz
###############################################################

def build_ansatz(params):

    for i, op in enumerate(ansatz_ops):

        theta = params[i]

        exp_pauli(qv, op, theta)

###############################################################
# Energy Expectation
###############################################################

def energy_expectation(params):

    build_ansatz(params)

    energy = measure_expectation(
        qv,
        groups,
        backend=automatski_backend,
        shots=5000
    )

    return energy

###############################################################
# VQE Optimization
###############################################################

max_steps = 8

for step in range(max_steps):

    print("\nVQE Iteration:", step)

    ansatz_ops.append(operator_pool[step])
    parameters.append(0.0)

    result = minimize(
        energy_expectation,
        parameters,
        method="COBYLA"
    )

    parameters = list(result.x)

    print("Energy:", result.fun)

###############################################################
# Final Energy
###############################################################

final_energy = energy_expectation(parameters)

print("\nFinal Ground State Energy:")
print(final_energy)
