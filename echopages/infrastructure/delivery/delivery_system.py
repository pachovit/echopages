import logging
import os
import uuid
from typing import List

import markdown
from jinja2 import Template
from postmarker.core import PostmarkClient

from echopages.domain.model import Content, DigestDeliverySystem, DigestFormatter

logger = logging.getLogger(__name__)


class HTMLDigestFormatter(DigestFormatter):
    def format(self, contents: List[Content]) -> str:
        if not contents:
            return ""

        template_str = open(
            "echopages/infrastructure/templates/digest_template.html"
        ).read()
        template = Template(template_str)

        contents_to_render = [
            {
                "source": content.source,
                "author": content.author,
                "location": content.location,
                "html_text": markdown.markdown(content.text),
            }
            for content in contents
        ]

        return template.render(contents=contents_to_render)


class PostmarkDigestDeliverySystem(DigestDeliverySystem):
    def __init__(self, recipient_email: str) -> None:
        self.recipient_email = recipient_email

    def deliver_digest(self, digest_str: str) -> None:
        """Sends an email to the specified recipient with the provided digest
        content."""

        app_email_address = os.getenv("APP_EMAIL_ADDRESS")
        api_token = os.getenv("POSTMARK_SERVER_API_TOKEN")

        pm = PostmarkClient(server_token=api_token)
        pm.emails.send(
            From=app_email_address,
            To=self.recipient_email,
            Subject="EchoPages Digest",
            HtmlBody=digest_str,
        )


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
