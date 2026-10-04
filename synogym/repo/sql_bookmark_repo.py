import sqlite3
from synogym.data_classes import Bookmark, BookmarkWithMeaning, Meaning
from synogym.repo.bookmark_repo import BookmarkRepo

class SqlBookmarkRepo(BookmarkRepo):
    INSERT_BOOKMARK_SQL = "INSERT INTO bookmarks (user_id, meaning_id, note, tags) VALUES (?, ?, ?, ?)"
    LIST_WITH_MEANINGS_SQL = """
        SELECT b.id AS bookmark_id, b.user_id, b.meaning_id, b.note, b.tags,
               m.query, m.definition, m.pos
        FROM bookmarks b JOIN meanings m ON m.id = b.meaning_id
        WHERE b.user_id = ?
        ORDER BY b.id
    """
    SELECT_BOOKMARK_SQL = "SELECT * FROM bookmarks WHERE id = ?"
    SELECT_BY_USER_AND_MEANING_SQL = "SELECT * FROM bookmarks WHERE user_id = ? AND meaning_id = ?"
    UPDATE_BOOKMARK_SQL = "UPDATE bookmarks SET note = ?, tags = ? WHERE id = ?"
    DELETE_BOOKMARK_SQL = "DELETE FROM bookmarks WHERE id = ?"

    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection

    def list_with_meanings(self, user_id: int) -> list[BookmarkWithMeaning]:
        cursor = self.connection.execute(self.LIST_WITH_MEANINGS_SQL, (user_id,))
        return [self._create_bookmark_with_meaning(row) for row in cursor.fetchall()]

    def create(self, bookmark: Bookmark) -> Bookmark:
        cursor = self.connection.execute(self.INSERT_BOOKMARK_SQL, self._get_values(bookmark))
        self.connection.commit()
        bookmark.id = cursor.lastrowid
        return bookmark

    def find(self, bookmark_id: int) -> Bookmark | None:
        row = self.connection.execute(self.SELECT_BOOKMARK_SQL, (bookmark_id,)).fetchone()
        return self._create_bookmark(row) if row else None

    def find_by_user_and_meaning(self, user_id: int, meaning_id: int) -> Bookmark | None:
        row = self.connection.execute(self.SELECT_BY_USER_AND_MEANING_SQL, (user_id, meaning_id)).fetchone()
        return self._create_bookmark(row) if row else None

    def update(self, bookmark: Bookmark) -> Bookmark:
        self.connection.execute(self.UPDATE_BOOKMARK_SQL, (bookmark.note, bookmark.tags, bookmark.id))
        self.connection.commit()
        return bookmark

    def delete(self, bookmark_id: int):
        self.connection.execute(self.DELETE_BOOKMARK_SQL, (bookmark_id,))
        self.connection.commit()

    def _get_values(self, bookmark: Bookmark) -> tuple[int, int, str, str]:
        return bookmark.user_id, bookmark.meaning_id, bookmark.note, bookmark.tags

    def _create_bookmark(self, row: sqlite3.Row) -> Bookmark:
        return Bookmark(id=row["id"], user_id=row["user_id"], meaning_id=row["meaning_id"], note=row["note"],
                        tags=row["tags"])

    def _create_bookmark_with_meaning(self, row: sqlite3.Row) -> BookmarkWithMeaning:
        meaning = Meaning(id=row["meaning_id"], query=row["query"], definition=row["definition"], pos=row["pos"])
        return BookmarkWithMeaning(id=row["bookmark_id"], user_id=row["user_id"], meaning_id=row["meaning_id"],
                                   note=row["note"], tags=row["tags"], meaning=meaning)
