import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import pandas as pd
import sqlite3
import sys
import os 
from collections import defaultdict 
import re # Necesario para la detección avanzada de alias

# --- 1. CONFIGURACIÓN DE DATOS Y EJERCICIOS ---

# Contenido SQL para las tablas de la base de datos de prueba. 
# NOTA: Todo está en sintaxis SQLite compatible y listo para ser ejecutado por executescript.
# Mantenemos las cadenas para el fallback, ya que son obligatorias.

SQL_BRANDS_SETUP = """DROP TABLE IF EXISTS brands;
CREATE TABLE brands (brand_id INTEGER PRIMARY KEY, brand_name TEXT NOT NULL);
INSERT INTO brands(brand_id,brand_name) VALUES(1,'Electra');
INSERT INTO brands(brand_id,brand_name) VALUES(2,'Haro');
INSERT INTO brands(brand_id,brand_name) VALUES(3,'Heller');
INSERT INTO brands(brand_id,brand_name) VALUES(4,'Pure Cycles');
INSERT INTO brands(brand_id,brand_name) VALUES(5,'Ritchey');
INSERT INTO brands(brand_id,brand_name) VALUES(6,'Strider');
INSERT INTO brands(brand_id,brand_name) VALUES(7,'Sun Bicycles');
INSERT INTO brands(brand_id,brand_name) VALUES(8,'Surly');
INSERT INTO brands(brand_id,brand_name) VALUES(9,'Trek');
"""

SQL_CATEGORIES_SETUP = """DROP TABLE IF EXISTS categories;
CREATE TABLE categories (category_id INTEGER PRIMARY KEY, category_name TEXT NOT NULL);
INSERT INTO categories(category_id,category_name) VALUES(1,'Children Bicycles');
INSERT INTO categories(category_id,category_name) VALUES(2,'Comfort Bicycles');
INSERT INTO categories(category_id,category_name) VALUES(3,'Cruisers Bicycles');
INSERT INTO categories(category_id,category_name) VALUES(4,'Cyclocross Bicycles');
INSERT INTO categories(category_id,category_name) VALUES(5,'Electric Bikes');
INSERT INTO categories(category_id,category_name) VALUES(6,'Mountain Bikes');
INSERT INTO categories(category_id,category_name) VALUES(7,'Road Bikes');
"""

SQL_PRODUCTS_SETUP = """
DROP TABLE IF EXISTS products;
CREATE TABLE products (
	product_id INTEGER PRIMARY KEY,
	product_name TEXT NOT NULL,
	brand_id INTEGER NOT NULL,
	category_id INTEGER NOT NULL,
	model_year INTEGER NOT NULL,
	list_price REAL NOT NULL, 
	FOREIGN KEY (category_id) REFERENCES categories (category_id),
	FOREIGN KEY (brand_id) REFERENCES brands (brand_id)
);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(1,'Trek 820 - 2016',9,6,2016,379.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(2,'Ritchey Timberwolf Frameset - 2016',5,6,2016,749.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(3,'Surly Wednesday Frameset - 2016',8,6,2016,999.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(4,'Trek Fuel EX 8 29 - 2016',9,6,2016,2899.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(5,'Heller Shagamaw Frame - 2016',3,6,2016,1320.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(6,'Surly Ice Cream Truck Frameset - 2016',8,6,2016,469.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(7,'Trek Slash 8 27.5 - 2016',9,6,2016,3999.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(8,'Trek Remedy 29 Carbon Frameset - 2016',9,6,2016,1799.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(9,'Trek Conduit+ - 2016',9,5,2016,2999.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(10,'Surly Straggler - 2016',8,4,2016,1549);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(11,'Surly Straggler 650b - 2016',8,4,2016,1680.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(12,'Electra Townie Original 21D - 2016',1,3,2016,549.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(13,'Electra Cruiser 1 (24-Inch) - 2016',1,3,2016,269.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(14,'Electra Girl''s Hawaii 1 (16-inch) - 2015/2016',1,3,2016,269.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(15,'Electra Moto 1 - 2016',1,3,2016,529.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(16,'Electra Townie Original 7D EQ - 2016',1,3,2016,599.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(17,'Pure Cycles Vine 8-Speed - 2016',4,3,2016,429);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(18,'Pure Cycles Western 3-Speed - Women''s - 2015/2016',4,3,2016,449);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(19,'Pure Cycles William 3-Speed - 2016',4,3,2016,449);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(20,'Electra Townie Original 7D EQ - Women''s - 2016',1,3,2016,599.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(21,'Electra Cruiser 1 (24-Inch) - 2016',1,1,2016,269.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(22,'Electra Girl''s Hawaii 1 (16-inch) - 2015/2016',1,1,2016,269.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(23,'Electra Girl''s Hawaii 1 (20-inch) - 2015/2016',1,1,2016,299.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(24,'Electra Townie Original 21D - 2016',1,2,2016,549.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(25,'Electra Townie Original 7D - 2015/2016',1,2,2016,499.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(26,'Electra Townie Original 7D EQ - 2016',1,2,2016,599.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(27,'Surly Big Dummy Frameset - 2017',8,6,2017,999.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(28,'Surly Karate Monkey 27.5+ Frameset - 2017',8,6,2017,2499.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(29,'Trek X-Caliber 8 - 2017',9,6,2017,999.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(30,'Surly Ice Cream Truck Frameset - 2017',8,6,2017,999.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(31,'Surly Wednesday - 2017',8,6,2017,1632.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(32,'Trek Farley Alloy Frameset - 2017',9,6,2017,469.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(33,'Surly Wednesday Frameset - 2017',8,6,2017,469.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(34,'Trek Session DH 27.5 Carbon Frameset - 2017',9,6,2017,469.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(35,'Sun Bicycles Spider 3i - 2017',7,6,2017,832.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(36,'Surly Troll Frameset - 2017',8,6,2017,832.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(37,'Haro Flightline One ST - 2017',2,6,2017,379.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(38,'Haro Flightline Two 26 Plus - 2017',2,6,2017,549.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(39,'Trek Stache 5 - 2017',9,6,2017,1499.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(40,'Trek Fuel EX 9.8 29 - 2017',9,6,2017,4999.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(41,'Haro Shift R3 - 2017',2,6,2017,1469.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(42,'Trek Fuel EX 5 27.5 Plus - 2017',9,6,2017,2299.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(43,'Trek Fuel EX 9.8 27.5 Plus - 2017',9,6,2017,5299.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(44,'Haro SR 1.1 - 2017',2,6,2017,539.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(45,'Haro SR 1.2 - 2017',2,6,2017,869.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(46,'Haro SR 1.3 - 2017',2,6,2017,1409.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(47,'Trek Remedy 9.8 - 2017',9,6,2017,5299.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(48,'Trek Emonda S 4 - 2017',9,7,2017,1499.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(49,'Trek Domane SL 6 - 2017',9,7,2017,3499.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(50,'Trek Silque SLR 7 Women''s - 2017',9,7,2017,5999.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(51,'Trek Silque SLR 8 Women''s - 2017',9,7,2017,6499.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(52,'Surly Steamroller - 2017',8,7,2017,875.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(53,'Surly Ogre Frameset - 2017',8,7,2017,749.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(54,'Trek Domane SL Disc Frameset - 2017',9,7,2017,3199.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(55,'Trek Domane S 6 - 2017',9,7,2017,2699.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(56,'Trek Domane SLR 6 Disc - 2017',9,7,2017,5499.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(57,'Trek Emonda S 5 - 2017',9,7,2017,1999.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(58,'Trek Madone 9.2 - 2017',9,7,2017,4999.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(59,'Trek Domane S 5 Disc - 2017',9,7,2017,2599.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(60,'Sun Bicycles ElectroLite - 2017',7,5,2017,1559.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(61,'Trek Powerfly 8 FS Plus - 2017',9,5,2017,4999.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(62,'Trek Boone 7 - 2017',9,4,2017,3499.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(63,'Trek Boone Race Shop Limited - 2017',9,4,2017,3499.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(64,'Electra Townie Original 7D - 2017',1,3,2017,489.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(65,'Sun Bicycles Lil Bolt Type-R - 2017',7,3,2017,346.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(66,'Sun Bicycles Revolutions 24 - 2017',7,3,2017,250.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(67,'Sun Bicycles Revolutions 24 - Girl''s - 2017',7,3,2017,250.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(68,'Sun Bicycles Cruz 3 - 2017',7,3,2017,449.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(69,'Sun Bicycles Cruz 7 - 2017',7,3,2017,416.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(70,'Electra Amsterdam Original 3i - 2015/2017',1,3,2017,659.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(71,'Sun Bicycles Atlas X-Type - 2017',7,3,2017,416.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(72,'Sun Bicycles Biscayne Tandem 7 - 2017',7,3,2017,619.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(73,'Sun Bicycles Brickell Tandem 7 - 2017',7,3,2017,749.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(74,'Electra Cruiser Lux 1 - 2017',1,3,2017,439.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(75,'Electra Cruiser Lux Fat Tire 1 Ladies - 2017',1,3,2017,599.99);
"""

SQL_SALES_SETUP = """
DROP TABLE IF EXISTS sales;
CREATE TABLE sales (
    sale_id INTEGER PRIMARY KEY,
    product_id INTEGER,
    quantity INTEGER,
    sale_date TEXT,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
INSERT INTO sales (sale_id, product_id, quantity, sale_date) VALUES (101, 1, 2, '2023-10-01');
INSERT INTO sales (sale_id, product_id, quantity, sale_date) VALUES (102, 3, 5, '2023-10-02');
INSERT INTO sales (sale_id, product_id, quantity, sale_date) VALUES (103, 2, 10, '2023-10-03');
INSERT INTO sales (sale_id, product_id, quantity, sale_date) VALUES (104, 4, 1, '2023-10-04');
INSERT INTO sales (sale_id, product_id, quantity, sale_date) VALUES (105, 1, 3, '2023-10-05');
"""

SQL_CUSTOMERS_SETUP = """
DROP TABLE IF EXISTS customers;
CREATE TABLE customers (
	customer_id INTEGER PRIMARY KEY,
	first_name TEXT NOT NULL,
	last_name TEXT NOT NULL,
	phone TEXT,
	email TEXT NOT NULL,
	street TEXT,
	city TEXT,
	state TEXT,
	zip_code TEXT
);
INSERT INTO customers(customer_id, first_name, last_name, phone, email, street, city, state, zip_code) VALUES(1,'Debra','Burks',NULL,'debra.burks@yahoo.com','9273 Thorne Ave. ','Orchard Park','NY','14127');
INSERT INTO customers(customer_id, first_name, last_name, phone, email, street, city, state, zip_code) VALUES(2,'Kasha','Todd',NULL,'kasha.todd@yahoo.com','910 Vine Street ','Campbell','CA','95008');
INSERT INTO customers(customer_id, first_name, last_name, phone, email, street, city, state, zip_code) VALUES(3,'Tameka','Fisher',NULL,'tameka.fisher@aol.com','769C Honey Creek St. ','Redondo Beach','CA','90278');
INSERT INTO customers(customer_id, first_name, last_name, phone, email, street, city, state, zip_code) VALUES(4,'Daryl','Spence',NULL,'daryl.spence@aol.com','988 Pearl Lane ','Uniondale','NY','11553');
INSERT INTO customers(customer_id, first_name, last_name, phone, email, street, city, state, zip_code) VALUES(5,'Charolette','Rice','(916) 381-6003','charolette.rice@msn.com','107 River Dr. ','Sacramento','CA','95820');
INSERT INTO customers(customer_id, first_name, last_name, phone, email, street, city, state, zip_code) VALUES(6,'Lyndsey','Bean',NULL,'lyndsey.bean@hotmail.com','769 West Road ','Fairport','NY','14450');
INSERT INTO customers(customer_id, first_name, last_name, phone, email, street, city, state, zip_code) VALUES(7,'Latasha','Hays','(716) 986-3359','latasha.hays@hotmail.com','7014 Manor Station Rd. ','Buffalo','NY','14215');
INSERT INTO customers(customer_id, first_name, last_name, phone, email, street, city, state, zip_code) VALUES(8,'Jacquline','Duncan',NULL,'jacquline.duncan@yahoo.com','15 Brown St. ','Jackson Heights','NY','11372');
INSERT INTO customers(customer_id, first_name, last_name, phone, email, street, city, state, zip_code) VALUES(9,'Genoveva','Baldwin',NULL,'genoveva.baldwin@msn.com','8550 Spruce Drive ','Port Washington','NY','11050');
INSERT INTO customers(customer_id, first_name, last_name, phone, email, street, city, state, zip_code) VALUES(10,'Pamelia','Newman',NULL,'pamelia.newman@gmail.com','476 Chestnut Ave. ','Monroe','NY','10950');
"""

SQL_STORES_SETUP = """
DROP TABLE IF EXISTS stores;
CREATE TABLE stores (
	store_id INTEGER PRIMARY KEY,
	store_name TEXT NOT NULL,
	phone TEXT,
	email TEXT,
	street TEXT,
	city TEXT,
	state TEXT,
	zip_code TEXT
);
INSERT INTO stores(store_id,store_name, phone, email, street, city, state, zip_code) VALUES(1,'Santa Cruz Bikes','(831) 476-4321','santacruz@bikes.shop','3700 Portola Drive', 'Santa Cruz','CA','95060');
INSERT INTO stores(store_id,store_name, phone, email, street, city, state, zip_code) VALUES(2,'Baldwin Bikes','(516) 379-8888','baldwin@bikes.shop','4200 Chestnut Lane', 'Baldwin','NY','11432');
INSERT INTO stores(store_id,store_name, phone, email, street, city, state, zip_code) VALUES(3,'Rowlett Bikes','(972) 530-5555','rowlett@bikes.shop','8000 Fairway Avenue', 'Rowlett','TX','75088');
"""

SQL_STAFFS_SETUP = """
DROP TABLE IF EXISTS staffs;
CREATE TABLE staffs (
	staff_id INTEGER PRIMARY KEY,
	first_name TEXT NOT NULL,
	last_name TEXT NOT NULL,
	email TEXT NOT NULL UNIQUE,
	phone TEXT,
	active INTEGER NOT NULL,
	store_id INTEGER NOT NULL,
	manager_id INTEGER,
	FOREIGN KEY (store_id) REFERENCES stores (store_id),
	FOREIGN KEY (manager_id) REFERENCES staffs (staff_id)
);

INSERT INTO staffs(staff_id, first_name, last_name, email, phone, active, store_id, manager_id) VALUES(1,'Fabiola','Jackson','fabiola.jackson@bikes.shop','(831) 555-5554',1,1,NULL);
INSERT INTO staffs(staff_id, first_name, last_name, email, phone, active, store_id, manager_id) VALUES(2,'Mireya','Copeland','mireya.copeland@bikes.shop','(831) 555-5555',1,1,1);
INSERT INTO staffs(staff_id, first_name, last_name, email, phone, active, store_id, manager_id) VALUES(3,'Genna','Serrano','genna.serrano@bikes.shop','(831) 555-5556',1,1,2);
INSERT INTO staffs(staff_id, first_name, last_name, email, phone, active, store_id, manager_id) VALUES(4,'Virgie','Wiggins','virgie.wiggins@bikes.shop','(831) 555-5557',1,1,2);
INSERT INTO staffs(staff_id, first_name, last_name, email, phone, active, store_id, manager_id) VALUES(5,'Jannette','David','jannette.david@bikes.shop','(516) 379-4444',1,2,1);
INSERT INTO staffs(staff_id, first_name, last_name, email, phone, active, store_id, manager_id) VALUES(6,'Marcelene','Boyer','marcelene.boyer@bikes.shop','(516) 379-4445',1,2,5);
INSERT INTO staffs(staff_id, first_name, last_name, email, phone, active, store_id, manager_id) VALUES(7,'Venita','Daniel','venita.daniel@bikes.shop','(516) 379-4446',1,2,5);
INSERT INTO staffs(staff_id, first_name, last_name, email, phone, active, store_id, manager_id) VALUES(8,'Kali','Vargas','kali.vargas@bikes.shop','(972) 530-5555',1,3,1);
INSERT INTO staffs(staff_id, first_name, last_name, email, phone, active, store_id, manager_id) VALUES(9,'Layla','Terrell','layla.terrell@bikes.shop','(972) 530-5556',1,3,7);
INSERT INTO staffs(staff_id, first_name, last_name, email, phone, active, store_id, manager_id) VALUES(10,'Bernardine','Houston','bernardine.houston@bikes.shop','(972) 530-5557',1,3,7);
"""

SQL_ORDERS_SETUP = """
DROP TABLE IF EXISTS orders;
CREATE TABLE orders (
	order_id INTEGER PRIMARY KEY, 
	customer_id INTEGER,
	order_status INTEGER NOT NULL, 
	order_date TEXT NOT NULL,
	required_date TEXT NOT NULL,
	shipped_date TEXT,
	store_id INTEGER NOT NULL,
	staff_id INTEGER NOT NULL,
	FOREIGN KEY (customer_id) REFERENCES customers (customer_id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (store_id) REFERENCES stores (store_id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (staff_id) REFERENCES staffs (staff_id) ON DELETE NO ACTION ON UPDATE NO ACTION
);
-- Datos de ejemplo simples para la tabla orders
INSERT INTO orders(order_id, customer_id, order_status, order_date, required_date, shipped_date, store_id, staff_id) VALUES(1, 1, 4, '2023-10-01', '2023-10-05', '2023-10-03', 1, 2);
INSERT INTO orders(order_id, customer_id, order_status, order_date, required_date, shipped_date, store_id, staff_id) VALUES(2, 5, 4, '2023-10-02', '2023-10-06', '2023-10-04', 2, 6);
INSERT INTO orders(order_id, customer_id, order_status, order_date, required_date, shipped_date, store_id, staff_id) VALUES(3, 8, 3, '2023-10-03', '2023-10-07', NULL, 3, 9);
"""

SQL_CITIES_STAFF_SETUP = """
DROP TABLE IF EXISTS cities_staff;
CREATE TABLE cities_staff (
	city_id INTEGER PRIMARY KEY,
	city_name TEXT NOT NULL,
	first_name TEXT NOT NULL,
	last_name TEXT NOT NULL
);

INSERT INTO cities_staff(city_id, city_name, first_name, last_name) VALUES(1,'Madrid','Fabiola','Jackson');
INSERT INTO cities_staff(city_id, city_name, first_name, last_name) VALUES(2,'Madrid','Mireya','Copeland');
INSERT INTO cities_staff(city_id, city_name, first_name, last_name) VALUES(3,'Madrid','Genna','Serrano');
INSERT INTO cities_staff(city_id, city_name, first_name, last_name) VALUES(4,'Valencia','Virgie','Wiggins');
INSERT INTO cities_staff(city_id, city_name, first_name, last_name) VALUES(5,'Valencia','Jannette','David');
INSERT INTO cities_staff(city_id, city_name, first_name, last_name) VALUES(6,'Barcelona','Marcelene','Boyer');
INSERT INTO cities_staff(city_id, city_name, first_name, last_name) VALUES(7,'Barcelona','Venita','Daniel');
INSERT INTO cities_staff(city_id, city_name, first_name, last_name) VALUES(8,'Barcelona','Kali','Vargas');
INSERT INTO cities_staff(city_id, city_name, first_name, last_name) VALUES(9,'Barcelona','Layla','Terrell');
INSERT INTO cities_staff(city_id, city_name, first_name, last_name) VALUES(10,'Sevilla','Bernardine','Houston');
"""


# Definición de las tablas. 
TABLES = {
    'brands': {
        'file_path': 'sql_setup/brands.sql',
        'content': SQL_BRANDS_SETUP,
        'description': "Registra las marcas de bicicletas.",
        'columns': "brand_id (clave), brand_name (nombre de la marca)."
    },
    'categories': {
        'file_path': 'sql_setup/categories.sql',
        'content': SQL_CATEGORIES_SETUP,
        'description': "Contiene las categorías de productos.",
        'columns': "category_id (clave), category_name (nombre de la categoría)."
    },
    'products': {
        'file_path': 'sql_setup/products.sql',
        'content': SQL_PRODUCTS_SETUP,
        'description': "Contiene información sobre los artículos que se venden.",
        'columns': "product_id (clave), product_name (nombre), list_price (precio), brand_id (FK), category_id (FK), model_year (año)."
    },
    'sales': {
        'file_path': 'sql_setup/sales.sql',
        'content': SQL_SALES_SETUP,
        'description': "Registra las transacciones de venta.",
        'columns': "sale_id (clave), product_id (FK), quantity (cantidad vendida), sale_date (fecha)."
    },
    'stores': {
        'file_path': 'sql_setup/stores.sql',
        'content': SQL_STORES_SETUP,
        'description': "Registra la información de las tiendas.",
        'columns': "store_id (clave), store_name (nombre), phone, email, street, city, state, zip_code."
    },
    'customers': {
        'file_path': 'sql_setup/customers.sql',
        'content': SQL_CUSTOMERS_SETUP,
        'description': "Registra la información de los clientes.",
        'columns': "customer_id (clave), first_name, last_name, phone, email, street, city, state, zip_code."
    },
    'staffs': {
        'file_path': 'sql_setup/staffs.sql',
        'content': SQL_STAFFS_SETUP,
        'description': "Registra la información de los empleados.",
        'columns': "staff_id (clave), first_name, last_name, email, store_id (FK), manager_id (FK)."
    },
    'orders': {
        'file_path': 'sql_setup/orders.sql',
        'content': SQL_ORDERS_SETUP,
        'description': "Registra las órdenes de venta.",
        'columns': "order_id (clave), customer_id (FK), order_status, order_date, required_date, shipped_date, store_id (FK), staff_id (FK)."
    },
    'cities_staff': {
        'file_path': 'sql_setup/cities_staff.sql',
        'content': SQL_CITIES_STAFF_SETUP,
        'description': "Registra el personal asignado a una ciudad.",
        'columns': "city_id (clave), city_name (nombre de la ciudad), first_name, last_name."
    }
}

# Definición de los ejercicios 
EXERCISES = [
    {
        'prompt': "Ejercicio 1/3: Muestra el `product_name` y el `list_price` de todos los productos. Ordena por nombre alfabéticamente.",
        'correct_query': "SELECT product_name, list_price FROM products ORDER BY product_name ASC"
    },
    {
        'prompt': "Ejercicio 2/3: Calcula la suma total de ítems vendidos (`quantity`) para el producto con `product_id` 1. Nombra la columna resultante como `total_sold`.",
        'correct_query': "SELECT SUM(quantity) AS total_sold FROM sales WHERE product_id = 1"
    },
    {
        'prompt': "Ejercicio 3/3: Encuentra el nombre del producto (`product_name`) de los productos de la `brand_id` 9 (Trek) con un `list_price` superior a 500.",
        'correct_query': "SELECT product_name FROM products WHERE brand_id = 9 AND list_price > 500"
    }
]

# --- 2. CLASE PRINCIPAL DE LA APLICACIÓN ---

class SQLTesterApp:
    def __init__(self, master, tables, exercises):
        # Configuración inicial
        self.master = master
        master.title("Evaluador de Conocimientos SQL")
        master.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.tables = tables
        self.exercises = exercises
        self.current_exercise_index = 0

        # Inicializar la base de datos en memoria
        # Habilitar la compatibilidad con Foreign Keys en SQLite
        self.conn = sqlite3.connect(':memory:')
        self.conn.execute("PRAGMA foreign_keys = ON;") 
        self.conn.commit()
        
        # 1. Cargar las tablas (ejecuta el SQL, crea las tablas en la DB)
        self._load_tables_to_db()

        # 2. Después de cargar las tablas, lee el esquema REAL de la DB para autocompletar
        self.schema_metadata = self._get_schema_metadata()
        

        # Configurar el estilo
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Inter', 10, 'bold'), padding=8)
        self.style.configure('TLabel', font=('Inter', 10))
        self.style.configure('Prompt.TLabel', font=('Inter', 12, 'bold'), foreground='#336699')
        self.style.configure('Schema.TLabel', font=('Consolas', 10), foreground='#005500') 
        
        # Configurar la grid principal
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=1)
        master.grid_rowconfigure(0, weight=1)
        
        # Contenedor de paneles (Izquierda y Derecha)
        main_frame = ttk.Frame(master, padding="10 10 10 10")
        main_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        
        # --- UI: Panel Izquierdo (Input y Schema) ---
        input_frame = ttk.Frame(main_frame, relief="flat", padding="5")
        input_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        input_frame.grid_rowconfigure(2, weight=1) # Fila de la query
        input_frame.grid_columnconfigure(0, weight=1)

        # 1. Panel de Información de Tablas
        schema_frame = ttk.LabelFrame(input_frame, text="ESQUEMA DE LA BASE DE DATOS", padding="10")
        schema_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        self.schema_text = tk.StringVar()
        self.schema_label = ttk.Label(schema_frame, textvariable=self.schema_text, 
                                     justify=tk.LEFT, style='Schema.TLabel') 
        self.schema_label.pack(fill='x', expand=True) 
        self._update_schema_display()


        # 2. Área de Entrada de Query
        ttk.Label(input_frame, text="Escribe tu Consulta SQL aquí (Usa TAB para autocompletar):", font=('Inter', 11, 'bold')).grid(row=1, column=0, sticky="w", pady=(0, 5))
        
        self.query_input = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, height=10, font=('Consolas', 10))
        self.query_input.grid(row=2, column=0, sticky="nsew", pady=(0, 10))
        
        # Enlazar la tecla TAB al método de autocompletado
        self.query_input.bind("<Tab>", self._autocomplete)
        self.query_input.bind("<Key>", lambda e: 'break' if e.keysym == 'Tab' else None) # Evita el foco por defecto del tab

        # Popup de sugerencias (Listbox dentro de Toplevel), inicialmente oculto
        self._suggestion_popup = tk.Toplevel(self.master)
        self._suggestion_popup.withdraw()
        self._suggestion_popup.overrideredirect(True)
        self._suggestion_listbox = tk.Listbox(self._suggestion_popup, height=6)
        self._suggestion_listbox.pack(fill='both', expand=True)
        # Bindings para selección/navegación
        self._suggestion_listbox.bind('<Double-Button-1>', lambda e: self._apply_selected_suggestion())
        self._suggestion_listbox.bind('<Return>', lambda e: self._apply_selected_suggestion())
        self._suggestion_listbox.bind('<Escape>', lambda e: self._hide_suggestions())
        # Permitir aceptar la sugerencia con TAB mientras la lista tiene el foco
        self._suggestion_listbox.bind('<Tab>', self._on_listbox_tab)
        # Estado auxiliar
        self._last_token = ''
        self._last_table_prefix = ''
        self._last_column_prefix = ''

        # Botones
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=3, column=0, sticky="ew")
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        ttk.Button(button_frame, text="EJECUTAR CONSULTA", command=self.execute_query, style='TButton').grid(row=0, column=0, sticky="ew", padx=2, pady=5)
        ttk.Button(button_frame, text="COMPROBAR SOLUCIÓN", command=self.check_solution, style='TButton').grid(row=0, column=1, sticky="ew", padx=2, pady=5)
        
        self.message_label = ttk.Label(input_frame, text="", foreground='blue', font=('Inter', 10, 'italic'))
        self.message_label.grid(row=4, column=0, sticky="ew", pady=(5, 0))

        # --- UI: Panel Derecho (Output) ---
        output_frame = ttk.Frame(main_frame, relief="flat", padding="5")
        output_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        output_frame.grid_rowconfigure(1, weight=1)
        output_frame.grid_columnconfigure(0, weight=1)

        ttk.Label(output_frame, text="Resultado de la Consulta:", font=('Inter', 11, 'bold')).grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        self.tree = ttk.Treeview(output_frame, show='headings')
        self.tree.grid(row=1, column=0, sticky='nsew')

        # Scrollbar vertical para el Treeview
        vsb = ttk.Scrollbar(output_frame, orient="vertical", command=self.tree.yview)
        vsb.grid(row=1, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=vsb.set)
        
        # --- UI: Recuadro Inferior (Prompt) ---
        prompt_frame = ttk.Frame(master, padding="10 5", relief="groove")
        prompt_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        
        self.prompt_label = ttk.Label(prompt_frame, text="", style='Prompt.TLabel', wraplength=700)
        self.prompt_label.pack(expand=True, fill='x')

        # Cargar el primer ejercicio
        self.load_exercise()

    # --- 3. FUNCIONES DE BASE DE DATOS Y LÓGICA ---
    
    def _get_schema_metadata(self):
        """
        Genera un diccionario con {tabla: [columna1, columna2, ...]} 
        Consultando el esquema real de la base de datos en memoria mediante
        PRAGMA table_info(<table>). Esto es más fiable cuando las queries
        se gestionan desde archivos externos y no hay un campo 'columns'
        en `self.tables`.
        """
        metadata = defaultdict(list)

        try:
            # Listar tablas presentes en la conexión sqlite
            cur = self.conn.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables_in_db = [r[0] for r in cur.fetchall()]

            for table_name in tables_in_db:
                try:
                    cur.execute(f"PRAGMA table_info({table_name})")
                    cols = [row[1].lower() for row in cur.fetchall()]  # segunda columna es el nombre
                    metadata[table_name.lower()] = cols
                except Exception:
                    # Si falla la extracción para una tabla, la ignoramos pero no rompemos todo
                    metadata[table_name.lower()] = []
        except Exception:
            # Si algo falla, devolvemos un dict vacío (autocompletado seguirá intentando con tablas conocidas)
            return dict()

        return metadata

    def _get_alias_map(self, full_text):
        """
        Extrae un mapa de alias -> tabla a partir del texto SQL dado.
        - Maneja cláusulas FROM con varias tablas separadas por comas.
        - Maneja JOINs y formas con/without AS: e.g. `FROM products p`, `JOIN brands AS b`.
        Devuelve dict con claves en minúsculas.
        """
        alias_map = {}
        try:
            text = full_text or ''
            # Buscar la porción AFTER FROM hasta WHERE/GROUP/ORDER/LIMIT u fin
            for m in re.finditer(r'\bfrom\b\s+(.*?)(?:\bwhere\b|\bgroup\b|\border\b|\bhaving\b|\blimit\b|$)', text, flags=re.I|re.S):
                from_seg = m.group(1)
                # separar por comas en el FROM
                parts = [p.strip() for p in re.split(r',', from_seg) if p.strip()]
                for part in parts:
                    # part puede ser: table [AS] alias, o subquery (ignoramos subqueries)
                    sub = re.match(r'([A-Za-z_]\w*)(?:\s+(?:as\s+)?([A-Za-z_]\w*))?', part, flags=re.I)
                    if sub:
                        table = sub.group(1).lower()
                        alias = sub.group(2).lower() if sub.group(2) else None
                        if alias:
                            alias_map[alias] = table
                        # Mapear el nombre de tabla a sí mismo también ayuda en resoluciones directas
                        alias_map[table] = table

            # También capturar JOIN ... table [AS] alias
            for jm in re.finditer(r'\bjoin\b\s+([A-Za-z_]\w*)(?:\s+(?:as\s+)?([A-Za-z_]\w*))?', text, flags=re.I):
                table = jm.group(1).lower()
                alias = jm.group(2).lower() if jm.group(2) else None
                if alias:
                    alias_map[alias] = table
                alias_map[table] = table
        except Exception:
            return {}

        return alias_map
    
    def _autocomplete(self, event):
        """
        Maneja el autocompletado en el área de consulta al presionar TAB.
        Soporta autocompletado de tablas y de columnas (usando sintaxis table.column).
        """
        
        text_widget = self.query_input
        # Obtener el texto desde el inicio hasta la posición actual del cursor
        current_text = text_widget.get("1.0", "insert")
        
        # Patrón mejorado para capturar el último token que puede ser un prefijo de tabla o de columna.
        match = re.search(r"([\w]+\.?[\w]*)$", current_text)
        
        if not match:
            return "break"

        last_token = match.group(0)
        last_token_lower = last_token.lower()

        # Determinamos la posición de inicio del token para la inserción
        start_index = "insert - %sc" % len(last_token)

        if "." in last_token:
            # --- Caso 1: Autocompletado de Columna (Ej: products.produ) ---
            parts = last_token.split('.')
            table_prefix = parts[0].lower()
            column_prefix = parts[1].lower() if len(parts) > 1 else ''
            
            resolved_table = None
            # Intentar resolver alias usando el SQL ya escrito en el buffer
            alias_map = self._get_alias_map(text_widget.get("1.0", tk.END))
            if table_prefix in alias_map:
                resolved_table = alias_map[table_prefix]

            # Si no se resolvió por alias, buscar por prefijo entre los nombres de tabla reales
            if not resolved_table:
                for full_name in self.schema_metadata.keys():
                    if full_name.startswith(table_prefix):
                        resolved_table = full_name
                        break
            
            if resolved_table and resolved_table in self.schema_metadata:
                suggestions = [
                    col for col in self.schema_metadata[resolved_table]
                    if col.startswith(column_prefix)
                ]

                if suggestions:
                    # Guardamos contexto para aplicar la sugerencia más tarde
                    self._last_token = last_token
                    self._last_table_prefix = resolved_table
                    self._last_column_prefix = column_prefix

                    # Mostrar popup con las sugerencias de columnas
                    display_items = suggestions
                    self._show_suggestions(display_items)
                    return "break"
        
        else:
            # --- Caso 2: Autocompletado de Tabla o Palabra Clave SQL (Ej: sel o prod) ---
            
            # Palabras clave SQL comunes
            sql_keywords = ["SELECT", "FROM", "WHERE", "JOIN", "ON", "AND", "OR", "ORDER BY", "GROUP BY", "DESCRIBE"]

            # Nombres de todas las tablas (aseguramos minúsculas)
            table_names = [t.lower() for t in list(self.tables.keys())]

            all_keywords = [k.lower() for k in sql_keywords] + table_names

            suggestions = [
                keyword for keyword in all_keywords
                if keyword.startswith(last_token_lower) and keyword != last_token_lower
            ]

            if suggestions:
                # Si sólo hay una sugerencia, autocompletamos inmediatamente
                if len(suggestions) == 1:
                    completion = suggestions[0].upper()
                    # Reemplazar la última palabra por la sugerencia completa
                    text_widget.delete(start_index, "insert")
                    text_widget.insert("insert", completion)
                    return "break"

                # Guardamos contexto para aplicar la sugerencia más tarde
                self._last_token = last_token
                self._last_table_prefix = ''
                self._last_column_prefix = ''

                # Presentar sugerencias (keywords y tablas)
                display_items = [s.upper() for s in suggestions]
                self._show_suggestions(display_items)
                return "break"

        return "break" # Evita que TAB mueva el foco

    def _update_schema_display(self):
        """Genera y muestra el texto del esquema de la base de datos de forma compacta y dinámica."""
        
        # Detecta automáticamente las tablas definidas en el diccionario TABLES
        table_keys = sorted(list(self.tables.keys())) # Ordenamos alfabéticamente para consistencia
        
        # Formatea los nombres de las tablas en una sola línea continua (ej: BRANDS, CATEGORIES, PRODUCTS, SALES)
        formatted_names = [name.upper() for name in table_keys]
        
        # Usa join para unir todos los nombres de tabla en una sola línea.
        schema_info = "Tablas Disponibles: " + ", ".join(formatted_names)
        
        # Añadimos la instrucción para ver detalles
        schema_info += ". Usa 'DESCRIBE nombre_tabla' para ver columnas."
        
        self.schema_text.set(schema_info.strip())

    # --- Sugerencias / Popup de autocompletado ---
    def _show_suggestions(self, items):
        """Muestra el popup con una lista de `items` (strings)."""
        if not items:
            self._hide_suggestions()
            return

        # Rellenar listbox
        self._suggestion_listbox.delete(0, tk.END)
        for it in items:
            self._suggestion_listbox.insert(tk.END, it)
        # Seleccionar primer elemento
        self._suggestion_listbox.selection_set(0)

        # Posicionar el popup justo debajo del cursor del Text
        try:
            bbox = self.query_input.bbox("insert")
            if bbox:
                x, y, w, h = bbox
                abs_x = self.query_input.winfo_rootx() + x
                abs_y = self.query_input.winfo_rooty() + y + h
                self._suggestion_popup.geometry(f"+{abs_x}+{abs_y}")
        except Exception:
            # En caso de fallo, dejar popup en su posición por defecto
            pass

        self._suggestion_popup.deiconify()
        self._suggestion_popup.lift()
        # Dar foco a la lista para permitir navegación con teclado
        self._suggestion_listbox.focus_set()

    def _hide_suggestions(self):
        try:
            self._suggestion_popup.withdraw()
        except Exception:
            pass

    def _apply_selected_suggestion(self):
        """Toma la selección actual y la aplica en el Text reemplazando el token."""
        # Si el popup no está visible (por ejemplo cuando ya se hizo autocompletado
        # inmediato y no se mostró la lista), no hacemos nada.
        try:
            if not self._suggestion_popup.winfo_ismapped():
                return
        except Exception:
            # Si por alguna razón no podemos consultar el estado, procedemos con cautela.
            pass

        sel = None
        try:
            idx = self._suggestion_listbox.curselection()
            if not idx:
                sel = self._suggestion_listbox.get(0)
            else:
                sel = self._suggestion_listbox.get(idx[0])
        except Exception:
            self._hide_suggestions()
            return

        if not sel:
            self._hide_suggestions()
            return

        # Aplicar según el contexto (columna o tabla/keyword)
        text_widget = self.query_input
        # Volvemos al Text widget y aplicamos la inserción
        text_widget.focus_set()

        if '.' in self._last_token:
            # El token era table.column -> sólo sustituir la porción de columna
            prefix_len = len(self._last_column_prefix)
            if prefix_len > 0:
                col_start_index = "insert - %sc" % prefix_len
                try:
                    text_widget.delete(col_start_index, "insert")
                except Exception:
                    pass
            # Insertar la columna (mantener minúsculas)
            text_widget.insert("insert", sel)
        else:
            # Token simple (tabla o keyword): sustituir la última palabra
            try:
                start_index = "insert - %sc" % len(self._last_token)
                text_widget.delete(start_index, "insert")
            except Exception:
                pass
            # Insertar la sugerencia (si es keyword, ya viene en mayúsculas)
            text_widget.insert("insert", sel)

        # Ocultar popup
        self._hide_suggestions()
        # Reset contexto
        self._last_token = ''
        self._last_table_prefix = ''
        self._last_column_prefix = ''

    def _on_listbox_tab(self, event):
        """Handler para la tecla TAB mientras la lista de sugerencias tiene el foco.
        Acepta la sugerencia actual y evita que el foco cambie fuera del widget.
        """
        try:
            self._apply_selected_suggestion()
        except Exception:
            pass
        return "break"


    def _load_tables_to_db(self):
        """Carga las tablas ejecutando scripts SQL (desde archivo o fallback) en la base de datos SQLite."""
        
        # Ordenamos las tablas para cargar primero las que no tienen FK, y luego las que las referencian.
        # Orden necesario: brands, categories, stores, customers -> staffs, products, sales, orders, cities_staff
        ordered_tables_to_load = ['brands', 'categories', 'stores', 'customers', 'staffs', 'products', 'sales', 'orders', 'cities_staff']
        
        try:
            # Activamos las Foreign Keys antes de ejecutar cualquier script
            self.conn.execute("PRAGMA foreign_keys = ON;") 
            self.conn.commit() 
            
            for table_name in ordered_tables_to_load:
                if table_name not in self.tables:
                    continue
                    
                data = self.tables[table_name]
                sql_script = data['content'] # Usamos el contenido interno por defecto
                file_path = data['file_path']
                
                # A continuación, el código que intenta leer el archivo externo
                try:
                    # Abrimos el archivo en modo lectura
                    with open(file_path, 'r', encoding='utf-8') as f:
                        sql_script = f.read()
                    
                    # Limpiamos el script de sintaxis incompatible con SQLite 
                    lines = [
                        line for line in sql_script.split('\n') 
                        if not line.strip().upper().startswith(('USE ', 'GO', 'SET IDENTITY_INSERT', '--'))
                    ]
                    sql_script = ' '.join(lines)
                    
                    # Aseguramos que haya punto y coma entre comandos
                    sql_script = sql_script.replace(');INSERT', ');\nINSERT')

                    print(f"Éxito: Leyendo la configuración SQL desde el archivo: {file_path}")
                except FileNotFoundError:
                    # Usamos el contenido interno (fallback)
                    pass 
                except Exception as e:
                    # Este catch sirve para atrapar errores de lectura o procesamiento del archivo externo
                    messagebox.showwarning("Advertencia de Archivo", f"Error al leer/procesar {file_path}. Usando datos internos: {e}")
                    sql_script = data['content']

                # Ejecutar el script SQL (CREATE TABLE + INSERTs)
                self.conn.executescript(sql_script)

            self.conn.commit() # Confirmar todas las transacciones
            print("Tablas cargadas exitosamente ejecutando scripts SQL en la DB en memoria.")
        except Exception as e:
            # Captura el error específico para el usuario
            messagebox.showerror("Error de Inicialización SQL", f"No se pudo ejecutar el script SQL para crear las tablas: {e}")
            sys.exit(1)


    def execute_query(self):
        """Ejecuta la consulta del usuario y muestra el resultado en el Treeview, maneja DESCRIBE/PRAGMA."""
        query = self.query_input.get("1.0", tk.END).strip()
        if not query:
            self.message_label.config(text="Por favor, introduce una consulta SQL.")
            self.clear_treeview()
            return

        # Detección y corrección para el comando DESCRIBE no soportado en SQLite
        upper_query = query.upper()
        if upper_query.startswith('DESCRIBE') or upper_query.startswith('DESC '):
            try:
                # Extrae el nombre de la tabla
                parts = query.split()
                if len(parts) < 2:
                    raise IndexError("Missing table name.")
                table_name = parts[1].strip(';').lower()
                
                # Verifica si la tabla existe en nuestro set de datos
                if table_name in self.tables:
                    # Usa PRAGMA table_info (equivalente a DESCRIBE en SQLite)
                    pragma_query = f"PRAGMA table_info({table_name})"
                    
                    result_df = pd.read_sql_query(pragma_query, self.conn)
                    self.display_result(result_df)
                    
                    # Mensaje informativo para el usuario
                    self.message_label.config(
                        text=f"Consulta PRAGMA ejecutada (equivalente a DESCRIBE). Resultado a la derecha.", 
                        foreground='purple'
                    )
                    return 
                else:
                    self.clear_treeview()
                    self.message_label.config(text=f"ERROR SQL: Tabla '{table_name}' no encontrada.", foreground='red')
                    return
            except IndexError:
                self.clear_treeview()
                self.message_label.config(text="ERROR: Sintaxis de DESCRIBE inválida. Usa 'DESCRIBE nombre_tabla'.", foreground='red')
                return
            except Exception as e:
                self.clear_treeview()
                self.message_label.config(text=f"ERROR en DESCRIBE/PRAGMA: {e}", foreground='red')
                return


        # Si no es DESCRIBE, procede con la ejecución normal de la consulta (SELECT, etc.)
        try:
            # Ejecutar la consulta y obtener el DataFrame resultante
            result_df = pd.read_sql_query(query, self.conn)
            self.display_result(result_df)
            self.message_label.config(text="Consulta ejecutada. Revisa los resultados a la derecha.")
        except Exception as e:
            self.clear_treeview()
            self.message_label.config(text=f"ERROR SQL: {e}", foreground='red') 

    def display_result(self, df):
        """Muestra un DataFrame en el widget Treeview."""
        self.clear_treeview()

        # Configurar columnas
        columns = list(df.columns)
        self.tree["columns"] = columns
        
        for col in columns:
            self.tree.heading(col, text=col.capitalize(), anchor="center")
            # Ajustar el ancho de las columnas (ejemplo: 80-150 píxeles)
            self.tree.column(col, anchor="center", width=int(self.tree.winfo_width() / len(columns) * 0.9) if self.tree.winfo_width() > 0 and len(columns) > 0 else 100)

        # Insertar filas
        for index, row in df.iterrows():
            self.tree.insert("", "end", values=list(row))
            
    def clear_treeview(self):
        """Limpia el contenido del Treeview."""
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = [] # También limpia las columnas

    def check_solution(self):
        """Compara el resultado del usuario con la solución esperada."""
        user_query = self.query_input.get("1.0", tk.END).strip()
        
        if not user_query:
            self.message_label.config(text="No hay consulta para validar.", foreground='orange')
            return

        current_exercise = self.exercises[self.current_exercise_index]
        correct_query = current_exercise['correct_query']

        try:
            # 1. Obtener el resultado esperado
            expected_df = pd.read_sql_query(correct_query, self.conn)
            
            # 2. Obtener el resultado del usuario
            user_df = pd.read_sql_query(user_query, self.conn)

            # 3. Normalizar DataFrames para una comparación estricta (compatibilidad de versiones de Pandas)
            
            # Chequear nombres de columnas (ignorando mayúsculas/minúsculas)
            expected_cols = [c.lower() for c in expected_df.columns]
            user_cols = [c.lower() for c in user_df.columns]

            if expected_cols != user_cols:
                raise AssertionError(
                    f"Las columnas no coinciden. Esperado: {expected_cols}, Obtenido: {user_cols}"
                )
            
            # Reordenar las columnas del usuario para que coincidan con el orden esperado (necesario para la validación de Pandas)
            user_df = user_df[[col for col in expected_df.columns]]
            
            # Reiniciar índices para la comparación (ignora el orden de las filas si el ORDER BY es el mismo)
            expected_df = expected_df.reset_index(drop=True)
            user_df = user_df.reset_index(drop=True)
            
            # Comparar el contenido de los DataFrames
            pd.testing.assert_frame_equal(
                expected_df, 
                user_df,
                check_dtype=True, 
                check_exact=False # Permite pequeñas diferencias en floats
            )

            # Si la comparación es exitosa (no lanza error)
            self.message_label.config(text="¡CORRECTO! Pasando al siguiente ejercicio...", foreground='green')
            self.master.after(1500, self.next_exercise) # Espera 1.5s antes de avanzar

        except AssertionError as e:
            # Los DataFrames son diferentes (estructura o contenido)
            self.message_label.config(text="INCORRECTO. El resultado no coincide con la solución esperada.", foreground='red')
            print(f"Detalle de la diferencia (debug): {e}")
        except Exception as e:
            # Error de sintaxis o de ejecución de la consulta
            self.message_label.config(text=f"ERROR SQL o de validación: {e}", foreground='red') 


    def load_exercise(self):
        """Carga el ejercicio actual en la UI."""
        if self.current_exercise_index < len(self.exercises):
            exercise = self.exercises[self.current_exercise_index]
            self.prompt_label.config(text=exercise['prompt'])
            self.query_input.delete("1.0", tk.END)
            self.clear_treeview()
            self.message_label.config(text="Escribe tu consulta y compruébala.", foreground='blue')
        else:
            # Final de los ejercicios
            self.master.destroy()
            messagebox.showinfo("¡Felicidades!","Has completado todos los ejercicios. La aplicación se cerrará.")

    def next_exercise(self):
        """Avanza al siguiente ejercicio."""
        self.current_exercise_index += 1
        self.load_exercise()
        
    def on_closing(self):
        """Cierra la conexión a la DB y la aplicación."""
        if self.conn:
            self.conn.close()
        self.master.destroy()

# --- 4. EJECUCIÓN DEL SCRIPT ---

if __name__ == "__main__":
    # La aplicación requiere pandas y sqlite3 (que viene con python)
    try:
        root = tk.Tk()
        app = SQLTesterApp(root, TABLES, EXERCISES)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Error Fatal", f"Ocurrió un error inesperado al iniciar la aplicación: {e}")