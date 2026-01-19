import { Lock } from 'lucide-react';

export default function SecretKey({ key }) {
  return (
    <div className="card">
      <h2 className="card-title">
        <Lock /> Shared Secret Key
      </h2>

      <div className="key-display">
        <div className="key-label">Binary Format:</div>
        <div className="key-value">{key.binary}</div>

        <div className="key-label">Hexadecimal Format:</div>
        <div className="key-value key-value-large">{key.hex}</div>
      </div>

      <div className="grid-3" style={{ marginTop: '1rem' }}>
        <div className="stat-box stat-box-purple">
          <div className="stat-label">Key Length</div>
          <div className="stat-value">{key.length} bits</div>
        </div>

        <div className="stat-box stat-box-blue">
          <div className="stat-label">Balance</div>
          <div className="stat-value">
            {(key.quality.balance * 100).toFixed(1)}%
          </div>
        </div>

        <div className="stat-box stat-box-green">
          <div className="stat-label">Quality</div>
          <div className="stat-value">
            {key.quality.is_balanced ? '✓ Balanced' : '✗ Imbalanced'}
          </div>
        </div>
      </div>
    </div>
  );
}
