-- initial SQL

-- DROP TABLE
DROP TABLE menus;
DROP TABLE categories;

-- CREATE TABLE
CREATE TABLE categories(
    id integer primary key autoincrement,
    category_id text not null,
    category text not null,
    name text not null
);

CREATE TABLE menus(
    id integer primary key autoincrement,
    name text not null,
    category_id text not null,
    price integer not null
);

-- INSERT DATA
.mode csv
.import csv/categories.csv categories
.import csv/menus.csv menus

-- SELECT
.print categories ->
SELECT count(id) FROM categories;
.print menus ->
SELECT count(id) FROM menus;
