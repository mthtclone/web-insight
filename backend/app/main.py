import asyncio
import sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(
        asyncio.WindowsProactorEventLoopPolicy()
    )

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel, HttpUrl


from app.browser import capture_page

app = FastAPI()

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


class AnalyzeRequest(BaseModel):
    url: HttpUrl

@app.post("/api/analyze")
async def analyze_website(request: AnalyzeRequest):
    try:
        loop = asyncio.get_running_loop()

        print("===============")
        print("EVENT LOOP:", type(loop))
        print("LOOP POLICY", type(asyncio.get_event_loop))
        print("WINDOWS:", sys.platform)
        print("===============")
        
        result = await capture_page(str(request.url))

        return result

    except Exception as error:
        print(f"Analysis error: {type(error).__name__}: {error}")

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )