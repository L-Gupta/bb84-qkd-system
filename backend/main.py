"""
FastAPI application entry point for BB84 QKD System.

Main application that serves the BB84 quantum key distribution API.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
import uvicorn

from api.routes import router

# Create FastAPI app
app = FastAPI(
    title="BB84 Quantum Key Distribution API",
    description="""
    Complete implementation of the BB84 Quantum Key Distribution protocol.
    
    ## Features
    
    * **Execute Protocol**: Run BB84 with configurable parameters
    * **Eavesdropper Simulation**: Test security with simulated attacks
    * **Batch Execution**: Run multiple protocol instances
    * **Security Analysis**: Analyze QBER and detect eavesdropping
    * **Statistics**: Comprehensive metrics and performance analysis
    
    ## Security
    
    The protocol automatically detects eavesdropping when QBER exceeds 11%.
    Any intercepted communication will create detectable quantum disturbances.
    
    ## Documentation
    
    - Interactive API docs: `/docs`
    - Alternative docs: `/redoc`
    - Health check: `/health`
    """,
    version="1.0.0",
    contact={
        "name": "Lucky",
        "email": "your.email@example.com",
        "url": "https://github.com/L-Gupta/bb84-qkd-system"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    }
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React default
        "http://localhost:5173",  # Vite default
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router)


# Root endpoint - redirect to docs
@app.get("/", include_in_schema=False)
async def root():
    """Redirect root to API documentation."""
    return RedirectResponse(url="/docs")


# Startup event
@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    print("=" * 70)
    print("🔐 BB84 Quantum Key Distribution API")
    print("=" * 70)
    print("✅ Core components initialized")
    print("✅ API routes registered")
    print("✅ CORS configured")
    print("\n📚 Documentation available at:")
    print("   • Interactive: http://localhost:8000/docs")
    print("   • Alternative: http://localhost:8000/redoc")
    print("\n🔍 Health check: http://localhost:8000/api/health")
    print("\n🚀 Ready to distribute quantum keys!")
    print("=" * 70)


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    print("\n" + "=" * 70)
    print("🛑 Shutting down BB84 API...")
    print("=" * 70)


# Run with uvicorn
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )