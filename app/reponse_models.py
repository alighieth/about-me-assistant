
from pydantic import BaseModel


class AIResponseModel(BaseModel):
    inputTokenUsage: int
    outputTokenUsage: int
    totalTokenUsage: int = 0
    cost: float = 0.0
    model: str
    response: str

