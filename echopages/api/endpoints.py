from datetime import datetime

from fastapi import Depends, FastAPI, status
from pydantic import BaseModel, field_validator

import echopages.config
from echopages import bootstrap
from echopages.application import services
from echopages.domain import model, repositories
from echopages.infrastructure.database import sql
from echopages.infrastructure.delivery import samplers, schedulers
from echopages.infrastructure.delivery.delivery_system import HTMLDigestFormatter

app = FastAPI()


class Content(BaseModel):
    text: str


class AddContentResponse(BaseModel):
    content_id: int


class GetContentResponse(BaseModel):
    text: str


@app.post(
    "/add_content",
    status_code=status.HTTP_201_CREATED,
    response_model=AddContentResponse,
)
async def add_content(
    content: Content,
    uow: repositories.UnitOfWork = Depends(sql.get_unit_of_work),
) -> AddContentResponse:
    # Simulate adding content
    content_id = services.add_content(uow, content.text)
    return AddContentResponse(content_id=content_id)


@app.get("/contents/{content_id}", response_model=GetContentResponse)
async def get_content(
    content_id: int,
    uow: repositories.UnitOfWork = Depends(sql.get_unit_of_work),
) -> GetContentResponse:
    content_str = services.get_content_by_id(uow, content_id)

    if content_str is None:
        text = "Content Not Found"
    else:
        text = content_str
    return GetContentResponse(text=text)


class TriggerDigest(BaseModel):
    n_units: int = 1


class TriggerDigestResponse(BaseModel):
    digest_str: str


@app.post("/trigger_digest")
async def trigger_digest(
    trigger_digest_request: TriggerDigest,
    uow: repositories.UnitOfWork = Depends(sql.get_unit_of_work),
    digest_delivery_system: model.DigestDeliverySystem = Depends(
        bootstrap.get_digest_delivery_system
    ),
) -> TriggerDigestResponse:
    content_sampler = samplers.SimpleContentSampler()
    digest_formatter = HTMLDigestFormatter()

    digest_str = services.delivery_service(
        uow,
        content_sampler,
        trigger_digest_request.n_units,
        digest_formatter,
        digest_delivery_system,
    )

    assert digest_str is not None
    return TriggerDigestResponse(digest_str=digest_str)


class Schedule(BaseModel):
    time_of_day: str

    @field_validator("time_of_day")
    def check_time_format(cls, v: str) -> str:
        datetime.strptime(v, "%H:%M")
        return v


class ConfigureScheduleResponse(BaseModel):
    message: str = "Schedule updated"


@app.post("/configure_schedule")
async def configure_schedule(
    schedule: Schedule,
    uow: repositories.UnitOfWork = Depends(sql.get_unit_of_work),
) -> ConfigureScheduleResponse:
    content_sampler = samplers.SimpleContentSampler()

    scheduler = schedulers.SimpleScheduler(
        lambda: services.generate_digest(
            uow,
            content_sampler,
            echopages.config.NUMBER_OF_UNITS_PER_DIGEST,
        )
    )

    services.configure_schedule(scheduler, schedule.time_of_day)

    return ConfigureScheduleResponse()
