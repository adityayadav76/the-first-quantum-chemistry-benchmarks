from qrisp import *
from qrisp.operators.qubit import X,Y,Z

# Problem Hamiltonian
c = [-0.81054, 0.16614, 0.16892, 0.17218, -0.22573, 0.12091, 0.166145, 0.04523]
H = c[0] \
    + c[1]*Z(0)*Z(2) \
    + c[2]*Z(1)*Z(3) \
    + c[3]*(Z(3) + Z(1)) \
    + c[4]*(Z(2) + Z(0)) \
    + c[5]*(Z(2)*Z(3) + Z(0)*Z(1)) \
    + c[6]*(Z(0)*Z(3) + Z(1)*Z(2)) \
    + c[7]*(Y(0)*Y(1)*Y(2)*Y(3) + X(0)*X(1)*Y(2)*Y(3) + Y(0)*Y(1)*X(2)*X(3) + X(0)*X(1)*X(2)*X(3))

# Ansatz
def ansatz(qv,theta):
    for i in range(4):
        ry(theta[i],qv[i])
    for i in range(3):
        cx(qv[i],qv[i+1])
    cx(qv[3],qv[0])

from qrisp.vqe.vqe_problem import *

vqe = VQEProblem(hamiltonian = H,
                 ansatz_function = ansatz,
                 num_params = 4,
                 callback = True)

# ============================================================
# Run on Automatski Backend
# ============================================================

import sys
sys.path.append('../../')
from AutomatskiKomencoQiskit import AutomatskiKomencoQiskit

backend = AutomatskiKomencoQiskit(
    host="xxx.xxx.xxx.xxx",
    port=xx
)

from AutomatskiBackendQrisp import *
automatski_backend = AutomatskiBackend(backend = backend)

vqe.set_callback()
energy = vqe.run(QuantumVariable(4),
              depth = 1,
              max_iter = 50,
              mes_kwargs={
                    "backend": automatski_backend
                })
print(energy)
# Yields -1.864179046

vqe.visualize_energy(exact=False)