class MeaningListComponent {
  constructor(router, meaningApi, bookmarkApi, page_size = null) {
    this.router = router;
    this.meaningApi = meaningApi;
    this.bookmarkApi = bookmarkApi;
    this.page_size = page_size || this.choosePageSize();
    this.meanings = [];
    this.keptMeanings = [];
    this.pageIndex = 0;
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
      this.showBookmarks(await this.bookmarkApi.listBookmarkedMeanings());
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
    this.keepBookmarks(result.body.data);
  }

  keepBookmarks(bookmarks) {
    const meanings = this.getVisibleBookmarks(bookmarks);
    this.keptMeanings = this.isNotes() ? this.shuffle(meanings) : meanings;
    this.showPage(0);
  }

  shuffle(meanings) {
    const items = [...meanings];
    for (let i = items.length - 1; i > 0; i--) {
      const index = Math.floor(Math.random() * (i + 1));
      [items[i], items[index]] = [items[index], items[i]];
    }
    return items;
  }

  showPage(pageIndex) {
    this.pageIndex = pageIndex;
    this.meanings = this.keptMeanings.slice(this.pageIndex, this.pageIndex + this.page_size);
    this.emptyMessage = this.meanings.length ? "" : this.getBookmarkMessage();
    this.showStatus(this.label());
  }

  showNext() {
    const pageIndex = this.pageIndex + this.page_size;
    if (pageIndex < this.keptMeanings.length) {
      this.showPage(pageIndex);
      this.scrollTop();
    }
  }

  scrollTop() {
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  resize() {
    this.showPage(0);
  }

  choosePageSize() {
    if (this.isNotes() && window.matchMedia("(max-width: 540px)").matches) return 1;
    return 4;
  }

  hasNext() {
    return this.pageIndex + this.page_size < this.keptMeanings.length;
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
    this.keptMeanings = [];
    this.pageIndex = 0;
    this.meanings = result.body.data;
    this.emptyMessage = this.meanings.length ? "" : "No words found.";
    this.showStatus(this.label());
  }

  meaningText(meaning) {
    return this.isNotes() ? this.note(meaning) : meaning.definition;
  }

  render(text) {
    return String(text || "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll("&lt;em&gt;", "<em>")
      .replaceAll("&lt;/em&gt;", "</em>");
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
    this.keptMeanings = [];
    this.emptyMessage = "";
    this.status = message;
  }
}
