from dataclasses import asdict
from sqlalchemy import text
from sqlalchemy.engine import Connection, RowMapping
from synogym.data_classes import LlmCall
from synogym.repo.llm_call_repo import LlmCallRepo

class SqlLlmCallRepo(LlmCallRepo):
    def __init__(self, connection: Connection):
        self.connection = connection

    def create(self, call: LlmCall) -> LlmCall:
        sql = """INSERT INTO llm_calls (llm_name, reasoning_effort, operation, input_token_count, output_token_count,
                                        first_token_latency, generation_latency)
                 VALUES (:llm_name, :reasoning_effort, :operation, :input_token_count, :output_token_count,
                         :first_token_latency, :generation_latency) RETURNING id"""
        call.id = self.connection.execute(text(sql), self._get_values(call)).scalar_one()
        self.connection.commit()
        return call

    def find(self, call_id: int) -> LlmCall | None:
        sql = "SELECT * FROM llm_calls WHERE id = :id"
        row = self.connection.execute(text(sql), {"id": call_id}).mappings().fetchone()
        return LlmCall(**dict(row)) if row else None

    def _get_values(self, call: LlmCall) -> dict[str, object]:
        return {key: value for key, value in asdict(call).items() if key != "id"}
 