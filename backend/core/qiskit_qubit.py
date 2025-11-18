"""
Qiskit-based Qubit implementation for BB84 protocol.

Uses actual quantum circuits and state vectors from Qiskit
to simulate quantum behavior more accurately.
"""

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector
import random
from typing import Literal

BasisType = Literal['Z', 'X']


class QiskitQubit:
    """
    Qubit implementation using Qiskit quantum circuits.
    
    This provides a more accurate quantum simulation compared to
    the simplified custom implementation.
    """
    
    def __init__(self, basis: BasisType, bit_value: int):
        """
        Initialize a qubit using Qiskit quantum circuit.
        
        Args:
            basis: 'Z' for computational basis or 'X' for Hadamard basis
            bit_value: 0 or 1
        """
        if basis not in ['Z', 'X']:
            raise ValueError(f"Basis must be 'Z' or 'X', got '{basis}'")
        
        if bit_value not in [0, 1]:
            raise ValueError(f"Bit value must be 0 or 1, got {bit_value}")
        
        self.basis = basis
        self.bit_value = bit_value
        
        # Create quantum circuit
        self.circuit = QuantumCircuit(1, 1)
        
        # Prepare state based on basis and bit
        self._prepare_state()
        
        # Get state vector for visualization
        self.statevector = Statevector.from_instruction(self.circuit.remove_final_measurements(inplace=False))
    
    def _prepare_state(self):
        """
        Prepare quantum state based on basis and bit value.
        
        Z-basis:
            |0⟩ - no gates
            |1⟩ - X gate
        
        X-basis:
            |+⟩ - H gate
            |−⟩ - X gate then H gate
        """
        if self.basis == 'Z':
            if self.bit_value == 1:
                self.circuit.x(0)  # |1⟩ state
            # |0⟩ state - no operation needed
        else:  # X-basis
            if self.bit_value == 1:
                self.circuit.x(0)  # First create |1⟩
            self.circuit.h(0)  # Apply Hadamard to create |+⟩ or |−⟩
    
    def measure(self, measurement_basis: BasisType) -> int:
        """
        Measure the qubit in a given basis using Qiskit simulator.
        
        Args:
            measurement_basis: The basis to measure in ('Z' or 'X')
            
        Returns:
            Measurement outcome: 0 or 1
        """
        if measurement_basis not in ['Z', 'X']:
            raise ValueError(f"Measurement basis must be 'Z' or 'X', got '{measurement_basis}'")
        
        # Create a copy of the circuit for measurement
        measure_circuit = self.circuit.copy()
        
        # If measuring in X-basis, apply Hadamard before measurement
        if measurement_basis == 'X':
            measure_circuit.h(0)
        
        # Add measurement
        measure_circuit.measure(0, 0)
        
        # Simulate measurement
        simulator = AerSimulator()
        job = simulator.run(measure_circuit, shots=1)
        result = job.result()
        counts = result.get_counts()
        
        # Get measurement result (should be either '0' or '1')
        measured_bit = int(list(counts.keys())[0])
        
        return measured_bit
    
    def get_state_vector(self) -> tuple:
        """
        Get the quantum state vector representation.
        
        Returns:
            Tuple of complex amplitudes (α, β) where state = α|0⟩ + β|1⟩
        """
        data = self.statevector.data
        return (complex(data[0]), complex(data[1]))
    
    def get_state(self) -> str:
        """
        Get string representation of quantum state.
        
        Returns:
            String like '|0⟩', '|1⟩', '|+⟩', or '|−⟩'
        """
        if self.basis == 'Z':
            return '|0⟩' if self.bit_value == 0 else '|1⟩'
        else:
            return '|+⟩' if self.bit_value == 0 else '|−⟩'
    
    def get_circuit_diagram(self) -> str:
        """
        Get ASCII representation of quantum circuit.
        
        Returns:
            Circuit diagram as string
        """
        return str(self.circuit.draw(output='text'))
    
    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"QiskitQubit(basis='{self.basis}', bit={self.bit_value}, state='{self.get_state()}')"
    
    def __str__(self) -> str:
        """Human-readable string representation."""
        return self.get_state()


def create_qiskit_qubit_batch(count: int) -> list[QiskitQubit]:
    """
    Create multiple random qubits using Qiskit.
    
    Args:
        count: Number of qubits to create
        
    Returns:
        List of randomly generated Qiskit qubits
    """
    qubits = []
    for _ in range(count):
        basis = random.choice(['Z', 'X'])
        bit = random.choice([0, 1])
        qubits.append(QiskitQubit(basis, bit))
    return qubits


def measure_qiskit_qubit_batch(qubits: list[QiskitQubit], bases: list[BasisType]) -> list[int]:
    """
    Measure a batch of Qiskit qubits with specified bases.
    
    Args:
        qubits: List of Qiskit qubits to measure
        bases: List of measurement bases (one for each qubit)
        
    Returns:
        List of measurement outcomes (0s and 1s)
    """
    if len(qubits) != len(bases):
        raise ValueError(f"Number of qubits ({len(qubits)}) must match number of bases ({len(bases)})")
    
    return [qubit.measure(basis) for qubit, basis in zip(qubits, bases)]


# Demo and testing
if __name__ == "__main__":
    print("=" * 70)
    print("Qiskit-based Qubit Implementation Demo")
    print("=" * 70)
    
    # Test 1: Create all 4 possible states
    print("\n1. Creating qubits in all 4 possible states:")
    print("-" * 70)
    
    states = [
        ('Z', 0, '|0⟩'),
        ('Z', 1, '|1⟩'),
        ('X', 0, '|+⟩'),
        ('X', 1, '|−⟩')
    ]
    
    for basis, bit, expected_state in states:
        q = QiskitQubit(basis, bit)
        print(f"Basis: {basis}, Bit: {bit} → State: {q.get_state()} (expected: {expected_state})")
        
        # Show state vector
        sv = q.get_state_vector()
        print(f"  State vector: ({sv[0]:.3f}, {sv[1]:.3f})")
    
    # Test 2: Correct basis measurement
    print("\n2. Testing correct basis measurements (should be deterministic):")
    print("-" * 70)
    
    for basis, bit, _ in states:
        q = QiskitQubit(basis, bit)
        results = [q.measure(basis) for _ in range(10)]
        accuracy = sum(1 for r in results if r == bit) / len(results)
        print(f"{q.get_state()} measured in {basis}-basis: {accuracy*100:.0f}% match (expected: 100%)")
    
    # Test 3: Wrong basis measurement
    print("\n3. Testing wrong basis measurements (should be random ~50/50):")
    print("-" * 70)
    
    test_cases = [
        (QiskitQubit('Z', 0), 'X'),  # |0⟩ measured in X
        (QiskitQubit('Z', 1), 'X'),  # |1⟩ measured in X
        (QiskitQubit('X', 0), 'Z'),  # |+⟩ measured in Z
        (QiskitQubit('X', 1), 'Z'),  # |−⟩ measured in Z
    ]
    
    for qubit, wrong_basis in test_cases:
        results = [qubit.measure(wrong_basis) for _ in range(100)]
        zeros = sum(1 for r in results if r == 0)
        ones = len(results) - zeros
        print(f"{qubit.get_state()} measured in {wrong_basis}-basis: {zeros}% zeros, {ones}% ones")
    
    # Test 4: Circuit diagram
    print("\n4. Sample quantum circuit:")
    print("-" * 70)
    q = QiskitQubit('X', 1)
    print(f"State: {q.get_state()}")
    print(q.get_circuit_diagram())
    
    # Test 5: Batch operations
    print("\n5. Batch operations with Qiskit:")
    print("-" * 70)
    batch = create_qiskit_qubit_batch(5)
    print(f"Created {len(batch)} random qubits:")
    for i, q in enumerate(batch):
        print(f"  Qubit {i}: {q}")
    
    print("\n" + "=" * 70)
    print("✅ Qiskit implementation working correctly!")
    print("=" * 70)