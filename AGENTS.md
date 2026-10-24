## Project Overview

LLM-powered vocabulary learning tool.

## Project Map

- `main.py`: Creates all components and starts the Flask app.
- `synogym/data_classes.py`: shared dataclasses used across the project.
- `synogym/rest_server.py`: small Flask wrapper for routes, auth checks, static home, error handling.
- `synogym/controller/`: route registration classes, they only delegate to services.
- `synogym/service/`: business/use-case logic, they use repo/generator abstractions.
- `synogym/repo/`: repository interfaces, in-memory implementations, SqlAlchemy implementations.
- `synogym/generator/`: LLM-backed generation workflows.
- `synogym/parser/`: YAML parsers for LLM responses.
- `synogym/client/`: external clients like GptClient and BrainyClient.
- `tests/`: unit tests for the backend modules.
- `web/`: vanilla JS frontend split into `api/`, `component/`, `helper/`, `view/`, `main.js`.
- `config.yaml`: application config file.
- `schema-sqlite.sql`: database schema.

## Coding

- Write minimal code focused on the request.
- Use only verbs for function names.
- Use only nouns for variable/class names.
- Use one letter names if the variable scope is very few lines.
- Use TDD in the backend by default.
- Use small and easy to read functions.
- Add types in function declarations except None return.
- Add type when a variable is initialized using a function call.
- Use no empty line between imports.
- Use less than 120 characters in each line.
- Start private method names with underscore.

## Commands

- `uv sync`
- `uv run pytest`
- `uv run python main.py`
