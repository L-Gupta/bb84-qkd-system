"""
Utility functions for BB84 QKD system.
"""

from .key_utils import (
    bits_to_hex,
    hex_to_bits,
    bits_to_bytes,
    bytes_to_bits,
    bits_to_base64,
    base64_to_bits,
    bits_to_string,
    string_to_bits,
    calculate_hamming_distance,
    calculate_hamming_weight,
    xor_bits,
    format_key_display,
    validate_key_quality
)

from .statistics import (
    calculate_sifting_efficiency,
    calculate_qber,
    calculate_key_rate,
    calculate_mutual_information,
    calculate_secure_key_rate,
    is_secure,
    calculate_expected_qber_from_intercept,
    calculate_protocol_efficiency_score,
    generate_statistics_summary,
    compare_protocol_runs,
    analyze_qber_trend
)

__all__ = [
    # Key utilities
    'bits_to_hex',
    'hex_to_bits',
    'bits_to_bytes',
    'bytes_to_bits',
    'bits_to_base64',
    'base64_to_bits',
    'bits_to_string',
    'string_to_bits',
    'calculate_hamming_distance',
    'calculate_hamming_weight',
    'xor_bits',
    'format_key_display',
    'validate_key_quality',
    
    # Statistics
    'calculate_sifting_efficiency',
    'calculate_qber',
    'calculate_key_rate',
    'calculate_mutual_information',
    'calculate_secure_key_rate',
    'is_secure',
    'calculate_expected_qber_from_intercept',
    'calculate_protocol_efficiency_score',
    'generate_statistics_summary',
    'compare_protocol_runs',
    'analyze_qber_trend',
]