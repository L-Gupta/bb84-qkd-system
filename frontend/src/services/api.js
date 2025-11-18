/**
 * API service for BB84 QKD Backend
 * 
 * Handles all communication with the FastAPI backend
 */

import axios from 'axios';

// Base URL for API
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 second timeout
});

// API service object
const api = {
  /**
   * Execute BB84 protocol (custom implementation)
   * @param {Object} config - Protocol configuration
   * @returns {Promise} Protocol execution result
   */
  executeProtocol: async (config) => {
    try {
      const response = await apiClient.post('/protocol/execute', config);
      return response.data;
    } catch (error) {
      console.error('Error executing protocol:', error);
      throw error;
    }
  },

  /**
   * Execute BB84 protocol using Qiskit
   * @param {Object} config - Protocol configuration
   * @returns {Promise} Protocol execution result
   */
  executeProtocolQiskit: async (config) => {
    try {
      const response = await apiClient.post('/protocol/execute-qiskit', config);
      return response.data;
    } catch (error) {
      console.error('Error executing Qiskit protocol:', error);
      throw error;
    }
  },

  /**
   * Execute multiple protocol runs
   * @param {number} runs - Number of runs
   * @param {Object} config - Protocol configuration
   * @returns {Promise} Batch execution results
   */
  executeBatch: async (runs, config) => {
    try {
      const response = await apiClient.post('/protocol/batch', {
        runs,
        config
      });
      return response.data;
    } catch (error) {
      console.error('Error executing batch:', error);
      throw error;
    }
  },

  /**
   * Get protocol information
   * @returns {Promise} Protocol info
   */
  getProtocolInfo: async () => {
    try {
      const response = await apiClient.get('/protocol/info');
      return response.data;
    } catch (error) {
      console.error('Error fetching protocol info:', error);
      throw error;
    }
  },

  /**
   * Get security threshold information
   * @returns {Promise} Security threshold info
   */
  getSecurityThreshold: async () => {
    try {
      const response = await apiClient.get('/security/threshold');
      return response.data;
    } catch (error) {
      console.error('Error fetching security threshold:', error);
      throw error;
    }
  },

  /**
   * Analyze eavesdropper impact
   * @param {Array} intercept_rates - List of intercept rates to analyze
   * @returns {Promise} Analysis results
   */
  analyzeEavesdropper: async (intercept_rates) => {
    try {
      const response = await apiClient.post('/analyze/eavesdropper', {
        intercept_rates,
        key_length: 256
      });
      return response.data;
    } catch (error) {
      console.error('Error analyzing eavesdropper:', error);
      throw error;
    }
  },

  /**
   * Health check
   * @returns {Promise} Health status
   */
  healthCheck: async () => {
    try {
      const response = await apiClient.get('/health');
      return response.data;
    } catch (error) {
      console.error('Error checking health:', error);
      throw error;
    }
  }
};

export default api;