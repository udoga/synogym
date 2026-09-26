const form = document.querySelector("#search-form");
const input = document.querySelector("#query-input");
const button = document.querySelector("#search-button");
const statusText = document.querySelector("#status");
const results = document.querySelector("#results");

form.addEventListener("submit", searchMeanings);

async function searchMeanings(event) {
  event.preventDefault();
  const query = input.value.trim();
  if (!query) return;
  await fetchMeanings(query);
}

async function fetchMeanings(query) {
  setLoading(true);
  await requestMeanings(query);
  setLoading(false);
}

async function requestMeanings(query) {
  try {
    await renderResponse(await fetch(`/meanings/${encodeURIComponent(query)}`));
  } catch {
    showError("Could not reach the server.");
  }
}

async function renderResponse(response) {
  const body = await response.json();
  if (!response.ok) return showError(body.error?.message || "Search failed.");
  renderMeanings(body);
}

function renderMeanings(meanings) {
  results.replaceChildren(...meanings.map(createMeaningCard));
  const text = meanings.length ? `${meanings.length} meaning(s) found.` : "No meanings found.";
  showStatus(text);
}

function createMeaningCard(meaning) {
  const card = document.createElement("article");
  card.className = "meaning-card";
  card.innerHTML = createMeaningHtml(meaning);
  return card;
}

function createMeaningHtml(meaning) {
  const query = escapeHtml(meaning.query);
  const pos = escapeHtml(meaning.pos);
  const definition = escapeHtml(meaning.definition);
  return `<h2>${query}<span class="pos">${pos}</span></h2><p>${definition}</p>`;
}

function setLoading(isLoading) {
  button.disabled = isLoading;
  input.disabled = isLoading;
  if (isLoading) showStatus("Searching...");
}

function showStatus(message) {
  statusText.className = "status";
  statusText.textContent = message;
}

function showError(message) {
  results.replaceChildren();
  statusText.className = "status error";
  statusText.textContent = message;
}

function escapeHtml(value) {
  const element = document.createElement("span");
  element.textContent = value ?? "";
  return element.innerHTML;
}
