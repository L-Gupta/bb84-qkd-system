export default function ProtocolInfo() {
  return (
    <div className="info-box">
      <h3 className="info-title">How BB84 Works</h3>

      <div className="info-content">
        <p><strong>1. Preparation:</strong> Alice generates random bits and encodes them in random bases (Z or X)</p>
        <p><strong>2. Transmission:</strong> Alice sends qubits to Bob through the quantum channel</p>
        <p><strong>3. Measurement:</strong> Bob measures each qubit in a randomly chosen basis</p>
        <p><strong>4. Sifting:</strong> Bases are compared and matching bits are kept (~50%)</p>
        <p><strong>5. Error Check:</strong> QBER is estimated by sacrificing some bits</p>
        <p><strong>6. Privacy Amplification:</strong> Remaining bits form the shared key</p>

        <p className="info-highlight">
          <strong>Security:</strong> QBER &gt; 11% indicates possible eavesdropping
        </p>
      </div>
    </div>
  );
}
