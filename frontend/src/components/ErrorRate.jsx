import React from 'react';
import { Shield, AlertCircle } from 'lucide-react';

export default function ErrorRate({ result }) {
  if (!result) return null;

  return (
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
  );
}
