import json
from dataclasses import fields
from sqlalchemy import text
from sqlalchemy.engine import Connection, RowMapping
from synogym.data_classes import Bookmark, MeaningWithBookmark, ExampleWithBookmark
from synogym.repo.bookmark_repo import BookmarkRepo

class SqlBookmarkRepo(BookmarkRepo):
    def __init__(self, connection: Connection):
        self.connection = connection

    def list_by(self, user_id: int, meaning_id: int | None) -> list[Bookmark]:
        sql = "SELECT * FROM bookmarks WHERE user_id = :user_id"
        if meaning_id: sql += " AND meaning_id = :meaning_id"
        values = {"user_id": user_id, "meaning_id": meaning_id}
        rows = self.connection.execute(text(sql + " ORDER BY id"), values).mappings().all()
        return [self._get_bookmark(row) for row in rows]

    def list_meanings_with_bookmark(self, user_id: int) -> list[MeaningWithBookmark]:
        sql = """SELECT m.id AS meaning_id, m.query, m.definition, m.pos, b.id, b.user_id, b.note, b.tags
                 FROM meanings m JOIN bookmarks b ON b.meaning_id = m.id
                 WHERE b.user_id = :user_id ORDER BY b.id"""
        rows = self.connection.execute(text(sql), {"user_id": user_id})
        return [self._get_meaning_with_bookmark(row) for row in rows.mappings().all()]

    def list_examples_with_bookmark(self, user_id: int) -> list[ExampleWithBookmark]:
        sql = """SELECT e.meaning_id, e.sentence, e.replacements, b.id, b.user_id, b.note, b.tags
                 FROM examples e JOIN bookmarks b ON b.meaning_id = e.meaning_id
                 WHERE b.user_id = :user_id ORDER BY b.id, e.id"""
        rows = self.connection.execute(text(sql), {"user_id": user_id})
        return [self._get_example_with_bookmark(row) for row in rows.mappings().all()]

    def create(self, b: Bookmark) -> Bookmark:
        sql = """INSERT INTO bookmarks (user_id, meaning_id, note, tags)
                 VALUES (:user_id, :meaning_id, :note, :tags) RETURNING id"""
        values = {"user_id": b.user_id, "meaning_id": b.meaning_id, "note": b.note, "tags": b.tags}
        b.id = self.connection.execute(text(sql), values).scalar_one()
        self.connection.commit()
        return b

    def find(self, bookmark_id: int) -> Bookmark | None:
        sql = "SELECT * FROM bookmarks WHERE id = :id"
        row = self.connection.execute(text(sql), {"id": bookmark_id}).mappings().fetchone()
        return self._get_bookmark(row) if row else None

    def update(self, bookmark: Bookmark) -> Bookmark:
        sql = "UPDATE bookmarks SET note = :note, tags = :tags WHERE id = :id"
        values = {"id": bookmark.id, "note": bookmark.note, "tags": bookmark.tags}
        self.connection.execute(text(sql), values)
        self.connection.commit()
        return bookmark

    def delete(self, bookmark_id: int):
        sql = "DELETE FROM bookmarks WHERE id = :id"
        self.connection.execute(text(sql), {"id": bookmark_id})
        self.connection.commit()

    def _get_bookmark(self, row: RowMapping) -> Bookmark:
        return Bookmark(**{field.name: row[field.name] for field in fields(Bookmark)})

    def _get_meaning_with_bookmark(self, row: RowMapping) -> MeaningWithBookmark:
        return MeaningWithBookmark(id=row["meaning_id"],
                                   query=row["query"],
                                   definition=row["definition"],
                                   pos=row["pos"],
                                   bookmark=self._get_bookmark(row))

    def _get_example_with_bookmark(self, row: RowMapping) -> ExampleWithBookmark:
        return ExampleWithBookmark(meaning_id=row["meaning_id"],
                                   sentence=row["sentence"],
                                   replacements=json.loads(row["replacements"]),
                                   bookmark=self._get_bookmark(row))
