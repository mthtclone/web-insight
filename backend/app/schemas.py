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


class AnalyzeResponse(BaseModel):
    screenshot: str
    html: str
    elements: list[ElementData]