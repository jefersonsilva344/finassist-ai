from pydantic import BaseModel, Field


class FinancialMessageRequest(BaseModel):
    external_user_id: str = Field(min_length=1)
    message: str = Field(min_length=1)


class FinancialMessageResponse(BaseModel):
    response: str