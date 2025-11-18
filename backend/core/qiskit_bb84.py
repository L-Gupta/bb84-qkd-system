"""
Qiskit-based BB84 Protocol Implementation.

Uses Qiskit quantum circuits for more accurate quantum simulation.
"""

import random
from dataclasses import dataclass
from typing import Optional
from .qiskit_qubit import QiskitQubit, BasisType
from .eavesdropper import Eavesdropper


@dataclass
class QiskitBB84Result:
    """Result from Qiskit-based BB84 protocol execution."""
    alice_bits: list[int]
    alice_bases: list[BasisType]
    bob_bits: list[int]
    bob_bases: list[BasisType]
    sifted_alice_bits: list[int]
    sifted_bob_bits: list[int]
    matching_indices: list[int]
    error_rate: float
    errors_found: int
    checked_indices: list[int]
    sample_size: int
    is_secure: bool
    final_key: list[int]
    total_transmitted: int
    total_sifted: int
    final_key_length: int
    sifting_efficiency: float
    eavesdropper_present: bool
    eavesdropper_stats: Optional[dict] = None
    implementation: str = "Qiskit"


class QiskitBB84Protocol:
    """
    BB84 Protocol using Qiskit quantum circuits.
    
    This provides a more realistic quantum simulation using
    Qiskit's state vectors and quantum operations.
    """
    
    def __init__(self, key_length: int = 256, transmission_multiplier: int = 4):
        """
        Initialize Qiskit-based BB84 protocol.
        
        Args:
            key_length: Desired final key length in bits
            transmission_multiplier: Transmission overhead multiplier
        """
        if key_length <= 0:
            raise ValueError(f"Key length must be positive, got {key_length}")
        
        if transmission_multiplier < 2:
            raise ValueError(f"Transmission multiplier must be >= 2, got {transmission_multiplier}")
        
        self.key_length = key_length
        self.transmission_multiplier = transmission_multiplier
        self.qber_threshold = 0.11
    
    def execute(
        self,
        with_eavesdropper: bool = False,
        eavesdropper_intercept_rate: float = 0.5
    ) -> QiskitBB84Result:
        """
        Execute BB84 protocol using Qiskit quantum circuits.
        
        Args:
            with_eavesdropper: Whether to simulate an eavesdropper
            eavesdropper_intercept_rate: Fraction of qubits Eve intercepts
            
        Returns:
            QiskitBB84Result with all protocol data
        """
        # Step 1: Alice prepares qubits using Qiskit
        alice_bits, alice_bases, qubits = self._alice_prepare()
        
        # Step 2: Quantum transmission (with optional Eve)
        transmitted_qubits = qubits
        eve_stats = None
        
        if with_eavesdropper:
            # Note: Our eavesdropper works with regular Qubits
            # For full Qiskit integration, we'd need to adapt it
            # For now, we'll use the existing eavesdropper
            from .qubit import Qubit
            
            # Convert Qiskit qubits to regular qubits for Eve
            regular_qubits = [
                Qubit(q.basis, q.bit_value) for q in qubits
            ]
            
            eve = Eavesdropper(intercept_probability=eavesdropper_intercept_rate)
            intercepted_regular = eve.intercept(regular_qubits)
            eve_stats = eve.get_statistics()
            
            # Convert back to Qiskit qubits
            transmitted_qubits = [
                QiskitQubit(q.basis, q.bit_value) for q in intercepted_regular
            ]
        
        # Step 3: Bob measures using Qiskit
        bob_bits, bob_bases = self._bob_measure(transmitted_qubits)
        
        # Step 4: Basis sifting
        sifted_alice, sifted_bob, matching_indices = self._basis_sifting(
            alice_bits, alice_bases, bob_bits, bob_bases
        )
        
        # Step 5: Error estimation
        error_rate, errors, checked_indices, sample_size, is_secure = self._error_estimation(
            sifted_alice, sifted_bob
        )
        
        # Step 6: Privacy amplification
        final_key = self._privacy_amplification(sifted_alice, checked_indices)
        
        # Calculate statistics
        total_transmitted = len(alice_bits)
        total_sifted = len(sifted_alice)
        final_key_length = len(final_key)
        sifting_efficiency = (total_sifted / total_transmitted * 100) if total_transmitted > 0 else 0
        
        return QiskitBB84Result(
            alice_bits=alice_bits,
            alice_bases=alice_bases,
            bob_bits=bob_bits,
            bob_bases=bob_bases,
            sifted_alice_bits=sifted_alice,
            sifted_bob_bits=sifted_bob,
            matching_indices=matching_indices,
            error_rate=error_rate,
            errors_found=errors,
            checked_indices=checked_indices,
            sample_size=sample_size,
            is_secure=is_secure,
            final_key=final_key,
            total_transmitted=total_transmitted,
            total_sifted=total_sifted,
            final_key_length=final_key_length,
            sifting_efficiency=sifting_efficiency,
            eavesdropper_present=with_eavesdropper,
            eavesdropper_stats=eve_stats
        )
    
    def _alice_prepare(self) -> tuple[list[int], list[BasisType], list[QiskitQubit]]:
        """
        Step 1: Alice prepares qubits using Qiskit quantum circuits.
        
        Returns:
            Tuple of (bits, bases, qiskit_qubits)
        """
        n = self.key_length * self.transmission_multiplier
        
        alice_bits = [random.choice([0, 1]) for _ in range(n)]
        alice_bases = [random.choice(['Z', 'X']) for _ in range(n)]
        
        # Create Qiskit qubits
        qubits = [
            QiskitQubit(basis, bit)
            for basis, bit in zip(alice_bases, alice_bits)
        ]
        
        return alice_bits, alice_bases, qubits
    
    def _bob_measure(self, qubits: list[QiskitQubit]) -> tuple[list[int], list[BasisType]]:
        """
        Step 3: Bob measures qubits using Qiskit simulation.
        
        Args:
            qubits: List of Qiskit qubits
            
        Returns:
            Tuple of (measurement_results, measurement_bases)
        """
        n = len(qubits)
        bob_bases = [random.choice(['Z', 'X']) for _ in range(n)]
        
        # Measure each qubit using Qiskit
        bob_bits = [
            qubit.measure(basis)
            for qubit, basis in zip(qubits, bob_bases)
        ]
        
        return bob_bits, bob_bases
    
    def _basis_sifting(
        self,
        alice_bits: list[int],
        alice_bases: list[BasisType],
        bob_bits: list[int],
        bob_bases: list[BasisType]
    ) -> tuple[list[int], list[int], list[int]]:
        """Step 4: Basis sifting."""
        sifted_alice = []
        sifted_bob = []
        matching_indices = []
        
        for i in range(len(alice_bases)):
            if alice_bases[i] == bob_bases[i]:
                sifted_alice.append(alice_bits[i])
                sifted_bob.append(bob_bits[i])
                matching_indices.append(i)
        
        return sifted_alice, sifted_bob, matching_indices
    
    def _error_estimation(
        self,
        sifted_alice: list[int],
        sifted_bob: list[int],
        sample_fraction: float = 0.1
    ) -> tuple[float, int, list[int], int, bool]:
        """Step 5: Error estimation."""
        n = len(sifted_alice)
        sample_size = max(1, min(int(n * sample_fraction), n // 2))
        
        available_indices = list(range(n))
        random.shuffle(available_indices)
        checked_indices = sorted(available_indices[:sample_size])
        
        errors = sum(
            1 for i in checked_indices
            if sifted_alice[i] != sifted_bob[i]
        )
        
        error_rate = errors / sample_size if sample_size > 0 else 0.0
        is_secure = error_rate <= self.qber_threshold
        
        return error_rate, errors, checked_indices, sample_size, is_secure
    
    def _privacy_amplification(
        self,
        sifted_bits: list[int],
        checked_indices: list[int]
    ) -> list[int]:
        """Step 6: Privacy amplification."""
        remaining_bits = [
            bit for i, bit in enumerate(sifted_bits)
            if i not in checked_indices
        ]
        
        return remaining_bits[:self.key_length]


# Demo
if __name__ == "__main__":
    print("=" * 70)
    print("Qiskit-based BB84 Protocol Demo")
    print("=" * 70)
    
    # Scenario 1: No eavesdropper
    print("\n" + "=" * 70)
    print("SCENARIO 1: Secure Channel (Qiskit Simulation)")
    print("=" * 70)
    
    protocol = QiskitBB84Protocol(key_length=128)
    result = protocol.execute(with_eavesdropper=False)
    
    print(f"\nImplementation: {result.implementation}")
    print(f"Qubits transmitted: {result.total_transmitted}")
    print(f"After sifting: {result.total_sifted} ({result.sifting_efficiency:.1f}%)")
    print(f"Final key: {result.final_key_length} bits")
    print(f"QBER: {result.error_rate*100:.2f}%")
    print(f"Status: {'✓ SECURE' if result.is_secure else '⚠ INSECURE'}")
    
    # Scenario 2: With eavesdropper
    print("\n" + "=" * 70)
    print("SCENARIO 2: Channel with Eavesdropper (Qiskit Simulation)")
    print("=" * 70)
    
    result_eve = protocol.execute(with_eavesdropper=True, eavesdropper_intercept_rate=0.5)
    
    print(f"\nImplementation: {result_eve.implementation}")
    print(f"Qubits transmitted: {result_eve.total_transmitted}")
    print(f"After sifting: {result_eve.total_sifted} ({result_eve.sifting_efficiency:.1f}%)")
    print(f"Final key: {result_eve.final_key_length} bits")
    print(f"QBER: {result_eve.error_rate*100:.2f}%")
    print(f"Status: {'✓ SECURE' if result_eve.is_secure else '⚠ EAVESDROPPING DETECTED!'}")
    
    if result_eve.eavesdropper_stats:
        print(f"\nEve intercepted: {result_eve.eavesdropper_stats['total_intercepted']} qubits")
    
    print("\n" + "=" * 70)
    print("✅ Qiskit-based BB84 protocol complete!")
    print("=" * 70)