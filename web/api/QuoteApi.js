class QuoteApi extends JsonApi {
  list(word, pos) {
    return this.get(`/quotes/${encodeURIComponent(word)}/${encodeURIComponent(pos)}`);
  }
}
