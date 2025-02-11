# FastAPI Demo Project

This is a demo project showcasing a basic FastAPI application structure with common features and best practices.

## Features

*   **FastAPI:** A modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.
*   **Uvicorn:** An ASGI server for running FastAPI applications.
*   **Pydantic:** For data validation and settings management using Python type hints.
*   **SQLAlchemy:** For database ORM (Object-Relational Mapper).
*   **JWT Authentication:** User authentication using JSON Web Tokens.
*   **Dependency Injection:** Using FastAPI's dependency injection system.
*   **Docker:** Containerization for easy development and deployment.
*   **Pytest:** For writing and running tests.
*   **Coverage:** For measuring code coverage.
*   **Ruff:** For linting and formatting code.
*   **Pre-commit:** For running checks before committing code.
*   **Makefile:** For common tasks automation.

## Project Structure

(Copy the directory structure from the beginning of this response here)

## Prerequisites

*   Python 3.12+
*   Docker (optional, for containerization)
*   Docker Compose (optional, for containerization)

## Getting Started

1.  **Clone the repository:**

    ```bash
    git clone <your_repository_url>
    cd <repository_name>
    ```

2.  **Create a virtual environment:**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install dependencies:**

    ```bash
    python -m pip install uv
    uv pip install -r pyproject.toml
    ```

4.  **Create a `.env` file:**

    ```bash
    cp .env.example .env
    ```

    Edit the `.env` file and fill in your environment-specific configuration values (database credentials, secret keys, etc.).

5.  **Initialize the database (if using SQLAlchemy):**

    ```bash
    python app/db/init_db.py
    ```

6.  **Run the application:**

    ```bash
    make run
    ```

    Or, using uvicorn directly:

    ```bash
    uvicorn app.main:app --reload
    ```

7.  **Access the API documentation:**

    The API documentation will be available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) (Swagger UI) and [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) (ReDoc).

## Running Tests

```bash
make test
