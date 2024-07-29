# Contributing to EchoPages

Thank you for your interest in contributing to EchoPages! We welcome contributions from anyone and everyone.

## Development Practices

### Architecture

Onion Architecture with layers following Domain Driven Design (order from inside-out):
- `domain`: Domain objects, business logic and interfaces
- `application`: Orchestration of domain objects
- `infrastructure`: Lower-level concerns and specific implementations of interfaces
- `api`: Web endpoints with FastAPI

In which an inner layer should never depend in an outer layer. There's an architecture test [here](./tests/test_arch.py) that tests that there's no incorrect mixing of layers.

### BDD

For the main features of the application, we use BDD. The Gherkin features can be found in the [features](./features/) directory, and their corresponding tests (using [pytest-bdd](https://pytest-bdd.readthedocs.io/en/stable/)) in [tests/functional/*.py](./tests/functional).

The reason behind choosing `pytest-bdd` versus `behave`, was to have a centralized way of running tests and evaluating coverage, including the functional tests.

### CI/CD

We try to be as close as possible to trunk-based-development and Continuous Delivery. For that, the main branch has a pipeline with the following steps:
- `test`: Run all tests and mypy
- `build`: Build the docker image and push to [dockerhub](https://hub.docker.com/r/pachovit/echopages)
- `deploy`: to production

## Setting Up for Development

1. **Clone the Repository:**

    ```sh
    git clone https://github.com/pachovit/echopages.git
    cd echopages
    ```

2. **Install Dependencies:**

    ```sh
    poetry install
    ```

3. **Running Tests:**

    ```sh
    make test # Run all tests and mypy
    make functional # Runs only BDD tests of features defined in the `features` directory
    make coverage # Run all tests, compute coverage, and run mypy
    ```

3. **Running the Application locally:**

    ```sh
    make run
    ```
