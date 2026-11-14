class LayoutComponent {
  constructor(authApi, router) {
    this.authApi = authApi;
    this.router = router;
    this.query = "";
  }

  search() {
    const query = this.query.trim();
    if (!query) return;
    this.router.route(`#/meanings?query=${encodeURIComponent(query)}`);
  }

  home() {
    this.router.route("#/home");
  }

  async logout() {
    await this.authApi.logout();
    this.router.logout();
  }

}
