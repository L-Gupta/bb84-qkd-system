import Controls from "./components/Controls";
import Dashboard from "./components/Dashboard";
import ErrorRate from "./components/ErrorRate";
import ProtocolInfo from "./components/ProtocolInfo";
import SecretKey from "./components/SecretKey";
import Statistics from "./components/Statistics";
import "./App.css";

function App() {
  // 🔒 HARD-CODED DATA (TEMP FIX)
  const performance = {
    efficiency_score: 92.4,
    rating: "Excellent",
  };

  const information = {
    mutual_information: 0.982,
  };

  const executionTime = 12.4;

  const transmission = {
    total_qubits: 1024,
    sifted_bits: 512,
    final_key_bits: 256,
    sifting_efficiency: 50,
  };

  const security = {
    is_secure: true,
    qber: 2.1,
    errors_found: 10,
    bits_checked: 512,
  };

  <SecretKey
  secretKey={{
    binary: "1010101011001100",
    hex: "AACC",
    length: 16,
    quality: { balance: 0.5, is_balanced: true }
  }}
/>


  return (
    <div className="app-container">
      <Dashboard
        performance={performance}
        information={information}
        executionTime={executionTime}
      />

      <Controls
        keyLength={128}
        setKeyLength={() => {}}
        withEve={false}
        setWithEve={() => {}}
        eveRate={0.1}
        setEveRate={() => {}}
        loading={false}
        onRun={() => {}}
      />

      <Statistics transmission={transmission} />
      <ErrorRate security={security} />
      <SecretKey secretKey={secretKey} />
      <ProtocolInfo />
    </div>
  );
}

export default App;
