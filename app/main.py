from fastapi import FastAPI
import webbrowser
import uvicorn
import sys
import os

# Add the parent directory to sys.path so we can import the app module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.api import desktop

app = FastAPI(
    title="🖥️ Desktop MCP",
    description="An MCP for desktop operations",
    version="0.0.1",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.include_router(desktop.router)

if __name__ == "__main__":
    try:
        web_mode = "--web" in sys.argv

        if web_mode:
            print("🌐 Starting in web mode...")
            webbrowser.open("http://localhost:8000/docs")
            uvicorn.run("app.main:app", host="localhost", port=8000, reload=True)
        else:
            print("Starting in MCP mode...")
            from fastmcp import FastMCP

            mcp = FastMCP.from_fastapi(app)
            mcp.run()
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        import traceback

        traceback.print_exc()