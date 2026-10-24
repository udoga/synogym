class MeaningListComponent {
  constructor(router, meaningApi, bookmarkApi) {
    this.router = router;
    this.meaningApi = meaningApi;
    this.bookmarkApi = bookmarkApi;
    this.meanings = [];
    this.status = "";
    this.emptyMessage = "";
    this.isError = false;
    this.isLoading = false;
  }

  async load() {
    return this.isBookmarks() ? this.loadBookmarks() : this.loadMeanings();
  }

  isBookmarks() {
    return location.hash.startsWith("#/bookmarks/meanings") || location.hash === "#/bookmarks";
  }

  label() {
    if (this.isNotes()) return "Notes";
    return this.isBookmarks() ? "Words" : "Meanings";
  }

  isNotes() {
    return this.router.getUrlParams().notes === "true";
  }

  async loadBookmarks() {
    this.startLoading();
    try {
      this.showBookmarks(await this.bookmarkApi.listMeanings());
    } catch {
      this.showError("Could not reach the server.");
    }
    this.isLoading = false;
  }

  async loadMeanings() {
    const query = this.router.getUrlParams().query || "";
    if (!query.trim()) return this.showError("Search for a word.");
    this.startLoading();
    try {
      this.showMeanings(await this.meaningApi.list(query));
    } catch {
      this.showError("Could not reach the server.");
    }
    this.isLoading = false;
  }

  showBookmarks(result) {
    if (!result.response.ok) return this.showError(result.body.error?.message || "Could not load meanings.");
    this.meanings = this.getVisibleBookmarks(result.body.data);
    this.emptyMessage = this.meanings.length ? "" : this.getBookmarkMessage();
    this.showStatus(this.label());
  }

  getVisibleBookmarks(bookmarks) {
    return this.isNotes() ? bookmarks.filter(meaning => this.hasNote(meaning)) : bookmarks;
  }

  hasNote(meaning) {
    return Boolean(this.note(meaning).trim());
  }

  note(meaning) {
    return String(meaning?.bookmark?.note || "");
  }

  getBookmarkMessage() {
    if (this.isNotes()) return "Add a note to a saved word to see your notes.";
    return "Your words appear here once you search & save.";
  }

  showMeanings(result) {
    if (!result.response.ok) return this.showError(result.body.error?.message || "Search failed.");
    this.meanings = result.body.data;
    this.emptyMessage = this.meanings.length ? "" : "No words found.";
    this.showStatus(this.label());
  }

  meaningText(meaning) {
    return this.isNotes() ? this.note(meaning) : meaning.definition;
  }

  userTags(meaning) {
    return String(meaning?.bookmark?.tags || "").split(",").map(tag => tag.trim()).filter(Boolean);
  }

  openMeaning(meaning) {
    if (meaning?.id) this.router.route(`#/meaning/${meaning.id}`);
  }

  home() {
    this.router.route("#/home");
  }

  startLoading() {
    this.isLoading = true;
    this.emptyMessage = "";
    this.showStatus("Loading...");
  }

  showStatus(message) {
    this.isError = false;
    this.status = message;
  }

  showError(message) {
    this.isError = true;
    this.meanings = [];
    this.emptyMessage = "";
    this.status = message;
  }
}
