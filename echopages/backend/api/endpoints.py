from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

import echopages.backend.config
from echopages.backend import bootstrap
from echopages.backend.application import services
from echopages.backend.domain import model, repositories

api_router = APIRouter(prefix="/api")


class AddContentRequest(BaseModel):
    source: str = Field(
        "",
        description="The source of the content.",
        examples=["Book Name", "Article Title"],
    )
    author: str = Field(
        "", description="The author of the content.", examples=["Sample Author"]
    )
    location: str = Field(
        "",
        description="The location of the content.",
        examples=["Chapter 1", "Section 1.1", "Page 75"],
    )
    text: str = Field(
        "",
        description="The text of the content.",
        examples=["Some long *markdown* summary."],
    )


class AddContentResponse(BaseModel):
    content_id: int


class GetContentResponse(BaseModel):
    source: str
    author: str
    location: str
    text: str


@api_router.post(
    "/add_content",
    status_code=status.HTTP_201_CREATED,
    response_model=AddContentResponse,
    summary="Add new content",
)
async def add_content(
    content: AddContentRequest,
    uow: repositories.UnitOfWork = Depends(bootstrap.get_unit_of_work),
) -> AddContentResponse:
    if not content.text:
        raise HTTPException(status_code=400, detail="Text is required")

    content_id = services.add_content(uow, content.__dict__)
    return AddContentResponse(content_id=content_id)


@api_router.get(
    "/contents/{content_id}",
    response_model=GetContentResponse,
    summary="Get content by ID",
)
async def get_content(
    content_id: int,
    uow: repositories.UnitOfWork = Depends(bootstrap.get_unit_of_work),
) -> GetContentResponse:
    content_data = services.get_content_by_id(uow, content_id)

    if content_data is None:
        raise HTTPException(status_code=404, detail="Content Not Found")
    else:
        return GetContentResponse(**content_data)


class TriggerDigest(BaseModel):
    n_units: int = Field(1, description="The number of units to include in the digest.")


class TriggerDigestResponse(BaseModel):
    digest_title: str
    digest_content_str: str


@api_router.post(
    "/trigger_digest",
    response_model=TriggerDigestResponse,
    summary="Trigger a digest generation and delivery",
)
async def trigger_digest(
    trigger_digest_request: TriggerDigest,
    uow: repositories.UnitOfWork = Depends(bootstrap.get_unit_of_work),
    digest_delivery_system: model.DigestDeliverySystem = Depends(
        bootstrap.get_digest_delivery_system
    ),
) -> TriggerDigestResponse:
    content_sampler = bootstrap.get_sampler()
    digest_formatter = bootstrap.get_digest_formatter()

    digest_title, digest_content_str = services.delivery_service(
        uow,
        content_sampler,
        digest_formatter,
        digest_delivery_system,
    )

    return TriggerDigestResponse(
        digest_title=digest_title, digest_content_str=digest_content_str
    )


class DigestConfig(BaseModel):
    number_of_units_per_digest: int = Field(
        1, description="The number of units to include in the digest."
    )
    daily_time_of_digest: str = Field(
        "07:00",
        description="Time of day to send the daily digest, in the format HH:MM.",
    )


@api_router.get(
    "/get_config",
    response_model=DigestConfig,
    summary="Get current digest configuration.",
)
async def get_config() -> DigestConfig:
    config = echopages.backend.config.get_config()
    return DigestConfig(**config.model_dump())


@api_router.post(
    "/set_config",
    status_code=status.HTTP_201_CREATED,
    summary="Update the digest configuration",
)
async def set_config(
    requested_config: DigestConfig,
) -> None:
    scheduler = bootstrap.get_scheduler()

    number_of_units_per_digest = requested_config.number_of_units_per_digest
    daily_time_of_digest = requested_config.daily_time_of_digest

    services.update_digest_config(
        scheduler, number_of_units_per_digest, daily_time_of_digest
    )

    return None
