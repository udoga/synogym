class LoginComponent {
  constructor(authApi, router) {
    this.authApi = authApi;
    this.router = router;
    this.email = "";
    this.password = "";
    this.authMode = "sign-in";
    this.status = "";
    this.isLoading = false;
    this.googleClientId = "";
  }

  async load() {
    await this.loadConfig();
    this.renderGoogleButton();
  }

  async loadConfig() {
    try {
      const result = await this.authApi.config();
      this.googleClientId = result.body.data.google_client_id || "";
    } catch {}
  }

  renderGoogleButton() {
    if (!this.googleClientId) return;
    if (!window.google?.accounts?.id) return setTimeout(() => this.renderGoogleButton(), 100);
    if (!this.getButtonWidth()) return setTimeout(() => this.renderGoogleButton(), 100);
    this.initializeGoogleButton();
  }

  initializeGoogleButton() {
    const button = document.getElementById("google-signin-button");
    button.innerHTML = "";
    google.accounts.id.initialize({ client_id: this.googleClientId, callback: r => this.signInWithGoogle(r.credential) });
    google.accounts.id.renderButton(button, this.getGoogleButtonOptions());
  }

  getGoogleButtonOptions() {
    return { theme: "outline", size: "large", text: "continue_with", width: this.getButtonWidth() };
  }

  getButtonWidth() {
    const button = document.querySelector(".sign-in-form button");
    return Math.floor(button?.getBoundingClientRect().width || 0);
  }

  submit() {
    return this.authMode === "sign-up" ? this.signUp() : this.signIn();
  }

  async signIn() {
    await this.request(() => this.authApi.signIn(this.getCredentials()), "Sign-in failed.");
  }

  async signUp() {
    await this.request(() => this.authApi.signUp(this.getCredentials()), "Sign-up failed.");
  }

  async signInWithGoogle(credential) {
    if (!credential) return this.showError("Google did not return a credential.");
    await this.request(() => this.authApi.google(credential), "Google sign-in failed.");
  }

  async request(callApi, fallbackMessage) {
    this.startLoading();
    try {
      this.acceptResult(await callApi(), fallbackMessage);
    } catch {
      this.showError("Could not reach the server.");
    }
    this.isLoading = false;
  }

  acceptResult(result, fallbackMessage) {
    if (!result.response.ok) return this.showError(result.body.error?.message || fallbackMessage);
    this.password = "";
    this.router.login(result.body.data);
  }

  setAuthMode(authMode) {
    this.authMode = authMode;
    this.status = "";
    this.password = "";
  }

  submitText() {
    return this.authMode === "sign-up" ? "Register with Email" : "Sign In with Email";
  }

  passwordAutocomplete() {
    return this.authMode === "sign-up" ? "new-password" : "current-password";
  }

  getCredentials() {
    return { email: this.email, password: this.password };
  }

  startLoading() {
    this.isLoading = true;
    this.status = "";
  }

  showError(message) {
    this.status = message;
  }
}
