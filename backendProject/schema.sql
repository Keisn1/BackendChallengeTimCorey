DROP TABLE IF EXISTS purchase;
DROP TABLE IF EXISTS buyer;
DROP TABLE IF EXISTS product;

CREATE TABLE purchase (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       user_id INTEGER UNIQUE NOT NULL,
       product_id INTEGER NOT NULL,
       datetime TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
-- Examples
   --SELECT datetime('now', 'localtime')
   --insterting via SELECT datetime('now') of date('now')
   -- INSERT INTO datetime_text (d1, d2)
   -- SELECT strftime("%d", date('now'));
   -- VALUES(datetime('now'),datetime('now', 'localtime'));

CREATE TABLE user (
       user_id INTEGER NOT NULL,
       username TEXT NOT NULL,
       user_email TEXT UNIQUE NOT NULL,
       password TEXT UNIQUE NOT NULL,
       FOREIGN KEY (user_id) REFERENCES purchase (user_id)
);

CREATE TABLE product (
       product_id INTEGER NOT NULL,
       product_name TEXT NOT NULL,
       FOREIGN KEY (product_id) REFERENCES purchase (product_id)
);

