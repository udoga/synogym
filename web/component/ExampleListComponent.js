class ExampleListComponent {
  constructor(router, bookmarkApi) {
    this.router = router;
    this.bookmarkApi = bookmarkApi;
    this.examples = [];
    this.status = "";
    this.emptyMessage = "";
    this.isError = false;
    this.isLoading = false;
  }

  async load() {
    this.startLoading("Examples");
    try {
      this.showExamples(await this.bookmarkApi.listExamples());
    } catch {
      this.showError("Could not reach the server.");
    }
    this.isLoading = false;
  }

  async loadMore() {
    this.startLoading("Examples");
    try {
      this.addExamples(await this.bookmarkApi.listExamples());
    } catch {
      this.showAppendError("Could not reach the server.");
    }
    this.isLoading = false;
  }

  showExamples(result) {
    if (!result.response.ok) return this.showError(result.body.error?.message || "Could not load examples.");
    this.examples = this.deduplicateExamples(result.body.data);
    this.emptyMessage = this.examples.length ? "" : "Examples appear here once you save a word.";
    this.showStatus("Examples");
  }

  addExamples(result) {
    if (!result.response.ok) return this.showAppendError(result.body.error?.message || "Could not load examples.");
    this.examples = this.deduplicateExamples([...this.examples, ...result.body.data]);
    this.emptyMessage = this.examples.length ? "" : "Examples appear here once you save a word.";
    this.showStatus("Examples");
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

  home() {
    this.router.route("#/home");
  }

  joinWords(words) {
    return Array.isArray(words) && words.length ? words.join(", ") : "";
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
