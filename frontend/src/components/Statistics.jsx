import React from 'react';

export default function Statistics({ result }) {
  if (!result) return null;

  return (
    <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
      <h2 className="text-2xl font-bold text-white mb-4">Protocol Statistics</h2>
      <div className="grid md:grid-cols-4 gap-4">
        <div className="bg-blue-500/20 rounded-lg p-4 border border-blue-400/30">
          <div className="text-blue-300 text-sm mb-1">Transmitted Qubits</div>
          <div className="text-white text-2xl font-bold">{result.transmission.total_qubits}</div>
        </div>
        <div className="bg-green-500/20 rounded-lg p-4 border border-green-400/30">
          <div className="text-green-300 text-sm mb-1">After Sifting</div>
          <div className="text-white text-2xl font-bold">{result.transmission.sifted_bits}</div>
        </div>
        <div className="bg-purple-500/20 rounded-lg p-4 border border-purple-400/30">
          <div className="text-purple-300 text-sm mb-1">Final Key Length</div>
          <div className="text-white text-2xl font-bold">{result.transmission.final_key_bits}</div>
        </div>
        <div className="bg-yellow-500/20 rounded-lg p-4 border border-yellow-400/30">
          <div className="text-yellow-300 text-sm mb-1">Sifting Efficiency</div>
          <div className="text-white text-2xl font-bold">{result.transmission.sifting_efficiency}%</div>
        </div>
      </div>
    </div>
  );
}
