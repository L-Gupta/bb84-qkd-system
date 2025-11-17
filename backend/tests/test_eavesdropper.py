"""
Unit tests for the Eavesdropper class in BB84 protocol.

Tests interception behavior, QBER calculations, and attack strategies.
"""

import pytest
from core.qubit import Qubit, create_qubit_batch
from core.eavesdropper import Eavesdropper, calculate_expected_qber, simulate_interception


class TestEavesdropperCreation:
    """Test eavesdropper initialization."""
    
    def test_default_initialization(self):
        """Test eavesdropper with default parameters."""
        eve = Eavesdropper()
        assert eve.intercept_probability == 0.5
        assert eve.strategy == 'intercept-resend'
        assert eve.intercepted_count == 0
    
    def test_custom_intercept_probability(self):
        """Test eavesdropper with custom intercept rate."""
        eve = Eavesdropper(intercept_probability=0.7)
        assert eve.intercept_probability == 0.7
    
    def test_passive_strategy(self):
        """Test eavesdropper with passive strategy."""
        eve = Eavesdropper(strategy='passive')
        assert eve.strategy == 'passive'
    
    def test_invalid_intercept_probability_too_high(self):
        """Test that intercept probability > 1.0 raises error."""
        with pytest.raises(ValueError, match="must be between 0 and 1"):
            Eavesdropper(intercept_probability=1.5)
    
    def test_invalid_intercept_probability_negative(self):
        """Test that negative intercept probability raises error."""
        with pytest.raises(ValueError, match="must be between 0 and 1"):
            Eavesdropper(intercept_probability=-0.1)
    
    def test_invalid_strategy(self):
        """Test that invalid strategy raises error."""
        with pytest.raises(ValueError, match="Strategy must be"):
            Eavesdropper(strategy='invalid-strategy')


class TestNoInterception:
    """Test behavior when Eve doesn't intercept (intercept_rate = 0.0)."""
    
    def test_no_qubits_intercepted(self):
        """Test that 0% intercept rate means no qubits intercepted."""
        eve = Eavesdropper(intercept_probability=0.0)
        qubits = create_qubit_batch(100)
        result = eve.intercept(qubits)
        
        assert eve.intercepted_count == 0
        assert len(result) == 100
    
    def test_qubits_unchanged_with_no_interception(self):
        """Test that qubits pass through unchanged when not intercepted."""
        eve = Eavesdropper(intercept_probability=0.0)
        
        original_qubits = [
            Qubit('Z', 0),
            Qubit('X', 1),
            Qubit('Z', 1),
            Qubit('X', 0)
        ]
        
        result = eve.intercept(original_qubits)
        
        # Qubits should be the exact same objects (not modified)
        for i in range(len(original_qubits)):
            assert result[i] is original_qubits[i]
    
    def test_no_eve_data_recorded(self):
        """Test that Eve records no data when not intercepting."""
        eve = Eavesdropper(intercept_probability=0.0)
        qubits = create_qubit_batch(50)
        eve.intercept(qubits)
        
        assert len(eve.eve_bits) == 0
        assert len(eve.eve_bases) == 0
        assert len(eve.interception_indices) == 0


class TestFullInterception:
    """Test behavior when Eve intercepts all qubits (intercept_rate = 1.0)."""
    
    def test_all_qubits_intercepted(self):
        """Test that 100% intercept rate intercepts all qubits."""
        eve = Eavesdropper(intercept_probability=1.0)
        qubits = create_qubit_batch(50)
        result = eve.intercept(qubits)
        
        assert eve.intercepted_count == 50
        assert len(result) == 50
    
    def test_eve_records_all_measurements(self):
        """Test that Eve records data for all intercepted qubits."""
        eve = Eavesdropper(intercept_probability=1.0)
        qubits = create_qubit_batch(20)
        eve.intercept(qubits)
        
        assert len(eve.eve_bits) == 20
        assert len(eve.eve_bases) == 20
        assert len(eve.interception_indices) == 20
    
    def test_eve_uses_both_bases(self):
        """Test that Eve uses both Z and X bases randomly."""
        eve = Eavesdropper(intercept_probability=1.0)
        qubits = create_qubit_batch(100)
        eve.intercept(qubits)
        
        z_count = sum(1 for b in eve.eve_bases if b == 'Z')
        x_count = sum(1 for b in eve.eve_bases if b == 'X')
        
        # Should have both bases (statistically)
        assert z_count > 0
        assert x_count > 0
        assert z_count + x_count == 100
    
    def test_eve_measures_both_bit_values(self):
        """Test that Eve measures both 0 and 1 bits."""
        eve = Eavesdropper(intercept_probability=1.0)
        qubits = create_qubit_batch(100)
        eve.intercept(qubits)
        
        zeros = sum(1 for b in eve.eve_bits if b == 0)
        ones = sum(1 for b in eve.eve_bits if b == 1)
        
        # Should have both bit values (statistically)
        assert zeros > 0
        assert ones > 0
        assert zeros + ones == 100


class TestPartialInterception:
    """Test behavior with partial interception rates."""
    
    def test_partial_interception_rate(self):
        """Test that intercept rate approximately matches expected value."""
        eve = Eavesdropper(intercept_probability=0.5)
        qubits = create_qubit_batch(1000)
        eve.intercept(qubits)
        
        # Should intercept roughly 50% (with statistical tolerance)
        assert 400 <= eve.intercepted_count <= 600
    
    def test_different_intercept_rates(self):
        """Test various intercept rates work correctly."""
        rates = [0.1, 0.3, 0.7, 0.9]
        
        for rate in rates:
            eve = Eavesdropper(intercept_probability=rate)
            qubits = create_qubit_batch(1000)
            eve.intercept(qubits)
            
            expected = rate * 1000
            # Generous tolerance for randomness
            assert expected - 100 <= eve.intercepted_count <= expected + 100


class TestInterceptResendAttack:
    """Test the intercept-resend attack mechanics."""
    
    def test_intercepted_qubits_are_new_objects(self):
        """Test that Eve creates new qubits when intercepting."""
        eve = Eavesdropper(intercept_probability=1.0)
        
        original = Qubit('Z', 0)
        result = eve.intercept([original])
        
        # Should be a new qubit object, not the original
        assert result[0] is not original
    
    def test_eve_creates_qubits_in_her_basis(self):
        """Test that Eve's new qubits use her chosen basis."""
        eve = Eavesdropper(intercept_probability=1.0)
        qubits = create_qubit_batch(50)
        result = eve.intercept(qubits)
        
        # Each result qubit should match Eve's recorded basis
        for i, qubit in enumerate(result):
            assert qubit.basis == eve.eve_bases[i]
    
    def test_eve_qubit_matches_her_measurement(self):
        """Test that Eve's new qubits encode her measurement results."""
        eve = Eavesdropper(intercept_probability=1.0)
        qubits = create_qubit_batch(30)
        result = eve.intercept(qubits)
        
        # Each result qubit should encode Eve's measured bit
        for i, qubit in enumerate(result):
            assert qubit.bit_value == eve.eve_bits[i]


class TestPassiveStrategy:
    """Test passive observation strategy."""
    
    def test_passive_does_not_modify(self):
        """Test that passive strategy doesn't modify qubits."""
        eve = Eavesdropper(intercept_probability=1.0, strategy='passive')
        
        original_qubits = [
            Qubit('Z', 0),
            Qubit('X', 1),
            Qubit('Z', 1)
        ]
        
        result = eve.intercept(original_qubits)
        
        # Should be unchanged
        for i in range(len(original_qubits)):
            assert result[i] is original_qubits[i]
    
    def test_passive_no_interception_recorded(self):
        """Test that passive strategy records no interceptions."""
        eve = Eavesdropper(intercept_probability=1.0, strategy='passive')
        qubits = create_qubit_batch(50)
        eve.intercept(qubits)
        
        assert eve.intercepted_count == 0


class TestEavesdropperStatistics:
    """Test statistics tracking and reporting."""
    
    def test_get_statistics(self):
        """Test that statistics are correctly computed."""
        eve = Eavesdropper(intercept_probability=1.0)
        qubits = create_qubit_batch(100)
        eve.intercept(qubits)
        
        stats = eve.get_statistics()
        
        assert 'total_intercepted' in stats
        assert 'intercept_rate' in stats
        assert 'bases_used' in stats
        assert 'bits_measured' in stats
        assert stats['total_intercepted'] == 100
        assert stats['intercept_rate'] == 1.0
    
    def test_statistics_bases_count(self):
        """Test that basis counts are correct."""
        eve = Eavesdropper(intercept_probability=1.0)
        qubits = create_qubit_batch(50)
        eve.intercept(qubits)
        
        stats = eve.get_statistics()
        z_count = stats['bases_used']['Z']
        x_count = stats['bases_used']['X']
        
        assert z_count + x_count == 50
    
    def test_reset_clears_data(self):
        """Test that reset clears all tracking data."""
        eve = Eavesdropper(intercept_probability=1.0)
        qubits = create_qubit_batch(50)
        eve.intercept(qubits)
        
        # Verify data exists
        assert eve.intercepted_count > 0
        assert len(eve.eve_bits) > 0
        
        # Reset
        eve.reset()
        
        # Verify data cleared
        assert eve.intercepted_count == 0
        assert len(eve.eve_bits) == 0
        assert len(eve.eve_bases) == 0
        assert len(eve.interception_indices) == 0


class TestQBERCalculation:
    """Test QBER (Quantum Bit Error Rate) calculations."""
    
    def test_qber_no_interception(self):
        """Test that no interception yields 0% QBER."""
        qber = calculate_expected_qber(0.0)
        assert qber == 0.0
    
    def test_qber_full_interception(self):
        """Test that full interception yields 25% QBER."""
        qber = calculate_expected_qber(1.0)
        assert qber == 0.25
    
    def test_qber_half_interception(self):
        """Test that 50% interception yields 12.5% QBER."""
        qber = calculate_expected_qber(0.5)
        assert abs(qber - 0.125) < 1e-10
    
    def test_qber_linear_relationship(self):
        """Test that QBER scales linearly with intercept rate."""
        rates = [0.1, 0.2, 0.4, 0.6, 0.8]
        
        for rate in rates:
            qber = calculate_expected_qber(rate)
            expected = rate * 0.25
            assert abs(qber - expected) < 1e-10
    
    def test_qber_invalid_rate_high(self):
        """Test that invalid intercept rate raises error."""
        with pytest.raises(ValueError):
            calculate_expected_qber(1.5)
    
    def test_qber_invalid_rate_negative(self):
        """Test that negative intercept rate raises error."""
        with pytest.raises(ValueError):
            calculate_expected_qber(-0.1)
    
    def test_qber_security_threshold(self):
        """Test QBER relative to 11% security threshold."""
        # Below threshold (secure)
        qber_safe = calculate_expected_qber(0.3)
        assert qber_safe < 0.11  # 7.5% < 11%
        
        # Above threshold (detected)
        qber_detected = calculate_expected_qber(0.5)
        assert qber_detected > 0.11  # 12.5% > 11%


class TestSimulateInterception:
    """Test convenience function for simulating interception."""
    
    def test_simulate_interception_returns_tuple(self):
        """Test that simulate_interception returns qubits and eve."""
        qubits = create_qubit_batch(20)
        result, eve = simulate_interception(qubits, intercept_rate=0.5)
        
        assert isinstance(result, list)
        assert isinstance(eve, Eavesdropper)
    
    def test_simulate_interception_correct_length(self):
        """Test that returned qubits list has correct length."""
        qubits = create_qubit_batch(30)
        result, eve = simulate_interception(qubits, intercept_rate=0.7)
        
        assert len(result) == 30
    
    def test_simulate_interception_eve_configured(self):
        """Test that returned Eve has correct configuration."""
        qubits = create_qubit_batch(20)
        result, eve = simulate_interception(qubits, intercept_rate=0.3)
        
        assert eve.intercept_probability == 0.3


class TestEavesdropperRepr:
    """Test string representation of eavesdropper."""
    
    def test_repr_contains_key_info(self):
        """Test that repr includes important information."""
        eve = Eavesdropper(intercept_probability=0.7, strategy='intercept-resend')
        repr_str = repr(eve)
        
        assert 'intercept-resend' in repr_str
        assert '0.7' in repr_str
        assert 'Eavesdropper' in repr_str


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])