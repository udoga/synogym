import sqlite3
from synogym.data_classes import Bookmark
from synogym.repo.bookmark_repo import BookmarkRepo

class SqlBookmarkRepo(BookmarkRepo):
    INSERT_BOOKMARK_SQL = "INSERT INTO bookmarks (user_id, meaning_id, note, tags) VALUES (?, ?, ?, ?)"
    SELECT_BOOKMARK_SQL = "SELECT * FROM bookmarks WHERE id = ?"
    SELECT_BY_USER_AND_MEANING_SQL = "SELECT * FROM bookmarks WHERE user_id = ? AND meaning_id = ?"
    UPDATE_BOOKMARK_SQL = "UPDATE bookmarks SET note = ?, tags = ? WHERE id = ?"
    DELETE_BOOKMARK_SQL = "DELETE FROM bookmarks WHERE id = ?"

    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection

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
