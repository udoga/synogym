# Synogym

LLM-powered vocabulary learning tool (currently under development).

https://www.synogym.com

### Development

Set openai_api_key in [config.yaml](config.yaml).

```
uv sync
uv run python -m nltk.downloader wordnet averaged_perceptron_tagger_eng
uv run pytest
uv run python main.py
```

Load wikiquotes dataset (optional):

```
kaggle datasets download -d linuds/wikiquotes-english/3 -p data --unzip
sqlite3 synogym.sqlite < data/wikiquotes-english.sql
```
