from fastapi import Depends, FastAPI, status
from pydantic import BaseModel

from echopages.application import services
from echopages.bootstrap import get_managed_content_repo
from echopages.domain import repositories

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
    content_repo: repositories.ContentRepository = Depends(get_managed_content_repo),
) -> AddContentResponse:
    # Simulate adding content
    content_id = services.add_content(content_repo, content.text)
    return AddContentResponse(content_id=content_id)


@app.get("/contents/{content_id}", response_model=GetContentResponse)
async def get_content(
    content_id: int,
    content_repo: repositories.ContentRepository = Depends(get_managed_content_repo),
) -> GetContentResponse:
    content = content_repo.get_by_id(content_id)
    if content is None:
        text = "Content Not Found"
    else:
        text = content.text
    return GetContentResponse(text=text)


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
