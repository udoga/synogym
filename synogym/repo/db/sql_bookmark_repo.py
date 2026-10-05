from sqlalchemy import text
from sqlalchemy.engine import Connection, RowMapping
from synogym.data_classes import Bookmark, BookmarkWithMeaning, Meaning
from synogym.repo.bookmark_repo import BookmarkRepo

class SqlBookmarkRepo(BookmarkRepo):
    INSERT_BOOKMARK_SQL = """
        INSERT INTO bookmarks (user_id, meaning_id, note, tags)
        VALUES (:user_id, :meaning_id, :note, :tags)
        RETURNING id
    """
    LIST_WITH_MEANINGS_SQL = """
        SELECT b.id AS bookmark_id, b.user_id, b.meaning_id, b.note, b.tags,
               m.query, m.definition, m.pos
        FROM bookmarks b JOIN meanings m ON m.id = b.meaning_id
        WHERE b.user_id = :user_id
        ORDER BY b.id
    """
    SELECT_BOOKMARK_SQL = "SELECT * FROM bookmarks WHERE id = :id"
    SELECT_BY_USER_AND_MEANING_SQL = """
        SELECT * FROM bookmarks WHERE user_id = :user_id AND meaning_id = :meaning_id
    """
    UPDATE_BOOKMARK_SQL = "UPDATE bookmarks SET note = :note, tags = :tags WHERE id = :id"
    DELETE_BOOKMARK_SQL = "DELETE FROM bookmarks WHERE id = :id"

    def __init__(self, connection: Connection):
        self.connection = connection

    def list_with_meanings(self, user_id: int) -> list[BookmarkWithMeaning]:
        rows = self.connection.execute(text(self.LIST_WITH_MEANINGS_SQL), {"user_id": user_id}).mappings().all()
        return [self._create_bookmark_with_meaning(row) for row in rows]

    def create(self, bookmark: Bookmark) -> Bookmark:
        bookmark.id = self.connection.execute(text(self.INSERT_BOOKMARK_SQL), self._get_values(bookmark)).scalar_one()
        self.connection.commit()
        return bookmark

    def find(self, bookmark_id: int) -> Bookmark | None:
        row = self._fetch_one(self.SELECT_BOOKMARK_SQL, {"id": bookmark_id})
        return self._create_bookmark(row) if row else None

    def find_by_user_and_meaning(self, user_id: int, meaning_id: int) -> list[Bookmark]:
        values = {"user_id": user_id, "meaning_id": meaning_id}
        row = self._fetch_one(self.SELECT_BY_USER_AND_MEANING_SQL, values)
        return [self._create_bookmark(row)] if row else []

    def update(self, bookmark: Bookmark) -> Bookmark:
        self.connection.execute(text(self.UPDATE_BOOKMARK_SQL), self._get_update_values(bookmark))
        self.connection.commit()
        return bookmark

    def delete(self, bookmark_id: int):
        self.connection.execute(text(self.DELETE_BOOKMARK_SQL), {"id": bookmark_id})
        self.connection.commit()

    def _fetch_one(self, sql: str, values: dict) -> RowMapping | None:
        return self.connection.execute(text(sql), values).mappings().fetchone()

    def _get_values(self, bookmark: Bookmark) -> dict[str, int | str]:
        return {"user_id": bookmark.user_id, "meaning_id": bookmark.meaning_id,
                "note": bookmark.note, "tags": bookmark.tags}

    def _get_update_values(self, bookmark: Bookmark) -> dict[str, int | str]:
        return {"id": bookmark.id, "note": bookmark.note, "tags": bookmark.tags}

    def _create_bookmark(self, row: RowMapping) -> Bookmark:
        return Bookmark(id=row["id"], user_id=row["user_id"], meaning_id=row["meaning_id"], note=row["note"],
                        tags=row["tags"])

    def _create_bookmark_with_meaning(self, row: RowMapping) -> BookmarkWithMeaning:
        meaning = Meaning(id=row["meaning_id"], query=row["query"], definition=row["definition"], pos=row["pos"])
        return BookmarkWithMeaning(id=row["bookmark_id"], user_id=row["user_id"], meaning_id=row["meaning_id"],
                                   note=row["note"], tags=row["tags"], meaning=meaning)
