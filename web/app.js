document.addEventListener("alpine:init", () => Alpine.data("synogym", () => new Synogym()));

class QuoteLoader {
  constructor() {
    this.quotes = [];
    this.isLoading = false;
  }

  reset() {
    this.quotes = [];
    this.isLoading = false;
  }

  load(word) {
    if (!word) return;
    this._startLoading();
    return this._fetchQuotes(word);
  }

  _startLoading() {
    this.quotes = [];
    this.isLoading = true;
  }

  async _fetchQuotes(word) {
    try {
      await this._showResponse(await fetch(`/quotes/${encodeURIComponent(word)}`));
    } catch {
    } finally {
      this.isLoading = false;
    }
  }

  async _showResponse(response) {
    if (!response.ok) return;
    const body = await response.json();
    this.quotes = body.data;
  }
}

class Synogym {
  constructor() {
    this.query = "";
    this.status = "";
    this.isError = false;
    this.isLoading = false;
    this.view = "list";
    this.listTitle = "Bookmarks";
    this.meanings = [];
    this.selectedMeaning = null;
    this.selectedBookmark = null;
    this.newBookmarkTag = "";
    this.quoteLoader = new QuoteLoader();
    this.user = null;
    this.email = "";
    this.password = "";
    this.authMode = "sign-in";
    this.authStatus = "";
    this.googleClientId = "";
  }

  async init() {
    await this.fetchAuthConfig();
    await this.fetchCurrentUser();
    await this.fetchBookmarks();
    this.renderGoogleButton();
  }

  async fetchAuthConfig() {
    try {
      const response = await fetch("/auth/config");
      this.googleClientId = (await response.json()).data.google_client_id || "";
    } catch {}
  }

  async fetchCurrentUser() {
    try {
      const response = await fetch("/auth/me");
      this.user = (await response.json()).data;
    } catch {}
  }

  renderGoogleButton() {
    if (this.user || !this.googleClientId) return;
    if (!window.google?.accounts?.id) return setTimeout(() => this.renderGoogleButton(), 100);
    if (!this._getGoogleButtonWidth()) return setTimeout(() => this.renderGoogleButton(), 100);
    this.initializeGoogleButton();
  }

  initializeGoogleButton() {
    const button = document.getElementById("google-signin-button");
    const callback = response => this.signInWithGoogle(response.credential);
    button.innerHTML = "";
    google.accounts.id.initialize({ client_id: this.googleClientId, callback });
    const options = { theme: "outline", size: "large", text: "continue_with", width: this._getGoogleButtonWidth() };
    google.accounts.id.renderButton(button, options);
  }

  _getGoogleButtonWidth() {
    const width = document.getElementById("google-signin-button")?.getBoundingClientRect().width || 0;
    return Math.max(0, Math.floor(width) - 2);
  }

  signInWithGoogle(credential) {
    if (!credential) return this.showAuthError("Google did not return a credential.");
    return this.requestGoogleSignIn(credential);
  }

  async requestGoogleSignIn(credential) {
    this.isLoading = true;
    this.authStatus = "Signing in with Google...";
    try {
      await this.renderGoogleSignInResponse(await this.postJson("/auth/google", { credential }));
    } catch {
      this.showAuthError("Could not reach the server.");
    } finally {
      this.isLoading = false;
    }
  }

  async renderGoogleSignInResponse(response) {
    const body = await response.json();
    if (!response.ok) return this.showAuthError(body.error?.message || "Google sign-in failed.");
    this.setUser(body.data);
  }

  submitAuth() {
    return this.authMode === "sign-up" ? this.signUp() : this.signIn();
  }

  async signIn() {
    this.startLoading();
    await this.requestSignIn();
    this.stopLoading();
  }

  async requestSignIn() {
    try {
      const body = { email: this.email, password: this.password };
      await this.renderSignInResponse(await this.postJson("/auth/sign-in", body));
    } catch {
      this.showAuthError("Could not reach the server.");
    }
  }

  async renderSignInResponse(response) {
    const body = await response.json();
    if (!response.ok) return this.showAuthError(body.error?.message || "Sign-in failed.");
    this.setUser(body.data);
  }

  async signUp() {
    this.startLoading();
    await this.requestSignUp();
    this.stopLoading();
  }

  async requestSignUp() {
    try {
      const body = { email: this.email, password: this.password };
      await this.renderSignUpResponse(await this.postJson("/auth/sign-up", body));
    } catch {
      this.showAuthError("Could not reach the server.");
    }
  }

  async renderSignUpResponse(response) {
    const body = await response.json();
    if (!response.ok) return this.showAuthError(body.error?.message || "Sign-up failed.");
    this.setUser(body.data);
  }

  toggleAuthMode() {
    this.authMode = this.authMode === "sign-up" ? "sign-in" : "sign-up";
    this.authStatus = "";
    this.password = "";
  }

  authSubmitText() {
    return this.authMode === "sign-up" ? "Create account" : "Sign in";
  }

  authSwitchText() {
    return this.authMode === "sign-up" ? "Sign in" : "Create an account";
  }

  passwordAutocomplete() {
    return this.authMode === "sign-up" ? "new-password" : "current-password";
  }

  setUser(user) {
    this.user = user;
    this.password = "";
    this.authStatus = "";
    this.isError = false;
    this.fetchBookmarks();
  }

  async logout() {
    await this.postJson("/auth/logout", {});
    this.user = null;
    this.meanings = [];
    this.status = "";
    this.renderGoogleButton();
  }

  searchMeanings() {
    const query = this.query.trim();
    if (!query) return;
    return this.fetchMeanings(query);
  }

  showBookmarksWhenQueryCleared() {
    if (this.query.trim()) return;
    return this.fetchBookmarks();
  }

  async fetchBookmarks() {
    if (!this.user) return;
    this.startLoading();
    await this.requestBookmarks();
    this.stopLoading();
  }

  async requestBookmarks() {
    try {
      await this.renderBookmarksResponse(await fetch("/bookmarks/with-meaning"));
    } catch {
      this.showError("Could not reach the server.");
    }
  }

  async renderBookmarksResponse(response) {
    const body = await response.json();
    if (!response.ok) return this.showError(body.error?.message || "Could not load bookmarks.");
    this.showBookmarkedMeanings(body.data);
  }

  showBookmarkedMeanings(bookmarks) {
    this.meanings = bookmarks.map(bookmark => ({ ...bookmark.meaning, bookmark }));
    this.view = "list";
    this.listTitle = "Bookmarks";
    this.selectedMeaning = null;
    this.showStatus(this.meanings.length ? this.listTitle : "No bookmarks yet.");
  }

  async fetchMeanings(query) {
    this.startLoading();
    await this.requestMeanings(query);
    this.stopLoading();
  }

  async requestMeanings(query) {
    try {
      await this.renderMeaningsResponse(await fetch(`/meanings/${encodeURIComponent(query)}`));
    } catch {
      this.showError("Could not reach the server.");
    }
  }

  async renderMeaningsResponse(response) {
    const body = await response.json();
    if (!response.ok) return this.showError(body.error?.message || "Search failed.");
    this.showMeanings(body.data);
  }

  showMeanings(meanings) {
    this.meanings = meanings;
    this.view = "list";
    this.listTitle = "Meanings";
    this.selectedMeaning = null;
    this.showStatus(meanings.length ? this.listTitle : "No meanings found.");
  }

  async fetchMeaningDetail(meaningId) {
    if (!meaningId) return;
    this.startLoading();
    await this.requestMeaningDetail(meaningId);
    this.stopLoading();
  }

  async requestMeaningDetail(meaningId) {
    try {
      await this.renderDetailResponse(await fetch(`/meanings/${meaningId}`));
    } catch {
      this.showError("Could not reach the server.");
    }
  }

  async renderDetailResponse(response) {
    const body = await response.json();
    if (!response.ok) return this.showError(body.error?.message || "Could not load detail.");
    this.showDetail(body.data);
  }

  showDetail(meaning) {
    this.selectedMeaning = meaning;
    this.selectedBookmark = null;
    this.newBookmarkTag = "";
    this.quoteLoader.reset();
    this.view = "detail";
    this.fetchBookmark(meaning.id);
    this.quoteLoader.load(meaning.query);
    this.showStatus("Word Details");
  }

  showMeaningList() {
    this.view = "list";
    this.selectedMeaning = null;
    this.selectedBookmark = null;
    this.newBookmarkTag = "";
    this.showStatus(this.meanings.length ? this.listTitle : "No meanings found.");
  }

  async fetchBookmark(meaningId) {
    try {
      const response = await fetch(`/bookmarks?meaning_id=${encodeURIComponent(meaningId)}`);
      if (response.ok) this.showBookmark((await response.json()).data[0] || null);
    } catch {}
  }

  showBookmark(bookmark) {
    this.selectedBookmark = bookmark;
  }

  async saveBookmark() {
    if (this.selectedBookmark) return this.deleteBookmark();
    if (!this.selectedMeaning?.id) return;
    const response = await this.postJson("/bookmarks", { meaning_id: this.selectedMeaning.id });
    if (response.ok) this.selectedBookmark = (await response.json()).data;
  }

  async deleteBookmark() {
    if (!this.selectedBookmark || !window.confirm("Remove the bookmark?")) return;
    const bookmark = this.selectedBookmark;
    this.selectedBookmark = null;
    this.newBookmarkTag = "";
    const response = await this.deleteJson(`/bookmarks/${bookmark.id}`);
    if (!response.ok) this.selectedBookmark = bookmark;
  }

  async updateBookmark() {
    if (!this.selectedBookmark?.id) return;
    const response = await this.putJson(`/bookmarks/${this.selectedBookmark.id}`, this._getBookmarkBody());
    if (response.ok) this.selectedBookmark = (await response.json()).data;
  }

  bookmarkTags() {
    return this._splitTags(this.selectedBookmark?.tags || "");
  }

  addBookmarkTag() {
    const tag = this._cleanTag(this.newBookmarkTag);
    if (!tag) return;
    this.newBookmarkTag = "";
    return this._saveBookmarkTags([...this.bookmarkTags(), tag]);
  }

  removeBookmarkTag(tag) {
    return this._saveBookmarkTags(this.bookmarkTags().filter(bookmarkTag => bookmarkTag !== tag));
  }

  _saveBookmarkTags(tags) {
    this.selectedBookmark.tags = [...new Set(tags.map(tag => this._cleanTag(tag)).filter(Boolean))].join(", ");
    return this.updateBookmark();
  }

  _getBookmarkBody() {
    return { note: this.selectedBookmark.note || "", tags: this.selectedBookmark.tags || "" };
  }

  _splitTags(tags) {
    return tags.split(",").map(tag => this._cleanTag(tag)).filter(Boolean);
  }

  _cleanTag(tag) {
    return String(tag || "").trim();
  }

  searchWord(word) {
    this.query = word;
    return this.fetchMeanings(word);
  }

  detail() {
    return { ...this._createEmptyDetail(), ...this.selectedMeaning?.detail };
  }

  hasWords(words) {
    return Array.isArray(words) && words.length > 0;
  }

  joinWords(words) {
    return this.hasWords(words) ? words.join(", ") : "";
  }

  getLevelClass(level) {
    return level ? `level-${String(level).toLowerCase()}` : "";
  }

  isPageHeader() {
    return ["Bookmarks", "Meanings", "Word Details"].includes(this.status) && !this.isLoading && !this.isError;
  }

  postJson(url, body) {
    return fetch(url, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
  }

  putJson(url, body) {
    return fetch(url, { method: "PUT", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
  }

  deleteJson(url) {
    return fetch(url, { method: "DELETE" });
  }

  startLoading() {
    this.isLoading = true;
    this.showStatus("Loading...");
  }

  stopLoading() {
    this.isLoading = false;
  }

  showStatus(message) {
    this.isError = false;
    this.status = message;
  }

  showError(message) {
    this.view = "list";
    this.meanings = [];
    this.selectedMeaning = null;
    this.selectedBookmark = null;
    this.newBookmarkTag = "";
    this.isError = true;
    this.status = message;
  }

  showAuthError(message) {
    this.authStatus = message;
  }

  _createEmptyDetail() {
    return { examples: [], synonyms: [], formations: [] };
  }

}
