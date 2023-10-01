DROP TABLE IF EXISTS purchase;
DROP TABLE IF EXISTS clients;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS product;

CREATE TABLE purchase (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       client_id INTEGER UNIQUE NOT NULL,
       product_id INTEGER NOT NULL,
       datetime TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
-- Examples
   --SELECT datetime('now', 'localtime')
   --insterting via SELECT datetime('now') of date('now')
   -- INSERT INTO datetime_text (d1, d2)
   -- SELECT strftime("%d", date('now'));
   -- VALUES(datetime('now'),datetime('now', 'localtime'));

CREATE TABLE clients (
       client_id INTEGER PRIMARY KEY AUTOINCREMENT,
       client_name TEXT NOT NULL,
       client_email TEXT UNIQUE NOT NULL,
       password TEXT UNIQUE NOT NULL,
       FOREIGN KEY (client_id) REFERENCES purchase (client_id)
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  client_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (client_id) REFERENCES clients (client_id)
);

CREATE TABLE product (
       product_id INTEGER PRIMARY KEY AUTOINCREMENT,
       product_name TEXT NOT NULL,
       FOREIGN KEY (product_id) REFERENCES purchase (product_id)
);


INSERT INTO product (product_name) VALUES ('t-shirt');
INSERT INTO product (product_name) VALUES ('polo shirt');
INSERT INTO product (product_name) VALUES ('Sweat shirt');
INSERT INTO product (product_name) VALUES ('Long shirt');
