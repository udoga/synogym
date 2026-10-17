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
    return location.hash.startsWith("#/bookmarks");
  }

  label() {
    return this.isBookmarks() ? "Bookmarks" : "Meanings";
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
    if (!result.response.ok) return this.showError(result.body.error?.message || "Could not load bookmarks.");
    this.meanings = result.body.data;
    this.showStatus(this.meanings.length ? "Bookmarks" : "No bookmarks yet.");
  }

  showMeanings(result) {
    if (!result.response.ok) return this.showError(result.body.error?.message || "Search failed.");
    this.meanings = result.body.data;
    this.showStatus(this.meanings.length ? "Meanings" : "No meanings found.");
  }

  openMeaning(meaning) {
    if (meaning?.id) this.router.route(`#/meaning/${meaning.id}`);
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
