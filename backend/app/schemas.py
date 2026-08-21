from pydantic import BaseModel, HttpUrl


class AnalyzeRequest(BaseModel):
    url: HttpUrl



class ElementData(BaseModel):

    tag: str
    text: str

    x: float
    y: float

    width: float
    height: float

    attention_score: float
    attention_percentage: float
    attention_rank: int

    is_cta: bool



class UXMetrics(BaseModel):

    cta_visibility: float
    headline_prominence: float
    visual_hierarchy: float
    overall_ux_score: float



class AnalyzeResponse(BaseModel):

    elements: list[ElementData]

    metrics: UXMetrics

    ui_metrics: dict

    findings: list[str]
    
    recommendations: list[str]

    overlay: str