from synogym.generator import Generator
from synogym.data_classes import ComparisonRequest, LlmRequest

class ComparisonGenerator(Generator[ComparisonRequest, str]):
    PROMPT = """You are a comparison API for English learners.
Given a word/phrase with its definition and pos; and a selected {type}; describe their difference.

Rules:
- Compare the query and the {type}, ideally {sentence_count} concise sentences.
- ONLY content, no markdown, no additional text, no quotation marks.

Query: {query}
Definition: {definition}
Part of speech: {pos}
{type}: {selection}
"""

    def __init__(self, generator: Generator[LlmRequest, str]):
        self.generator: Generator[LlmRequest, str] = generator

    def generate(self, request: ComparisonRequest) -> str:
        sentence_counts = {"synonym": "3-4", "formation": "1-2"}
        prompt: str = self.PROMPT.format(query=request.meaning.query,
                                         definition=request.meaning.definition,
                                         pos=request.meaning.pos,
                                         selection=request.selection,
                                         type=request.type,
                                         sentence_count=sentence_counts.get(request.type, "3-4"))
        return self.generator.generate(LlmRequest(prompt, "comparison"))
