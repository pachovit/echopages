import logging
import os
import uuid
from datetime import datetime
from typing import List

import markdown
from jinja2 import Template
from postmarker.core import PostmarkClient

from echopages.domain import model
from echopages.domain.model import (
    Content,
    DigestContentStr,
    DigestDeliverySystem,
    DigestFormatter,
    DigestRepr,
    DigestTitle,
)

logger = logging.getLogger(__name__)


class HTMLDigestFormatter(DigestFormatter):
    """Converts a list of Content objects into a formatted HTML digest."""

    def _build_title(self, contents: List[Content]) -> str:
        """Builds the title of the digest based on the contents."""
        if not contents:
            return ""

        if len(contents) == 1:
            return f"Daily Digest: {contents[0].source} - {contents[0].location}"

        return "Daily Digest: " + ", ".join([content.source for content in contents])

    def _build_digest_str(self, contents: List[Content]) -> str:
        """Builds the HTML content of the digest."""
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
        now = datetime.now()
        current_date = now.strftime("%B %d, %Y")  # Format: Month Day, Year
        current_year = now.year
        text = template.render(
            contents=contents_to_render,
            current_date=current_date,
            current_year=current_year,
        )
        return text

    def format(self, contents: List[Content]) -> DigestRepr:
        if not contents:
            return DigestRepr(model.DigestTitle(""), model.DigestContentStr(""))

        title = DigestTitle(self._build_title(contents))
        text = DigestContentStr(self._build_digest_str(contents))

        return DigestRepr(title, text)


class PostmarkDigestDeliverySystem(DigestDeliverySystem):
    """Delivers a digest via email using Postmark."""

    def __init__(self, recipient_email: str) -> None:
        """Initializes the delivery system with the recipient's email address."""
        self.recipient_email = recipient_email

    def deliver_digest(self, digest_repr: DigestRepr) -> None:
        """Sends an email to the specified recipient with the provided digest
        content."""

        app_email_address = os.getenv("APP_EMAIL_ADDRESS", "")
        api_token = os.getenv("POSTMARK_SERVER_API_TOKEN", "")

        pm = PostmarkClient(server_token=api_token)
        pm.emails.send(
            From=f"EchoPages <{app_email_address}>",
            To=self.recipient_email,
            Subject=digest_repr.title,
            HtmlBody=digest_repr.contents_str,
        )
        logger.info(f"Sent digest to {self.recipient_email}")


class FileDigestDeliverySystem(DigestDeliverySystem):
    """Delivers a digest to disk as an HTML file."""

    def __init__(self, directory: str) -> None:
        """Initializes the delivery system with the directory to store the digests."""
        self.directory = directory

    def deliver_digest(self, digest_repr: DigestRepr) -> None:
        """Saves the digest to disk as an HTML file."""
        digest_id = uuid.uuid4().hex
        filename = f"digest_{digest_id}.html"
        # Ensure the directory exists
        os.makedirs(self.directory, exist_ok=True)
        file_path = os.path.join(self.directory, filename)
        with open(file_path, "w") as file:
            file.write(digest_repr.contents_str)
