
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as api_router

app = FastAPI(
    title="Instagram Downloader API",
    description="API for downloading Instagram Videos and Reels",
    version="0.1.0"
)

# CORS Configuration
# Allow all origins for development, restrict in production
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app.include_router(api_router, prefix="/api")

# Mount static files
app.mount("/static", StaticFiles(directory="../frontend"), name="static")

@app.get("/")
async def read_index():
    return FileResponse("../frontend/index.html")

# Serve other static assets if needed directly or via /static
@app.get("/styles.css")
async def read_css():
    return FileResponse("../frontend/styles.css")

@app.get("/app.js")
async def read_js():
    return FileResponse("../frontend/app.js")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
