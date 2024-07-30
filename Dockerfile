FROM cimg/python:3.9

# Set working directory
WORKDIR /app

# Copy only the necessary files first for dependency installation
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry config virtualenvs.create false && poetry install --no-dev

# Copy the rest of the application code
COPY echopages echopages

CMD ["poetry", "run", "python3", "-m", "echopages.main"]