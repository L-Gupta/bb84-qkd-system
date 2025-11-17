# BB84 Quantum Key Distribution System

A full-stack implementation of the BB84 Quantum Key Distribution protocol with interactive web dashboard and eavesdropper detection.

## 🔐 Overview

This project implements the BB84 protocol (Bennett & Brassard, 1984) for secure quantum key distribution, demonstrating how quantum mechanics enables cryptographically secure communication with guaranteed eavesdropping detection.

## 🏗️ Project Structure

```
bb84-qkd-system/
├── backend/                 # Python FastAPI backend
│   ├── core/               # Core quantum logic
│   │   ├── qubit.py       # Qubit implementation (Z/X basis)
│   │   ├── eavesdropper.py # Intercept-resend attack
│   │   └── bb84.py        # Complete BB84 protocol
│   ├── api/                # REST API endpoints
│   ├── utils/              # Helper utilities
│   ├── tests/              # Unit tests (65+ tests)
│   └── requirements.txt
│
├── frontend/               # React web dashboard
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── services/      # API clients
│   │   └── hooks/         # Custom hooks
│   └── package.json
│
├── docs/                   # Documentation
│   ├── API.md             # API documentation
│   ├── PROTOCOL.md        # BB84 explanation
│   └── DEPLOYMENT.md      # Deployment guide
│
└── README.md              # This file
```

## ✨ Features

### Backend (Python + FastAPI)
- ✅ **Complete BB84 Protocol**: All 6 steps implemented
  - Qubit preparation in Z/X bases
  - Quantum transmission simulation
  - Bob's measurement
  - Basis sifting (~50% efficiency)
  - Error estimation (QBER calculation)
  - Privacy amplification
  
- ✅ **Eavesdropper Simulation**: Configurable intercept-resend attack
- ✅ **Security Detection**: Automatic alert when QBER > 11%
- ✅ **Comprehensive Testing**: 65+ unit tests with pytest
- ⏳ **REST API**: FastAPI endpoints (in progress)

### Frontend (React)
- ⏳ **Interactive Dashboard**: Real-time protocol visualization
- ⏳ **Configuration Controls**: Adjust key length, Eve intercept rate
- ⏳ **Statistics Display**: QBER, efficiency metrics
- ⏳ **Security Alerts**: Visual eavesdropping warnings
- ⏳ **Key Display**: Binary and hex format

## 🚀 Quick Start

### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# Run demo
python -m core.bb84

# Start API server (coming soon)
uvicorn main:app --reload
```

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

## 📊 Current Progress

```
Backend:  ████████░░ 60% Complete
├─ Core Components: ✅ 100% (Qubit, Eve, BB84)
├─ Testing: ✅ 100% (65/65 tests passing)
├─ API Layer: ⏳ 0% (in progress)
└─ Main Server: ⏳ 0% (planned)

Frontend: ░░░░░░░░░░ 0% Complete
├─ Dashboard: ⏳ Planned
├─ Components: ⏳ Planned
└─ API Client: ⏳ Planned
```

## 💡 How BB84 Works

### The Protocol

1. **Alice prepares** qubits in random bases (Z: |0⟩,|1⟩ or X: |+⟩,|−⟩)
2. **Transmission** through quantum channel (Eve may intercept)
3. **Bob measures** in random bases
4. **Sifting**: Keep ~50% where bases matched
5. **Error check**: Calculate QBER to detect eavesdropping
6. **Key generation**: If secure (QBER < 11%), create final key

### Quantum Security

- **Heisenberg Uncertainty**: Wrong basis → 50% random result
- **No-Cloning Theorem**: Can't copy unknown quantum states
- **Measurement Disturbance**: Eve's measurement changes states
- **Detection**: Errors reveal eavesdropping (QBER > 11%)

## 🧪 Demo Results

### Secure Channel (No Eve)
```
Qubits sent: 1024
After sifting: ~512 (50% efficiency)
QBER: 0.00% ✓
Status: SECURE
Final key: 256 bits generated
```

### With Eavesdropper (50% intercept)
```
Qubits sent: 1024
Eve intercepted: ~512 qubits
After sifting: ~512 (50% efficiency)
QBER: 12.5% ⚠️
Status: EAVESDROPPING DETECTED!
Action: Protocol aborted, key discarded
```

## 📈 QBER vs Intercept Rate

| Eve Intercept | Expected QBER | Detection |
|---------------|---------------|-----------|
| 0%            | 0.0%          | ✓ Secure  |
| 20%           | 5.0%          | ✓ Secure  |
| 40%           | 10.0%         | ✓ Secure  |
| **50%**       | **12.5%**     | **⚠️ Detected** |
| 100%          | 25.0%         | ⚠️ Detected |

## 🛠️ Tech Stack

### Backend
- **Python 3.12**: Core implementation
- **FastAPI**: REST API framework
- **Pydantic**: Data validation
- **pytest**: Unit testing
- **NumPy**: Random number generation

### Frontend
- **React 18**: UI framework
- **Vite**: Build tool
- **Tailwind CSS**: Styling
- **Lucide React**: Icons
- **Recharts**: Data visualization

## 📚 References

- Bennett, C. H., & Brassard, G. (1984). "Quantum cryptography: Public key distribution and coin tossing"
- [Background Presentation](https://www.crowdcast.io/c/g6bsuwfzyxpa)
- Nielsen & Chuang. "Quantum Computation and Quantum Information"

## 🎯 Roadmap

### Phase 1: Core Implementation ✅
- [x] Qubit with Z/X bases
- [x] Eavesdropper simulation
- [x] BB84 protocol (6 steps)
- [x] Unit tests (65+ tests)

### Phase 2: Backend API (In Progress)
- [ ] FastAPI REST endpoints
- [ ] Request/response models
- [ ] Statistics utilities
- [ ] Error handling

### Phase 3: Frontend Dashboard
- [ ] Protocol configuration UI
- [ ] Real-time visualization
- [ ] Statistics display
- [ ] Security alerts
- [ ] Key display (binary/hex)

### Phase 4: Advanced Features
- [ ] Multiple protocol runs comparison
- [ ] Different attack strategies
- [ ] Performance benchmarking
- [ ] Export results (JSON/CSV)

## 🏆 Hackathon Project

**Event**: [Hackathon Name]  
**Timeline**: [Start Date] - [Submission Deadline]  
**Team**: Lucky (University of Wisconsin-Madison)

## 📝 License

MIT License

## 📧 Contact

**Lucky**  
University of Wisconsin-Madison  
Triple Major: Data Science, Computer Science, Mathematics

- GitHub: [Your GitHub]
- Email: [Your Email]
- LinkedIn: [Your LinkedIn]

---

⚛️ **Built with quantum mechanics. Secured by physics.**