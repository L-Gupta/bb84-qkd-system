"""
Qubit implementation for BB84 Quantum Key Distribution Protocol.

This module implements quantum bit (qubit) representation and measurement
using Z-basis (computational) and X-basis (Hadamard).
"""

import random
from typing import Literal

BasisType = Literal['Z', 'X']


class Qubit:
    """
    Represents a quantum bit (qubit) in BB84 protocol.
    
    The qubit can be prepared in one of two conjugate bases:
    - Z-basis (computational): |0⟩ or |1⟩
    - X-basis (Hadamard): |+⟩ or |−⟩
    
    Attributes:
        basis (str): The basis in which the qubit was prepared ('Z' or 'X')
        bit_value (int): The bit value encoded (0 or 1)
        state (str): String representation of the quantum state
    """
    
    def __init__(self, basis: BasisType, bit_value: int):
        """
        Initialize a qubit with a specific basis and bit value.
        
        Args:
            basis: 'Z' for computational basis or 'X' for Hadamard basis
            bit_value: 0 or 1
            
        Raises:
            ValueError: If basis is not 'Z' or 'X', or bit_value is not 0 or 1
        """
        if basis not in ['Z', 'X']:
            raise ValueError(f"Basis must be 'Z' or 'X', got '{basis}'")
        
        if bit_value not in [0, 1]:
            raise ValueError(f"Bit value must be 0 or 1, got {bit_value}")
        
        self.basis = basis
        self.bit_value = bit_value
        self.state = self._calculate_state()
    
    def _calculate_state(self) -> str:
        """
        Calculate the quantum state representation based on basis and bit value.
        
        Z-basis: |0⟩ or |1⟩
        X-basis: |+⟩ or |−⟩
        
        Returns:
            String representation of the quantum state
        """
        if self.basis == 'Z':
            return '|0⟩' if self.bit_value == 0 else '|1⟩'
        else:  # X-basis
            return '|+⟩' if self.bit_value == 0 else '|−⟩'
    
    def measure(self, measurement_basis: BasisType) -> int:
        """
        Measure the qubit in a given basis.
        
        Quantum measurement rules:
        - If measurement basis matches preparation basis: deterministic (get original bit)
        - If measurement basis differs: random outcome (50% probability each)
        
        This is the core quantum mechanical principle that makes BB84 secure!
        
        Args:
            measurement_basis: The basis to measure in ('Z' or 'X')
            
        Returns:
            Measurement outcome: 0 or 1
            
        Raises:
            ValueError: If measurement_basis is not 'Z' or 'X'
        """
        if measurement_basis not in ['Z', 'X']:
            raise ValueError(f"Measurement basis must be 'Z' or 'X', got '{measurement_basis}'")
        
        if measurement_basis == self.basis:
            # Correct basis: deterministic result
            # Measuring |0⟩ in Z-basis → always get 0
            # Measuring |+⟩ in X-basis → always get 0
            return self.bit_value
        else:
            # Wrong basis: random result (quantum uncertainty!)
            # Measuring |0⟩ in X-basis → 50% get 0, 50% get 1
            # Measuring |+⟩ in Z-basis → 50% get 0, 50% get 1
            return random.choice([0, 1])
    
    def get_state_vector(self) -> tuple:
        """
        Get the quantum state vector representation.
        
        For educational/debugging purposes. Returns normalized amplitudes.
        
        Z-basis:
            |0⟩ = (1, 0)
            |1⟩ = (0, 1)
        
        X-basis:
            |+⟩ = (1/√2, 1/√2)
            |−⟩ = (1/√2, -1/√2)
        
        Returns:
            Tuple of complex amplitudes (α, β) where state = α|0⟩ + β|1⟩
        """
        if self.basis == 'Z':
            if self.bit_value == 0:
                return (1.0, 0.0)  # |0⟩
            else:
                return (0.0, 1.0)  # |1⟩
        else:  # X-basis
            sqrt_2_inv = 1.0 / (2 ** 0.5)  # 1/√2
            if self.bit_value == 0:
                return (sqrt_2_inv, sqrt_2_inv)  # |+⟩
            else:
                return (sqrt_2_inv, -sqrt_2_inv)  # |−⟩
    
    def __repr__(self) -> str:
        """
        String representation for debugging.
        
        Returns:
            String showing basis, bit value, and state
        """
        return f"Qubit(basis='{self.basis}', bit={self.bit_value}, state='{self.state}')"
    
    def __str__(self) -> str:
        """
        Human-readable string representation.
        
        Returns:
            Quantum state notation
        """
        return self.state


# Utility functions for qubit operations
def create_random_qubit() -> Qubit:
    """
    Create a qubit with random basis and bit value.
    
    Used by Alice to prepare qubits for transmission.
    
    Returns:
        Qubit with random basis ('Z' or 'X') and random bit (0 or 1)
    """
    basis = random.choice(['Z', 'X'])
    bit_value = random.choice([0, 1])
    return Qubit(basis, bit_value)


def create_qubit_batch(count: int) -> list[Qubit]:
    """
    Create multiple random qubits.
    
    Args:
        count: Number of qubits to create
        
    Returns:
        List of randomly generated qubits
    """
    return [create_random_qubit() for _ in range(count)]


def measure_qubit_batch(qubits: list[Qubit], bases: list[BasisType]) -> list[int]:
    """
    Measure a batch of qubits with specified bases.
    
    Args:
        qubits: List of qubits to measure
        bases: List of measurement bases (one for each qubit)
        
    Returns:
        List of measurement outcomes (0s and 1s)
        
    Raises:
        ValueError: If lengths don't match
    """
    if len(qubits) != len(bases):
        raise ValueError(f"Number of qubits ({len(qubits)}) must match number of bases ({len(bases)})")
    
    return [qubit.measure(basis) for qubit, basis in zip(qubits, bases)]


# Quick demo for manual testing
if __name__ == "__main__":
    print("BB84 Qubit Demo")
    print("=" * 60)
    
    # Create all 4 possible states
    print("\nCreating qubits in all 4 possible states:")
    qubits = [
        Qubit('Z', 0),  # |0⟩
        Qubit('Z', 1),  # |1⟩
        Qubit('X', 0),  # |+⟩
        Qubit('X', 1),  # |−⟩
    ]
    
    for q in qubits:
        print(f"  {q}")
    
    # Demonstrate measurement
    print("\nMeasurement demonstration:")
    q = Qubit('Z', 0)
    print(f"Created qubit: {q}")
    print(f"  Measured in Z-basis: {q.measure('Z')} (correct basis, deterministic)")
    print(f"  Measured in X-basis: {q.measure('X')} (wrong basis, random)")
    
    print("\nFor comprehensive tests, run: pytest tests/test_qubit.py -v")
    print("=" * 60)