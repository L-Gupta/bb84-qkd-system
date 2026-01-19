import React from 'react';
import { Radio, Zap, Lock, Loader2, AlertCircle } from 'lucide-react';

export default function Controls({
  keyLength,
  setKeyLength,
  withEve,
  setWithEve,
  eveRate,
  setEveRate,
  loading,
  onRunProtocol,
  error,
  backendReady = true
}) {
  return (
    <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 mb-6 border border-white/20">
      <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
        <Zap className="w-6 h-6 text-yellow-400" />
        Protocol Configuration
      </h2>
      
      {!backendReady && (
        <div className="mb-4 bg-yellow-500/20 border border-yellow-400/30 rounded-lg p-3 flex items-start gap-2">
          <AlertCircle className="w-5 h-5 text-yellow-400 flex-shrink-0 mt-0.5" />
          <div className="text-yellow-300 text-sm">
            <strong>Backend Connecting...</strong> The server appears to be starting. Please wait a moment and refresh the page.
          </div>
        </div>
      )}
      
      <div className="grid md:grid-cols-2 gap-6">
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
      </div>
      
      {withEve && (
        <div className="mt-4">
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
      
      <button
        onClick={onRunProtocol}
        disabled={loading || !backendReady}
        className="mt-6 w-full bg-gradient-to-r from-cyan-500 to-blue-500 hover:from-cyan-600 hover:to-blue-600 text-white font-bold py-3 px-6 rounded-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
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
  );
}
