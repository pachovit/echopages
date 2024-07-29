<p align="center">
  <img src="https://github.com/pachovit/echopages/blob/main/.resources/logo_slogan.png" width="800"/>
</p>

---

# EchoPages

[![CI](https://img.shields.io/github/actions/workflow/status/pachovit/echopages/ci.yml)](https://github.com/pachovit/echopages/actions)
[![license](https://img.shields.io/github/license/pachovit/echopages)](https://github.com/pachovit/echopages/blob/main/LICENSE)
![issues](https://img.shields.io/github/issues/pachovit/echopages)
![stars](https://img.shields.io/github/stars/pachovit/echopages)
![forks](https://img.shields.io/github/forks/pachovit/echopages)

EchoPages is a service designed to provide users with scheduled digests of their chosen content, such as summaries of book chapters or articles. Inspired by services like [Readwise](https://readwise.io/), EchoPages enhances the reading and learning experience by sending personalized content snippets on a predefined schedule, ensuring continuous engagement and retention.

## Why Choose EchoPages?

- **Self-Managed Content**: EchoPages allows you to carefully manage your content. Whether it's a detailed summary of a book chapter or brief quotes, you have the flexibility to add any content that matters to you.
- **Customizable Delivery**: Configure EchoPages to deliver content that suits your needs. Receive a daily summary of a book chapter, or several smaller snippets, depending on your preference.
- **Free and Open Source**: EchoPages is free to use and fully open-source. You can self-host it and take complete control over your data and usage.

## Getting Started

### Prerequisites

- Docker
- Docker Compose
- Git
- A [Postmark](https://postmarkapp.com/) account, and a Postmark API token

### Installation

1. **Clone the Repository:**

  ```sh
  git clone https://github.com/pachovit/echopages.git
  cd echopages
  ```

2. **Setup Environment Variables:**

  Create a `.env` file in the root directory. You can take as reference the [example env file](example.env). Adjust the values as needed, and make sure to specify the following variables:

  - `TZ`: Timezone where your system runs. E.g. `Europe/Berlin`.
  - `NUMBER_OF_UNITS_PER_DIGEST`: How many content units you want to receive every digest.
  - `DAILY_TIME_OF_DIGEST`: What time of the day you want to receive your daily digest. In format `"HH:MM"`.
  - `RECIPIENT_EMAIL`: Where do you want to receive your digests.
  - `APP_EMAIL_ADDRESS`: Email address that is used to send the digests.
  - `POSTMARK_SERVER_API_TOKEN`: Postmark API token used to send the emails.

3. **Run with Docker Compose:**

  ```sh
  docker-compose --env-file /path/to/your/file.env up -d
  ```

4. **Access the Application:**

  The application will be available at `http://localhost:8000`.

### Usage

1. **Add Content:**

  Use the `/add_content` endpoint to add new content. You can do this via an HTTP client like curl or Postman:

  ```sh
  curl -X POST "http://localhost:8000/add_content" -H "Content-Type: application/json" -d '{"source": "Book Name", "author": "One Author", "location": "Chapter 1", "text": "some long markdown summary"}'
  ```

  The `text` is assumed to be in markdown format. In case you want to add content with images, they will need to be base64-encoded. For example for the following markdown file:

  ```
    # Some Nice Book Chapter Summary
    
    # Topic 1
    * Key point 1: Description of the point
    * Key point 2: Description of the other point
    ![nice-image.png](./path/to/nice-image.png)
    
    # Topic 2
    * Key point 1: Another nice thing
    * Key point 2: Yet another thing
  ```

  You'll have to convert the image to embed it (you can find an utility function to do this in [this file](utils/markdown_processing.py)):
  ```
  
    # Some Nice Book Chapter Summary
    
    # Topic 1
    * Key point 1: Description of the point
    * Key point 2: Description of the other point
    ![nice-image.png](data:image/png;base64,<base64-encoded-image>)
    
    # Topic 2
    * Key point 1: Another nice thing
    * Key point 2: Yet another thing
  ```
  
2. **Receive Digest:**

  The application will automatically send out digests based on your configured schedule.

## Contributing

We welcome contributions! Please read our [Contributing Guidelines](CONTRIBUTING.md) for more details.

## License

EchoPages is open-sourced software licensed under the [GPL-3.0 license](LICENSE).