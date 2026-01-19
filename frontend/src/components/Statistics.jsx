export default function Statistics({ transmission }) {
  return (
    <div className="card">
      <h2 className="card-title">Protocol Statistics</h2>

      <div className="grid-4">
        <div className="stat-box stat-box-blue">
          <div className="stat-label">Transmitted Qubits</div>
          <div className="stat-value">{transmission.total_qubits}</div>
        </div>

        <div className="stat-box stat-box-green">
          <div className="stat-label">After Sifting</div>
          <div className="stat-value">{transmission.sifted_bits}</div>
        </div>

        <div className="stat-box stat-box-purple">
          <div className="stat-label">Final Key Length</div>
          <div className="stat-value">{transmission.final_key_bits}</div>
        </div>

        <div className="stat-box stat-box-yellow">
          <div className="stat-label">Sifting Efficiency</div>
          <div className="stat-value">{transmission.sifting_efficiency}%</div>
        </div>
      </div>
    </div>
  );
}
