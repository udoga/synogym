class MeaningDetailComponent {
  constructor(router, meaningApi, bookmarkApi, quoteApi) {
    this.router = router;
    this.meaningApi = meaningApi;
    this.bookmarkApi = bookmarkApi;
    this.quoteApi = quoteApi;
    this.meaning = null;
    this.examples = [];
    this.meaningDetail = null;
    this.bookmark = null;
    this.bookmarkNote = "";
    this.newBookmarkTag = "";
    this.isAddingBookmarkTag = false;
    this.quotes = [];
    this.synonymComparison = "";
    this.formationComparison = "";
    this.isQuoteLoading = false;
    this.isExampleLoading = false;
    this.isDetailLoading = false;
    this.status = "";
    this.isError = false;
    this.isLoading = false;
  }

  async load() {
    const meaningId = this.router.getId();
    if (!meaningId) return this.showError("Meaning not found.");
    this.startLoading();
    try {
      await this.loadMeaning(meaningId);
    } catch {
      this.showError("Could not reach the server.");
    }
    this.isLoading = false;
    await this.loadExamples(meaningId);
    await this.loadDetail(meaningId);
    await this.loadQuotes(this.meaning?.query);
  }

  async loadMeaning(meaningId) {
    this.showMeaning(await this.meaningApi.read(meaningId));
  }

  showMeaning(result) {
    if (!result.response.ok) return this.showError(result.body.error?.message || "Could not load meaning.");
    this.meaning = result.body.data;
    this.showStatus("Word Details");
    this.loadBookmark();
  }

  async loadExamples(meaningId) {
    if (!this.meaning) return;
    this.isExampleLoading = true;
    try {
      this.showExamples(await this.meaningApi.listExamples(meaningId));
    } catch {
      this.showStatus("Could not reach the server.");
    }
    this.isExampleLoading = false;
  }

  showExamples(result) {
    if (!result.response.ok) return this.showStatus(result.body.error?.message || "Could not load examples.");
    this.examples = result.body.data;
  }

  async loadDetail(meaningId) {
    if (!this.meaning) return;
    this.isDetailLoading = true;
    try {
      this.showDetail(await this.meaningApi.readDetail(meaningId));
    } catch {
      this.showStatus("Could not reach the server.");
    }
    this.isDetailLoading = false;
  }

  showDetail(result) {
    if (!result.response.ok) return this.showStatus(result.body.error?.message || "Could not load detail.");
    this.meaningDetail = result.body.data;
  }

  async loadQuotes(word) {
    if (!word) return;
    this.quotes = [];
    this.isQuoteLoading = true;
    try {
      this.showQuotes(await this.quoteApi.list(word));
    } catch {}
    this.isQuoteLoading = false;
  }

  showQuotes(result) {
    if (result.response.ok) this.quotes = result.body.data;
  }

  async loadBookmark() {
    try {
      const result = await this.bookmarkApi.listByMeaningId(this.meaning.id);
      if (result.response.ok) this.showBookmark(result.body.data[0] || null);
    } catch {}
  }

  showBookmark(bookmark) {
    this.bookmark = bookmark;
    this.bookmarkNote = bookmark?.note || "";
  }

  async saveBookmark() {
    if (this.bookmark) return this.deleteBookmark();
    if (!this.meaning?.id) return;
    const result = await this.bookmarkApi.create(this.meaning.id);
    if (result.response.ok) this.bookmark = result.body.data;
  }

  async ensureBookmark() {
    if (this.bookmark?.id) return true;
    if (!this.meaning?.id) return false;
    const result = await this.bookmarkApi.create(this.meaning.id);
    if (!result.response.ok) return false;
    this.bookmark = result.body.data;
    return true;
  }

  async deleteBookmark() {
    if (!window.confirm("Remove the bookmark?")) return;
    const bookmark = this.bookmark;
    this.bookmark = null;
    this.bookmarkNote = "";
    const result = await this.bookmarkApi.deleteBookmark(bookmark.id);
    if (!result.response.ok) this.showBookmark(bookmark);
  }

  async updateBookmarkFromNote() {
    if (!this.bookmarkNote && !this.bookmark?.id) return;
    if (!await this.ensureBookmark()) return;
    this.bookmark.note = this.bookmarkNote;
    return this.updateBookmark({ keepFocusedNote: true });
  }

  async updateBookmark(options = {}) {
    if (!this.bookmark?.id) return;
    const result = await this.bookmarkApi.update(this.bookmark);
    if (result.response.ok) this.showUpdatedBookmark(result.body.data, options);
  }

  showUpdatedBookmark(bookmark, options) {
    if (options.keepFocusedNote && document.activeElement?.id === "bookmark-note-input") {
      this.bookmark.tags = bookmark.tags || "";
      return;
    }
    this.showBookmark(bookmark);
  }

  startBookmarkTag() {
    this.newBookmarkTag = "";
    this.isAddingBookmarkTag = true;
  }

  cancelBookmarkTag() {
    this.newBookmarkTag = "";
    this.isAddingBookmarkTag = false;
  }

  async addBookmarkTag() {
    const tag = this.cleanTag(this.newBookmarkTag);
    this.cancelBookmarkTag();
    if (!tag) return;
    return this.saveBookmarkTags([...this.bookmarkTags(), tag]);
  }

  removeBookmarkTag(tag) {
    return this.saveBookmarkTags(this.bookmarkTags().filter(bookmarkTag => bookmarkTag !== tag));
  }

  async saveBookmarkTags(tags) {
    if (!await this.ensureBookmark()) return;
    this.bookmark.note = this.bookmarkNote;
    this.bookmark.tags = [...new Set(tags.map(tag => this.cleanTag(tag)).filter(Boolean))].join(", ");
    return this.updateBookmark();
  }

  bookmarkTags() {
    return String(this.bookmark?.tags || "").split(",").map(tag => this.cleanTag(tag)).filter(Boolean);
  }

  cleanTag(tag) {
    return String(tag || "").trim();
  }

  async compareSynonym(synonym) {
    if (!this.meaning?.id) return;
    this.synonymComparison = "Comparing...";
    try {
      this.showSynonymComparison(await this.meaningApi.compare(this.meaning.id, "synonym", synonym), synonym);
    } catch {
      this.showStatus("Could not reach the server.");
    }
  }

  showSynonymComparison(result, synonym) {
    if (!result.response.ok) return this.showStatus(result.body.error?.message || "Could not load comparison.");
    this.synonymComparison = this.renderComparison(result.body.data, synonym);
  }

  async compareFormation(formation) {
    if (!this.meaning?.id) return;
    this.formationComparison = "Comparing...";
    try {
      this.showFormationComparison(await this.meaningApi.compare(this.meaning.id, "formation", formation), formation);
    } catch {
      this.showStatus("Could not reach the server.");
    }
  }

  showFormationComparison(result, formation) {
    if (!result.response.ok) return this.showStatus(result.body.error?.message || "Could not load comparison.");
    this.formationComparison = this.renderComparison(result.body.data, formation);
  }

  select(event) {
    event.target.parentElement.querySelectorAll(".word-button").forEach(button => button.removeAttribute("selected"));
    event.target.setAttribute("selected", "");
  }

  searchWord(word) {
    this.router.route(`#/meanings?query=${encodeURIComponent(word)}`);
  }

  back() {
    history.back();
  }

  detail() {
    return { synonyms: [], formations: [], ...this.meaningDetail };
  }

  hasWords(words) {
    return Array.isArray(words) && words.length > 0;
  }

  joinWords(words) {
    return this.hasWords(words) ? words.join(", ") : "";
  }

  render(sentence) {
    return this.escape(sentence)
      .replaceAll("&lt;em&gt;", "<em>")
      .replaceAll("&lt;/em&gt;", "</em>");
  }

  resolveQuoteIcon(url) {
    const source = String(url || "").toLowerCase();
    if (source.includes("wiki")) return "/web/image/wikiquote.svg";
    if (source.includes("brainy")) return "/web/image/brainy.png";
    return "";
  }

  labelQuoteSource(url) {
    const source = String(url || "").toLowerCase();
    if (source.includes("wiki")) return "Open on Wikiquote";
    if (source.includes("brainy")) return "Open on BrainyQuote";
    return "Open quote source";
  }

  renderComparison(text, selection) {
    const word = String(selection || "").trim();
    const html = this.escape(text);
    if (!word) return html;
    const expression = new RegExp(this.escapeExpression(this.escape(word)), "i");
    return html.replace(expression, `<a class="inline-word-link" href="#/meanings?query=${encodeURIComponent(word)}">$&</a>`);
  }

  escape(value) {
    return String(value || "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;");
  }

  escapeExpression(value) {
    return String(value).replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  }

  getLevelClass(level) {
    return level ? `level-${String(level).toLowerCase()}` : "";
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
    this.meaning = null;
    this.examples = [];
    this.meaningDetail = null;
    this.synonymComparison = "";
    this.formationComparison = "";
    this.bookmark = null;
    this.bookmarkNote = "";
    this.status = message;
  }
}
