import React, { useState } from 'react';
import { AlertCircle, Lock, Radio, Shield, Zap, Loader2, Cpu } from 'lucide-react';
import api from './services/api';

export default function App() {
  const [keyLength, setKeyLength] = useState(256);
  const [withEve, setWithEve] = useState(false);
  const [eveRate, setEveRate] = useState(0.5);
  const [useQiskit, setUseQiskit] = useState(false);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const runProtocol = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const config = {
        key_length: keyLength,
        with_eavesdropper: withEve,
        eavesdropper_intercept_rate: eveRate,
        transmission_multiplier: 4
      };

      // Use Qiskit or custom implementation
      const data = useQiskit 
        ? await api.executeProtocolQiskit(config)
        : await api.executeProtocol(config);
      
      setResult(data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to execute protocol');
      console.error('Protocol execution error:', err);
    } finally {
      setLoading(false);
    }
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
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Processing...
              </>
            ) : (
              <>
                <Lock className="w-5 h-5" />
                Execute BB84 Protocol
              </>
            )}
          </button>

          {error && (
            <div className="mt-4 bg-red-500/20 border border-red-400/30 rounded-lg p-4">
              <p className="text-red-300 font-semibold">Error: {error}</p>
            </div>
          )}
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

            {/* Error Rate */}
            <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
              <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
                {result.security.is_secure ? (
                  <>
                    <Shield className="w-6 h-6 text-green-400" />
                    Security Status
                  </>
                ) : (
                  <>
                    <AlertCircle className="w-6 h-6 text-red-400" />
                    Security Alert
                  </>
                )}
              </h2>
              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <div className="text-blue-200 mb-2">Quantum Bit Error Rate (QBER)</div>
                  <div className={`text-4xl font-bold ${
                    result.security.is_secure ? 'text-green-400' : 'text-red-400'
                  }`}>
                    {result.security.qber.toFixed(2)}%
                  </div>
                  <div className="text-sm text-blue-300 mt-2">
                    {result.security.errors_found} errors in {result.security.bits_checked} checked bits
                  </div>
                </div>
                <div className={`rounded-lg p-4 ${
                  result.security.is_secure
                    ? 'bg-green-500/20 border border-green-400/30' 
                    : 'bg-red-500/20 border border-red-400/30'
                }`}>
                  <div className={`font-bold mb-2 ${
                    result.security.is_secure ? 'text-green-300' : 'text-red-300'
                  }`}>
                    {result.security.is_secure ? '✓ Channel Secure' : '⚠️ Eavesdropping Detected!'}
                  </div>
                  <div className="text-sm text-white">
                    {result.security.is_secure
                      ? 'QBER within acceptable limits. Key exchange successful.'
                      : 'QBER exceeds 11% threshold. Possible eavesdropper present. Key should be discarded.'}
                  </div>
                </div>
              </div>
            </div>

            {/* Performance Metrics */}
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
                  {result.key.binary}
                </div>
                <div className="text-cyan-300 text-xs mb-2 font-mono">Hexadecimal Format:</div>
                <div className="text-white font-mono text-lg break-all">
                  {result.key.hex}
                </div>
              </div>
              
              {/* Key Quality */}
              <div className="mt-4 grid md:grid-cols-3 gap-4">
                <div className="bg-purple-500/20 rounded-lg p-3 border border-purple-400/30">
                  <div className="text-purple-300 text-xs mb-1">Key Length</div>
                  <div className="text-white font-bold">{result.key.length} bits</div>
                </div>
                <div className="bg-blue-500/20 rounded-lg p-3 border border-blue-400/30">
                  <div className="text-blue-300 text-xs mb-1">Balance</div>
                  <div className="text-white font-bold">{(result.key.quality.balance * 100).toFixed(1)}%</div>
                </div>
                <div className="bg-green-500/20 rounded-lg p-3 border border-green-400/30">
                  <div className="text-green-300 text-xs mb-1">Quality</div>
                  <div className="text-white font-bold">{result.key.quality.is_balanced ? '✓ Balanced' : '✗ Imbalanced'}</div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Protocol Info */}
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
      </div>
    </div>
  );
}