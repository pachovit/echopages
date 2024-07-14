from datetime import datetime
from typing import List

from fastapi import Depends, FastAPI, status
from pydantic import BaseModel, field_validator

import echopages.config
from echopages.application import services
from echopages.domain import repositories
from echopages.infrastructure import samplers, schedulers, sql
from echopages.infrastructure.fakes import FakeDigestDeliverySystem

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
    content = services.get_content_by_id(unit_of_work=uow, content_id=content_id)

    if content is None:
        text = "Content Not Found"
    else:
        text = content.text
    return GetContentResponse(text=text)


class TriggerDigest(BaseModel):
    n_units: int = 1


class TriggerDigestResponse(BaseModel):
    digest: List[str]


@app.post("/trigger_digest")
async def trigger_digest(
    trigger_digest_request: TriggerDigest,
    uow: repositories.UnitOfWork = Depends(sql.get_unit_of_work),
) -> TriggerDigestResponse:
    content_sampler = samplers.SimpleContentSampler()
    digest_delivery_system = FakeDigestDeliverySystem()

    digest = services.delivery_service(
        uow, content_sampler, trigger_digest_request.n_units, digest_delivery_system
    )

    return TriggerDigestResponse(digest=[content.text for content in digest.contents])


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
    content_repo: repositories.ContentRepository = Depends(
        sql.get_managed_content_repo
    ),
    digest_repo: repositories.DigestRepository = Depends(sql.get_managed_digest_repo),
) -> ConfigureScheduleResponse:
    content_sampler = samplers.SimpleContentSampler()

    scheduler = schedulers.SimpleScheduler(
        lambda: services.generate_digest(
            digest_repo,
            content_repo,
            content_sampler,
            echopages.config.NUMBER_OF_UNITS_PER_DIGEST,
        )
    )

    services.configure_schedule(scheduler, schedule.time_of_day)

    return ConfigureScheduleResponse()
