import React, { useState, useEffect } from 'react';
import { Shield } from 'lucide-react';
import api from './services/api';
import Controls from './components/Controls';
import Statistics from './components/Statistics';
import ErrorRate from './components/ErrorRate';
import Dashboard from './components/Dashboard';
import SecretKey from './components/SecretKey';
import ProtocolInfo from './components/ProtocolInfo';

export default function App() {
  const [keyLength, setKeyLength] = useState(256);
  const [withEve, setWithEve] = useState(false);
  const [eveRate, setEveRate] = useState(0.5);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [backendReady, setBackendReady] = useState(false);

  // Check backend connectivity on mount
  useEffect(() => {
    const checkBackend = async () => {
      try {
        const health = await api.healthCheck();
        console.log('Backend health:', health);
        setBackendReady(true);
      } catch (err) {
        console.warn('Backend not ready:', err.message);
        setBackendReady(false);
        setError('Backend not available. Ensure backend is running on port 8000');
      }
    };

    checkBackend();
  }, []);

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

      console.log('Sending config:', config);
      const data = await api.executeProtocol(config);
      console.log('Received result:', data);
      
      setResult(data);
    } catch (err) {
      console.error('Full error object:', err);
      const errorMessage = err.response?.data?.detail || err.message || 'Failed to execute protocol';
      setError(errorMessage);
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
          <p className="text-sm text-blue-300 mt-2">Bennett & Brassard (1984) • Powered by Qiskit</p>
        </div>

        {/* Controls */}
        <Controls
          keyLength={keyLength}
          setKeyLength={setKeyLength}
          withEve={withEve}
          setWithEve={setWithEve}
          eveRate={eveRate}
          setEveRate={setEveRate}
          loading={loading}
          onRunProtocol={runProtocol}
          error={error}
          backendReady={backendReady}
        />

        {/* Results */}
        {result && (
          <div className="space-y-6">
            <Statistics result={result} />
            <ErrorRate result={result} />
            <Dashboard result={result} />
            <SecretKey result={result} />
          </div>
        )}

        {/* Protocol Info */}
        <ProtocolInfo />
      </div>
    </div>
  );
}