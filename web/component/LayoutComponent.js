class LayoutComponent {
  constructor(authApi, router) {
    this.authApi = authApi;
    this.router = router;
    this.query = "";
    this.user = router.user;
  }

  load() {
    this.user = this.router.user;
  }

  search() {
    const query = this.query.trim();
    if (!query) return;
    this.router.route(`#/meanings?query=${encodeURIComponent(query)}`);
  }

  async logout() {
    await this.authApi.logout();
    this.router.logout();
  }

  username() {
    const firstName = this.user?.first_name || "";
    const lastName = this.user?.last_name || "";
    const name = `${firstName} ${lastName}`.trim() || this.user?.email || "";
    return name.split("@")[0];
  }
}
