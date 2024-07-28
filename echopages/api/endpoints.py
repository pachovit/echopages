from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, field_validator

import echopages.config
from echopages import bootstrap
from echopages.application import services
from echopages.domain import model, repositories
from echopages.infrastructure.delivery import schedulers

app = FastAPI()


class AddContentRequest(BaseModel):
    source: str = ""
    author: str = ""
    location: str = ""
    text: str = ""


class AddContentResponse(BaseModel):
    content_id: int


class GetContentResponse(BaseModel):
    source: str
    author: str
    location: str
    text: str


@app.post(
    "/add_content",
    status_code=status.HTTP_201_CREATED,
    response_model=AddContentResponse,
)
async def add_content(
    content: AddContentRequest,
    uow: repositories.UnitOfWork = Depends(bootstrap.get_unit_of_work),
) -> AddContentResponse:
    if not content.text:
        raise HTTPException(status_code=400, detail="Text is required")

    content_id = services.add_content(uow, content.__dict__)
    return AddContentResponse(content_id=content_id)


@app.get("/contents/{content_id}", response_model=GetContentResponse)
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
    n_units: int = 1


class TriggerDigestResponse(BaseModel):
    digest_title: str
    digest_content_str: str


@app.post("/trigger_digest")
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
        trigger_digest_request.n_units,
        digest_formatter,
        digest_delivery_system,
    )

    return TriggerDigestResponse(
        digest_title=digest_title, digest_content_str=digest_content_str
    )


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
    uow: repositories.UnitOfWork = Depends(bootstrap.get_unit_of_work),
) -> ConfigureScheduleResponse:
    content_sampler = bootstrap.get_sampler()
    config = echopages.config.get_config()
    scheduler = schedulers.SimpleScheduler(
        lambda: services.generate_digest(
            uow,
            content_sampler,
            config.number_of_units_per_digest,
        )
    )

    services.configure_schedule(scheduler, schedule.time_of_day)

    return ConfigureScheduleResponse()
