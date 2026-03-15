"""
********************************************************************************
* Copyright (c) 2026 Automatski 
********************************************************************************
"""

from qrisp.interface.virtual_backend import VirtualBackend


class AutomatskiBackend(VirtualBackend):

    def __init__(self, backend=None, port=None):

        if backend is None:
            raise ("Automatski Backend Needs To Be Provided.")


        # Create the run method
        def run(qasm_str, shots=None, token=""):
            if shots is None:
                shots = 100000
            # Convert to qiskit
            from qiskit import QuantumCircuit

            qiskit_qc = QuantumCircuit.from_qasm_str(qasm_str)

            # Make circuit with one monolithic register
            new_qiskit_qc = QuantumCircuit(len(qiskit_qc.qubits), len(qiskit_qc.clbits))
            for instr in qiskit_qc:
                new_qiskit_qc.append(
                    instr.operation,
                    [qiskit_qc.qubits.index(qb) for qb in instr.qubits],
                    [qiskit_qc.clbits.index(cb) for cb in instr.clbits],
                )

            from qiskit import transpile

            qiskit_qc = transpile(
                new_qiskit_qc,
                basis_gates=[
                    'ccx','ccz','cp','crz','cs','csdg','cswap','cu',
                    'cx','cy','cz','h','id','measure','p','rx','ry','rz',
                    's','sdg','swap','sx','sxdg','t','tdg','u','x','y','z'
                ],
                optimization_level=3
            )

            result_sim = backend.run(qiskit_qc, repetitions=shots, topK=100)
            # Remove the spaces in the qiskit result keys
            result_dic = result_sim.get_counts(None)
            return result_dic
        # Call VirtualBackend constructor
        name = "AutomatskiBackend"
        super().__init__(run, port=port)

