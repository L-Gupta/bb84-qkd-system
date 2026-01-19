# BB84 Quantum Key Distribution - Deployment Guide

Complete guide for deploying the BB84 QKD system in different environments.

## 📋 Prerequisites

### System Requirements
- **Python**: 3.8+ (for backend)
- **Node.js**: 14+ (for frontend)
- **RAM**: 2GB minimum
- **Disk**: 500MB for dependencies
- **OS**: Windows, macOS, or Linux

### Development Machine Setup

```bash
# Check Python version
python --version  # Should be 3.8+

# Check Node.js version
node --version    # Should be 14+
npm --version     # Should be 6+
```

---

## 🚀 Local Development Deployment

### Quick Start (5 minutes)

#### 1. Clone/Navigate to Project

```bash
cd quantum/
```

#### 2. Start Backend

```bash
# Navigate to backend
cd backend/

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start server
python main.py
```

Backend runs on: `http://localhost:8000`

#### 3. Start Frontend (new terminal)

```bash
# Navigate to frontend
cd frontend/

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend runs on: `http://localhost:3000`

#### 4. Access Application

- **Application**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health

---

## 🐳 Docker Deployment

### Prerequisites
- Docker Desktop installed
- Docker Compose (usually bundled)

### Dockerfile for Backend

Create `backend/Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/api/health')"

# Run application
CMD ["python", "main.py"]
```

### Dockerfile for Frontend

Create `frontend/Dockerfile`:

```dockerfile
FROM node:18-alpine as builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source
COPY . .

# Build
RUN npm run build

# Production stage
FROM node:18-alpine

WORKDIR /app

# Install serve to run the app
RUN npm install -g serve

# Copy built files from builder
COPY --from=builder /app/dist ./dist

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost:3000 || exit 1

# Run
CMD ["serve", "-s", "dist", "-l", "3000"]
```

### docker-compose.yml

Create `docker-compose.yml` at project root:

```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - PYTHONUNBUFFERED=1
    networks:
      - qkd-network
    volumes:
      - ./backend:/app
    restart: unless-stopped

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    depends_on:
      - backend
    networks:
      - qkd-network
    environment:
      - VITE_API_URL=http://backend:8000/api
    restart: unless-stopped

networks:
  qkd-network:
    driver: bridge
```

### Deploy with Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild images
docker-compose up -d --build
```

---

## ☁️ Cloud Deployment

### Heroku Deployment

#### Backend to Heroku

```bash
cd backend/

# Login to Heroku
heroku login

# Create app
heroku create your-bb84-api

# Set Python buildpack
heroku buildpacks:set heroku/python

# Create Procfile
echo "web: uvicorn main:app --host=0.0.0.0 --port=${PORT:-8000}" > Procfile

# Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main

# View logs
heroku logs --tail
```

#### Frontend to Vercel/Netlify

**Using Vercel:**

```bash
cd frontend/

# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Production deployment
vercel --prod
```

**Environment Variables:**
```
VITE_API_URL=https://your-bb84-api.herokuapp.com/api
```

### AWS Deployment

#### Using EC2

```bash
# SSH into instance
ssh -i your-key.pem ec2-user@your-instance-ip

# Install dependencies
sudo yum update
sudo yum install python3 nodejs npm

# Clone repo
git clone https://github.com/yourname/bb84-qkd.git
cd bb84-qkd/

# Backend setup
cd backend/
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
nohup python main.py > api.log 2>&1 &

# Frontend setup
cd ../frontend
npm install
npm run build
sudo npm install -g serve
nohup serve -s dist -l 3000 > frontend.log 2>&1 &
```

#### Using Lambda (Serverless)

Not ideal for this project due to long-running processes.

---

## 🔧 Production Deployment Checklist

### Backend

- [ ] Use production ASGI server (Gunicorn)
- [ ] Enable CORS properly
- [ ] Use environment variables for secrets
- [ ] Set up logging
- [ ] Configure error tracking (Sentry)
- [ ] Enable rate limiting
- [ ] Use HTTPS/SSL
- [ ] Set up monitoring
- [ ] Configure auto-restart on failure
- [ ] Set up backup strategy

### Frontend

- [ ] Build optimized bundle (`npm run build`)
- [ ] Use CDN for static assets
- [ ] Enable gzip compression
- [ ] Set cache headers
- [ ] Use HTTPS/SSL
- [ ] Configure error tracking
- [ ] Set up monitoring
- [ ] Enable service worker (PWA)
- [ ] Test in multiple browsers

### General

- [ ] Set up CI/CD pipeline
- [ ] Configure automated tests
- [ ] Set up staging environment
- [ ] Document deployment process
- [ ] Set up monitoring and alerts
- [ ] Plan for scalability
- [ ] Set up security scanning

---

## 📊 Performance Optimization

### Backend

```python
# Use connection pooling
# Implement caching
# Use async handlers
# Optimize database queries
# Profile with cProfile
```

### Frontend

```bash
# Analyze bundle
npm run build -- --analyze

# Optimize images
npm install -g imagemin-cli
imagemin src/assets/* --out-dir=dist/assets

# Enable gzip
npm install compression
```

---

## 🔒 Security Hardening

### Backend

```python
# environment.py
import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = os.getenv("DEBUG", "False") == "True"
SECRET_KEY = os.getenv("SECRET_KEY")
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost").split(",")

# CORS settings
CORS_ALLOWED_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
```

### Frontend

```javascript
// Sanitize user input
import DOMPurify from 'dompurify';

const clean = DOMPurify.sanitize(userInput);
```

### General

- [ ] Use HTTPS everywhere
- [ ] Keep dependencies updated
- [ ] Use strong passwords
- [ ] Implement rate limiting
- [ ] Set security headers
- [ ] Use environment variables
- [ ] Never commit secrets
- [ ] Use firewalls
- [ ] Enable logging and monitoring

---

## 📈 Monitoring & Maintenance

### Health Checks

```bash
# Check backend health
curl http://localhost:8000/api/health

# Monitor endpoint response times
# Use tools like New Relic, DataDog, or CloudWatch
```

### Logging

```python
# Backend logging
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Protocol executed successfully")
logger.error("Protocol execution failed", exc_info=True)
```

### Metrics to Monitor

- API response time
- Error rate
- QBER values
- Protocol execution success rate
- Resource usage (CPU, memory)
- Database connections
- User activity

---

## 🔄 Continuous Integration/Deployment

### GitHub Actions Example

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run backend tests
        run: |
          cd backend/
          pip install -r requirements.txt
          pytest tests/ -v
      
      - name: Run frontend tests
        run: |
          cd frontend/
          npm install
          npm run build

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to production
        run: |
          # Your deployment script here
          echo "Deploying to production..."
```

---

## 🆘 Troubleshooting

### Backend Won't Start

```bash
# Check if port is in use
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill process
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows

# Check logs for errors
tail -f api.log
```

### Frontend Can't Connect to Backend

```bash
# Check CORS headers
curl -i http://localhost:8000/api/health

# Check VITE_API_URL
echo $VITE_API_URL

# Clear browser cache
# Ctrl+Shift+Delete or Cmd+Shift+Delete
```

### High CPU/Memory Usage

```bash
# Profile application
python -m cProfile -s cumulative main.py

# Check for memory leaks
pip install memory-profiler
python -m memory_profiler main.py
```

---

## 📞 Support

- **Issues**: GitHub Issues
- **Documentation**: See PROTOCOL.md and API.md
- **Contact**: Submit issues on GitHub

---

## 📝 License

MIT License - See LICENSE file
