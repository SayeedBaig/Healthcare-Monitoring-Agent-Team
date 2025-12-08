CREATE TABLE IF NOT EXISTS medicines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    use_case TEXT,
    side_effects TEXT,
    precautions TEXT
);

CREATE TABLE IF NOT EXISTS interactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    medicine1 TEXT,
    medicine2 TEXT,
    description TEXT
);
