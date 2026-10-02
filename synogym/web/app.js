document.addEventListener("alpine:init", () => Alpine.data("synogym", () => new Synogym()));

class Synogym {
  constructor() {
    this.query = "";
    this.status = "";
    this.isError = false;
    this.isLoading = false;
    this.view = "list";
    this.meanings = [];
    this.selectedMeaning = null;
    this.quotes = [];
    this.quotesLoaded = false;
    this.user = null;
    this.email = "";
    this.password = "";
    this.authStatus = "";
    this.googleClientId = "";
  }

  async init() {
    await this.fetchAuthConfig();
    await this.fetchCurrentUser();
    this.renderGoogleButton();
  }

  async fetchAuthConfig() {
    try {
      const response = await fetch("/auth/config");
      this.googleClientId = (await response.json()).google_client_id || "";
    } catch {}
  }

  async fetchCurrentUser() {
    try {
      const response = await fetch("/auth/me");
      this.user = (await response.json()).user;
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
    google.accounts.id.renderButton(button, { theme: "outline", size: "large", width: this._getGoogleButtonWidth() });
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
    this.setUser(body.user);
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
    this.setUser(body.user);
  }

  setUser(user) {
    this.user = user;
    this.password = "";
    this.authStatus = "";
    this.status = "";
    this.isError = false;
  }

  async logout() {
    await this.postJson("/auth/logout", {});
    this.user = null;
    this.renderGoogleButton();
  }

  searchMeanings() {
    const query = this.query.trim();
    if (!query) return;
    return this.fetchMeanings(query);
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
    this.showMeanings(body);
  }

  showMeanings(meanings) {
    this.meanings = meanings;
    this.view = "list";
    this.selectedMeaning = null;
    this.showStatus(meanings.length ? "Meanings" : "No meanings found.");
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
    this.showDetail(body);
  }

  showDetail(meaning) {
    this.selectedMeaning = meaning;
    this.quotes = [];
    this.quotesLoaded = false;
    this.view = "detail";
    this.showStatus("Meaning Detail");
  }

  showMeaningList() {
    this.view = "list";
    this.selectedMeaning = null;
    this.showStatus(this.meanings.length ? "Meanings" : "No meanings found.");
  }

  searchWord(word) {
    this.query = word;
    return this.fetchMeanings(word);
  }

  async fetchQuotes(query) {
    this.startLoading();
    await this.requestQuotes(query);
    this.stopLoading();
  }

  async requestQuotes(query) {
    try {
      await this.renderQuoteResponse(await fetch(`/quotes/${encodeURIComponent(query)}`));
    } catch {
      this.showError("Could not reach the server.");
    }
  }

  async renderQuoteResponse(response) {
    const body = await response.json();
    if (!response.ok) return this.showError(body.error?.message || "Could not load quotes.");
    this.showQuotes(body);
  }

  showQuotes(quotes) {
    this.quotes = quotes;
    this.quotesLoaded = true;
    this.showStatus("Meaning Detail");
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

  postJson(url, body) {
    return fetch(url, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
  }

  highlightParts(sentence, word) {
    const text = String(sentence || "");
    if (!word) return [{ text, highlight: false }];
    return this._splitHighlightParts(text, this._createHighlightRegex(word));
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
    this.isError = true;
    this.status = message;
  }

  showAuthError(message) {
    this.authStatus = message;
  }

  _createEmptyDetail() {
    return { examples: [], synonyms: [], formations: [] };
  }

  _splitHighlightParts(text, regex) {
    const parts = [];
    let cursor = 0;
    for (const match of text.matchAll(regex)) cursor = this._addHighlightMatch(parts, text, match, cursor);
    this._addPlainPart(parts, text.slice(cursor));
    return parts;
  }

  _addHighlightMatch(parts, text, match, cursor) {
    this._addPlainPart(parts, text.slice(cursor, match.index));
    parts.push({ text: match[0], highlight: true });
    return match.index + match[0].length;
  }

  _addPlainPart(parts, text) {
    if (text) parts.push({ text, highlight: false });
  }

  _createHighlightRegex(word) {
    const base = this._escapeRegExp(String(word));
    return new RegExp(`\\b(${base}(?:d|ed)?)\\b`, "gi");
  }

  _escapeRegExp(value) {
    return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  }
}
