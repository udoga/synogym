## Project Overview

Interactive vocabulary practice tool for improving recall and paraphrase skills.

## Project Map

- `main.py`: Loads config, creates db connection, repositories, generators, services, and starts the Flask app.
- `synogym/data_classes.py`: shared dataclasses used across controllers, services, repos, parsers, and clients.
- `synogym/rest_server.py`: small Flask wrapper for routes, JSON responses, auth checks, static home, and errors.
- `synogym/controller/`: thin route registration classes. They should only delegate to services. No tests.
- `synogym/service/`: business/use-case logic. Services depend on repo abstractions and generator abstractions.
- `synogym/repo/`: repository interfaces; `repo/db/` SQLAlchemy implementations; `repo/list/` in-memory test doubles.
- `synogym/generator/`: LLM-backed generation workflows.
- `synogym/parser/`: YAML parsers for LLM responses.
- `synogym/client/`: external clients (`GptClient`, `BrainyClient`).
- `web/`: vanilla JS frontend split into `api/`, `component/`, `helper/`, `view/`, plus `main.js`.
- `tests/`: pytest/unittest tests for the backend modules.
- `schema-sqlite.sql` and `schema-postgres.sql`: database schemas.
- `.gitignore`: Ignore these files during scans.

## Common Commands

- `uv sync`
- `uv run pytest`
- `uv run python main.py`

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
