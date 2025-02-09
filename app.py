from fastapi import FastAPI
from fastapi.responses import JSONResponse
import os
import re
import requests
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI()

# Configure CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change this for security)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


@app.post("/run")
async def execute(task: str):
    """Execute a task and return the result"""
    
    print(f"Executing task: {task}")

    return {"result": task}


@app.get("/read")
async def read(path: str):
    """Read a file and return its contents"""
    
    print(f"Reading file: {path}")

    x = os.path.join(os.getcwd(),'./', path)

    return {"content": open(x).read()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)