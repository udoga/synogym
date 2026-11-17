## Project Overview

LLM-powered vocabulary learning tool.

## Coding

- Write minimal code focused on the request.
- Use only verbs for function names.
- Use only nouns for variable/class names.
- Use one letter names if the variable scope is very few lines.
- Use TDD in the backend by default.
- Use small and easy to read functions.
- Add types in function declarations except None return.
- Add type when a variable is initialized using a function call.
- Don't use empty line between imports.
- Don't use empty line inside functions.
- Use less than 120 characters in each line.
- Start private method names with underscore.

## Project Info

- `main.py`: Creates all components and starts the Flask app.
- `synogym/data_classes.py`: shared dataclasses used across the project.
- `synogym/rest_server.py`: Flask wrapper for routes, auth, error handling.
- `synogym/controller/`: route registration classes, they only delegate to services.
- `synogym/service/`: business/use-case logic, they use repo/generator abstractions.
- `synogym/repo/`: repository interfaces, in-memory implementations, SqlAlchemy implementations.
- `synogym/generator/`: LLM-backed generation workflows.
- `synogym/parser/`: YAML parsers for LLM responses.
- `tests/`: unit tests for the backend modules.
- `web/`: vanilla JS frontend split into `api/`, `component/`, `helper/`, `view/`, `main.js`.
- `config.yaml`: application config file.
- `schema-sqlite.sql`: database schema.
- `uv run pytest`: for running tests.
