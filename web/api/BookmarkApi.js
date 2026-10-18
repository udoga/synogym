class BookmarkApi extends JsonApi {
  listMeanings() {
    return this.get("/bookmarks/meanings");
  }

  listExamples() {
    return this.get("/bookmarks/examples");
  }

  listByMeaningId(meaningId) {
    return this.get(`/bookmarks?meaning_id=${encodeURIComponent(meaningId)}`);
  }

  create(meaningId) {
    return this.post("/bookmarks", { meaning_id: meaningId });
  }

  update(bookmark) {
    const body = { note: bookmark.note || "", tags: bookmark.tags || "" };
    return this.put(`/bookmarks/${bookmark.id}`, body);
  }

  deleteBookmark(id) {
    return this.delete(`/bookmarks/${id}`);
  }
}
