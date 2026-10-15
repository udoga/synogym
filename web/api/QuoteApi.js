class QuoteApi extends JsonApi {
  list(word) {
    return this.get(`/quotes/${encodeURIComponent(word)}`);
  }
}
