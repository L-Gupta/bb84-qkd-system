export default function Dashboard({ performance, information, executionTime }) {
  if (!performance || !information) return null;

  return (
    <div className="card">
      <h2 className="card-title">Performance Metrics</h2>

      <div className="grid-3">
        <div className="stat-box stat-box-indigo">
          <div className="stat-label">Efficiency Score</div>
          <div className="stat-value">
            {performance.efficiency_score.toFixed(1)}/100
          </div>
          <div className="stat-subtitle">{performance.rating}</div>
        </div>

        <div className="stat-box stat-box-cyan">
          <div className="stat-label">Mutual Information</div>
          <div className="stat-value">
            {information.mutual_information.toFixed(3)}
          </div>
        </div>

        <div className="stat-box stat-box-teal">
          <div className="stat-label">Execution Time</div>
          <div className="stat-value">
            {executionTime.toFixed(1)} ms
          </div>
        </div>
      </div>
    </div>
  );
}
