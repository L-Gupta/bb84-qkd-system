"""
Statistical analysis utilities for BB84 protocol.

Provides functions for calculating protocol efficiency metrics,
QBER analysis, and key rate calculations.
"""

import math
from typing import List, Dict, Optional


def calculate_sifting_efficiency(transmitted: int, sifted: int) -> float:
    """
    Calculate basis sifting efficiency.
    
    Theoretical efficiency is ~50% (when bases match randomly).
    
    Args:
        transmitted: Number of qubits transmitted
        sifted: Number of bits after sifting
        
    Returns:
        Efficiency as a fraction (0.0 to 1.0)
    """
    if transmitted == 0:
        return 0.0
    
    return sifted / transmitted


def calculate_qber(errors: int, total_checked: int) -> float:
    """
    Calculate Quantum Bit Error Rate (QBER).
    
    QBER is the fraction of bits that differ between Alice and Bob
    after basis sifting.
    
    Args:
        errors: Number of mismatched bits
        total_checked: Total number of bits compared
        
    Returns:
        QBER as a fraction (0.0 to 1.0)
    """
    if total_checked == 0:
        return 0.0
    
    return errors / total_checked


def calculate_key_rate(final_key_length: int, total_transmitted: int) -> float:
    """
    Calculate overall key generation rate.
    
    This is the fraction of transmitted qubits that become final key bits.
    
    Args:
        final_key_length: Length of final secure key
        total_transmitted: Number of qubits initially transmitted
        
    Returns:
        Key rate as a fraction (0.0 to 1.0)
    """
    if total_transmitted == 0:
        return 0.0
    
    return final_key_length / total_transmitted


def calculate_mutual_information(qber: float) -> float:
    """
    Calculate mutual information between Alice and Bob.
    
    Uses binary entropy function: I(A:B) = 1 - H(QBER)
    where H(p) = -p*log2(p) - (1-p)*log2(1-p)
    
    Args:
        qber: Quantum Bit Error Rate (0.0 to 1.0)
        
    Returns:
        Mutual information in bits (0.0 to 1.0)
    """
    if qber == 0.0 or qber == 1.0:
        return 1.0
    
    # Binary entropy
    h = -qber * math.log2(qber) - (1 - qber) * math.log2(1 - qber)
    
    return 1.0 - h


def calculate_secure_key_rate(qber: float, sifting_efficiency: float = 0.5) -> float:
    """
    Estimate secure key generation rate accounting for:
    - Sifting losses (~50%)
    - Error correction overhead
    - Privacy amplification
    
    Uses simplified formula: r ≈ efficiency * [1 - H(QBER)]
    
    Args:
        qber: Quantum Bit Error Rate
        sifting_efficiency: Fraction of bits kept after sifting
        
    Returns:
        Estimated secure key rate (bits per transmitted qubit)
    """
    if qber >= 0.11:  # Above security threshold
        return 0.0  # No secure key can be generated
    
    mutual_info = calculate_mutual_information(qber)
    
    return sifting_efficiency * mutual_info


def is_secure(qber: float, threshold: float = 0.11) -> bool:
    """
    Determine if protocol execution is secure based on QBER.
    
    Standard BB84 security threshold is 11% QBER.
    
    Args:
        qber: Quantum Bit Error Rate
        threshold: Security threshold (default 11%)
        
    Returns:
        True if QBER is below threshold (secure)
    """
    return qber <= threshold


def calculate_expected_qber_from_intercept(intercept_rate: float) -> float:
    """
    Calculate theoretical QBER for given eavesdropper intercept rate.
    
    For intercept-resend attack:
    - Eve chooses wrong basis 50% of time
    - Wrong basis causes 50% error when Bob measures
    - Combined: QBER = intercept_rate × 0.25
    
    Args:
        intercept_rate: Fraction of qubits intercepted (0.0 to 1.0)
        
    Returns:
        Expected QBER
    """
    return intercept_rate * 0.25


def calculate_protocol_efficiency_score(
    sifting_eff: float,
    qber: float,
    key_rate: float
) -> float:
    """
    Calculate overall protocol efficiency score (0-100).
    
    Weighted combination of:
    - Sifting efficiency (40%)
    - Low QBER (30%)
    - Key generation rate (30%)
    
    Args:
        sifting_eff: Sifting efficiency (0-1)
        qber: Quantum Bit Error Rate (0-1)
        key_rate: Key generation rate (0-1)
        
    Returns:
        Efficiency score (0-100)
    """
    # Normalize and weight components
    sift_score = sifting_eff * 40
    qber_score = (1 - min(qber / 0.11, 1.0)) * 30  # Lower QBER is better
    rate_score = key_rate * 30
    
    return sift_score + qber_score + rate_score


def generate_statistics_summary(
    transmitted: int,
    sifted: int,
    final_key_length: int,
    errors: int,
    checked: int,
    eavesdropper_present: bool = False
) -> Dict:
    """
    Generate comprehensive statistics summary for protocol execution.
    
    Args:
        transmitted: Qubits transmitted
        sifted: Bits after sifting
        final_key_length: Final key length
        errors: Errors found in check
        checked: Bits checked
        eavesdropper_present: Whether eavesdropper was present
        
    Returns:
        Dictionary with all statistics
    """
    sifting_eff = calculate_sifting_efficiency(transmitted, sifted)
    qber = calculate_qber(errors, checked)
    key_rate = calculate_key_rate(final_key_length, transmitted)
    mutual_info = calculate_mutual_information(qber)
    secure_rate = calculate_secure_key_rate(qber, sifting_eff)
    secure = is_secure(qber)
    efficiency_score = calculate_protocol_efficiency_score(sifting_eff, qber, key_rate)
    
    return {
        "transmission": {
            "total_qubits": transmitted,
            "sifted_bits": sifted,
            "final_key_bits": final_key_length,
            "sifting_efficiency": round(sifting_eff * 100, 2),
            "key_generation_rate": round(key_rate * 100, 2)
        },
        "security": {
            "qber": round(qber * 100, 4),
            "errors_found": errors,
            "bits_checked": checked,
            "is_secure": secure,
            "security_threshold": 11.0,
            "eavesdropper_detected": eavesdropper_present and not secure
        },
        "information_theory": {
            "mutual_information": round(mutual_info, 4),
            "secure_key_rate": round(secure_rate * 100, 2),
            "expected_final_bits": int(transmitted * secure_rate)
        },
        "performance": {
            "efficiency_score": round(efficiency_score, 2),
            "rating": _get_efficiency_rating(efficiency_score)
        }
    }


def _get_efficiency_rating(score: float) -> str:
    """
    Convert efficiency score to rating.
    
    Args:
        score: Efficiency score (0-100)
        
    Returns:
        Rating string
    """
    if score >= 80:
        return "Excellent"
    elif score >= 60:
        return "Good"
    elif score >= 40:
        return "Fair"
    elif score >= 20:
        return "Poor"
    else:
        return "Critical"


def compare_protocol_runs(runs: List[Dict]) -> Dict:
    """
    Compare statistics across multiple protocol runs.
    
    Args:
        runs: List of statistics dictionaries from multiple runs
        
    Returns:
        Comparison summary with averages and trends
    """
    if not runs:
        return {}
    
    n = len(runs)
    
    avg_sifting = sum(r["transmission"]["sifting_efficiency"] for r in runs) / n
    avg_qber = sum(r["security"]["qber"] for r in runs) / n
    avg_key_rate = sum(r["transmission"]["key_generation_rate"] for r in runs) / n
    secure_count = sum(1 for r in runs if r["security"]["is_secure"])
    
    return {
        "total_runs": n,
        "averages": {
            "sifting_efficiency": round(avg_sifting, 2),
            "qber": round(avg_qber, 4),
            "key_generation_rate": round(avg_key_rate, 2)
        },
        "security_summary": {
            "secure_runs": secure_count,
            "insecure_runs": n - secure_count,
            "success_rate": round(secure_count / n * 100, 2)
        },
        "best_run": max(runs, key=lambda r: r["performance"]["efficiency_score"]),
        "worst_run": min(runs, key=lambda r: r["performance"]["efficiency_score"])
    }


def analyze_qber_trend(qber_values: List[float], labels: Optional[List[str]] = None) -> Dict:
    """
    Analyze QBER trend across multiple measurements.
    
    Args:
        qber_values: List of QBER values
        labels: Optional labels for each measurement
        
    Returns:
        Trend analysis
    """
    if not qber_values:
        return {}
    
    n = len(qber_values)
    avg_qber = sum(qber_values) / n
    min_qber = min(qber_values)
    max_qber = max(qber_values)
    std_dev = math.sqrt(sum((q - avg_qber) ** 2 for q in qber_values) / n)
    
    # Count secure vs insecure
    secure_count = sum(1 for q in qber_values if q <= 0.11)
    
    return {
        "count": n,
        "average_qber": round(avg_qber * 100, 4),
        "min_qber": round(min_qber * 100, 4),
        "max_qber": round(max_qber * 100, 4),
        "std_deviation": round(std_dev * 100, 4),
        "secure_count": secure_count,
        "insecure_count": n - secure_count,
        "stability": "Stable" if std_dev < 0.02 else "Unstable"
    }


# Demo
if __name__ == "__main__":
    print("=" * 60)
    print("Statistics Utilities Demo")
    print("=" * 60)
    
    # Example protocol run
    print("\nExample Protocol Run:")
    print("-" * 60)
    
    stats = generate_statistics_summary(
        transmitted=1024,
        sifted=512,
        final_key_length=256,
        errors=2,
        checked=51,
        eavesdropper_present=False
    )
    
    print("\nTransmission:")
    for key, value in stats["transmission"].items():
        print(f"  {key}: {value}")
    
    print("\nSecurity:")
    for key, value in stats["security"].items():
        print(f"  {key}: {value}")
    
    print("\nInformation Theory:")
    for key, value in stats["information_theory"].items():
        print(f"  {key}: {value}")
    
    print("\nPerformance:")
    for key, value in stats["performance"].items():
        print(f"  {key}: {value}")
    
    # QBER analysis
    print("\n" + "=" * 60)
    print("QBER Analysis for Different Intercept Rates")
    print("=" * 60)
    
    print(f"{'Intercept %':<12} {'Expected QBER':<15} {'Secure?':<10} {'Key Rate'}")
    print("-" * 60)
    
    for rate in [0.0, 0.2, 0.4, 0.5, 0.6, 0.8, 1.0]:
        qber = calculate_expected_qber_from_intercept(rate)
        secure = "✓" if is_secure(qber) else "✗"
        key_rate = calculate_secure_key_rate(qber)
        print(f"{rate*100:<12.0f} {qber*100:<15.2f} {secure:<10} {key_rate*100:.2f}%")
    
    print("\n" + "=" * 60)