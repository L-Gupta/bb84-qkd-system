import React from 'react';
import { Lock } from 'lucide-react';

export default function SecretKey({ result }) {
  if (!result) return null;

  return (
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
  );
}
