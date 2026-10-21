class HomeComponent {
  constructor(router) {
    this.router = router;
  }

  openMeanings() {
    this.router.route("#/bookmarks/meanings");
  }

  openExamples() {
    this.router.route("#/bookmarks/examples");
  }

  openNotes() {
    this.router.route("#/bookmarks/meanings?notes=true");
  }
}
