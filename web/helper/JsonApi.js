class JsonApi {
  getJson(request) {
    return request.then(response => response.json().then(body => ({ response, body })));
  }

  get(url) {
    return this.getJson(fetch(url));
  }

  post(url, body) {
    return this.sendJson("POST", url, body);
  }

  put(url, body) {
    return this.sendJson("PUT", url, body);
  }

  delete(url) {
    return this.getJson(fetch(url, { method: "DELETE" }));
  }

  sendJson(method, url, body) {
    const options = { method, headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) };
    return this.getJson(fetch(url, options));
  }
}
