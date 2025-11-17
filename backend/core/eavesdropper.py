"""
Eavesdropper (Eve) implementation for BB84 protocol.

Simulates various attack strategies on quantum key distribution,
primarily the intercept-resend attack.
"""

import random
from typing import Literal
from .qubit import Qubit, BasisType


AttackStrategy = Literal['intercept-resend', 'passive']


class Eavesdropper:
    """
    Simulates an eavesdropper (Eve) attempting to intercept quantum communication.
    
    The primary attack is "intercept-resend":
    1. Eve intercepts a qubit from Alice
    2. Eve measures it in a randomly chosen basis
    3. Eve's measurement collapses the quantum state
    4. Eve creates a NEW qubit based on her measurement
    5. Eve sends this new qubit to Bob
    
    If Eve chooses the wrong basis (~50% of the time), she disturbs the state,
    causing detectable errors in Bob's measurements.
    
    Attributes:
        intercept_probability (float): Probability of intercepting each qubit (0.0 to 1.0)
        strategy (str): Attack strategy ('intercept-resend' or 'passive')
        intercepted_count (int): Number of qubits intercepted
        eve_bits (list): Bits Eve measured
        eve_bases (list): Bases Eve used for measurement
    """
    
    def __init__(self, intercept_probability: float = 0.5, strategy: AttackStrategy = 'intercept-resend'):
        """
        Initialize the eavesdropper.
        
        Args:
            intercept_probability: Fraction of qubits to intercept (0.0 = none, 1.0 = all)
            strategy: Attack strategy to use
            
        Raises:
            ValueError: If intercept_probability is not between 0 and 1
        """
        if not 0.0 <= intercept_probability <= 1.0:
            raise ValueError(f"Intercept probability must be between 0 and 1, got {intercept_probability}")
        
        if strategy not in ['intercept-resend', 'passive']:
            raise ValueError(f"Strategy must be 'intercept-resend' or 'passive', got '{strategy}'")
        
        self.intercept_probability = intercept_probability
        self.strategy = strategy
        
        # Track Eve's activity
        self.intercepted_count = 0
        self.eve_bits = []
        self.eve_bases = []
        self.interception_indices = []
    
    def intercept(self, qubits: list[Qubit]) -> list[Qubit]:
        """
        Intercept and potentially manipulate a list of qubits.
        
        For each qubit, Eve decides whether to intercept based on intercept_probability.
        If intercepted, Eve performs the chosen attack strategy.
        
        Args:
            qubits: List of qubits transmitted from Alice to Bob
            
        Returns:
            List of qubits (potentially modified by Eve) that Bob receives
        """
        if self.strategy == 'passive':
            # Passive attack: just observe, don't modify
            return qubits
        
        # Intercept-resend attack
        modified_qubits = []
        
        for idx, qubit in enumerate(qubits):
            if random.random() < self.intercept_probability:
                # Eve intercepts this qubit
                intercepted_qubit = self._intercept_and_resend(qubit)
                modified_qubits.append(intercepted_qubit)
                self.interception_indices.append(idx)
                self.intercepted_count += 1
            else:
                # Eve lets this qubit pass unchanged
                modified_qubits.append(qubit)
                
        return modified_qubits
    
    def _intercept_and_resend(self, qubit: Qubit) -> Qubit:
        """
        Perform intercept-resend attack on a single qubit.
        
        This is the core of Eve's attack:
        1. Choose a random measurement basis
        2. Measure the qubit (collapses its state!)
        3. Create a new qubit based on the measurement
        4. Send the new qubit to Bob
        
        Critical point: If Eve chooses the wrong basis, she disturbs the state,
        and this creates detectable errors.
        
        Args:
            qubit: The qubit to intercept
            
        Returns:
            New qubit created by Eve based on her measurement
        """
        # Eve randomly chooses a measurement basis
        eve_basis = random.choice(['Z', 'X'])
        
        # Eve measures the qubit (this collapses the quantum state!)
        eve_measurement = qubit.measure(eve_basis)
        
        # Record Eve's measurement
        self.eve_bits.append(eve_measurement)
        self.eve_bases.append(eve_basis)
        
        # Eve creates a NEW qubit based on what she measured
        # This is the "resend" part of intercept-resend
        new_qubit = Qubit(eve_basis, eve_measurement)
        
        return new_qubit
    
    def reset(self):
        """Reset Eve's tracking data for a new protocol run."""
        self.intercepted_count = 0
        self.eve_bits = []
        self.eve_bases = []
        self.interception_indices = []
    
    def get_statistics(self) -> dict:
        """
        Get statistics about Eve's interception activity.
        
        Returns:
            Dictionary containing:
                - total_intercepted: Number of qubits intercepted
                - intercept_rate: Actual interception rate achieved
                - bases_used: Count of Z and X bases used
                - bits_measured: Count of 0s and 1s measured
        """
        z_count = sum(1 for b in self.eve_bases if b == 'Z')
        x_count = sum(1 for b in self.eve_bases if b == 'X')
        
        zero_count = sum(1 for b in self.eve_bits if b == 0)
        one_count = sum(1 for b in self.eve_bits if b == 1)
        
        return {
            'total_intercepted': self.intercepted_count,
            'intercept_rate': self.intercept_probability,
            'bases_used': {
                'Z': z_count,
                'X': x_count
            },
            'bits_measured': {
                '0': zero_count,
                '1': one_count
            },
            'interception_indices': self.interception_indices
        }
    
    def __repr__(self) -> str:
        """String representation for debugging."""
        return (f"Eavesdropper(strategy='{self.strategy}', "
                f"intercept_prob={self.intercept_probability}, "
                f"intercepted={self.intercepted_count})")


def calculate_expected_qber(intercept_rate: float) -> float:
    """
    Calculate the theoretical Quantum Bit Error Rate (QBER) for a given intercept rate.
    
    Theory:
    - With no eavesdropping: QBER ≈ 0%
    - With perfect channel and Eve intercepting with random bases:
      * Eve chooses wrong basis 50% of the time
      * When wrong basis, she disturbs the state
      * This causes 25% error rate per intercepted qubit
      * Overall: QBER = intercept_rate × 0.25
    
    For example:
    - 0% interception → 0% QBER
    - 50% interception → 12.5% QBER (detectable! > 11% threshold)
    - 100% interception → 25% QBER (very obvious!)
    
    Args:
        intercept_rate: Fraction of qubits Eve intercepts (0.0 to 1.0)
        
    Returns:
        Expected QBER as a fraction (0.0 to 0.25)
    """
    if not 0.0 <= intercept_rate <= 1.0:
        raise ValueError(f"Intercept rate must be between 0 and 1, got {intercept_rate}")
    
    # Theoretical QBER formula for intercept-resend attack
    # Eve has 50% chance of choosing wrong basis
    # Wrong basis causes 50% measurement error
    # Combined: 0.5 × 0.5 = 0.25 error rate per intercepted qubit
    return intercept_rate * 0.25


def simulate_interception(
    qubits: list[Qubit],
    intercept_rate: float = 0.5
) -> tuple[list[Qubit], Eavesdropper]:
    """
    Convenience function to simulate Eve's attack on a list of qubits.
    
    Args:
        qubits: List of qubits from Alice
        intercept_rate: Fraction of qubits to intercept
        
    Returns:
        Tuple of (modified_qubits, eavesdropper_instance)
    """
    eve = Eavesdropper(intercept_probability=intercept_rate)
    modified_qubits = eve.intercept(qubits)
    return modified_qubits, eve


# Demo and testing
if __name__ == "__main__":
    from .qubit import create_qubit_batch
    
    print("=" * 60)
    print("BB84 Eavesdropper Demo")
    print("=" * 60)
    
    # Create sample qubits from Alice
    print("\n1. Alice prepares 20 qubits:")
    alice_qubits = create_qubit_batch(20)
    print(f"   Alice's qubits: {[str(q) for q in alice_qubits[:5]]}...")
    
    # Scenario 1: No eavesdropping
    print("\n2. Scenario: No eavesdropping (intercept_rate=0.0)")
    eve_none = Eavesdropper(intercept_probability=0.0)
    qubits_no_eve = eve_none.intercept(alice_qubits)
    print(f"   Intercepted: {eve_none.intercepted_count}/20")
    print(f"   Expected QBER: {calculate_expected_qber(0.0)*100:.1f}%")
    
    # Scenario 2: Partial eavesdropping
    print("\n3. Scenario: Moderate eavesdropping (intercept_rate=0.5)")
    eve_moderate = Eavesdropper(intercept_probability=0.5)
    qubits_moderate = eve_moderate.intercept(alice_qubits)
    print(f"   Intercepted: {eve_moderate.intercepted_count}/20")
    print(f"   Expected QBER: {calculate_expected_qber(0.5)*100:.1f}%")
    print(f"   Statistics: {eve_moderate.get_statistics()}")
    
    # Scenario 3: Full eavesdropping
    print("\n4. Scenario: Full eavesdropping (intercept_rate=1.0)")
    eve_full = Eavesdropper(intercept_probability=1.0)
    qubits_full = eve_full.intercept(alice_qubits)
    print(f"   Intercepted: {eve_full.intercepted_count}/20")
    print(f"   Expected QBER: {calculate_expected_qber(1.0)*100:.1f}%")
    
    # Expected QBER table
    print("\n5. Expected QBER for different intercept rates:")
    print("-" * 60)
    print("Intercept Rate | Expected QBER | Detectable?")
    print("-" * 60)
    for rate in [0.0, 0.1, 0.3, 0.5, 0.7, 1.0]:
        qber = calculate_expected_qber(rate) * 100
        detectable = "YES ⚠️" if qber > 11 else "NO ✓"
        print(f"{rate*100:13.0f}% | {qber:12.1f}% | {detectable}")
    
    print("\n" + "=" * 60)
    print("Note: BB84 security threshold is 11% QBER")
    print("Above 11% → Eavesdropping detected → Abort protocol")
    print("=" * 60)