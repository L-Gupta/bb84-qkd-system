import React, { useState } from 'react';
import { AlertCircle, Lock, Unlock, Radio, Shield, Zap } from 'lucide-react';

// Quantum state representation
class Qubit {
  constructor(basis, bit) {
    this.basis = basis; // 'rectilinear' (+) or 'diagonal' (x)
    this.bit = bit;     // 0 or 1
  }
  
  // Measure the qubit in a given basis
  measure(measurementBasis) {
    if (this.basis === measurementBasis) {
      return this.bit; // Correct basis - get correct bit
    } else {
      return Math.random() < 0.5 ? 0 : 1; // Wrong basis - random result
    }
  }
}

// BB84 Protocol Implementation
class BB84Protocol {
  constructor(keyLength = 256) {
    this.keyLength = keyLength;
    this.transmissionMultiplier = 4; // Send 4x more bits than needed
  }
  
  // Alice prepares qubits
  alicePrepare() {
    const n = this.keyLength * this.transmissionMultiplier;
    const aliceBits = Array.from({ length: n }, () => Math.random() < 0.5 ? 0 : 1);
    const aliceBases = Array.from({ length: n }, () => 
      Math.random() < 0.5 ? 'rectilinear' : 'diagonal'
    );
    
    const qubits = aliceBits.map((bit, i) => new Qubit(aliceBases[i], bit));
    
    return { aliceBits, aliceBases, qubits };
  }
  
  // Bob measures qubits
  bobMeasure(qubits) {
    const n = qubits.length;
    const bobBases = Array.from({ length: n }, () => 
      Math.random() < 0.5 ? 'rectilinear' : 'diagonal'
    );
    const bobBits = qubits.map((qubit, i) => qubit.measure(bobBases[i]));
    
    return { bobBases, bobBits };
  }
  
  // Sifting: Keep only bits where bases match
  sift(aliceBits, aliceBases, bobBits, bobBases) {
    const siftedAlice = [];
    const siftedBob = [];
    const matchingIndices = [];
    
    for (let i = 0; i < aliceBases.length; i++) {
      if (aliceBases[i] === bobBases[i]) {
        siftedAlice.push(aliceBits[i]);
        siftedBob.push(bobBits[i]);
        matchingIndices.push(i);
      }
    }
    
    return { siftedAlice, siftedBob, matchingIndices };
  }
  
  // Error estimation: Check random subset for eavesdropping
  estimateError(siftedAlice, siftedBob, sampleSize = 50) {
    const n = Math.min(siftedAlice.length, sampleSize);
    let errors = 0;
    const checkedIndices = [];
    
    // Randomly sample indices
    const availableIndices = [...Array(siftedAlice.length).keys()];
    for (let i = 0; i < n; i++) {
      const randomIndex = Math.floor(Math.random() * availableIndices.length);
      const index = availableIndices.splice(randomIndex, 1)[0];
      checkedIndices.push(index);
      
      if (siftedAlice[index] !== siftedBob[index]) {
        errors++;
      }
    }
    
    const errorRate = errors / n;
    return { errorRate, errors, checkedIndices, sampleSize: n };
  }
  
  // Privacy amplification: Generate final key
  privacyAmplification(siftedAlice, checkedIndices) {
    // Remove checked bits
    const finalKey = siftedAlice.filter((_, i) => !checkedIndices.includes(i));
    
    // Take only keyLength bits
    return finalKey.slice(0, this.keyLength);
  }
  
  // Simulate eavesdropper (Eve)
  eveIntercept(qubits, interceptProbability = 0.5) {
    return qubits.map(qubit => {
      if (Math.random() < interceptProbability) {
        // Eve intercepts and measures
        const eveBasis = Math.random() < 0.5 ? 'rectilinear' : 'diagonal';
        const measuredBit = qubit.measure(eveBasis);
        // Eve sends a new qubit based on her measurement
        return new Qubit(eveBasis, measuredBit);
      }
      return qubit;
    });
  }
  
  // Full protocol execution
  execute(withEavesdropper = false, eveInterceptRate = 0.5) {
    // Step 1: Alice prepares qubits
    const { aliceBits, aliceBases, qubits } = this.alicePrepare();
    
    // Step 2: Optional eavesdropper
    let transmittedQubits = qubits;
    if (withEavesdropper) {
      transmittedQubits = this.eveIntercept(qubits, eveInterceptRate);
    }
    
    // Step 3: Bob measures
    const { bobBases, bobBits } = this.bobMeasure(transmittedQubits);
    
    // Step 4: Sifting
    const { siftedAlice, siftedBob, matchingIndices } = this.sift(
      aliceBits, aliceBases, bobBits, bobBases
    );
    
    // Step 5: Error estimation
    const errorCheck = this.estimateError(siftedAlice, siftedBob);
    
    // Step 6: Privacy amplification
    const finalKey = this.privacyAmplification(siftedAlice, errorCheck.checkedIndices);
    
    return {
      aliceBits,
      aliceBases,
      bobBits,
      bobBases,
      siftedAlice,
      siftedBob,
      matchingIndices,
      errorCheck,
      finalKey,
      stats: {
        transmitted: aliceBits.length,
        sifted: siftedAlice.length,
        finalKeyLength: finalKey.length,
        siftingEfficiency: (siftedAlice.length / aliceBits.length * 100).toFixed(1),
      }
    };
  }
}

// Main React Component
export default function BB84Dashboard() {
  const [keyLength, setKeyLength] = useState(128);
  const [withEve, setWithEve] = useState(false);
  const [eveRate, setEveRate] = useState(0.5);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const runProtocol = () => {
    setLoading(true);
    setTimeout(() => {
      const protocol = new BB84Protocol(keyLength);
      const res = protocol.execute(withEve, eveRate);
      setResult(res);
      setLoading(false);
    }, 100);
  };

  const bitsToHex = (bits) => {
    let hex = '';
    for (let i = 0; i < bits.length; i += 4) {
      const chunk = bits.slice(i, i + 4).join('');
      hex += parseInt(chunk, 2).toString(16);
    }
    return hex.toUpperCase();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-3 mb-4">
            <Shield className="w-12 h-12 text-cyan-400" />
            <h1 className="text-5xl font-bold text-white">BB84 QKD Protocol</h1>
          </div>
          <p className="text-xl text-blue-200">Quantum Key Distribution Simulator</p>
          <p className="text-sm text-blue-300 mt-2">Bennett & Brassard (1984)</p>
        </div>

        {/* Controls */}
        <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 mb-6 border border-white/20">
          <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
            <Zap className="w-6 h-6 text-yellow-400" />
            Protocol Configuration
          </h2>
          
          <div className="grid md:grid-cols-3 gap-6">
            <div>
              <label className="block text-white mb-2 font-semibold">Key Length (bits)</label>
              <input
                type="number"
                value={keyLength}
                onChange={(e) => setKeyLength(parseInt(e.target.value))}
                className="w-full px-4 py-2 bg-white/20 border border-white/30 rounded-lg text-white"
                min="64"
                max="512"
                step="64"
              />
            </div>
            
            <div>
              <label className="flex items-center gap-2 text-white mb-2 font-semibold">
                <Radio className="w-5 h-5 text-red-400" />
                Eavesdropper (Eve)
              </label>
              <label className="flex items-center gap-3 cursor-pointer">
                <input
                  type="checkbox"
                  checked={withEve}
                  onChange={(e) => setWithEve(e.target.checked)}
                  className="w-5 h-5"
                />
                <span className="text-white">Enable Interception</span>
              </label>
            </div>
            
            {withEve && (
              <div>
                <label className="block text-white mb-2 font-semibold">
                  Interception Rate: {(eveRate * 100).toFixed(0)}%
                </label>
                <input
                  type="range"
                  value={eveRate}
                  onChange={(e) => setEveRate(parseFloat(e.target.value))}
                  className="w-full"
                  min="0"
                  max="1"
                  step="0.1"
                />
              </div>
            )}
          </div>
          
          <button
            onClick={runProtocol}
            disabled={loading}
            className="mt-6 w-full bg-gradient-to-r from-cyan-500 to-blue-500 hover:from-cyan-600 hover:to-blue-600 text-white font-bold py-3 px-6 rounded-lg transition-all disabled:opacity-50 flex items-center justify-center gap-2"
          >
            {loading ? (
              <>Processing...</>
            ) : (
              <>
                <Lock className="w-5 h-5" />
                Execute BB84 Protocol
              </>
            )}
          </button>
        </div>

        {/* Results */}
        {result && (
          <div className="space-y-6">
            {/* Statistics */}
            <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
              <h2 className="text-2xl font-bold text-white mb-4">Protocol Statistics</h2>
              <div className="grid md:grid-cols-4 gap-4">
                <div className="bg-blue-500/20 rounded-lg p-4 border border-blue-400/30">
                  <div className="text-blue-300 text-sm mb-1">Transmitted Qubits</div>
                  <div className="text-white text-2xl font-bold">{result.stats.transmitted}</div>
                </div>
                <div className="bg-green-500/20 rounded-lg p-4 border border-green-400/30">
                  <div className="text-green-300 text-sm mb-1">After Sifting</div>
                  <div className="text-white text-2xl font-bold">{result.stats.sifted}</div>
                </div>
                <div className="bg-purple-500/20 rounded-lg p-4 border border-purple-400/30">
                  <div className="text-purple-300 text-sm mb-1">Final Key Length</div>
                  <div className="text-white text-2xl font-bold">{result.stats.finalKeyLength}</div>
                </div>
                <div className="bg-yellow-500/20 rounded-lg p-4 border border-yellow-400/30">
                  <div className="text-yellow-300 text-sm mb-1">Sifting Efficiency</div>
                  <div className="text-white text-2xl font-bold">{result.stats.siftingEfficiency}%</div>
                </div>
              </div>
            </div>

            {/* Error Rate */}
            <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
              <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
                {result.errorCheck.errorRate > 0.11 ? (
                  <>
                    <AlertCircle className="w-6 h-6 text-red-400" />
                    Security Alert
                  </>
                ) : (
                  <>
                    <Shield className="w-6 h-6 text-green-400" />
                    Security Status
                  </>
                )}
              </h2>
              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <div className="text-blue-200 mb-2">Quantum Bit Error Rate (QBER)</div>
                  <div className={`text-4xl font-bold ${
                    result.errorCheck.errorRate > 0.11 ? 'text-red-400' : 'text-green-400'
                  }`}>
                    {(result.errorCheck.errorRate * 100).toFixed(2)}%
                  </div>
                  <div className="text-sm text-blue-300 mt-2">
                    {result.errorCheck.errors} errors in {result.errorCheck.sampleSize} checked bits
                  </div>
                </div>
                <div className={`rounded-lg p-4 ${
                  result.errorCheck.errorRate > 0.11 
                    ? 'bg-red-500/20 border border-red-400/30' 
                    : 'bg-green-500/20 border border-green-400/30'
                }`}>
                  <div className={`font-bold mb-2 ${
                    result.errorCheck.errorRate > 0.11 ? 'text-red-300' : 'text-green-300'
                  }`}>
                    {result.errorCheck.errorRate > 0.11 
                      ? '⚠️ Eavesdropping Detected!' 
                      : '✓ Channel Secure'}
                  </div>
                  <div className="text-sm text-white">
                    {result.errorCheck.errorRate > 0.11
                      ? 'QBER exceeds 11% threshold. Possible eavesdropper present. Key should be discarded.'
                      : 'QBER within acceptable limits. Key exchange successful.'}
                  </div>
                </div>
              </div>
            </div>

            {/* Final Key */}
            <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
              <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
                <Lock className="w-6 h-6 text-cyan-400" />
                Shared Secret Key
              </h2>
              <div className="bg-black/30 rounded-lg p-4 border border-cyan-400/30">
                <div className="text-cyan-300 text-xs mb-2 font-mono">Binary Format:</div>
                <div className="text-white font-mono text-sm break-all mb-4">
                  {result.finalKey.join('')}
                </div>
                <div className="text-cyan-300 text-xs mb-2 font-mono">Hexadecimal Format:</div>
                <div className="text-white font-mono text-lg break-all">
                  {bitsToHex(result.finalKey)}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Protocol Info */}
        <div className="mt-8 bg-white/5 backdrop-blur-lg rounded-xl p-6 border border-white/10">
          <h3 className="text-xl font-bold text-white mb-3">How BB84 Works</h3>
          <div className="text-blue-200 space-y-2 text-sm">
            <p><strong>1. Preparation:</strong> Alice generates random bits and encodes them in random bases (rectilinear or diagonal)</p>
            <p><strong>2. Transmission:</strong> Alice sends qubits to Bob through quantum channel</p>
            <p><strong>3. Measurement:</strong> Bob measures each qubit in a randomly chosen basis</p>
            <p><strong>4. Sifting:</strong> Alice and Bob publicly compare bases and keep bits where bases matched (~50%)</p>
            <p><strong>5. Error Check:</strong> They sacrifice some bits to estimate error rate (QBER)</p>
            <p><strong>6. Privacy Amplification:</strong> Remaining bits become the shared secret key</p>
            <p className="text-yellow-300 mt-3"><strong>Security:</strong> Any eavesdropper disturbs quantum states, creating detectable errors (QBER &gt; 11% indicates attack)</p>
          </div>
        </div>
      </div>
    </div>
  );
}