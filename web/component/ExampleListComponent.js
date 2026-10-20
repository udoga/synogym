class ExampleListComponent {
  constructor(router, bookmarkApi) {
    this.router = router;
    this.bookmarkApi = bookmarkApi;
    this.examples = [];
    this.status = "";
    this.isError = false;
    this.isLoading = false;
  }

  async load() {
    this.startLoading("Loading...");
    try {
      this.showExamples(await this.bookmarkApi.listExamples());
    } catch {
      this.showError("Could not reach the server.");
    }
    this.isLoading = false;
  }

  async loadMore() {
    this.startLoading("Loading more...");
    try {
      this.addExamples(await this.bookmarkApi.listExamples());
    } catch {
      this.showAppendError("Could not reach the server.");
    }
    this.isLoading = false;
  }

  showExamples(result) {
    if (!result.response.ok) return this.showError(result.body.error?.message || "Could not load examples.");
    this.examples = result.body.data;
    this.showStatus(this.examples.length ? "Examples" : "No saved examples yet.");
  }

  addExamples(result) {
    if (!result.response.ok) return this.showAppendError(result.body.error?.message || "Could not load examples.");
    this.examples = [...this.examples, ...result.body.data];
    this.showStatus(this.examples.length ? "Examples" : "No saved examples yet.");
  }

  openExample(example) {
    if (example?.meaning_id) this.router.route(`#/meaning/${example.meaning_id}`);
  }

  home() {
    this.router.route("#/home");
  }

  joinWords(words) {
    return Array.isArray(words) && words.length ? words.join(", ") : "";
  }

  startLoading(message) {
    this.isLoading = true;
    this.showStatus(message);
  }

  showStatus(message) {
    this.isError = false;
    this.status = message;
  }

  showError(message) {
    this.isError = true;
    this.examples = [];
    this.status = message;
  }

  showAppendError(message) {
    this.isError = true;
    this.status = message;
  }
}
