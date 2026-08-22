from fastapi import APIRouter, Depends, Request

from src.api.schemas.financial_message import (
    FinancialMessageRequest,
    FinancialMessageResponse,
)
from src.bootstrap.factory import build_application

from src.bootstrap.container import (
    ApplicationContainer,
)

from src.persistence.session import get_db_session
from src.observability.logger import logger


router = APIRouter(
    prefix="/financial",
    tags=["Financial"],
)


def get_container(
    db=Depends(get_db_session),
) -> ApplicationContainer:
    return build_application(db)


@router.post(
    "/messages",
    response_model=FinancialMessageResponse,
)
def process_financial_message(
    request: Request,
    data: FinancialMessageRequest,
    container: ApplicationContainer = Depends(get_container),
) -> FinancialMessageResponse:

    request_id = request.state.request_id

    logger.info(
        "Financial message processing started | request_id=%s",
        request_id,
    )

    response = container.financial_flow.process_message(
        external_user_id=data.external_user_id,
        message=data.message,
    )

    logger.info(
        "Financial message processing completed | request_id=%s",
        request_id,
    )

    return FinancialMessageResponse(
        response=response,
    )