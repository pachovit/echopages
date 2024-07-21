import logging
import os
import uuid

from jinja2 import Template

from echopages.domain.model import Digest, DigestDeliverySystem, DigestFormatter

logger = logging.getLogger(__name__)


class HTMLDigestFormatter(DigestFormatter):
    def format(self, digest: Digest) -> str:
        if not digest.contents:
            return ""

        template_str = open(
            "echopages/infrastructure/templates/digest_template.html"
        ).read()
        template = Template(template_str)
        return template.render(digest=digest)


# class PostmarkDigestDeliverySystem(DigestDeliverySystem):
#     def __init__(self, recipient_email: str) -> None:
#         self.recipient_email = recipient_email

#     def deliver_digest(self, digest_str: str) -> None:
#         """Sends an email to the specified recipient with the provided digest
#         content."""

#         app_email_address = os.getenv("APP_EMAIL_ADDRESS")
#         api_token = os.getenv("POSTMARK_SERVER_API_TOKEN")

#         pm = PostmarkClient(server_token=api_token)
#         pm.emails.send(
#             From=app_email_address,
#             To=self.recipient_email,
#             Subject="EchoPages Digest",
#             HtmlBody=digest_str,
#         )


class DiskDigestDeliverySystem(DigestDeliverySystem):
    def __init__(self, directory: str) -> None:
        self.directory = directory

    def deliver_digest(self, digest_str: str) -> None:
        digest_id = uuid.uuid4().hex
        filename = f"digest_{digest_id}.html"
        # Ensure the directory exists
        os.makedirs(self.directory, exist_ok=True)
        file_path = os.path.join(self.directory, filename)
        with open(file_path, "w") as file:
            file.write(digest_str)
