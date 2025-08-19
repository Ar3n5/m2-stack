CREATE TABLE IF NOT EXISTS current_name (
  id INT PRIMARY KEY,
  name TEXT NOT NULL
);

INSERT INTO current_name (id, name) VALUES (1, 'Your Name')
ON CONFLICT (id) DO NOTHING;
