import { Shield, AlertCircle } from "lucide-react";

export default function ErrorRate({ security }) {
  if (!security) return null;

  const secure = security.is_secure;

  return (
    <div className="card">
      <h2 className="card-title">
        {secure ? <Shield /> : <AlertCircle />}
        {secure ? "Security Status" : "Security Alert"}
      </h2>

      <div className="grid-2">
        <div>
          <div className="stat-label">Quantum Bit Error Rate (QBER)</div>
          <div className="stat-value">{security.qber.toFixed(2)}%</div>
          <div className="stat-subtitle">
            {security.errors_found} errors in {security.bits_checked} checked bits
          </div>
        </div>

        <div
          className={`security-box ${
            secure ? "security-secure" : "security-insecure"
          }`}
        >
          <div
            className={`security-title ${
              secure
                ? "security-title-secure"
                : "security-title-insecure"
            }`}
          >
            {secure ? "✓ Channel Secure" : "⚠ Eavesdropping Detected"}
          </div>
          <div className="security-message">
            {secure
              ? "QBER within acceptable limits. Key exchange successful."
              : "QBER exceeds 11% threshold. Key should be discarded."}
          </div>
        </div>
      </div>
    </div>
  );
}
