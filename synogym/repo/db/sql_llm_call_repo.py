from sqlalchemy import text
from sqlalchemy.engine import Connection, RowMapping
from synogym.data_classes import LlmCall
from synogym.repo.llm_call_repo import LlmCallRepo

class SqlLlmCallRepo(LlmCallRepo):
    INSERT_SQL = """
        INSERT INTO llm_calls (llm_name, reasoning_effort, operation, input_token_count, output_token_count,
                               first_token_latency, generation_latency)
        VALUES (:llm_name, :reasoning_effort, :operation, :input_token_count, :output_token_count,
                :first_token_latency, :generation_latency)
        RETURNING id
    """
    READ_SQL = "SELECT * FROM llm_calls WHERE id = :id"

    def __init__(self, connection: Connection):
        self.connection = connection

    def create(self, call: LlmCall) -> LlmCall:
        call.id = self.connection.execute(text(self.INSERT_SQL), self._get_values(call)).scalar_one()
        self.connection.commit()
        return call

    def find(self, call_id: int) -> LlmCall | None:
        row = self.connection.execute(text(self.READ_SQL), {"id": call_id}).mappings().fetchone()
        return self._get_call(row) if row else None

    def _get_values(self, call: LlmCall) -> dict[str, str | int | float]:
        return {"llm_name": call.llm_name, "reasoning_effort": call.reasoning_effort,
                "operation": call.operation, "input_token_count": call.input_token_count,
                "output_token_count": call.output_token_count, "first_token_latency": call.first_token_latency,
                "generation_latency": call.generation_latency}

    def _get_call(self, row: RowMapping) -> LlmCall:
        return LlmCall(id=row["id"], llm_name=row["llm_name"], reasoning_effort=row["reasoning_effort"],
                       operation=row["operation"], input_token_count=row["input_token_count"],
                       output_token_count=row["output_token_count"], first_token_latency=row["first_token_latency"],
                       generation_latency=row["generation_latency"])
