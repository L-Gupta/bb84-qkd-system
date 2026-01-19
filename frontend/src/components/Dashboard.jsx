import React from 'react';

export default function Dashboard({ result }) {
  if (!result) return null;

  return (
    <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
      <h2 className="text-2xl font-bold text-white mb-4">Performance Metrics</h2>
      <div className="grid md:grid-cols-3 gap-4">
        <div className="bg-indigo-500/20 rounded-lg p-4 border border-indigo-400/30">
          <div className="text-indigo-300 text-sm mb-1">Efficiency Score</div>
          <div className="text-white text-2xl font-bold">{result.performance.efficiency_score.toFixed(1)}/100</div>
          <div className="text-sm text-indigo-300 mt-1">{result.performance.rating}</div>
        </div>
        <div className="bg-cyan-500/20 rounded-lg p-4 border border-cyan-400/30">
          <div className="text-cyan-300 text-sm mb-1">Mutual Information</div>
          <div className="text-white text-2xl font-bold">{result.information_theory.mutual_information.toFixed(3)}</div>
        </div>
        <div className="bg-teal-500/20 rounded-lg p-4 border border-teal-400/30">
          <div className="text-teal-300 text-sm mb-1">Execution Time</div>
          <div className="text-white text-2xl font-bold">{result.execution_time_ms.toFixed(1)}ms</div>
        </div>
      </div>
      <div className="mt-3 text-center">
        <span className="text-cyan-400 font-semibold">⚛️ Powered by Qiskit Quantum Circuits</span>
      </div>
    </div>
  );
}
