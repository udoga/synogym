from abc import ABC, abstractmethod
from synogym.data_classes import Bookmark, BookmarkWithMeaning, ExampleWithBookmark

class BookmarkRepo(ABC):
    @abstractmethod
    def list_by(self, user_id: int, meaning_id: int | None) -> list[Bookmark]:
        pass

    @abstractmethod
    def list_with_meanings(self, user_id: int) -> list[BookmarkWithMeaning]:
        pass

    @abstractmethod
    def list_examples_with_bookmark(self, user_id: int) -> list[ExampleWithBookmark]:
        pass

    @abstractmethod
    def create(self, bookmark: Bookmark) -> Bookmark:
        pass

    @abstractmethod
    def find(self, bookmark_id: int) -> Bookmark | None:
        pass

    @abstractmethod
    def update(self, bookmark: Bookmark) -> Bookmark:
        pass

    @abstractmethod
    def delete(self, bookmark_id: int):
        pass
