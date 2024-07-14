from fastapi import FastAPI, status
from pydantic import BaseModel

from echopages.application import services
from echopages.bootstrap import get_content_repo

app = FastAPI()


class Content(BaseModel):
    text: str


class AddContentResponse(BaseModel):
    content_unit_id: int


class GetContentUnitResponse(BaseModel):
    text: str


@app.post(
    "/add_content",
    status_code=status.HTTP_201_CREATED,
    response_model=AddContentResponse,
)
async def add_content(
    content: Content,
):
    # Simulate adding content
    content_repo = get_content_repo()
    content_unit_id = services.add_content(content_repo, content.text)
    return AddContentResponse(content_unit_id=content_unit_id)


@app.get("/content_units/{content_unit_id}", response_model=GetContentUnitResponse)
async def get_content_unit(
    content_unit_id: str,
):
    content_repo = get_content_repo()
    content_unit = content_repo.get_by_id(content_unit_id)

    return (
        GetContentUnitResponse(text=content_unit.text)
        if content_unit
        else {"error": f"Content unit with id {content_unit_id} not found"}
    )


# class Schedule(BaseModel):
#     time_of_day: str = Field(
#         ...,
#         regex=r"^([01]\d|2[0-3]):([0-5]\d)$",  # regex for HH:MM format
#         example="12:30",
#     )

# @app.post("/configure_schedule")
# async def configure_schedule(schedule: Schedule):
#     digest_repo = repositories.DigestRepository([])
#     content_repo = repositories.ContentRepository([])
#     content_sampler = samplers.SimpleContentSampler()
#     number_of_units = config.NUMBER_OF_UNITS_PER_DIGEST
#     scheduler = schedulers.SimpleScheduler(
#         services.generate_digest(
#             digest_repo, content_repo, content_sampler, number_of_units
#         )
#     )
#     services.configure_schedule(scheduler, schedule.time_of_day)
#     scheduler.update_schedule(schedule.time_of_day)
#     return {"message": "Schedule updated"}
