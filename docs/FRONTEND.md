# BB84 Quantum Key Distribution - Frontend

Interactive React web dashboard for the BB84 Quantum Key Distribution protocol simulator.

## 🎨 Features

- **Real-time Protocol Visualization**: Configure and execute BB84 protocol
- **Interactive Controls**: Adjust key length, eavesdropper settings
- **Live Statistics**: View transmission metrics, sifting efficiency, QBER
- **Security Alerts**: Visual indicators for eavesdropping detection
- **Key Display**: View generated keys in binary and hexadecimal formats
- **Backend Integration**: Health checks and error handling

## 🏗️ Project Structure

```
src/
├── components/
│   ├── Controls.jsx         # Protocol configuration controls
│   ├── Statistics.jsx       # Transmission statistics display
│   ├── ErrorRate.jsx        # Security status and QBER
│   ├── Dashboard.jsx        # Performance metrics
│   ├── SecretKey.jsx        # Final key display
│   └── ProtocolInfo.jsx     # Protocol explanation
├── services/
│   └── api.js               # Backend API client
├── App.jsx                  # Main application component
├── main.jsx                 # Entry point
├── index.css                # Global styles
└── App.css                  # Component styles

public/                       # Static assets
```

## 🚀 Getting Started

### Prerequisites
- Node.js 14+
- npm or yarn
- Backend running on `http://localhost:8000`

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

The application will open at `http://localhost:3000` with hot module reloading (HMR).

### Build for Production

```bash
# Build optimized bundle
npm run build

# Preview production build
npm run preview
```

## 🔌 API Integration

The frontend communicates with the FastAPI backend via:

**Base URL**: `http://localhost:8000/api` (configurable via `.env.local`)

**Key Endpoints**:
- `GET /health` - Backend health check
- `POST /protocol/execute` - Execute BB84 protocol

**Environment Variables** (`.env.local`):
```
VITE_API_URL=http://localhost:8000/api
```

## 🎯 Component Architecture

### Controls
- Key length configuration (64-512 bits)
- Eavesdropper toggle
- Interception rate slider
- Execute button with loading state
- Error display

### Statistics
- Transmitted qubits count
- Sifted bits after basis comparison
- Final key length
- Sifting efficiency percentage

### ErrorRate
- Quantum Bit Error Rate (QBER) display
- Errors found vs. bits checked
- Security status indicator
- Eavesdropping detection

### Dashboard
- Efficiency score (0-100)
- Mutual information metric
- Execution time in milliseconds
- Protocol version indicator

### SecretKey
- Binary format display
- Hexadecimal format display
- Key length
- Balance percentage
- Quality indicator

### ProtocolInfo
- 6-step BB84 protocol explanation
- Security mechanism description

## 📦 Dependencies

### Core
- **react**: UI framework
- **react-dom**: DOM rendering

### UI & Styling
- **tailwindcss**: Utility-first CSS
- **lucide-react**: Icon library

### API & State
- **axios**: HTTP client

### Build & Development
- **vite**: Fast build tool
- **@vitejs/plugin-react**: React support for Vite

## 🔄 State Management

The app uses React hooks for state:
- `keyLength`: Desired final key length
- `withEve`: Enable eavesdropper simulation
- `eveRate`: Eavesdropper intercept rate
- `result`: Protocol execution result
- `loading`: Execution progress state
- `error`: Error messages
- `backendReady`: Backend connectivity status

## 🛠️ Development

### Adding New Components

Create a new component in `src/components/`:

```jsx
import React from 'react';

export default function MyComponent({ prop }) {
  return (
    <div>
      {/* Component JSX */}
    </div>
  );
}
```

Import and use in `App.jsx`.

### Styling

Uses **Tailwind CSS** utility classes. Customize in `tailwind.config.js`.

### API Calls

Use the `api` service from `src/services/api.js`:

```javascript
import api from './services/api';

const result = await api.executeProtocol(config);
const health = await api.healthCheck();
```

## 📊 Available Scripts

```bash
npm run dev      # Start development server
npm run build    # Build for production
npm run preview  # Preview production build
npm run lint     # Run ESLint (if configured)
```

## 🐛 Troubleshooting

### Backend Not Connecting
- Ensure backend is running on `http://localhost:8000`
- Check `.env.local` has correct `VITE_API_URL`
- Browser console will show connection errors

### Components Not Rendering
- Check browser console for React errors
- Verify props are passed correctly from `App.jsx`
- Ensure component files export default function

### Styling Issues
- Rebuild Tailwind with `npm run dev`
- Clear browser cache (Ctrl+Shift+Delete)
- Check CSS specificity in custom styles

## 📚 Learn More

- [React Documentation](https://react.dev)
- [Vite Guide](https://vitejs.dev/guide/)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [Axios Documentation](https://axios-http.com/)

## 📝 License

MIT License - See root [LICENSE](../LICENSE) file

