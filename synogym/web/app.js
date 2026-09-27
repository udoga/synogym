const form = document.querySelector("#search-form");
const input = document.querySelector("#query-input");
const button = document.querySelector("#search-button");
const statusText = document.querySelector("#status");
const backButton = document.querySelector("#back-button");
const results = document.querySelector("#results");
let currentMeanings = [];

form.addEventListener("submit", searchMeanings);
backButton.addEventListener("click", showMeaningList);
results.addEventListener("click", handleResultsClick);

async function searchMeanings(event) {
  event.preventDefault();
  const query = input.value.trim();
  if (!query) return;
  await fetchMeanings(query);
}

async function fetchMeanings(query) {
  backButton.hidden = true;
  setLoading(true);
  await requestMeanings(query);
  setLoading(false);
}

async function requestMeanings(query) {
  try {
    await renderSearchResponse(await fetch(`/meanings/${encodeURIComponent(query)}`));
  } catch {
    showError("Could not reach the server.");
  }
}

async function renderSearchResponse(response) {
  const body = await response.json();
  if (!response.ok) return showError(body.error?.message || "Search failed.");
  renderMeanings(body);
}

function renderMeanings(meanings) {
  currentMeanings = meanings;
  backButton.hidden = true;
  results.replaceChildren(...meanings.map(createMeaningCard));
  showStatus(meanings.length ? "Meanings" : "No meanings found.");
}

function createMeaningCard(meaning) {
  const card = document.createElement("button");
  card.className = "meaning-card";
  card.type = "button";
  card.dataset.meaningId = meaning.id ?? "";
  card.innerHTML = createMeaningHtml(meaning);
  return card;
}

function createMeaningHtml(meaning) {
  const query = escapeHtml(meaning.query);
  const pos = escapeHtml(meaning.pos);
  const definition = escapeHtml(meaning.definition);
  return `<h2>${query}<span class="pos">${pos}</span></h2><p>${definition}</p>`;
}

async function handleResultsClick(event) {
  const wordButton = event.target.closest("[data-search-word]");
  if (wordButton) return searchWord(wordButton.dataset.searchWord);
  await openMeaningDetail(event);
}

async function searchWord(word) {
  input.value = word;
  await fetchMeanings(word);
}

async function openMeaningDetail(event) {
  const card = event.target.closest("[data-meaning-id]");
  if (!card?.dataset.meaningId) return;
  await fetchMeaningDetail(card.dataset.meaningId);
}

async function fetchMeaningDetail(meaningId) {
  setLoading(true);
  await requestMeaningDetail(meaningId);
  setLoading(false);
}

async function requestMeaningDetail(meaningId) {
  try {
    await renderDetailResponse(await fetch(`/meanings/${meaningId}`));
  } catch {
    showError("Could not reach the server.");
  }
}

async function renderDetailResponse(response) {
  const body = await response.json();
  if (!response.ok) return showError(body.error?.message || "Could not load detail.");
  renderDetail(body);
}

function renderDetail(meaning) {
  backButton.hidden = false;
  results.replaceChildren(createDetailPanel(meaning));
  showStatus("Meaning Detail");
}

function showMeaningList() {
  renderMeanings(currentMeanings);
}

function createDetailPanel(meaning) {
  const panel = document.createElement("article");
  panel.className = "detail-panel";
  panel.innerHTML = createDetailHtml(meaning);
  return panel;
}

function createDetailHtml(meaning) {
  const detail = meaning.detail || {};
  return `${createDetailHeader(meaning, detail)}${createDetailBody(detail, meaning.query)}`;
}

function createDetailHeader(meaning, detail) {
  const query = escapeHtml(meaning.query);
  const pos = escapeHtml(meaning.pos);
  const level = createLevelTag(detail.level);
  return `<section class="detail-card detail-header"><h2>${query}<span class="pos">${pos}</span>${level}</h2>` +
    `<p>${escapeHtml(meaning.definition)}</p></section>`;
}

function createLevelTag(level) {
  if (!level) return "";
  const className = `level-tag ${getLevelClass(level)}`;
  return `<span class="${className}">${escapeHtml(level)}</span>`;
}

function getLevelClass(level) {
  return `level-${String(level).toLowerCase()}`;
}

function createDetailBody(detail, query) {
  return `${createExamples(detail.examples, query)}${createList("Synonyms", detail.synonyms)}` +
    `${createList("Formations", detail.formations)}${createField("Description", detail.description)}` +
    `${createField("History", detail.history)}`;
}

function createField(title, value) {
  if (!value) return "";
  return `<section class="detail-card"><h3>${title}</h3><p>${escapeHtml(value)}</p></section>`;
}

function createList(title, values) {
  if (!values?.length) return "";
  return `<section class="detail-card"><h3>${title}</h3><p>${values.map(createWordButton).join(" ")}</p></section>`;
}

function createWordButton(word) {
  const safeWord = escapeHtml(word);
  return `<button class="word-button" type="button" data-search-word="${safeWord}">${safeWord}</button>`;
}

function createExamples(examples, query) {
  if (!examples?.length) return "";
  const content = examples.map((example) => createExample(example, query)).join("");
  return `<section class="detail-card"><h3>Examples</h3>${content}</section>`;
}

function createExample(example, query) {
  const replacements = example.replacements?.map(escapeHtml).join(", ") || "";
  return `<p>${highlightWord(example.sentence, query)}<br><small>${replacements}</small></p>`;
}

function highlightWord(sentence, word) {
  const text = escapeHtml(sentence);
  if (!word) return text;
  const regex = new RegExp(`\\b(${escapeRegExp(escapeHtml(word))})\\b`, "gi");
  return text.replace(regex, "<mark>$1</mark>");
}

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function setLoading(isLoading) {
  button.disabled = isLoading;
  input.disabled = isLoading;
  if (isLoading) showStatus("Loading...");
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
