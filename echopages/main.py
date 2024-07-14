import uvicorn

from echopages import bootstrap
from echopages.application import services
from echopages.infrastructure import samplers, schedulers, web
from echopages.infrastructure.fakes import (
    FakeDigestDeliverySystem,
    FakeDigestRepository,
)

if __name__ == "__main__":
    content_repo = bootstrap.get_content_repo()
    digest_repo = FakeDigestRepository([])
    delivery_system = FakeDigestDeliverySystem()
    content_sampler = samplers.SimpleContentSampler()

    # Configure Scheduler
    scheduler = schedulers.SimpleScheduler(
        lambda: services.delivery_service(
            digest_repo, content_repo, content_sampler, 1, delivery_system
        ),
        time_of_day="14:52",
    )
    scheduler.start()
    uvicorn.run(web.app, host="0.0.0.0", port=8000)
