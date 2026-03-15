'''
pip install qrisp
pip install pyscf
pip install openfermion
pip install openfermionpyscf
pip install scipy

~1,000,000 Pauli terms
~300 logical qubits
~10^9 circuit evaluations

solving it would likely be a Nobel Prize–level result.


'''

###############################################################
# FeMoco Simulation with Qrisp
# UCCSD + Orbital Freezing + Qubit Tapering + ADAPT-VQE
# Runs on Automatski Quantum Backend
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

sys.path.append('../../')

from AutomatskiKomencoQiskit import AutomatskiKomencoQiskit
from AutomatskiBackendQrisp import *

backend = AutomatskiKomencoQiskit(
    host="XXX.XXX.XXX.XXX",
    port=XX
)

automatski_backend = AutomatskiBackend(backend=backend)

###############################################################
# FeMoco Geometry (simplified cluster)
###############################################################

geometry = [
("Mo",(0.0,0.0,0.0)),
("Fe",(2.6,0.0,0.0)),
("Fe",(-2.6,0.0,0.0)),
("Fe",(0.0,2.6,0.0)),
("Fe",(0.0,-2.6,0.0)),
("Fe",(1.8,1.8,1.8)),
("Fe",(-1.8,-1.8,1.8)),
("Fe",(1.8,-1.8,-1.8)),
("S",(3.8,1.0,0.0)),
("S",(-3.8,-1.0,0.0)),
("S",(1.0,3.8,0.0)),
("S",(-1.0,-3.8,0.0)),
("S",(0.0,0.0,3.5)),
("S",(0.0,0.0,-3.5)),
("C",(0.0,0.0,0.8))
]

###############################################################
# PySCF Electronic Structure
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
# Orbital Freezing
###############################################################

frozen_core = 10

hamiltonian = molecule.get_molecular_hamiltonian(
    occupied_indices=range(frozen_core),
    active_indices=range(frozen_core, frozen_core + 54)
)

fermion_hamiltonian = get_fermion_operator(hamiltonian)

###############################################################
# Fermion → Qubit Mapping
###############################################################

qubit_hamiltonian = jordan_wigner(fermion_hamiltonian)

n_qubits = count_qubits(qubit_hamiltonian)

print("Qubits before tapering:", n_qubits)

###############################################################
# (Optional) Qubit tapering placeholder
###############################################################
# Symmetry tapering libraries vary, so this step is left simple.
# In real experiments Z2 symmetries are removed here.

tapered_hamiltonian = qubit_hamiltonian

###############################################################
# Measurement Reduction
###############################################################

print("Grouping Pauli operators...")

groups = group_into_tensor_product_basis_sets(tapered_hamiltonian)

print("Measurement groups:", len(groups))

###############################################################
# Quantum Register
###############################################################

qv = QuantumVariable(count_qubits(tapered_hamiltonian))

###############################################################
# UCCSD Operator Pool (simplified Pauli pool)
###############################################################

from openfermion.utils import hermitian_conjugated

operator_pool = []

for term in tapered_hamiltonian.terms:
    operator_pool.append(term)

###############################################################
# ADAPT-VQE Ansatz
###############################################################

ansatz_ops = []
parameters = []

###############################################################
# Build circuit
###############################################################

def build_ansatz(params):

    for i, op in enumerate(ansatz_ops):

        theta = params[i]

        exp_pauli(qv, op, theta)

###############################################################
# Energy function (runs on your backend)
###############################################################

def energy_expectation(params):

    build_ansatz(params)

    energy = measure_expectation(
        qv,
        groups,
        backend=automatski_backend,
        shots=1000000000
    )

    return energy

###############################################################
# ADAPT-VQE Loop
###############################################################

max_adapt_steps = 10

for step in range(max_adapt_steps):

    print("\nADAPT Iteration:", step)

    gradients = []

    for op in operator_pool[:20]:

        ansatz_ops.append(op)
        parameters.append(0.0)

        grad = energy_expectation(parameters)

        gradients.append(abs(grad))

        ansatz_ops.pop()
        parameters.pop()

    best_index = np.argmax(gradients)

    best_op = operator_pool[best_index]

    ansatz_ops.append(best_op)
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

print("\nEstimated FeMoco Ground State Energy:")
print(final_energy)