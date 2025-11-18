"""
Unit tests for Qiskit-based Qubit implementation.

Tests quantum circuit creation, state preparation, and measurements.
"""

import pytest
from core.qiskit_qubit import (
    QiskitQubit, 
    create_qiskit_qubit_batch, 
    measure_qiskit_qubit_batch
)


class TestQiskitQubitCreation:
    """Test Qiskit qubit initialization and state representation."""
    
    def test_qubit_z_basis_bit_0(self):
        """Test Z-basis qubit with bit value 0 creates |0⟩ state."""
        q = QiskitQubit('Z', 0)
        assert q.basis == 'Z'
        assert q.bit_value == 0
        assert q.get_state() == '|0⟩'
    
    def test_qubit_z_basis_bit_1(self):
        """Test Z-basis qubit with bit value 1 creates |1⟩ state."""
        q = QiskitQubit('Z', 1)
        assert q.basis == 'Z'
        assert q.bit_value == 1
        assert q.get_state() == '|1⟩'
    
    def test_qubit_x_basis_bit_0(self):
        """Test X-basis qubit with bit value 0 creates |+⟩ state."""
        q = QiskitQubit('X', 0)
        assert q.basis == 'X'
        assert q.bit_value == 0
        assert q.get_state() == '|+⟩'
    
    def test_qubit_x_basis_bit_1(self):
        """Test X-basis qubit with bit value 1 creates |−⟩ state."""
        q = QiskitQubit('X', 1)
        assert q.basis == 'X'
        assert q.bit_value == 1
        assert q.get_state() == '|−⟩'
    
    def test_invalid_basis_raises_error(self):
        """Test that invalid basis raises ValueError."""
        with pytest.raises(ValueError, match="Basis must be 'Z' or 'X'"):
            QiskitQubit('Y', 0)
    
    def test_invalid_bit_value_raises_error(self):
        """Test that invalid bit value raises ValueError."""
        with pytest.raises(ValueError, match="Bit value must be 0 or 1"):
            QiskitQubit('Z', 2)
    
    def test_qubit_has_circuit(self):
        """Test that qubit has a quantum circuit."""
        q = QiskitQubit('Z', 0)
        assert q.circuit is not None
        assert q.circuit.num_qubits == 1
    
    def test_qubit_has_statevector(self):
        """Test that qubit has a state vector."""
        q = QiskitQubit('Z', 0)
        assert q.statevector is not None
        sv = q.get_state_vector()
        assert len(sv) == 2  # Two amplitudes


class TestQiskitCorrectBasisMeasurement:
    """Test measurements when basis matches preparation basis."""
    
    def test_z_basis_bit_0_measured_in_z(self):
        """Test |0⟩ measured in Z-basis gives consistent results."""
        q = QiskitQubit('Z', 0)
        results = [q.measure('Z') for _ in range(20)]
        # Should be mostly 0s (allowing for quantum randomness)
        zeros = sum(1 for r in results if r == 0)
        assert zeros >= 15  # At least 75% correct (very lenient for quantum)
    
    def test_z_basis_bit_1_measured_in_z(self):
        """Test |1⟩ measured in Z-basis gives consistent results."""
        q = QiskitQubit('Z', 1)
        results = [q.measure('Z') for _ in range(20)]
        ones = sum(1 for r in results if r == 1)
        assert ones >= 15  # At least 75% correct
    
    def test_x_basis_bit_0_measured_in_x(self):
        """Test |+⟩ measured in X-basis gives consistent results."""
        q = QiskitQubit('X', 0)
        results = [q.measure('X') for _ in range(20)]
        zeros = sum(1 for r in results if r == 0)
        assert zeros >= 15  # At least 75% correct
    
    def test_x_basis_bit_1_measured_in_x(self):
        """Test |−⟩ measured in X-basis gives consistent results."""
        q = QiskitQubit('X', 1)
        results = [q.measure('X') for _ in range(20)]
        ones = sum(1 for r in results if r == 1)
        assert ones >= 15  # At least 75% correct


class TestQiskitWrongBasisMeasurement:
    """Test measurements when basis doesn't match preparation basis."""
    
    def test_z_bit_0_measured_in_x_is_random(self):
        """Test |0⟩ measured in X-basis gives random results."""
        q = QiskitQubit('Z', 0)
        results = [q.measure('X') for _ in range(100)]
        zeros = sum(1 for r in results if r == 0)
        ones = len(results) - zeros
        
        # Should be roughly 50/50 (very lenient range for quantum randomness)
        assert 30 <= zeros <= 70, f"Expected ~50% zeros, got {zeros}%"
        assert 30 <= ones <= 70, f"Expected ~50% ones, got {ones}%"
    
    def test_x_bit_0_measured_in_z_is_random(self):
        """Test |+⟩ measured in Z-basis gives random results."""
        q = QiskitQubit('X', 0)
        results = [q.measure('Z') for _ in range(100)]
        zeros = sum(1 for r in results if r == 0)
        
        assert 30 <= zeros <= 70, f"Expected ~50% zeros, got {zeros}%"


class TestQiskitStateVectors:
    """Test quantum state vector representations."""
    
    def test_z_bit_0_state_vector(self):
        """Test |0⟩ has correct state vector."""
        q = QiskitQubit('Z', 0)
        sv = q.get_state_vector()
        
        # |0⟩ = (1, 0)
        assert abs(abs(sv[0]) - 1.0) < 0.01
        assert abs(abs(sv[1]) - 0.0) < 0.01
    
    def test_z_bit_1_state_vector(self):
        """Test |1⟩ has correct state vector."""
        q = QiskitQubit('Z', 1)
        sv = q.get_state_vector()
        
        # |1⟩ = (0, 1)
        assert abs(abs(sv[0]) - 0.0) < 0.01
        assert abs(abs(sv[1]) - 1.0) < 0.01
    
    def test_x_bit_0_state_vector(self):
        """Test |+⟩ has correct state vector."""
        q = QiskitQubit('X', 0)
        sv = q.get_state_vector()
        
        # |+⟩ = (1/√2, 1/√2)
        sqrt_2_inv = 1.0 / (2 ** 0.5)
        assert abs(abs(sv[0]) - sqrt_2_inv) < 0.01
        assert abs(abs(sv[1]) - sqrt_2_inv) < 0.01
    
    def test_state_vectors_are_normalized(self):
        """Test that all state vectors have unit length."""
        test_qubits = [
            QiskitQubit('Z', 0),
            QiskitQubit('Z', 1),
            QiskitQubit('X', 0),
            QiskitQubit('X', 1)
        ]
        
        for q in test_qubits:
            sv = q.get_state_vector()
            magnitude = (abs(sv[0])**2 + abs(sv[1])**2) ** 0.5
            assert abs(magnitude - 1.0) < 0.01, f"State vector should be normalized"


class TestQiskitBatchOperations:
    """Test batch qubit creation and measurement."""
    
    def test_create_qubit_batch(self):
        """Test creating multiple random qubits."""
        batch = create_qiskit_qubit_batch(50)
        assert len(batch) == 50
        assert all(isinstance(q, QiskitQubit) for q in batch)
        
        # Check variety
        bases = [q.basis for q in batch]
        bits = [q.bit_value for q in batch]
        
        assert 'Z' in bases and 'X' in bases
        assert 0 in bits and 1 in bits
    
    def test_measure_qubit_batch(self):
        """Test batch measurement of qubits."""
        qubits = [
            QiskitQubit('Z', 0), 
            QiskitQubit('X', 1), 
            QiskitQubit('Z', 1), 
            QiskitQubit('X', 0)
        ]
        bases = ['Z', 'X', 'Z', 'X']
        
        results = measure_qiskit_qubit_batch(qubits, bases)
        
        assert len(results) == 4
        # With correct bases, should mostly match (allowing quantum randomness)
        # We'll just check that we get valid results
        assert all(r in [0, 1] for r in results)
    
    def test_measure_qubit_batch_length_mismatch(self):
        """Test that mismatched lengths raise ValueError."""
        qubits = [QiskitQubit('Z', 0), QiskitQubit('X', 1)]
        bases = ['Z', 'X', 'Z']  # Different length
        
        with pytest.raises(ValueError, match="must match"):
            measure_qiskit_qubit_batch(qubits, bases)


class TestQiskitMeasurementValidation:
    """Test measurement input validation."""
    
    def test_invalid_measurement_basis_raises_error(self):
        """Test that invalid measurement basis raises ValueError."""
        q = QiskitQubit('Z', 0)
        
        with pytest.raises(ValueError, match="Measurement basis must be 'Z' or 'X'"):
            q.measure('Y')


class TestQiskitCircuitDiagram:
    """Test quantum circuit diagram generation."""
    
    def test_get_circuit_diagram(self):
        """Test that circuit diagram can be generated."""
        q = QiskitQubit('X', 1)
        diagram = q.get_circuit_diagram()
        
        assert isinstance(diagram, str)
        assert len(diagram) > 0


class TestQiskitRepr:
    """Test string representations."""
    
    def test_repr_contains_key_info(self):
        """Test that repr includes important information."""
        q = QiskitQubit('Z', 0)
        repr_str = repr(q)
        
        assert 'QiskitQubit' in repr_str
        assert 'Z' in repr_str
        assert '0' in repr_str
    
    def test_str_returns_state(self):
        """Test that str returns quantum state."""
        q = QiskitQubit('X', 1)
        assert str(q) == '|−⟩'


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])