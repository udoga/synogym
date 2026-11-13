class ExampleListComponent {
  constructor(router, bookmarkApi, page_size = null) {
    this.router = router;
    this.bookmarkApi = bookmarkApi;
    this.page_size = page_size || this.choosePageSize();
    this.examples = [];
    this.keptExamples = [];
    this.pageIndex = 0;
    this.replacementsByKey = {};
    this.status = "";
    this.emptyMessage = "";
    this.isError = false;
    this.isLoading = false;
  }

  async load() {
    this.startLoading("Examples");
    try {
      this.showExamples(await this.bookmarkApi.listBookmarkedMeaningExamples());
    } catch {
      this.showError("Could not reach the server.");
    }
    this.isLoading = false;
  }

  async showNext() {
    const pageIndex = this.pageIndex + this.page_size;
    if (pageIndex < this.keptExamples.length) return this.showPage(pageIndex);
    this.startLoading("Examples");
    try {
      this.replaceExamples(await this.bookmarkApi.listBookmarkedMeaningExamples());
    } catch {
      this.showAppendError("Could not reach the server.");
    }
    this.isLoading = false;
  }

  showExamples(result) {
    if (!result.response.ok) return this.showError(result.body.error?.message || "Could not load examples.");
    this.keepExamples(result.body.data);
  }

  replaceExamples(result) {
    if (!result.response.ok) return this.showAppendError(result.body.error?.message || "Could not load examples.");
    this.keepExamples(result.body.data);
  }

  keepExamples(examples) {
    this.keptExamples = this.deduplicateExamples(examples).slice(0, 50);
    this.showPage(0);
  }

  showPage(pageIndex) {
    this.pageIndex = pageIndex;
    this.replacementsByKey = {};
    this.examples = this.keptExamples.slice(this.pageIndex, this.pageIndex + this.page_size);
    this.emptyMessage = this.examples.length ? "" : "Examples appear here once you save a word.";
    this.showStatus("Examples");
  }

  resize() {
    this.showPage(0);
  }

  choosePageSize() {
    return window.matchMedia("(max-width: 540px)").matches ? 1 : 4;
  }

  deduplicateExamples(examples) {
    const examplesByKey = new Map();
    for (const example of examples) examplesByKey.set(this.identifyExample(example), example);
    return [...examplesByKey.values()];
  }

  identifyExample(example) {
    return `${example.meaning_id}-${example.sentence}`;
  }

  openExample(example) {
    if (example?.meaning_id) this.router.route(`#/meaning/${example.meaning_id}`);
  }

  toggleReplacements(example) {
    const key = this.identifyExample(example);
    this.replacementsByKey = { ...this.replacementsByKey, [key]: !this.replacementsByKey[key] };
  }

  showReplacements(example) {
    return Boolean(this.replacementsByKey[this.identifyExample(example)]);
  }

  home() {
    this.router.route("#/home");
  }

  joinWords(words) {
    return Array.isArray(words) && words.length ? words.join(", ") : "";
  }

  render(sentence) {
    return String(sentence || "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll("&lt;em&gt;", "<em>")
      .replaceAll("&lt;/em&gt;", "</em>");
  }

  startLoading(message) {
    this.isLoading = true;
    this.emptyMessage = "";
    this.showStatus(message);
  }

  showStatus(message) {
    this.isError = false;
    this.status = message;
  }

  showError(message) {
    this.isError = true;
    this.examples = [];
    this.emptyMessage = "";
    this.status = message;
  }

  showAppendError(message) {
    this.isError = true;
    this.status = message;
  }
}
