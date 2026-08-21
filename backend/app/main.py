import asyncio
import sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(
        asyncio.WindowsProactorEventLoopPolicy()
    )


from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .schemas import (
    AnalyzeRequest,
    AnalyzeResponse,
)

from app.browser import capture_page

from ml.saliency import SaliencyAnalyzer

from ml.analysis import (
    calculate_element_attention,
    normalize_attention_scores,
    rank_elements,
    detect_cta_elements,
    generate_ux_metrics,
    generate_recommendations,
)


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


@app.post(
    "/api/analyze",
    response_model=AnalyzeResponse
)
async def analyze_website(
    request: AnalyzeRequest
):

    try:

        print("===============")
        print("Starting analysis")
        print("===============")


        # 1. Capture webpage

        result = await capture_page(
            str(request.url)
        )


        screenshot_path = result[
            "screenshot_path"
        ]

        elements = result[
            "elements"
        ]


        # 2. Generate saliency map + overlay

        saliency_map = (
            saliency_analyzer.generate_saliency(
                result["screenshot_path"]
            )
        )


        overlay_path = (
            saliency_analyzer.generate_overlay(
                result["screenshot_path"],
                saliency_map,
                "data/overlay.png"
            )
        )


        # 3. Analyze DOM elements

        elements = calculate_element_attention(
            saliency_map,
            elements
        )


        elements = normalize_attention_scores(
            elements
        )


        elements = rank_elements(
            elements
        )


        elements = detect_cta_elements(
            elements
        )


        # 4. Generate UX metrics

        metrics = generate_ux_metrics(
            elements
        )


        # 5. Generate recommendations

        recommendations = (
            generate_recommendations(
                metrics
            )
        )


        return {

            "elements": elements,

            "metrics": metrics,

            "recommendations": recommendations,

            "overlay": overlay_path

        }


    except Exception as error:

        print(
            f"Analysis error: {type(error).__name__}: {error}"
        )

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )