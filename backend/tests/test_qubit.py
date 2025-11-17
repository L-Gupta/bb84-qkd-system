"""
Unit tests for the Qubit class in BB84 protocol.

Tests quantum measurement behavior, state representations,
and batch operations.
"""

import pytest
from core.qubit import Qubit, create_random_qubit, create_qubit_batch, measure_qubit_batch


class TestQubitCreation:
    """Test qubit initialization and state representation."""
    
    def test_qubit_z_basis_bit_0(self):
        """Test Z-basis qubit with bit value 0 creates |0⟩ state."""
        q = Qubit('Z', 0)
        assert q.basis == 'Z'
        assert q.bit_value == 0
        assert q.state == '|0⟩'
    
    def test_qubit_z_basis_bit_1(self):
        """Test Z-basis qubit with bit value 1 creates |1⟩ state."""
        q = Qubit('Z', 1)
        assert q.basis == 'Z'
        assert q.bit_value == 1
        assert q.state == '|1⟩'
    
    def test_qubit_x_basis_bit_0(self):
        """Test X-basis qubit with bit value 0 creates |+⟩ state."""
        q = Qubit('X', 0)
        assert q.basis == 'X'
        assert q.bit_value == 0
        assert q.state == '|+⟩'
    
    def test_qubit_x_basis_bit_1(self):
        """Test X-basis qubit with bit value 1 creates |−⟩ state."""
        q = Qubit('X', 1)
        assert q.basis == 'X'
        assert q.bit_value == 1
        assert q.state == '|−⟩'
    
    def test_invalid_basis_raises_error(self):
        """Test that invalid basis raises ValueError."""
        with pytest.raises(ValueError, match="Basis must be 'Z' or 'X'"):
            Qubit('Y', 0)
        
        with pytest.raises(ValueError, match="Basis must be 'Z' or 'X'"):
            Qubit('invalid', 1)
    
    def test_invalid_bit_value_raises_error(self):
        """Test that invalid bit value raises ValueError."""
        with pytest.raises(ValueError, match="Bit value must be 0 or 1"):
            Qubit('Z', 2)
        
        with pytest.raises(ValueError, match="Bit value must be 0 or 1"):
            Qubit('X', -1)
    
    def test_qubit_repr(self):
        """Test string representation of qubit."""
        q = Qubit('Z', 0)
        repr_str = repr(q)
        assert 'Z' in repr_str
        assert '0' in repr_str
        assert '|0⟩' in repr_str
    
    def test_qubit_str(self):
        """Test human-readable string of qubit."""
        q = Qubit('X', 1)
        assert str(q) == '|−⟩'


class TestCorrectBasisMeasurement:
    """Test measurements when basis matches preparation basis."""
    
    def test_z_basis_bit_0_measured_in_z(self):
        """Test |0⟩ measured in Z-basis always gives 0."""
        q = Qubit('Z', 0)
        results = [q.measure('Z') for _ in range(100)]
        assert all(r == 0 for r in results), "All measurements should return 0"
        assert sum(results) == 0
    
    def test_z_basis_bit_1_measured_in_z(self):
        """Test |1⟩ measured in Z-basis always gives 1."""
        q = Qubit('Z', 1)
        results = [q.measure('Z') for _ in range(100)]
        assert all(r == 1 for r in results), "All measurements should return 1"
        assert sum(results) == 100
    
    def test_x_basis_bit_0_measured_in_x(self):
        """Test |+⟩ measured in X-basis always gives 0."""
        q = Qubit('X', 0)
        results = [q.measure('X') for _ in range(100)]
        assert all(r == 0 for r in results), "All measurements should return 0"
        assert sum(results) == 0
    
    def test_x_basis_bit_1_measured_in_x(self):
        """Test |−⟩ measured in X-basis always gives 1."""
        q = Qubit('X', 1)
        results = [q.measure('X') for _ in range(100)]
        assert all(r == 1 for r in results), "All measurements should return 1"
        assert sum(results) == 100
    
    def test_correct_basis_is_deterministic(self):
        """Test that correct basis measurements are 100% deterministic."""
        test_cases = [
            ('Z', 0, 'Z'),
            ('Z', 1, 'Z'),
            ('X', 0, 'X'),
            ('X', 1, 'X')
        ]
        
        for prep_basis, bit, meas_basis in test_cases:
            q = Qubit(prep_basis, bit)
            results = [q.measure(meas_basis) for _ in range(100)]
            accuracy = sum(1 for r in results if r == bit) / len(results)
            assert accuracy == 1.0, f"Correct basis should be 100% accurate for {q.state}"


class TestWrongBasisMeasurement:
    """Test measurements when basis doesn't match preparation basis."""
    
    def test_z_bit_0_measured_in_x_is_random(self):
        """Test |0⟩ measured in X-basis gives ~50% 0s and 50% 1s."""
        q = Qubit('Z', 0)
        results = [q.measure('X') for _ in range(1000)]
        zeros = sum(1 for r in results if r == 0)
        ones = len(results) - zeros
        
        # Statistical test: should be within 40-60% range (very lenient)
        assert 400 <= zeros <= 600, f"Expected ~50% zeros, got {zeros/10}%"
        assert 400 <= ones <= 600, f"Expected ~50% ones, got {ones/10}%"
    
    def test_z_bit_1_measured_in_x_is_random(self):
        """Test |1⟩ measured in X-basis gives ~50% 0s and 50% 1s."""
        q = Qubit('Z', 1)
        results = [q.measure('X') for _ in range(1000)]
        zeros = sum(1 for r in results if r == 0)
        ones = len(results) - zeros
        
        assert 400 <= zeros <= 600, f"Expected ~50% zeros, got {zeros/10}%"
        assert 400 <= ones <= 600, f"Expected ~50% ones, got {ones/10}%"
    
    def test_x_bit_0_measured_in_z_is_random(self):
        """Test |+⟩ measured in Z-basis gives ~50% 0s and 50% 1s."""
        q = Qubit('X', 0)
        results = [q.measure('Z') for _ in range(1000)]
        zeros = sum(1 for r in results if r == 0)
        ones = len(results) - zeros
        
        assert 400 <= zeros <= 600, f"Expected ~50% zeros, got {zeros/10}%"
        assert 400 <= ones <= 600, f"Expected ~50% ones, got {ones/10}%"
    
    def test_x_bit_1_measured_in_z_is_random(self):
        """Test |−⟩ measured in Z-basis gives ~50% 0s and 50% 1s."""
        q = Qubit('X', 1)
        results = [q.measure('Z') for _ in range(1000)]
        zeros = sum(1 for r in results if r == 0)
        ones = len(results) - zeros
        
        assert 400 <= zeros <= 600, f"Expected ~50% zeros, got {zeros/10}%"
        assert 400 <= ones <= 600, f"Expected ~50% ones, got {ones/10}%"
    
    def test_wrong_basis_creates_uncertainty(self):
        """Test that wrong basis measurements have high variance."""
        # Multiple runs should give different results
        q = Qubit('Z', 0)
        run1 = sum(q.measure('X') for _ in range(100))
        run2 = sum(q.measure('X') for _ in range(100))
        run3 = sum(q.measure('X') for _ in range(100))
        
        # Very unlikely all three runs are identical if truly random
        assert not (run1 == run2 == run3), "Random measurements should vary between runs"


class TestMeasurementValidation:
    """Test measurement input validation."""
    
    def test_invalid_measurement_basis_raises_error(self):
        """Test that invalid measurement basis raises ValueError."""
        q = Qubit('Z', 0)
        
        with pytest.raises(ValueError, match="Measurement basis must be 'Z' or 'X'"):
            q.measure('Y')
        
        with pytest.raises(ValueError, match="Measurement basis must be 'Z' or 'X'"):
            q.measure('invalid')


class TestStateVectors:
    """Test quantum state vector representations."""
    
    def test_z_bit_0_state_vector(self):
        """Test |0⟩ has state vector (1, 0)."""
        q = Qubit('Z', 0)
        vec = q.get_state_vector()
        assert vec == (1.0, 0.0)
    
    def test_z_bit_1_state_vector(self):
        """Test |1⟩ has state vector (0, 1)."""
        q = Qubit('Z', 1)
        vec = q.get_state_vector()
        assert vec == (0.0, 1.0)
    
    def test_x_bit_0_state_vector(self):
        """Test |+⟩ has state vector (1/√2, 1/√2)."""
        q = Qubit('X', 0)
        vec = q.get_state_vector()
        sqrt_2_inv = 1.0 / (2 ** 0.5)
        assert abs(vec[0] - sqrt_2_inv) < 1e-10
        assert abs(vec[1] - sqrt_2_inv) < 1e-10
    
    def test_x_bit_1_state_vector(self):
        """Test |−⟩ has state vector (1/√2, -1/√2)."""
        q = Qubit('X', 1)
        vec = q.get_state_vector()
        sqrt_2_inv = 1.0 / (2 ** 0.5)
        assert abs(vec[0] - sqrt_2_inv) < 1e-10
        assert abs(vec[1] - (-sqrt_2_inv)) < 1e-10
    
    def test_state_vectors_are_normalized(self):
        """Test that all state vectors have unit length."""
        test_qubits = [
            Qubit('Z', 0),
            Qubit('Z', 1),
            Qubit('X', 0),
            Qubit('X', 1)
        ]
        
        for q in test_qubits:
            vec = q.get_state_vector()
            magnitude = (vec[0]**2 + vec[1]**2) ** 0.5
            assert abs(magnitude - 1.0) < 1e-10, f"State vector {vec} should be normalized"


class TestBatchOperations:
    """Test batch qubit creation and measurement."""
    
    def test_create_random_qubit(self):
        """Test random qubit creation."""
        q = create_random_qubit()
        assert q.basis in ['Z', 'X']
        assert q.bit_value in [0, 1]
        assert q.state in ['|0⟩', '|1⟩', '|+⟩', '|−⟩']
    
    def test_create_qubit_batch(self):
        """Test creating multiple random qubits."""
        batch = create_qubit_batch(100)
        assert len(batch) == 100
        assert all(isinstance(q, Qubit) for q in batch)
        
        # Check we have variety in bases and bits
        bases = [q.basis for q in batch]
        bits = [q.bit_value for q in batch]
        
        # Should have both Z and X bases (statistically)
        assert 'Z' in bases and 'X' in bases
        # Should have both 0 and 1 bits (statistically)
        assert 0 in bits and 1 in bits
    
    def test_measure_qubit_batch(self):
        """Test batch measurement of qubits."""
        qubits = [Qubit('Z', 0), Qubit('X', 1), Qubit('Z', 1), Qubit('X', 0)]
        bases = ['Z', 'X', 'Z', 'X']
        
        results = measure_qubit_batch(qubits, bases)
        
        assert len(results) == 4
        assert results == [0, 1, 1, 0]  # All correct basis measurements
    
    def test_measure_qubit_batch_length_mismatch(self):
        """Test that mismatched lengths raise ValueError."""
        qubits = [Qubit('Z', 0), Qubit('X', 1)]
        bases = ['Z', 'X', 'Z']  # Different length
        
        with pytest.raises(ValueError, match="must match"):
            measure_qubit_batch(qubits, bases)
    
    def test_batch_with_mixed_bases(self):
        """Test batch measurement with mixed correct/incorrect bases."""
        qubits = [
            Qubit('Z', 0),  # Will measure in Z (correct)
            Qubit('Z', 1),  # Will measure in X (wrong)
            Qubit('X', 0),  # Will measure in X (correct)
            Qubit('X', 1),  # Will measure in Z (wrong)
        ]
        bases = ['Z', 'X', 'X', 'Z']
        
        # Run multiple times to account for randomness
        for _ in range(10):
            results = measure_qubit_batch(qubits, bases)
            assert results[0] == 0  # Correct basis, should be deterministic
            assert results[2] == 0  # Correct basis, should be deterministic
            # results[1] and results[3] are random, so we don't assert specific values


class TestQuantumBehavior:
    """Integration tests for quantum mechanical behavior."""
    
    def test_measurement_collapse(self):
        """Test that measurement doesn't change qubit properties."""
        q = Qubit('Z', 0)
        
        # Measure multiple times
        result1 = q.measure('Z')
        result2 = q.measure('Z')
        result3 = q.measure('Z')
        
        # Qubit properties shouldn't change
        assert q.basis == 'Z'
        assert q.bit_value == 0
        assert q.state == '|0⟩'
        
        # Results should be consistent (correct basis)
        assert result1 == result2 == result3 == 0
    
    def test_basis_independence(self):
        """Test that different qubits are independent."""
        q1 = Qubit('Z', 0)
        q2 = Qubit('Z', 0)
        
        # Measuring one shouldn't affect the other
        r1 = q1.measure('X')  # Random
        r2 = q2.measure('X')  # Random
        
        # Both should still have original properties
        assert q1.basis == 'Z' and q1.bit_value == 0
        assert q2.basis == 'Z' and q2.bit_value == 0
        
        # Results can be different (they're independent random)
        # No assertion on r1 vs r2 since they're independent


# Run tests with detailed output
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])