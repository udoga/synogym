class MeaningApi extends JsonApi {
  list(query) {
    return this.get(`/meanings/${encodeURIComponent(query)}`);
  }

  read(id) {
    return this.get(`/meanings/${encodeURIComponent(id)}`);
  }

  listExamples(id) {
    return this.get(`/meanings/${encodeURIComponent(id)}/examples`);
  }

  readDetail(id) {
    return this.get(`/meanings/${encodeURIComponent(id)}/detail`);
  }
}
