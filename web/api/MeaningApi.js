class MeaningApi extends JsonApi {
  list(query) {
    return this.get(`/meanings/${encodeURIComponent(query)}`);
  }

  read(id) {
    return this.get(`/meanings/${encodeURIComponent(id)}`);
  }
}
