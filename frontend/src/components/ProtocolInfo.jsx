import React from 'react';

export default function ProtocolInfo() {
  return (
    <div className="mt-8 bg-white/5 backdrop-blur-lg rounded-xl p-6 border border-white/10">
      <h3 className="text-xl font-bold text-white mb-3">How BB84 Works</h3>
      <div className="text-blue-200 space-y-2 text-sm">
        <p><strong>1. Preparation:</strong> Alice generates random bits and encodes them in random bases (Z or X)</p>
        <p><strong>2. Transmission:</strong> Alice sends qubits to Bob through quantum channel</p>
        <p><strong>3. Measurement:</strong> Bob measures each qubit in a randomly chosen basis</p>
        <p><strong>4. Sifting:</strong> Alice and Bob publicly compare bases and keep bits where bases matched (~50%)</p>
        <p><strong>5. Error Check:</strong> They sacrifice some bits to estimate error rate (QBER)</p>
        <p><strong>6. Privacy Amplification:</strong> Remaining bits become the shared secret key</p>
        <p className="text-yellow-300 mt-3"><strong>Security:</strong> Any eavesdropper disturbs quantum states, creating detectable errors (QBER &gt; 11% indicates attack)</p>
      </div>
    </div>
  );
}
