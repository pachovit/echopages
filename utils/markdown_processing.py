import base64
import os
import re


def convert_images_to_base64(text: str, root_dir: str) -> str:
    """Converts all image paths in a given text to base64 data URIs.

    Args:
        text: The text that contains image paths.
        root_dir: The root directory where the images are located.

    Returns:
        The text with all image paths replaced by base64 data URIs.
    """
    # Regular expression to find image paths
    image_pattern = re.compile(r"!\[.*?\]\((.*?)\)")

    # Find all image paths in the text
    matches = image_pattern.findall(text)

    # Replace each image path with the corresponding base64 data URI
    for match in matches:
        image_path = os.path.join(root_dir, match)
        with open(image_path, "rb") as img_file:
            base64_image = base64.b64encode(img_file.read()).decode("utf-8")
            image_data_uri = f"data:image/png;base64,{base64_image}"
            text = text.replace(match, image_data_uri)

    return text
