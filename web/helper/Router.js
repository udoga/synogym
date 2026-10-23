class Router {
  constructor(authApi) {
    this.authApi = authApi;
    this.nestedNodes = [];
    this.user = null;
    this.isReady = false;
  }

  async refresh() {
    await this.loadUser();
    this.redirectIfNeeded();
    this.reloadNodes();
  }

  route(hashUrl) {
    location.hash = hashUrl;
  }

  async loadUser() {
    if (this.isReady) return;
    try {
      const result = await this.authApi.me();
      this.user = result.response.ok ? result.body.data : null;
    } catch {
      this.user = null;
    }
    this.isReady = true;
  }

  redirectIfNeeded() {
    const hashUrl = location.hash;
    if (!this.user && hashUrl !== "#/login") this.redirect("#/login");
    if (this.user && ["", "#", "#/", "#/login"].includes(hashUrl)) this.redirect("#/home");
  }

  redirect(hashUrl) {
    if (location.hash === hashUrl) return;
    history.replaceState(null, "", hashUrl);
  }

  login(user) {
    this.user = user;
    this.isReady = true;
    this.refresh();
  }

  logout() {
    this.user = null;
    this.isReady = true;
    this.refresh();
  }

  loadNode(element) {
    const view = this.findViews()[this.nestedNodes.length];
    if (!view) return;
    this.nestedNodes.push({ element, view });
    fetch(`/web/view/${view}.html`).then(response => response.text()).then(html => {
      element.innerHTML = html;
    });
  }

  reloadNodes() {
    const views = this.findViews();
    let index = 0;
    while (index < this.nestedNodes.length && this.nestedNodes[index].view === views[index]) index++;
    this.nestedNodes = this.nestedNodes.slice(0, index + 1);
    if (this.nestedNodes.length) this.loadNode(this.nestedNodes.pop().element);
  }

  getId() {
    const parts = this.getUrlWithoutQuery().split("/");
    return parts[parts.length - 1] || null;
  }

  getUrlWithoutQuery() {
    const index = location.hash.indexOf("?");
    return index === -1 ? location.hash : location.hash.substring(0, index);
  }

  getUrlParams() {
    if (!location.hash.includes("?")) return {};
    return Object.fromEntries(new URLSearchParams(location.hash.substring(location.hash.indexOf("?") + 1)));
  }

  findViews() {
    if (!this.user) return ["login"];
    if (location.hash.startsWith("#/home")) return ["layout", "home"];
    if (location.hash.startsWith("#/meanings")) return ["layout", "meaning-list"];
    if (location.hash.startsWith("#/meaning/")) return ["layout", "meaning-detail"];
    if (location.hash.startsWith("#/bookmarks/examples")) return ["layout", "example-list"];
    if (location.hash.startsWith("#/bookmarks")) return ["layout", "meaning-list"];
    return ["layout", "not-found"];
  }
}
