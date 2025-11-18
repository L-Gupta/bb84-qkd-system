"""
Key utility functions for BB84 protocol.

Provides conversion functions between different key representations
(binary, hexadecimal, base64) and key quality metrics.
"""

import base64
from typing import List


def bits_to_hex(bits: List[int]) -> str:
    """
    Convert a list of bits to hexadecimal string.
    
    Args:
        bits: List of 0s and 1s
        
    Returns:
        Hexadecimal string (uppercase)
        
    Example:
        >>> bits_to_hex([1, 0, 1, 0, 1, 1, 0, 1])
        'AD'
    """
    if not bits:
        return ""
    
    hex_string = ""
    
    # Process in chunks of 4 bits
    for i in range(0, len(bits), 4):
        chunk = bits[i:i+4]
        
        # Pad last chunk if necessary
        while len(chunk) < 4:
            chunk.append(0)
        
        # Convert to hex digit (0-15)
        value = chunk[0] * 8 + chunk[1] * 4 + chunk[2] * 2 + chunk[3]
        hex_string += format(value, 'X')
    
    return hex_string


def hex_to_bits(hex_string: str) -> List[int]:
    """
    Convert hexadecimal string to list of bits.
    
    Args:
        hex_string: Hexadecimal string
        
    Returns:
        List of 0s and 1s
        
    Example:
        >>> hex_to_bits('AD')
        [1, 0, 1, 0, 1, 1, 0, 1]
    """
    bits = []
    
    for hex_char in hex_string:
        # Convert hex character to integer
        value = int(hex_char, 16)
        
        # Convert to 4 bits
        for i in range(3, -1, -1):
            bits.append((value >> i) & 1)
    
    return bits


def bits_to_bytes(bits: List[int]) -> bytes:
    """
    Convert list of bits to bytes.
    
    Args:
        bits: List of 0s and 1s
        
    Returns:
        Bytes object
    """
    if not bits:
        return b""
    
    # Pad to multiple of 8
    padded_bits = bits.copy()
    while len(padded_bits) % 8 != 0:
        padded_bits.append(0)
    
    byte_array = bytearray()
    
    # Process in chunks of 8 bits
    for i in range(0, len(padded_bits), 8):
        byte_value = 0
        for j in range(8):
            byte_value = (byte_value << 1) | padded_bits[i + j]
        byte_array.append(byte_value)
    
    return bytes(byte_array)


def bytes_to_bits(data: bytes) -> List[int]:
    """
    Convert bytes to list of bits.
    
    Args:
        data: Bytes object
        
    Returns:
        List of 0s and 1s
    """
    bits = []
    
    for byte in data:
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)
    
    return bits


def bits_to_base64(bits: List[int]) -> str:
    """
    Convert list of bits to base64 encoded string.
    
    Args:
        bits: List of 0s and 1s
        
    Returns:
        Base64 encoded string
    """
    byte_data = bits_to_bytes(bits)
    return base64.b64encode(byte_data).decode('utf-8')


def base64_to_bits(b64_string: str) -> List[int]:
    """
    Convert base64 string to list of bits.
    
    Args:
        b64_string: Base64 encoded string
        
    Returns:
        List of 0s and 1s
    """
    byte_data = base64.b64decode(b64_string)
    return bytes_to_bits(byte_data)


def bits_to_string(bits: List[int]) -> str:
    """
    Convert list of bits to binary string.
    
    Args:
        bits: List of 0s and 1s
        
    Returns:
        Binary string (e.g., "10110101")
        
    Example:
        >>> bits_to_string([1, 0, 1, 1])
        '1011'
    """
    return ''.join(str(bit) for bit in bits)


def string_to_bits(bit_string: str) -> List[int]:
    """
    Convert binary string to list of bits.
    
    Args:
        bit_string: Binary string (e.g., "10110101")
        
    Returns:
        List of 0s and 1s
        
    Raises:
        ValueError: If string contains non-binary characters
    """
    if not all(c in '01' for c in bit_string):
        raise ValueError("String must contain only 0s and 1s")
    
    return [int(c) for c in bit_string]


def calculate_hamming_distance(bits1: List[int], bits2: List[int]) -> int:
    """
    Calculate Hamming distance between two bit sequences.
    
    The Hamming distance is the number of positions where bits differ.
    
    Args:
        bits1: First bit sequence
        bits2: Second bit sequence
        
    Returns:
        Number of differing bits
        
    Raises:
        ValueError: If sequences have different lengths
    """
    if len(bits1) != len(bits2):
        raise ValueError(f"Bit sequences must have same length: {len(bits1)} vs {len(bits2)}")
    
    return sum(b1 != b2 for b1, b2 in zip(bits1, bits2))


def calculate_hamming_weight(bits: List[int]) -> int:
    """
    Calculate Hamming weight (number of 1s) in bit sequence.
    
    Args:
        bits: Bit sequence
        
    Returns:
        Number of 1s in the sequence
    """
    return sum(bits)


def xor_bits(bits1: List[int], bits2: List[int]) -> List[int]:
    """
    XOR two bit sequences.
    
    Args:
        bits1: First bit sequence
        bits2: Second bit sequence
        
    Returns:
        XOR result
        
    Raises:
        ValueError: If sequences have different lengths
    """
    if len(bits1) != len(bits2):
        raise ValueError(f"Bit sequences must have same length: {len(bits1)} vs {len(bits2)}")
    
    return [b1 ^ b2 for b1, b2 in zip(bits1, bits2)]


def format_key_display(bits: List[int], format_type: str = "hex", group_size: int = 4) -> str:
    """
    Format key for display with grouping.
    
    Args:
        bits: Bit sequence
        format_type: 'binary', 'hex', or 'base64'
        group_size: Number of characters per group (for readability)
        
    Returns:
        Formatted key string with spaces for readability
        
    Example:
        >>> format_key_display([1,0,1,0,1,1,0,1], 'hex', 2)
        'AD'
        >>> format_key_display([1,0,1,0,1,1,0,1], 'binary', 4)
        '1010 1101'
    """
    if format_type == "hex":
        raw = bits_to_hex(bits)
    elif format_type == "base64":
        raw = bits_to_base64(bits)
    elif format_type == "binary":
        raw = bits_to_string(bits)
    else:
        raise ValueError(f"Invalid format_type: {format_type}")
    
    # Group characters for readability
    if group_size > 0:
        grouped = ' '.join(raw[i:i+group_size] for i in range(0, len(raw), group_size))
        return grouped
    
    return raw


def validate_key_quality(bits: List[int]) -> dict:
    """
    Analyze key quality metrics.
    
    A good cryptographic key should have approximately equal numbers of 0s and 1s.
    
    Args:
        bits: Key bit sequence
        
    Returns:
        Dictionary with quality metrics:
            - length: Key length in bits
            - ones: Number of 1s
            - zeros: Number of 0s
            - balance: Ratio of 1s (should be ~0.5 for good key)
            - is_balanced: True if ratio is between 0.4 and 0.6
    """
    length = len(bits)
    ones = calculate_hamming_weight(bits)
    zeros = length - ones
    
    balance = ones / length if length > 0 else 0.0
    is_balanced = 0.4 <= balance <= 0.6
    
    return {
        "length": length,
        "ones": ones,
        "zeros": zeros,
        "balance": balance,
        "is_balanced": is_balanced
    }


# Demo
if __name__ == "__main__":
    print("=" * 60)
    print("Key Utilities Demo")
    print("=" * 60)
    
    # Sample key
    sample_bits = [1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1]
    
    print("\nOriginal bits:")
    print(f"  {sample_bits}")
    
    print("\nConversions:")
    print(f"  Binary: {bits_to_string(sample_bits)}")
    print(f"  Hex: {bits_to_hex(sample_bits)}")
    print(f"  Base64: {bits_to_base64(sample_bits)}")
    
    print("\nFormatted displays:")
    print(f"  Hex (grouped): {format_key_display(sample_bits, 'hex', 2)}")
    print(f"  Binary (grouped): {format_key_display(sample_bits, 'binary', 4)}")
    
    print("\nKey quality:")
    quality = validate_key_quality(sample_bits)
    print(f"  Length: {quality['length']} bits")
    print(f"  Ones: {quality['ones']}, Zeros: {quality['zeros']}")
    print(f"  Balance: {quality['balance']:.2%}")
    print(f"  Is balanced: {'✓' if quality['is_balanced'] else '✗'}")
    
    print("\nHamming distance:")
    bits2 = [1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1]
    distance = calculate_hamming_distance(sample_bits, bits2)
    print(f"  Distance between keys: {distance} bits")
    
    print("\n" + "=" * 60)