PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS meanings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query TEXT NOT NULL,
    definition TEXT NOT NULL,
    pos TEXT NOT NULL,
    UNIQUE (query, definition, pos)
);

CREATE TABLE IF NOT EXISTS detailed_meanings (
    meaning_id INTEGER PRIMARY KEY,
    level TEXT NOT NULL,
    description TEXT NOT NULL,
    synonyms TEXT NOT NULL DEFAULT '[]',
    history TEXT NOT NULL,
    related TEXT NOT NULL DEFAULT '[]',
    FOREIGN KEY (meaning_id) REFERENCES meanings(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS examples (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    meaning_id INTEGER NOT NULL,
    sentence TEXT NOT NULL,
    replacements TEXT NOT NULL DEFAULT '[]',
    FOREIGN KEY (meaning_id) REFERENCES meanings(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_meanings_query ON meanings(query);
CREATE INDEX IF NOT EXISTS idx_examples_meaning_id ON examples(meaning_id);
