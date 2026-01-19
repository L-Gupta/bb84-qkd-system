# BB84 API Documentation

Complete REST API documentation for the BB84 Quantum Key Distribution backend.

## Base URL

```
http://localhost:8000/api
```

## Authentication

Currently, no authentication is required. All endpoints are publicly accessible.

---

## Endpoints

### Health Check

**GET** `/health`

Check if the API server is running and Qiskit availability.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-01-19T12:00:00.000Z",
  "version": "1.0.0",
  "qiskit_available": true
}
```

**Status Codes:**
- `200` - Server is healthy

---

### Execute Protocol

**POST** `/protocol/execute`

Execute the BB84 protocol with the given configuration.

**Request Body:**
```json
{
  "key_length": 256,
  "with_eavesdropper": false,
  "eavesdropper_intercept_rate": 0.5,
  "transmission_multiplier": 4
}
```

**Parameters:**
- `key_length` (integer, 64-1024): Desired final key length in bits
- `with_eavesdropper` (boolean): Whether to simulate an eavesdropper
- `eavesdropper_intercept_rate` (float, 0.0-1.0): Fraction of qubits Eve intercepts
- `transmission_multiplier` (integer, 2-10): Multiplier for transmission overhead

**Response:**
```json
{
  "success": true,
  "key": {
    "binary": "1010101011001100...",
    "hex": "AACC...",
    "base64": "qssM...",
    "length": 256,
    "quality": {
      "balance": 0.5,
      "is_balanced": true
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
    "qber": 2.1,
    "errors_found": 10,
    "bits_checked": 512,
    "is_secure": true,
    "security_threshold": 11.0,
    "eavesdropper_detected": false
  },
  "information_theory": {
    "mutual_information": 0.982,
    "secure_key_rate": 24.5,
    "expected_final_bits": 260
  },
  "performance": {
    "efficiency_score": 87.3,
    "rating": "Excellent"
  },
  "eavesdropper": null,
  "execution_time_ms": 12.4,
  "timestamp": "2026-01-19T12:00:00.000Z",
  "protocol_version": "BB84-Python"
}
```

**Status Codes:**
- `200` - Protocol executed successfully
- `422` - Validation error (invalid parameters)
- `500` - Protocol execution failed

**Error Response:**
```json
{
  "detail": "Protocol execution failed: [error message]"
}
```

---

### Batch Protocol Execution

**POST** `/protocol/batch`

Execute the BB84 protocol multiple times with the same configuration.

**Request Body:**
```json
{
  "runs": 5,
  "config": {
    "key_length": 256,
    "with_eavesdropper": false,
    "eavesdropper_intercept_rate": 0.5,
    "transmission_multiplier": 4
  }
}
```

**Parameters:**
- `runs` (integer, 1-100): Number of protocol runs
- `config` (object): Protocol configuration (same as `/protocol/execute`)

**Response:**
```json
{
  "success": true,
  "total_runs": 5,
  "successful": 5,
  "failed": 0,
  "results": [
    { /* Protocol result 1 */ },
    { /* Protocol result 2 */ }
  ],
  "statistics": {
    "avg_qber": 1.8,
    "avg_efficiency": 85.2,
    "all_secure": true,
    "execution_time_ms": 78.5
  }
}
```

**Status Codes:**
- `200` - Batch execution completed
- `422` - Validation error
- `500` - Batch execution failed

---

### Protocol Information

**GET** `/protocol/info`

Get information about the BB84 protocol implementation.

**Response:**
```json
{
  "protocol_name": "BB84",
  "authors": "Bennett & Brassard (1984)",
  "steps": 6,
  "description": "Quantum Key Distribution protocol...",
  "features": [
    "Quantum bit distribution",
    "Basis sifting",
    "Error detection",
    "Eavesdropper simulation"
  ]
}
```

**Status Codes:**
- `200` - Protocol information retrieved

---

### Security Threshold

**GET** `/security/threshold`

Get security threshold information.

**Response:**
```json
{
  "qber_threshold": 11.0,
  "description": "QBER above 11% indicates possible eavesdropping",
  "explanation": "With a 50% intercept rate, Eve introduces ~12.5% errors"
}
```

**Status Codes:**
- `200` - Threshold information retrieved

---

### Analyze Eavesdropper

**POST** `/analyze/eavesdropper`

Analyze expected QBER for different eavesdropper intercept rates.

**Request Body:**
```json
{
  "intercept_rates": [0.0, 0.2, 0.5, 0.8, 1.0],
  "key_length": 256
}
```

**Parameters:**
- `intercept_rates` (array of floats): List of intercept rates to analyze
- `key_length` (integer): Desired key length

**Response:**
```json
{
  "analysis": [
    {
      "intercept_rate": 0.0,
      "expected_qber": 0.0,
      "detectable": false
    },
    {
      "intercept_rate": 0.5,
      "expected_qber": 12.5,
      "detectable": true
    }
  ]
}
```

**Status Codes:**
- `200` - Analysis completed
- `422` - Validation error
- `500` - Analysis failed

---

## Error Handling

All errors return a JSON response with a `detail` field:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common Errors

| Status | Message | Cause |
|--------|---------|-------|
| 422 | Validation error | Invalid request parameters |
| 500 | Protocol execution failed | Error in BB84 execution |
| 501 | Qiskit not available | Qiskit library not installed |

---

## Example Usage

### Using curl

```bash
# Health check
curl http://localhost:8000/api/health

# Execute protocol
curl -X POST http://localhost:8000/api/protocol/execute \
  -H "Content-Type: application/json" \
  -d '{
    "key_length": 256,
    "with_eavesdropper": false,
    "eavesdropper_intercept_rate": 0.5,
    "transmission_multiplier": 4
  }'
```

### Using JavaScript/Fetch

```javascript
const config = {
  key_length: 256,
  with_eavesdropper: false,
  eavesdropper_intercept_rate: 0.5,
  transmission_multiplier: 4
};

const response = await fetch('http://localhost:8000/api/protocol/execute', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(config)
});

const result = await response.json();
console.log(result);
```

### Using Python/Requests

```python
import requests

config = {
    "key_length": 256,
    "with_eavesdropper": False,
    "eavesdropper_intercept_rate": 0.5,
    "transmission_multiplier": 4
}

response = requests.post(
    'http://localhost:8000/api/protocol/execute',
    json=config
)

result = response.json()
print(result)
```

---

## Response Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 422 | Unprocessable Entity (validation error) |
| 500 | Internal Server Error |

---

## Rate Limiting

Currently, no rate limiting is implemented. Each request is processed immediately.

## CORS

CORS is enabled for local development on:
- `http://localhost:3000`
- `http://localhost:5173`
- `http://127.0.0.1:3000`
- `http://127.0.0.1:5173`

---

## Performance

- Average execution time: 10-50ms per protocol run
- No persistent storage (stateless API)
- Concurrent requests supported

---

## API Documentation UI

Interactive API documentation available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
