class MeaningListComponent {
  constructor(router, meaningApi, bookmarkApi) {
    this.router = router;
    this.meaningApi = meaningApi;
    this.bookmarkApi = bookmarkApi;
    this.meanings = [];
    this.status = "";
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
    return this.isNotes() ? "Notes" : "Meanings";
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
    this.showStatus(this.getBookmarkStatus());
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

  getBookmarkStatus() {
    if (this.meanings.length) return this.label();
    if (this.isNotes()) return "Search, save a word, and add a note to see your notes here.";
    return "Search and save a word to see your meanings here.";
  }

  showMeanings(result) {
    if (!result.response.ok) return this.showError(result.body.error?.message || "Search failed.");
    this.meanings = result.body.data;
    this.showStatus(this.meanings.length ? "Meanings" : "No meanings found.");
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
    this.showStatus("Loading...");
  }

  showStatus(message) {
    this.isError = false;
    this.status = message;
  }

  showError(message) {
    this.isError = true;
    this.meanings = [];
    this.status = message;
  }
}
