"""
FastAPI routes for BB84 QKD API.

Provides REST endpoints for executing the BB84 protocol,
analyzing results, and accessing protocol information.
"""

from fastapi import APIRouter, HTTPException, status
from datetime import datetime
import time
from typing import List

from core import QISKIT_AVAILABLE, QiskitBB84Protocol, BB84Protocol
from utils.key_utils import bits_to_hex, bits_to_base64, validate_key_quality
from utils.statistics import (
    generate_statistics_summary,
    calculate_expected_qber_from_intercept,
    compare_protocol_runs
)
from .models import (
    ProtocolRequest,
    ProtocolResponse,
    KeyData,
    TransmissionStats,
    SecurityStats,
    InformationTheoryStats,
    PerformanceStats,
    EavesdropperStats,
    BatchProtocolRequest,
    BatchProtocolResponse,
    ProtocolInfoResponse,
    SecurityThresholdResponse,
    AnalyzeEavesdropperRequest,
    AnalyzeEavesdropperResponse,
    ErrorResponse
)

# Create router
router = APIRouter(prefix="/api", tags=["BB84 Protocol"])


@router.post(
    "/protocol/execute",
    response_model=ProtocolResponse,
    status_code=status.HTTP_200_OK,
    summary="Execute BB84 Protocol",
    description="Execute BB84 using available implementation (Qiskit or Python)"
)
async def execute_protocol(request: ProtocolRequest):
    """
    Execute BB84 protocol using available implementation.
    
    Prefers Qiskit if available, falls back to pure Python implementation.
    
    Returns complete protocol results including:
    - Final shared key
    - Transmission statistics
    - Security metrics (QBER)
    - Performance analysis
    """
    
    try:
        start_time = time.time()
        
        # Use Qiskit if available, otherwise use pure Python implementation
        if QISKIT_AVAILABLE:
            protocol = QiskitBB84Protocol(
                key_length=request.key_length,
                transmission_multiplier=request.transmission_multiplier
            )
            protocol_version = "BB84-Qiskit"
        else:
            protocol = BB84Protocol(
                key_length=request.key_length,
                transmission_multiplier=request.transmission_multiplier
            )
            protocol_version = "BB84-Python"
        
        result = protocol.execute(
            with_eavesdropper=request.with_eavesdropper,
            eavesdropper_intercept_rate=request.eavesdropper_intercept_rate
        )
        
        # Generate comprehensive statistics
        stats = generate_statistics_summary(
            transmitted=result.total_transmitted,
            sifted=result.total_sifted,
            final_key_length=result.final_key_length,
            errors=result.errors_found,
            checked=result.sample_size,
            eavesdropper_present=request.with_eavesdropper
        )
        
        # Convert key to multiple formats
        key_hex = bits_to_hex(result.final_key)
        key_base64 = bits_to_base64(result.final_key)
        key_binary = ''.join(str(b) for b in result.final_key)
        key_quality = validate_key_quality(result.final_key)
        
        # Build response
        response = ProtocolResponse(
            success=True,
            key=KeyData(
                binary=key_binary,
                hex=key_hex,
                base64=key_base64,
                length=len(result.final_key),
                quality=key_quality
            ),
            transmission=TransmissionStats(**stats["transmission"]),
            security=SecurityStats(**stats["security"]),
            information_theory=InformationTheoryStats(**stats["information_theory"]),
            performance=PerformanceStats(**stats["performance"]),
            eavesdropper=EavesdropperStats(**result.eavesdropper_stats) if result.eavesdropper_stats else None,
            execution_time_ms=(time.time() - start_time) * 1000,
            timestamp=datetime.utcnow(),
            protocol_version=protocol_version
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Protocol execution failed: {str(e)}"
        )


@router.post(
    "/protocol/batch",
    response_model=BatchProtocolResponse,
    status_code=status.HTTP_200_OK,
    summary="Execute Multiple Protocol Runs",
    description="Execute BB84 protocol multiple times and aggregate results"
)
async def execute_batch_protocol(request: BatchProtocolRequest):
    """
    Execute BB84 protocol multiple times with same configuration.
    
    Useful for:
    - Statistical analysis
    - Testing protocol stability
    - Comparing different scenarios
    """
    try:
        start_time = time.time()
        
        results = []
        successful = 0
        failed = 0
        
        # Execute multiple runs
        for _ in range(request.runs):
            try:
                run_result = await execute_protocol(request.config)
                results.append(run_result)
                successful += 1
            except Exception:
                failed += 1
        
        # Generate aggregate statistics
        if results:
            stats_list = [
                {
                    "transmission": r.transmission.model_dump(),
                    "security": r.security.model_dump(),
                    "performance": r.performance.model_dump()
                }
                for r in results
            ]
            summary = compare_protocol_runs(stats_list)
        else:
            summary = {}
        
        total_time = (time.time() - start_time) * 1000
        
        return BatchProtocolResponse(
            total_runs=request.runs,
            successful_runs=successful,
            failed_runs=failed,
            results=results,
            summary=summary,
            execution_time_ms=total_time
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Batch execution failed: {str(e)}"
        )


@router.get(
    "/protocol/info",
    response_model=ProtocolInfoResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Protocol Information",
    description="Get information about the BB84 protocol"
)
async def get_protocol_info():
    """
    Get information about BB84 protocol.
    
    Returns:
    - Protocol name and description
    - Available features
    - Configurable parameters
    - Security threshold
    """
    return ProtocolInfoResponse()


@router.get(
    "/security/threshold",
    response_model=SecurityThresholdResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Security Threshold Information",
    description="Get information about QBER security threshold"
)
async def get_security_threshold():
    """
    Get security threshold information.
    
    Returns:
    - QBER threshold (11%)
    - Explanation
    - Example intercept rates and expected QBERs
    """
    return SecurityThresholdResponse()


@router.post(
    "/analyze/eavesdropper",
    response_model=AnalyzeEavesdropperResponse,
    status_code=status.HTTP_200_OK,
    summary="Analyze Eavesdropper Impact",
    description="Analyze how different eavesdropper intercept rates affect QBER"
)
async def analyze_eavesdropper(request: AnalyzeEavesdropperRequest):
    """
    Analyze eavesdropper impact across different intercept rates.
    
    Returns:
    - Expected QBER for each intercept rate
    - Security status
    - Detection threshold
    """
    try:
        analysis = []
        
        for rate in request.intercept_rates:
            expected_qber = calculate_expected_qber_from_intercept(rate)
            is_secure = expected_qber <= 0.11
            
            analysis.append({
                "intercept_rate": round(rate * 100, 1),
                "expected_qber": round(expected_qber * 100, 2),
                "is_secure": is_secure,
                "status": "Secure" if is_secure else "Detected"
            })
        
        # Find detection threshold (where QBER exceeds 11%)
        # Theoretical: 0.11 = rate * 0.25 => rate = 0.44
        detection_threshold = 0.44
        
        summary = (
            f"Analyzed {len(request.intercept_rates)} intercept rates. "
            f"Eavesdropping is detectable when intercept rate exceeds {detection_threshold*100:.0f}% "
            f"(corresponding to QBER > 11%)."
        )
        
        return AnalyzeEavesdropperResponse(
            analysis=analysis,
            detection_threshold=detection_threshold,
            summary=summary
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Health Check",
    description="Check if API is running"
)
async def health_check():
    """Simple health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "version": "1.0.0",
        "qiskit_available": QISKIT_AVAILABLE
    }