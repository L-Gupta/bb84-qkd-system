"""
BB84 Quantum Key Distribution Protocol Implementation.

Implements the complete 6-step BB84 protocol:
1. Alice prepares qubits in random bases
2. Quantum transmission (with optional eavesdropper)
3. Bob measures qubits in random bases
4. Basis sifting (keep only matching bases)
5. Error estimation (check for eavesdropping)
6. Privacy amplification (generate final key)
"""

import random
from typing import Optional
from dataclasses import dataclass
from .qubit import Qubit, BasisType
from .eavesdropper import Eavesdropper


@dataclass
class BB84Result:
    """
    Complete result of BB84 protocol execution.
    
    Contains all intermediate and final data from the protocol run.
    """
    # Step 1: Alice's preparation
    alice_bits: list[int]
    alice_bases: list[BasisType]
    
    # Step 3: Bob's measurement
    bob_bits: list[int]
    bob_bases: list[BasisType]
    
    # Step 4: Sifting
    sifted_alice_bits: list[int]
    sifted_bob_bits: list[int]
    matching_indices: list[int]
    
    # Step 5: Error estimation
    error_rate: float
    errors_found: int
    checked_indices: list[int]
    sample_size: int
    is_secure: bool
    
    # Step 6: Final key
    final_key: list[int]
    
    # Statistics
    total_transmitted: int
    total_sifted: int
    final_key_length: int
    sifting_efficiency: float
    
    # Eavesdropper info (if applicable)
    eavesdropper_present: bool
    eavesdropper_stats: Optional[dict] = None


class BB84Protocol:
    """
    Implementation of the BB84 Quantum Key Distribution protocol.
    
    The protocol allows two parties (Alice and Bob) to establish a shared
    secret key over an insecure quantum channel, with guaranteed detection
    of any eavesdropping attempts.
    """
    
    def __init__(self, key_length: int = 256, transmission_multiplier: int = 4):
        """
        Initialize the BB84 protocol.
        
        Args:
            key_length: Desired length of final shared key in bits
            transmission_multiplier: How many extra bits to transmit
                                    (due to sifting and error checking losses)
        
        Raises:
            ValueError: If parameters are invalid
        """
        if key_length <= 0:
            raise ValueError(f"Key length must be positive, got {key_length}")
        
        if transmission_multiplier < 2:
            raise ValueError(f"Transmission multiplier must be >= 2, got {transmission_multiplier}")
        
        self.key_length = key_length
        self.transmission_multiplier = transmission_multiplier
        self.qber_threshold = 0.11  # 11% security threshold
    
    def execute(
        self,
        with_eavesdropper: bool = False,
        eavesdropper_intercept_rate: float = 0.5
    ) -> BB84Result:
        """
        Execute the complete BB84 protocol.
        
        Args:
            with_eavesdropper: Whether to simulate an eavesdropper
            eavesdropper_intercept_rate: Fraction of qubits Eve intercepts
            
        Returns:
            BB84Result containing all protocol data and final key
        """
        # Step 1: Alice prepares qubits
        alice_bits, alice_bases, qubits = self._alice_prepare()
        
        # Step 2: Quantum transmission (with optional Eve)
        transmitted_qubits = qubits
        eve_stats = None
        
        if with_eavesdropper:
            eve = Eavesdropper(intercept_probability=eavesdropper_intercept_rate)
            transmitted_qubits = eve.intercept(qubits)
            eve_stats = eve.get_statistics()
        
        # Step 3: Bob measures
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
        
        return BB84Result(
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
    
    def _alice_prepare(self) -> tuple[list[int], list[BasisType], list[Qubit]]:
        """
        Step 1: Alice prepares qubits with random bits and bases.
        
        Returns:
            Tuple of (bits, bases, qubits)
        """
        n = self.key_length * self.transmission_multiplier
        
        # Generate random bits and bases
        alice_bits = [random.choice([0, 1]) for _ in range(n)]
        alice_bases = [random.choice(['Z', 'X']) for _ in range(n)]
        
        # Create qubits
        qubits = [Qubit(basis, bit) for basis, bit in zip(alice_bases, alice_bits)]
        
        return alice_bits, alice_bases, qubits
    
    def _bob_measure(self, qubits: list[Qubit]) -> tuple[list[int], list[BasisType]]:
        """
        Step 3: Bob measures qubits with random bases.
        
        Args:
            qubits: List of qubits received from Alice (possibly intercepted by Eve)
            
        Returns:
            Tuple of (measurement_results, measurement_bases)
        """
        n = len(qubits)
        
        # Bob randomly chooses measurement bases
        bob_bases = [random.choice(['Z', 'X']) for _ in range(n)]
        
        # Bob measures each qubit
        bob_bits = [qubit.measure(basis) for qubit, basis in zip(qubits, bob_bases)]
        
        return bob_bits, bob_bases
    
    def _basis_sifting(
        self,
        alice_bits: list[int],
        alice_bases: list[BasisType],
        bob_bits: list[int],
        bob_bases: list[BasisType]
    ) -> tuple[list[int], list[int], list[int]]:
        """
        Step 4: Basis sifting - keep only bits where bases matched.
        
        Alice and Bob publicly announce their bases (NOT the bit values).
        They keep only the bits where they used the same basis.
        
        Args:
            alice_bits: Alice's bit values
            alice_bases: Alice's preparation bases
            bob_bits: Bob's measurement results
            bob_bases: Bob's measurement bases
            
        Returns:
            Tuple of (sifted_alice_bits, sifted_bob_bits, matching_indices)
        """
        sifted_alice = []
        sifted_bob = []
        matching_indices = []
        
        for i in range(len(alice_bases)):
            if alice_bases[i] == bob_bases[i]:
                # Bases match - keep this bit
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
        """
        Step 5: Error estimation - check for eavesdropping.
        
        Alice and Bob publicly compare a random sample of their sifted bits.
        If error rate is too high (> 11%), eavesdropping is detected.
        
        Args:
            sifted_alice: Alice's sifted bits
            sifted_bob: Bob's sifted bits
            sample_fraction: Fraction of bits to check (default 10%)
            
        Returns:
            Tuple of (error_rate, errors_found, checked_indices, sample_size, is_secure)
        """
        n = len(sifted_alice)
        sample_size = max(1, min(int(n * sample_fraction), n // 2))
        
        # Randomly select indices to check
        available_indices = list(range(n))
        random.shuffle(available_indices)
        checked_indices = sorted(available_indices[:sample_size])
        
        # Compare bits at checked indices
        errors = sum(
            1 for i in checked_indices
            if sifted_alice[i] != sifted_bob[i]
        )
        
        # Calculate Quantum Bit Error Rate (QBER)
        error_rate = errors / sample_size if sample_size > 0 else 0.0
        
        # Check security threshold
        is_secure = error_rate <= self.qber_threshold
        
        return error_rate, errors, checked_indices, sample_size, is_secure
    
    def _privacy_amplification(
        self,
        sifted_bits: list[int],
        checked_indices: list[int]
    ) -> list[int]:
        """
        Step 6: Privacy amplification - generate final secure key.
        
        Remove bits that were used for error checking, then take
        the first key_length bits as the final key.
        
        In a real implementation, this would involve error correction
        (e.g., Cascade protocol) and hash-based privacy amplification.
        Here we use a simplified version.
        
        Args:
            sifted_bits: Sifted bits from Alice (or Bob, they should match)
            checked_indices: Indices of bits used for error checking
            
        Returns:
            Final secure key
        """
        # Remove checked bits
        remaining_bits = [
            bit for i, bit in enumerate(sifted_bits)
            if i not in checked_indices
        ]
        
        # Take first key_length bits
        final_key = remaining_bits[:self.key_length]
        
        return final_key


# Utility functions
def bits_to_hex(bits: list[int]) -> str:
    """
    Convert a list of bits to hexadecimal string.
    
    Args:
        bits: List of 0s and 1s
        
    Returns:
        Hexadecimal string representation
    """
    hex_string = ""
    
    # Process in chunks of 4 bits
    for i in range(0, len(bits), 4):
        chunk = bits[i:i+4]
        
        # Pad last chunk if necessary
        while len(chunk) < 4:
            chunk.append(0)
        
        # Convert to hex digit
        value = chunk[0] * 8 + chunk[1] * 4 + chunk[2] * 2 + chunk[3]
        hex_string += format(value, 'X')
    
    return hex_string


def bits_to_string(bits: list[int]) -> str:
    """
    Convert a list of bits to a binary string.
    
    Args:
        bits: List of 0s and 1s
        
    Returns:
        Binary string (e.g., "10110101")
    """
    return ''.join(str(bit) for bit in bits)


# Demo and testing
if __name__ == "__main__":
    print("=" * 70)
    print("BB84 Quantum Key Distribution Protocol Demo")
    print("=" * 70)
    
    # Scenario 1: Secure channel (no eavesdropper)
    print("\n" + "=" * 70)
    print("SCENARIO 1: Secure Channel (No Eavesdropper)")
    print("=" * 70)
    
    protocol = BB84Protocol(key_length=256)
    result = protocol.execute(with_eavesdropper=False)
    
    print(f"\nTransmission:")
    print(f"  Qubits sent: {result.total_transmitted}")
    print(f"  After sifting: {result.total_sifted} ({result.sifting_efficiency:.1f}% efficiency)")
    print(f"  Final key length: {result.final_key_length} bits")
    
    print(f"\nSecurity Check:")
    print(f"  QBER: {result.error_rate*100:.2f}%")
    print(f"  Errors found: {result.errors_found}/{result.sample_size}")
    print(f"  Status: {'✓ SECURE' if result.is_secure else '⚠ INSECURE'}")
    
    print(f"\nFinal Key (first 64 bits):")
    print(f"  Binary: {bits_to_string(result.final_key[:64])}")
    print(f"  Hex: {bits_to_hex(result.final_key[:64])}")
    
    # Scenario 2: Channel with eavesdropper
    print("\n" + "=" * 70)
    print("SCENARIO 2: Channel with Eavesdropper (50% interception)")
    print("=" * 70)
    
    result_eve = protocol.execute(with_eavesdropper=True, eavesdropper_intercept_rate=0.5)
    
    print(f"\nTransmission:")
    print(f"  Qubits sent: {result_eve.total_transmitted}")
    print(f"  After sifting: {result_eve.total_sifted} ({result_eve.sifting_efficiency:.1f}% efficiency)")
    print(f"  Final key length: {result_eve.final_key_length} bits")
    
    print(f"\nEavesdropper Activity:")
    if result_eve.eavesdropper_stats:
        print(f"  Intercepted: {result_eve.eavesdropper_stats['total_intercepted']} qubits")
        print(f"  Intercept rate: {result_eve.eavesdropper_stats['intercept_rate']*100:.0f}%")
    
    print(f"\nSecurity Check:")
    print(f"  QBER: {result_eve.error_rate*100:.2f}%")
    print(f"  Errors found: {result_eve.errors_found}/{result_eve.sample_size}")
    print(f"  Status: {'✓ SECURE' if result_eve.is_secure else '⚠ EAVESDROPPING DETECTED!'}")
    
    if not result_eve.is_secure:
        print(f"\n  ⚠ WARNING: QBER exceeds {protocol.qber_threshold*100:.0f}% threshold!")
        print(f"  → Protocol should be ABORTED")
        print(f"  → Key is compromised and should NOT be used")
    
    # Comparison table
    print("\n" + "=" * 70)
    print("QBER Analysis for Different Intercept Rates")
    print("=" * 70)
    print(f"{'Intercept Rate':<20} {'Expected QBER':<20} {'Status':<20}")
    print("-" * 70)
    
    test_rates = [0.0, 0.2, 0.4, 0.5, 0.6, 0.8, 1.0]
    for rate in test_rates:
        expected_qber = rate * 0.25  # Theoretical QBER
        status = "✓ Secure" if expected_qber <= 0.11 else "⚠ Detected"
        print(f"{rate*100:<18.0f}%  {expected_qber*100:<18.1f}%  {status}")
    
    print("\n" + "=" * 70)
    print("Protocol execution complete!")
    print("=" * 70)