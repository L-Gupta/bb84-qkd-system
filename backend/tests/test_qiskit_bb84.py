"""
Unit tests for Qiskit-based BB84 protocol implementation.

Tests the complete quantum key distribution protocol using Qiskit.
"""

import pytest
from core.qiskit_bb84 import QiskitBB84Protocol, QiskitBB84Result


class TestQiskitBB84Creation:
    """Test Qiskit BB84 protocol initialization."""
    
    def test_default_initialization(self):
        """Test protocol with default parameters."""
        protocol = QiskitBB84Protocol()
        assert protocol.key_length == 256
        assert protocol.transmission_multiplier == 4
        assert protocol.qber_threshold == 0.11
    
    def test_custom_key_length(self):
        """Test protocol with custom key length."""
        protocol = QiskitBB84Protocol(key_length=128)
        assert protocol.key_length == 128
    
    def test_invalid_key_length_raises_error(self):
        """Test that invalid key length raises ValueError."""
        with pytest.raises(ValueError, match="Key length must be positive"):
            QiskitBB84Protocol(key_length=0)
    
    def test_invalid_multiplier_raises_error(self):
        """Test that invalid multiplier raises ValueError."""
        with pytest.raises(ValueError, match="must be >= 2"):
            QiskitBB84Protocol(transmission_multiplier=1)


class TestQiskitBB84WithoutEavesdropper:
    """Test protocol execution without eavesdropper."""
    
    def test_protocol_executes_successfully(self):
        """Test that protocol executes without errors."""
        protocol = QiskitBB84Protocol(key_length=64)
        result = protocol.execute(with_eavesdropper=False)
        
        assert result is not None
        assert isinstance(result, QiskitBB84Result)
    
    def test_protocol_generates_key(self):
        """Test that protocol generates a key."""
        protocol = QiskitBB84Protocol(key_length=64)
        result = protocol.execute(with_eavesdropper=False)
        
        assert len(result.final_key) > 0
        assert len(result.final_key) <= 64
    
    def test_qber_is_low_without_eve(self):
        """Test that QBER is low without eavesdropper."""
        protocol = QiskitBB84Protocol(key_length=64)
        result = protocol.execute(with_eavesdropper=False)
        
        # QBER should be low (< 15% to account for quantum randomness)
        assert result.error_rate < 0.15
    
    def test_sifting_efficiency(self):
        """Test that sifting keeps approximately 50% of bits."""
        protocol = QiskitBB84Protocol(key_length=64)
        result = protocol.execute(with_eavesdropper=False)
        
        efficiency = result.sifting_efficiency
        # Should be roughly 50% (allowing 30-70% range for quantum randomness)
        assert 30 <= efficiency <= 70
    
    def test_implementation_is_qiskit(self):
        """Test that implementation is marked as Qiskit."""
        protocol = QiskitBB84Protocol(key_length=64)
        result = protocol.execute(with_eavesdropper=False)
        
        assert result.implementation == "Qiskit"


class TestQiskitBB84WithEavesdropper:
    """Test protocol execution with eavesdropper."""
    
    def test_protocol_with_eve_executes(self):
        """Test that protocol executes with eavesdropper."""
        protocol = QiskitBB84Protocol(key_length=64)
        result = protocol.execute(
            with_eavesdropper=True,
            eavesdropper_intercept_rate=0.5
        )
        
        assert result is not None
        assert result.eavesdropper_present is True
    
    def test_eve_statistics_recorded(self):
        """Test that eavesdropper statistics are recorded."""
        protocol = QiskitBB84Protocol(key_length=64)
        result = protocol.execute(
            with_eavesdropper=True,
            eavesdropper_intercept_rate=0.5
        )
        
        assert result.eavesdropper_stats is not None
        assert 'total_intercepted' in result.eavesdropper_stats
    
    def test_high_intercept_rate_detected(self):
        """Test that high intercept rate creates detectable errors."""
        protocol = QiskitBB84Protocol(key_length=128)
        result = protocol.execute(
            with_eavesdropper=True,
            eavesdropper_intercept_rate=0.8
        )
        
        # High interception should cause high QBER (though quantum randomness applies)
        # We'll be lenient and just check it's elevated
        assert result.error_rate > 0.05  # Should have some errors


class TestQiskitBB84Results:
    """Test protocol result structure."""
    
    def test_result_has_alice_data(self):
        """Test that result contains Alice's data."""
        protocol = QiskitBB84Protocol(key_length=64)
        result = protocol.execute(with_eavesdropper=False)
        
        assert hasattr(result, 'alice_bits')
        assert hasattr(result, 'alice_bases')
        assert len(result.alice_bits) == len(result.alice_bases)
    
    def test_result_has_bob_data(self):
        """Test that result contains Bob's data."""
        protocol = QiskitBB84Protocol(key_length=64)
        result = protocol.execute(with_eavesdropper=False)
        
        assert hasattr(result, 'bob_bits')
        assert hasattr(result, 'bob_bases')
        assert len(result.bob_bits) == len(result.bob_bases)
    
    def test_result_has_sifted_data(self):
        """Test that result contains sifted data."""
        protocol = QiskitBB84Protocol(key_length=64)
        result = protocol.execute(with_eavesdropper=False)
        
        assert hasattr(result, 'sifted_alice_bits')
        assert hasattr(result, 'sifted_bob_bits')
        assert hasattr(result, 'matching_indices')
    
    def test_result_has_error_data(self):
        """Test that result contains error checking data."""
        protocol = QiskitBB84Protocol(key_length=64)
        result = protocol.execute(with_eavesdropper=False)
        
        assert hasattr(result, 'error_rate')
        assert hasattr(result, 'errors_found')
        assert hasattr(result, 'is_secure')
    
    def test_result_has_statistics(self):
        """Test that result contains statistics."""
        protocol = QiskitBB84Protocol(key_length=64)
        result = protocol.execute(with_eavesdropper=False)
        
        assert hasattr(result, 'total_transmitted')
        assert hasattr(result, 'total_sifted')
        assert hasattr(result, 'final_key_length')
        assert hasattr(result, 'sifting_efficiency')


class TestQiskitBB84KeyGeneration:
    """Test key generation specifics."""
    
    def test_key_length_matches_request(self):
        """Test that final key has requested length (or close to it)."""
        protocol = QiskitBB84Protocol(key_length=128)
        result = protocol.execute(with_eavesdropper=False)
        
        # Should be close to requested length (may be slightly less due to losses)
        assert result.final_key_length >= 64  # At least half
        assert result.final_key_length <= 128
    
    def test_key_contains_valid_bits(self):
        """Test that key contains only 0s and 1s."""
        protocol = QiskitBB84Protocol(key_length=64)
        result = protocol.execute(with_eavesdropper=False)
        
        assert all(bit in [0, 1] for bit in result.final_key)
    
    def test_multiple_runs_different_keys(self):
        """Test that multiple runs produce different keys."""
        protocol = QiskitBB84Protocol(key_length=64)
        
        result1 = protocol.execute(with_eavesdropper=False)
        result2 = protocol.execute(with_eavesdropper=False)
        
        # Keys should be different (very unlikely to be identical)
        assert result1.final_key != result2.final_key


class TestQiskitBB84Transmission:
    """Test transmission and sifting."""
    
    def test_transmission_multiplier_effect(self):
        """Test that transmission multiplier works."""
        protocol = QiskitBB84Protocol(key_length=64, transmission_multiplier=4)
        result = protocol.execute(with_eavesdropper=False)
        
        # Should transmit approximately 4x the key length
        expected = 64 * 4
        assert result.total_transmitted == expected
    
    def test_bases_are_random(self):
        """Test that Alice and Bob use random bases."""
        protocol = QiskitBB84Protocol(key_length=128)
        result = protocol.execute(with_eavesdropper=False)
        
        # Both should have Z and X bases
        assert 'Z' in result.alice_bases and 'X' in result.alice_bases
        assert 'Z' in result.bob_bases and 'X' in result.bob_bases


class TestQiskitBB84Security:
    """Test security threshold detection."""
    
    def test_low_qber_is_secure(self):
        """Test that low QBER is marked as secure."""
        protocol = QiskitBB84Protocol(key_length=64)
        result = protocol.execute(with_eavesdropper=False)
        
        if result.error_rate <= 0.11:
            assert result.is_secure is True
    
    def test_security_threshold_is_11_percent(self):
        """Test that security threshold is 11%."""
        protocol = QiskitBB84Protocol(key_length=64)
        assert protocol.qber_threshold == 0.11


class TestQiskitBB84Integration:
    """Integration tests for complete protocol."""
    
    def test_full_protocol_without_eve(self):
        """Test complete protocol execution without eavesdropper."""
        protocol = QiskitBB84Protocol(key_length=256)
        result = protocol.execute(with_eavesdropper=False)
        
        # Basic sanity checks
        assert result.total_transmitted > 0
        assert result.total_sifted > 0
        assert result.final_key_length > 0
        assert len(result.final_key) > 0
        assert result.eavesdropper_present is False
    
    def test_full_protocol_with_eve(self):
        """Test complete protocol execution with eavesdropper."""
        protocol = QiskitBB84Protocol(key_length=256)
        result = protocol.execute(
            with_eavesdropper=True,
            eavesdropper_intercept_rate=0.5
        )
        
        # Basic sanity checks
        assert result.total_transmitted > 0
        assert result.total_sifted > 0
        assert result.eavesdropper_present is True
        assert result.eavesdropper_stats is not None


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])