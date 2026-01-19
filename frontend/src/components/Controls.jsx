import { Lock, Radio, Zap, Loader2 } from 'lucide-react';

export default function Controls({
  keyLength,
  setKeyLength,
  withEve,
  setWithEve,
  eveRate,
  setEveRate,
  loading,
  onRun
}) {
  return (
    <div className="card">
      <h2 className="card-title">
        <Zap /> Protocol Configuration
      </h2>

      <div className="grid-2">
        <div className="form-group">
          <label className="form-label">Key Length (bits)</label>
          <input
            type="number"
            className="form-input"
            min="64"
            max="512"
            step="64"
            value={keyLength}
            onChange={(e) => setKeyLength(Number(e.target.value))}
          />
        </div>

        <div className="form-group">
          <label className="form-label">
            <Radio /> Eavesdropper (Eve)
          </label>
          <label className="checkbox-group">
            <input
              type="checkbox"
              checked={withEve}
              onChange={(e) => setWithEve(e.target.checked)}
            />
            Enable Interception
          </label>
        </div>
      </div>

      {withEve && (
        <div className="form-group">
          <label className="form-label">
            Interception Rate: {(eveRate * 100).toFixed(0)}%
          </label>
          <input
            type="range"
            className="slider"
            min="0"
            max="1"
            step="0.1"
            value={eveRate}
            onChange={(e) => setEveRate(Number(e.target.value))}
          />
        </div>
      )}

      <button className="btn-primary" onClick={onRun} disabled={loading}>
        {loading ? (
          <>
            <Loader2 className="spinner" /> Processing…
          </>
        ) : (
          <>
            <Lock /> Execute BB84 Protocol
          </>
        )}
      </button>
    </div>
  );
}
