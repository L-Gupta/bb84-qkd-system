"""
Pydantic models for BB84 API requests and responses.

Defines data schemas for API endpoints with validation.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict
from datetime import datetime


class ProtocolRequest(BaseModel):
    """
    Request model for executing BB84 protocol.
    """
    key_length: int = Field(
        default=256,
        ge=64,
        le=1024,
        description="Desired final key length in bits (64-1024)"
    )
    
    with_eavesdropper: bool = Field(
        default=False,
        description="Whether to simulate an eavesdropper"
    )
    
    eavesdropper_intercept_rate: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Fraction of qubits Eve intercepts (0.0-1.0)"
    )
    
    transmission_multiplier: int = Field(
        default=4,
        ge=2,
        le=10,
        description="Multiplier for transmission overhead (2-10)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "key_length": 256,
                "with_eavesdropper": True,
                "eavesdropper_intercept_rate": 0.5,
                "transmission_multiplier": 4
            }
        }


class TransmissionStats(BaseModel):
    """Statistics about qubit transmission and sifting."""
    total_qubits: int = Field(description="Total qubits transmitted")
    sifted_bits: int = Field(description="Bits remaining after sifting")
    final_key_bits: int = Field(description="Final secure key length")
    sifting_efficiency: float = Field(description="Sifting efficiency percentage")
    key_generation_rate: float = Field(description="Key generation rate percentage")


class SecurityStats(BaseModel):
    """Security and error checking statistics."""
    qber: float = Field(description="Quantum Bit Error Rate (percentage)")
    errors_found: int = Field(description="Number of errors detected")
    bits_checked: int = Field(description="Number of bits checked")
    is_secure: bool = Field(description="Whether channel is secure")
    security_threshold: float = Field(description="QBER security threshold")
    eavesdropper_detected: bool = Field(description="Whether eavesdropping was detected")


class InformationTheoryStats(BaseModel):
    """Information theory metrics."""
    mutual_information: float = Field(description="Mutual information between Alice and Bob")
    secure_key_rate: float = Field(description="Secure key generation rate percentage")
    expected_final_bits: int = Field(description="Expected number of final key bits")


class PerformanceStats(BaseModel):
    """Overall performance metrics."""
    efficiency_score: float = Field(description="Overall efficiency score (0-100)")
    rating: str = Field(description="Efficiency rating (Excellent/Good/Fair/Poor/Critical)")


class EavesdropperStats(BaseModel):
    """Eavesdropper activity statistics."""
    total_intercepted: int = Field(description="Total qubits intercepted")
    intercept_rate: float = Field(description="Intercept rate")
    bases_used: Dict[str, int] = Field(description="Count of Z and X bases used")
    bits_measured: Dict[str, int] = Field(description="Count of 0s and 1s measured")
    interception_indices: List[int] = Field(description="Indices of intercepted qubits")


class KeyData(BaseModel):
    """Final key in multiple formats."""
    binary: str = Field(description="Key in binary format")
    hex: str = Field(description="Key in hexadecimal format")
    base64: str = Field(description="Key in base64 format")
    length: int = Field(description="Key length in bits")
    quality: Dict = Field(description="Key quality metrics")


class ProtocolResponse(BaseModel):
    """
    Complete response from BB84 protocol execution.
    """
    success: bool = Field(description="Whether protocol completed successfully")
    
    key: KeyData = Field(description="Final shared key")
    
    transmission: TransmissionStats = Field(description="Transmission statistics")
    
    security: SecurityStats = Field(description="Security statistics")
    
    information_theory: InformationTheoryStats = Field(description="Information theory metrics")
    
    performance: PerformanceStats = Field(description="Performance metrics")
    
    eavesdropper: Optional[EavesdropperStats] = Field(
        default=None,
        description="Eavesdropper statistics (if applicable)"
    )
    
    execution_time_ms: float = Field(description="Protocol execution time in milliseconds")
    
    timestamp: datetime = Field(description="Execution timestamp")
    
    protocol_version: str = Field(default="BB84-1.0", description="Protocol version")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "key": {
                    "binary": "10101010...",
                    "hex": "AAFF...",
                    "base64": "qv8=...",
                    "length": 256,
                    "quality": {
                        "balance": 0.52,
                        "is_balanced": True
                    }
                },
                "transmission": {
                    "total_qubits": 1024,
                    "sifted_bits": 512,
                    "final_key_bits": 256,
                    "sifting_efficiency": 50.0,
                    "key_generation_rate": 25.0
                },
                "security": {
                    "qber": 3.92,
                    "errors_found": 2,
                    "bits_checked": 51,
                    "is_secure": True,
                    "security_threshold": 11.0,
                    "eavesdropper_detected": False
                },
                "execution_time_ms": 125.5,
                "timestamp": "2024-01-01T00:00:00Z"
            }
        }


class BatchProtocolRequest(BaseModel):
    """Request for executing multiple protocol runs."""
    runs: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Number of protocol runs to execute"
    )
    
    config: ProtocolRequest = Field(description="Configuration for each run")
    
    class Config:
        json_schema_extra = {
            "example": {
                "runs": 10,
                "config": {
                    "key_length": 256,
                    "with_eavesdropper": True,
                    "eavesdropper_intercept_rate": 0.5
                }
            }
        }


class BatchProtocolResponse(BaseModel):
    """Response from batch protocol execution."""
    total_runs: int = Field(description="Total number of runs executed")
    
    successful_runs: int = Field(description="Number of successful runs")
    
    failed_runs: int = Field(description="Number of failed runs")
    
    results: List[ProtocolResponse] = Field(description="Individual run results")
    
    summary: Dict = Field(description="Aggregate statistics across all runs")
    
    execution_time_ms: float = Field(description="Total execution time")


class ProtocolInfoResponse(BaseModel):
    """Information about the BB84 protocol."""
    name: str = Field(default="BB84")
    description: str = Field(
        default="Bennett-Brassard 1984 Quantum Key Distribution Protocol"
    )
    version: str = Field(default="1.0")
    
    features: List[str] = Field(
        default=[
            "Quantum key distribution",
            "Eavesdropper detection",
            "Information-theoretic security",
            "Configurable parameters"
        ]
    )
    
    parameters: Dict = Field(
        default={
            "key_length": {
                "type": "integer",
                "min": 64,
                "max": 1024,
                "default": 256,
                "description": "Desired final key length in bits"
            },
            "with_eavesdropper": {
                "type": "boolean",
                "default": False,
                "description": "Enable eavesdropper simulation"
            },
            "eavesdropper_intercept_rate": {
                "type": "float",
                "min": 0.0,
                "max": 1.0,
                "default": 0.5,
                "description": "Fraction of qubits intercepted by Eve"
            }
        }
    )
    
    security_threshold: float = Field(
        default=11.0,
        description="QBER threshold for security (percentage)"
    )


class SecurityThresholdResponse(BaseModel):
    """Information about security thresholds."""
    qber_threshold: float = Field(
        default=11.0,
        description="Maximum acceptable QBER percentage"
    )
    
    explanation: str = Field(
        default="QBER above 11% indicates possible eavesdropping. Protocol should be aborted."
    )
    
    intercept_rate_examples: List[Dict] = Field(
        default=[
            {"intercept_rate": 0.0, "expected_qber": 0.0, "secure": True},
            {"intercept_rate": 0.2, "expected_qber": 5.0, "secure": True},
            {"intercept_rate": 0.4, "expected_qber": 10.0, "secure": True},
            {"intercept_rate": 0.5, "expected_qber": 12.5, "secure": False},
            {"intercept_rate": 1.0, "expected_qber": 25.0, "secure": False},
        ]
    )


class AnalyzeEavesdropperRequest(BaseModel):
    """Request for analyzing eavesdropper impact."""
    intercept_rates: List[float] = Field(
        default=[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
        description="List of intercept rates to analyze"
    )
    
    key_length: int = Field(default=256, ge=64, le=1024)
    
    @field_validator('intercept_rates')
    @classmethod
    def validate_rates(cls, v):
        """Validate that all rates are between 0 and 1."""
        if not all(0.0 <= rate <= 1.0 for rate in v):
            raise ValueError("All intercept rates must be between 0.0 and 1.0")
        return v


class AnalyzeEavesdropperResponse(BaseModel):
    """Response from eavesdropper analysis."""
    analysis: List[Dict] = Field(description="Analysis for each intercept rate")
    
    detection_threshold: float = Field(
        default=0.44,
        description="Intercept rate above which eavesdropping is detected"
    )
    
    summary: str = Field(
        description="Summary of analysis results"
    )


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(description="Error type")
    message: str = Field(description="Error message")
    details: Optional[str] = Field(default=None, description="Additional error details")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field(default="healthy")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: str = Field(default="1.0.0")