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
    this.startLoading();
    try {
      this.showExamples(await this.bookmarkApi.listExamples());
    } catch {
      this.showError("Could not reach the server.");
    }
    this.isLoading = false;
  }

  showExamples(result) {
    if (!result.response.ok) return this.showError(result.body.error?.message || "Could not load examples.");
    this.examples = result.body.data;
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
    this.examples = [];
    this.status = message;
  }
}
