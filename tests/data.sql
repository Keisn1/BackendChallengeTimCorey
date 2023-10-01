INSERT INTO clients (client_name, client_email, password)
VALUES
  ('test_name1', 'test_email1', 'pbkdf2:sha256:600000$TTYIvmjBeLhzFi0Y$5da7d9c678493068417ec618fa1cb8b8db9ffb59893f593a37054dc26f04e150'),
  ('test_name2', 'test_email2', 'pbkdf2:sha256:600000$WF5jQYsC9LEGHQFS$0945b5afb0ecfea079d86c860d5f98a31a247d750bdd3587500c23fe0669cc10');

INSERT INTO post (title, body, client_id, created)
VALUES
  ('test title', 'test' || x'0a' || 'body', 1, '2018-01-01 00:00:00');
