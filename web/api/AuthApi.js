class AuthApi extends JsonApi {
  config() {
    return this.get("/auth/config");
  }

  me() {
    return this.get("/auth/me");
  }

  signIn(credentials) {
    return this.post("/auth/sign-in", credentials);
  }

  signUp(credentials) {
    return this.post("/auth/sign-up", credentials);
  }

  google(credential) {
    return this.post("/auth/google", { credential });
  }

  logout() {
    return this.post("/auth/logout", {});
  }
}
