"""
Core quantum cryptography components for BB84 protocol.
"""

from .qubit import Qubit, create_random_qubit, create_qubit_batch, measure_qubit_batch
from .eavesdropper import Eavesdropper, calculate_expected_qber, simulate_interception
from .bb84 import BB84Protocol, BB84Result, bits_to_hex, bits_to_string

# Qiskit implementations (optional)
try:
    from .qiskit_qubit import QiskitQubit, create_qiskit_qubit_batch, measure_qiskit_qubit_batch
    from .qiskit_bb84 import QiskitBB84Protocol, QiskitBB84Result
    QISKIT_AVAILABLE = True
except ImportError:
    QISKIT_AVAILABLE = False
    QiskitQubit = None
    QiskitBB84Protocol = None
    QiskitBB84Result = None

__all__ = [
    'Qubit',
    'create_random_qubit',
    'create_qubit_batch',
    'measure_qubit_batch',
    'Eavesdropper',
    'calculate_expected_qber',
    'simulate_interception',
    'BB84Protocol',
    'BB84Result',
    'bits_to_hex',
    'bits_to_string',
    'QISKIT_AVAILABLE',
    'QiskitQubit',
    'QiskitBB84Protocol',
    'QiskitBB84Result',
]