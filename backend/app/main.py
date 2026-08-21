import asyncio
import sys

from fastapi.responses import FileResponse
from ml.saliency import SaliencyAnalyzer

if sys.platform == "win32":
    asyncio.set_event_loop_policy(
        asyncio.WindowsProactorEventLoopPolicy()
    )

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from .schemas import (
    AnalyzeRequest,
    AnalyzeResponse,
)

from app.browser import capture_page

app = FastAPI()
saliency_analyzer = SaliencyAnalyzer()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/analyze", response_model=AnalyzeResponse)
async def analyze_website(request: AnalyzeRequest):
    try:
        loop = asyncio.get_running_loop()

        print("===============")
        print("EVENT LOOP:", type(loop))
        print("LOOP POLICY", type(asyncio.get_event_loop))
        print("WINDOWS:", sys.platform)
        print("===============")
        
        result = await capture_page(str(request.url))

        overlay_path = saliency_analyzer.generate_overlay(
            result["screenshot_path"],
            "data/overlay.png"
        )
        
        return FileResponse(
            overlay_path,
            media_type="image/png"
        )

    except Exception as error:
        print(f"Analysis error: {type(error).__name__}: {error}")

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )