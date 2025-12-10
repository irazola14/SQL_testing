import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import pandas as pd
import sqlite3
import sys
import os # Necesario para la lectura de archivos

# --- 1. CONFIGURACIÓN DE DATOS Y EJERCICIOS ---

# Contenido simulado de archivos SQL (DDL y DML).
# Estos comandos CREATE y INSERT se ejecutarán para crear las tablas y poblarlas.
SQL_PRODUCTS_SETUP = """
DROP TABLE IF EXISTS products;
CREATE TABLE products (
	product_id INTEGER PRIMARY KEY,
	product_name TEXT NOT NULL,
	brand_id INTEGER NOT NULL,
	category_id INTEGER NOT NULL,
	model_year INTEGER,
	list_price INTEGER NOT NULL,
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
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(76,'Electra Girl''s Hawaii 1 16" - 2017',1,3,2017,299.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(77,'Electra Glam Punk 3i Ladies'' - 2017',1,3,2017,799.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(78,'Sun Bicycles Biscayne Tandem CB - 2017',7,3,2017,647.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(79,'Sun Bicycles Boardwalk (24-inch Wheels) - 2017',7,3,2017,402.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(80,'Sun Bicycles Brickell Tandem CB - 2017',7,3,2017,761.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(81,'Electra Amsterdam Fashion 7i Ladies'' - 2017',1,3,2017,1099.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(82,'Electra Amsterdam Original 3i Ladies'' - 2017',1,3,2017,659.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(83,'Trek Boy''s Kickster - 2015/2017',9,1,2017,149.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(84,'Sun Bicycles Lil Kitt''n - 2017',7,1,2017,109.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(85,'Haro Downtown 16 - 2017',2,1,2017,329.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(86,'Trek Girl''s Kickster - 2017',9,1,2017,149.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(87,'Trek Precaliber 12 Boys - 2017',9,1,2017,189.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(88,'Trek Precaliber 12 Girls - 2017',9,1,2017,189.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(89,'Trek Precaliber 16 Boys - 2017',9,1,2017,209.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(90,'Trek Precaliber 16 Girls - 2017',9,1,2017,209.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(91,'Trek Precaliber 24 (21-Speed) - Girls - 2017',9,1,2017,349.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(92,'Haro Shredder 20 - 2017',2,1,2017,209.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(93,'Haro Shredder 20 Girls - 2017',2,1,2017,209.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(94,'Haro Shredder Pro 20 - 2017',2,1,2017,249.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(95,'Electra Girl''s Hawaii 1 16" - 2017',1,1,2017,299.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(96,'Electra Moto 3i (20-inch) - Boy''s - 2017',1,1,2017,349.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(97,'Electra Savannah 3i (20-inch) - Girl''s - 2017',1,1,2017,349.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(98,'Electra Straight 8 3i (20-inch) - Boy''s - 2017',1,1,2017,489.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(99,'Electra Sugar Skulls 1 (20-inch) - Girl''s - 2017',1,1,2017,299.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(100,'Electra Townie 3i EQ (20-inch) - Boys'' - 2017',1,1,2017,489.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(101,'Electra Townie 7D (20-inch) - Boys'' - 2017',1,1,2017,339.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(102,'Electra Townie Original 7D - 2017',1,2,2017,489.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(103,'Sun Bicycles Streamway 3 - 2017',7,2,2017,551.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(104,'Sun Bicycles Streamway - 2017',7,2,2017,481.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(105,'Sun Bicycles Streamway 7 - 2017',7,2,2017,533.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(106,'Sun Bicycles Cruz 3 - 2017',7,2,2017,449.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(107,'Sun Bicycles Cruz 7 - 2017',7,2,2017,416.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(108,'Sun Bicycles Cruz 3 - Women''s - 2017',7,2,2017,449.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(109,'Sun Bicycles Cruz 7 - Women''s - 2017',7,2,2017,416.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(110,'Sun Bicycles Drifter 7 - 2017',7,2,2017,470.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(111,'Sun Bicycles Drifter 7 - Women''s - 2017',7,2,2017,470.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(112,'Trek 820 - 2018',9,6,2018,379.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(113,'Trek Marlin 5 - 2018',9,6,2018,489.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(114,'Trek Marlin 6 - 2018',9,6,2018,579.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(115,'Trek Fuel EX 8 29 - 2018',9,6,2018,3199.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(116,'Trek Marlin 7 - 2017/2018',9,6,2018,749.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(117,'Trek Ticket S Frame - 2018',9,6,2018,1469.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(118,'Trek X-Caliber 8 - 2018',9,6,2018,999.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(119,'Trek Kids'' Neko - 2018',9,6,2018,469.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(120,'Trek Fuel EX 7 29 - 2018',9,6,2018,2499.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(121,'Surly Krampus Frameset - 2018',8,6,2018,2499.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(122,'Surly Troll Frameset - 2018',8,6,2018,2499.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(123,'Trek Farley Carbon Frameset - 2018',9,6,2018,999.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(124,'Surly Krampus - 2018',8,6,2018,1499);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(125,'Trek Kids'' Dual Sport - 2018',9,6,2018,469.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(126,'Surly Big Fat Dummy Frameset - 2018',8,6,2018,469.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(127,'Surly Pack Rat Frameset - 2018',8,6,2018,469.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(128,'Surly ECR 27.5 - 2018',8,6,2018,1899);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(129,'Trek X-Caliber 7 - 2018',9,6,2018,919.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(130,'Trek Stache Carbon Frameset - 2018',9,6,2018,919.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(131,'Heller Bloodhound Trail - 2018',3,6,2018,2599);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(132,'Trek Procal AL Frameset - 2018',9,6,2018,1499.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(133,'Trek Procaliber Frameset - 2018',9,6,2018,1499.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(134,'Trek Remedy 27.5 C Frameset - 2018',9,6,2018,1499.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(135,'Trek X-Caliber Frameset - 2018',9,6,2018,1499.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(136,'Trek Procaliber 6 - 2018',9,6,2018,1799.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(137,'Heller Shagamaw GX1 - 2018',3,6,2018,2599);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(138,'Trek Fuel EX 5 Plus - 2018',9,6,2018,2249.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(139,'Trek Remedy 7 27.5 - 2018',9,6,2018,2999.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(140,'Trek Remedy 9.8 27.5 - 2018',9,6,2018,4999.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(141,'Trek Stache 5 - 2018',9,6,2018,1599.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(142,'Trek Fuel EX 8 29 XT - 2018',9,6,2018,3199.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(143,'Trek Domane ALR 3 - 2018',9,7,2018,1099.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(144,'Trek Domane ALR 4 Disc - 2018',9,7,2018,1549.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(145,'Trek Domane ALR 5 Disc - 2018',9,7,2018,1799.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(146,'Trek Domane SLR 6 - 2018',9,7,2018,4999.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(147,'Trek Domane ALR 5 Gravel - 2018',9,7,2018,1799.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(148,'Trek Domane SL 8 Disc - 2018',9,7,2018,5499.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(149,'Trek Domane SLR 8 Disc - 2018',9,7,2018,7499.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(150,'Trek Emonda SL 7 - 2018',9,7,2018,4499.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(151,'Trek Domane ALR 4 Disc Women''s - 2018',9,7,2018,1549.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(152,'Trek Domane SL 5 Disc Women''s - 2018',9,7,2018,2499.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(153,'Trek Domane SL 7 Women''s - 2018',9,7,2018,4999.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(154,'Trek Domane SLR 6 Disc Women''s - 2018',9,7,2018,5499.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(155,'Trek Domane SLR 9 Disc - 2018',9,7,2018,11999.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(156,'Trek Domane SL Frameset - 2018',9,7,2018,6499.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(157,'Trek Domane SL Frameset Women''s - 2018',9,7,2018,6499.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(158,'Trek CrossRip 1 - 2018',9,7,2018,959.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(159,'Trek Emonda ALR 6 - 2018',9,7,2018,2299.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(160,'Trek Emonda SLR 6 - 2018',9,7,2018,4499.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(161,'Surly ECR - 2018',8,7,2018,1899);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(162,'Trek Emonda SL 6 Disc - 2018',9,7,2018,2999.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(163,'Surly Pack Rat - 2018',8,7,2018,1349);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(164,'Surly Straggler 650b - 2018',8,7,2018,1549);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(165,'Trek 1120 - 2018',9,7,2018,2499.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(166,'Trek Domane AL 2 Women''s - 2018',9,7,2018,749.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(167,'Surly ECR Frameset - 2018',8,7,2018,749.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(168,'Surly Straggler - 2018',8,7,2018,1549);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(169,'Trek Emonda SLR 8 - 2018',9,7,2018,6499.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(170,'Trek CrossRip 2 - 2018',9,7,2018,1299.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(171,'Trek Domane SL 6 - 2018',9,7,2018,3199.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(172,'Trek Domane ALR Disc Frameset - 2018',9,7,2018,3199.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(173,'Trek Domane ALR Frameset - 2018',9,7,2018,3199.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(174,'Trek Domane SLR Disc Frameset - 2018',9,7,2018,3199.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(175,'Trek Domane SLR Frameset - 2018',9,7,2018,3199.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(176,'Trek Madone 9 Frameset - 2018',9,7,2018,3199.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(177,'Trek Domane SLR 6 Disc - 2018',9,7,2018,5499.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(178,'Trek Domane AL 2 - 2018',9,7,2018,749.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(179,'Trek Domane AL 3 - 2018',9,7,2018,919.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(180,'Trek Domane AL 3 Women''s - 2018',9,7,2018,919.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(181,'Trek Domane SL 5 - 2018',9,7,2018,2199.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(182,'Trek Domane SL 5 Disc - 2018',9,7,2018,2499.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(183,'Trek Domane SL 5 Women''s - 2018',9,7,2018,2199.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(184,'Trek Domane SL 6 Disc - 2018',9,7,2018,3499.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(185,'Trek Conduit+ - 2018',9,5,2018,2799.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(186,'Trek CrossRip+ - 2018',9,5,2018,4499.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(187,'Trek Neko+ - 2018',9,5,2018,2799.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(188,'Trek XM700+ Lowstep - 2018',9,5,2018,3499.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(189,'Trek Lift+ Lowstep - 2018',9,5,2018,2799.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(190,'Trek Dual Sport+ - 2018',9,5,2018,2799.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(191,'Electra Loft Go! 8i - 2018',1,5,2018,2799.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(192,'Electra Townie Go! 8i - 2017/2018',1,5,2018,2599.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(193,'Trek Lift+ - 2018',9,5,2018,2799.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(194,'Trek XM700+ - 2018',9,5,2018,3499.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(195,'Electra Townie Go! 8i Ladies'' - 2018',1,5,2018,2599.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(196,'Trek Verve+ - 2018',9,5,2018,2299.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(197,'Trek Verve+ Lowstep - 2018',9,5,2018,2299.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(198,'Electra Townie Commute Go! - 2018',1,5,2018,2999.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(199,'Electra Townie Commute Go! Ladies'' - 2018',1,5,2018,2999.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(200,'Trek Powerfly 5 - 2018',9,5,2018,3499.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(201,'Trek Powerfly 5 FS - 2018',9,5,2018,4499.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(202,'Trek Powerfly 5 Women''s - 2018',9,5,2018,3499.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(203,'Trek Powerfly 7 FS - 2018',9,5,2018,4999.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(204,'Trek Super Commuter+ 7 - 2018',9,5,2018,3599.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(205,'Trek Super Commuter+ 8S - 2018',9,5,2018,4999.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(206,'Trek Boone 5 Disc - 2018',9,4,2018,3299.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(207,'Trek Boone 7 Disc - 2018',9,4,2018,3999.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(208,'Trek Crockett 5 Disc - 2018',9,4,2018,1799.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(209,'Trek Crockett 7 Disc - 2018',9,4,2018,2999.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(210,'Surly Straggler - 2018',8,4,2018,1549);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(211,'Surly Straggler 650b - 2018',8,4,2018,1549);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(212,'Electra Townie Original 21D - 2018',1,3,2018,559.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(213,'Electra Cruiser 1 - 2016/2017/2018',1,3,2018,269.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(214,'Electra Tiger Shark 3i - 2018',1,3,2018,899.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(215,'Electra Queen of Hearts 3i - 2018',1,3,2018,749.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(216,'Electra Super Moto 8i - 2018',1,3,2018,899.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(217,'Electra Straight 8 3i - 2018',1,3,2018,909.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(218,'Electra Cruiser 7D - 2016/2017/2018',1,3,2018,319.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(219,'Electra Moto 3i - 2018',1,3,2018,639.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(220,'Electra Cruiser 1 Ladies'' - 2018',1,3,2018,269.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(221,'Electra Cruiser 7D Ladies'' - 2016/2018',1,3,2018,319.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(222,'Electra Cruiser 1 Tall - 2016/2018',1,3,2018,269.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(223,'Electra Cruiser Lux 3i - 2018',1,3,2018,529.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(224,'Electra Cruiser Lux 7D - 2018',1,3,2018,479.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(225,'Electra Delivery 3i - 2016/2017/2018',1,3,2018,959.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(226,'Electra Townie Original 21D EQ - 2017/2018',1,3,2018,679.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(227,'Electra Cruiser 7D (24-Inch) Ladies'' - 2016/2018',1,3,2018,319.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(228,'Electra Cruiser 7D Tall - 2016/2018',1,3,2018,319.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(229,'Electra Cruiser Lux 1 - 2016/2018',1,3,2018,429.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(230,'Electra Cruiser Lux 1 Ladies'' - 2018',1,3,2018,429.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(231,'Electra Cruiser Lux 3i Ladies'' - 2018',1,3,2018,529.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(232,'Electra Cruiser Lux 7D Ladies'' - 2018',1,3,2018,479.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(233,'Electra Cruiser Lux Fat Tire 7D - 2018',1,3,2018,639.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(234,'Electra Daydreamer 3i Ladies'' - 2018',1,3,2018,899.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(235,'Electra Koa 3i Ladies'' - 2018',1,3,2018,899.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(236,'Electra Morningstar 3i Ladies'' - 2018',1,3,2018,749.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(237,'Electra Relic 3i - 2018',1,3,2018,849.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(238,'Electra Townie Balloon 8D EQ - 2016/2017/2018',1,3,2018,749.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(239,'Electra Townie Balloon 8D EQ Ladies'' - 2016/2017/2018',1,3,2018,749.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(240,'Electra Townie Commute 27D Ladies - 2018',1,3,2018,899.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(241,'Electra Townie Commute 8D - 2018',1,3,2018,749.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(242,'Electra Townie Commute 8D Ladies'' - 2018',1,3,2018,699.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(243,'Electra Townie Original 21D EQ Ladies'' - 2018',1,3,2018,679.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(244,'Electra Townie Original 21D Ladies'' - 2018',1,3,2018,559.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(245,'Electra Townie Original 3i EQ - 2017/2018',1,3,2018,659.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(246,'Electra Townie Original 3i EQ Ladies'' - 2018',1,3,2018,639.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(247,'Electra Townie Original 7D EQ - 2018',1,3,2018,599.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(248,'Electra Townie Original 7D EQ Ladies'' - 2017/2018',1,3,2018,599.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(249,'Electra White Water 3i - 2018',1,3,2018,749.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(250,'Electra Townie Go! 8i - 2017/2018',1,3,2018,2599.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(251,'Electra Townie Commute Go! - 2018',1,3,2018,2999.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(252,'Electra Townie Commute Go! Ladies'' - 2018',1,3,2018,2999.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(253,'Electra Townie Go! 8i Ladies'' - 2018',1,3,2018,2599.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(254,'Electra Townie Balloon 3i EQ - 2017/2018',1,3,2018,749.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(255,'Electra Townie Balloon 7i EQ Ladies'' - 2017/2018',1,3,2018,899.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(256,'Electra Townie Commute 27D - 2018',1,3,2018,899.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(257,'Electra Amsterdam Fashion 3i Ladies'' - 2017/2018',1,3,2018,899.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(258,'Electra Amsterdam Royal 8i - 2017/2018',1,3,2018,1259.9);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(259,'Electra Amsterdam Royal 8i Ladies - 2018',1,3,2018,1199.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(260,'Electra Townie Balloon 3i EQ Ladies'' - 2018',1,3,2018,799.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(261,'Electra Townie Balloon 7i EQ - 2018',1,3,2018,899.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(262,'Trek MT 201 - 2018',9,1,2018,249.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(263,'Strider Classic 12 Balance Bike - 2018',6,1,2018,89.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(264,'Strider Sport 16 - 2018',6,1,2018,249.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(265,'Strider Strider 20 Sport - 2018',6,1,2018,289.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(266,'Trek Superfly 20 - 2018',9,1,2018,399.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(267,'Trek Precaliber 12 Girl''s - 2018',9,1,2018,199.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(268,'Trek Kickster - 2018',9,1,2018,159.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(269,'Trek Precaliber 12 Boy''s - 2018',9,1,2018,199.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(270,'Trek Precaliber 16 Boy''s - 2018',9,1,2018,209.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(271,'Trek Precaliber 16 Girl''s - 2018',9,1,2018,209.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(272,'Trek Precaliber 20 6-speed Boy''s - 2018',9,1,2018,289.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(273,'Trek Precaliber 20 6-speed Girl''s - 2018',9,1,2018,289.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(274,'Trek Precaliber 20 Boy''s - 2018',9,1,2018,229.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(275,'Trek Precaliber 20 Girl''s - 2018',9,1,2018,229.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(276,'Trek Precaliber 24 (7-Speed) - Boys - 2018',9,1,2018,319.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(277,'Trek Precaliber 24 21-speed Boy''s - 2018',9,1,2018,369.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(278,'Trek Precaliber 24 21-speed Girl''s - 2018',9,1,2018,369.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(279,'Trek Precaliber 24 7-speed Girl''s - 2018',9,1,2018,319.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(280,'Trek Superfly 24 - 2017/2018',9,1,2018,489.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(281,'Electra Cruiser 7D (24-Inch) Ladies'' - 2016/2018',1,1,2018,319.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(282,'Electra Cyclosaurus 1 (16-inch) - Boy''s - 2018',1,1,2018,279.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(283,'Electra Heartchya 1 (20-inch) - Girl''s - 2018',1,1,2018,319.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(284,'Electra Savannah 1 (20-inch) - Girl''s - 2018',1,1,2018,319.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(285,'Electra Soft Serve 1 (16-inch) - Girl''s - 2018',1,1,2018,279.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(286,'Electra Starship 1 16" - 2018',1,1,2018,279.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(287,'Electra Straight 8 1 (16-inch) - Boy''s - 2018',1,1,2018,279.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(288,'Electra Straight 8 1 (20-inch) - Boy''s - 2018',1,1,2018,389.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(289,'Electra Superbolt 1 20" - 2018',1,1,2018,319.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(290,'Electra Superbolt 3i 20" - 2018',1,1,2018,369.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(291,'Electra Sweet Ride 1 (20-inch) - Girl''s - 2018',1,1,2018,319.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(292,'Electra Sweet Ride 3i (20-inch) - Girls'' - 2018',1,1,2018,369.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(293,'Electra Tiger Shark 1 (20-inch) - Boys'' - 2018',1,1,2018,319.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(294,'Electra Tiger Shark 3i (20-inch) - Boys'' - 2018',1,1,2018,369.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(295,'Electra Treasure 1 20" - 2018',1,1,2018,319.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(296,'Electra Treasure 3i 20" - 2018',1,1,2018,369.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(297,'Electra Under-The-Sea 1 16" - 2018',1,1,2018,279.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(298,'Electra Water Lily 1 (16-inch) - Girl''s - 2018',1,1,2018,279.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(299,'Electra Townie Original 21D - 2018',1,2,2018,559.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(300,'Electra Townie Balloon 3i EQ Ladies'' - 2018',1,2,2018,799.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(301,'Electra Townie Balloon 7i EQ - 2018',1,2,2018,899.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(302,'Electra Townie Original 1 - 2018',1,2,2018,449.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(303,'Electra Townie Go! 8i - 2017/2018',1,2,2018,2599.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(304,'Electra Townie Original 21D EQ - 2017/2018',1,2,2018,679.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(305,'Electra Townie Balloon 3i EQ - 2017/2018',1,2,2018,749.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(306,'Electra Townie Balloon 7i EQ Ladies'' - 2017/2018',1,2,2018,899.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(307,'Electra Townie Balloon 8D EQ - 2016/2017/2018',1,2,2018,749.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(308,'Electra Townie Balloon 8D EQ Ladies'' - 2016/2017/2018',1,2,2018,749.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(309,'Electra Townie Commute 27D - 2018',1,2,2018,899.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(310,'Electra Townie Commute 27D Ladies - 2018',1,2,2018,899.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(311,'Electra Townie Commute 8D - 2018',1,2,2018,749.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(312,'Electra Townie Commute 8D Ladies'' - 2018',1,2,2018,699.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(313,'Electra Townie Original 1 Ladies'' - 2018',1,2,2018,449.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(314,'Electra Townie Original 21D EQ Ladies'' - 2018',1,2,2018,679.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(315,'Electra Townie Original 21D Ladies'' - 2018',1,2,2018,559.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(316,'Trek Checkpoint ALR 4 Women''s - 2019',9,7,2019,1699.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(317,'Trek Checkpoint ALR 5 - 2019',9,7,2019,1999.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(318,'Trek Checkpoint ALR 5 Women''s - 2019',9,7,2019,1999.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(319,'Trek Checkpoint SL 5 Women''s - 2019',9,7,2019,2799.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(320,'Trek Checkpoint SL 6 - 2019',9,7,2019,3799.99);
INSERT INTO products(product_id, product_name, brand_id, category_id, model_year, list_price) VALUES(321,'Trek Checkpoint ALR Frameset - 2019',9,7,2019,3199.99);
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

SQL_CATEGORIES_SETUP = """
DROP TABLE IF EXISTS categories;
CREATE TABLE categories (
	category_id INTEGER PRIMARY KEY,
	category_name TEXT NOT NULL
);

INSERT INTO categories(category_id,category_name) VALUES(1,'Children Bicycles');
INSERT INTO categories(category_id,category_name) VALUES(2,'Comfort Bicycles');
INSERT INTO categories(category_id,category_name) VALUES(3,'Cruisers Bicycles');
INSERT INTO categories(category_id,category_name) VALUES(4,'Cyclocross Bicycles');
INSERT INTO categories(category_id,category_name) VALUES(5,'Electric Bikes');
INSERT INTO categories(category_id,category_name) VALUES(6,'Mountain Bikes');
INSERT INTO categories(category_id,category_name) VALUES(7,'Road Bikes');
"""

SQL_BRANDS_SETUP = """
DROP TABLE IF EXISTS brands;
CREATE TABLE brands (
	brand_id INTEGER PRIMARY KEY,
	brand_name TEXT (255) NOT NULL
);

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

# Definición de las tablas. Ahora contienen la ruta al archivo .sql y el contenido interno (fallback).
TABLES = {
    'products': {
        'file_path': 'sql_setup/products.sql', # Ruta al archivo SQL para el entorno real
        'content': SQL_PRODUCTS_SETUP, # Contenido SQL interno para fallback
        'description': "Contiene información sobre los artículos que se venden."
    },
    'sales': {
        'file_path': 'sql_setup/sales.sql', # Ruta al archivo SQL para el entorno real
        'content': SQL_SALES_SETUP, # Contenido SQL interno para fallback
        'description': "Registra las transacciones de venta.",
    },
    'brands': {
        'file_path': 'sql_setup/brands.sql', # Ruta al archivo SQL para el entorno real
        'content': SQL_BRANDS_SETUP, # Contenido SQL interno para fallback
        'description': "Registra las marcas.",
    },
    'categories': {
        'file_path': 'sql_setup/categories.sql', # Ruta al archivo SQL para el entorno real
        'content': SQL_CATEGORIES_SETUP, # Contenido SQL interno para fallback
        'description': "Registra las categorias.",
    }
}

# Definición de los ejercicios (sin cambios)
EXERCISES = [
    {
        'prompt': "Ejercicio 1/3: Muestra el `name` y el `price` de todos los productos. Ordena por nombre alfabéticamente.",
        'correct_query': "SELECT name, price FROM products ORDER BY name ASC"
    },
    {
        'prompt': "Ejercicio 2/3: Calcula la suma total de ítems vendidos (`quantity`) para el producto con `product_id` 1. Nombra la columna resultante como `total_sold`.",
        'correct_query': "SELECT SUM(quantity) AS total_sold FROM sales WHERE product_id = 1"
    },
    {
        'prompt': "Ejercicio 3/3: Encuentra el nombre (`name`) de los productos que pertenecen a la categoría 'Electronics' y cuyo precio (`price`) es superior a 100.",
        'correct_query': "SELECT name FROM products WHERE category = 'Electronics' AND price > 100"
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
        self.conn = sqlite3.connect(':memory:')
        self._load_tables_to_db()

        # Configurar el estilo
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Inter', 10, 'bold'), padding=8)
        self.style.configure('TLabel', font=('Inter', 10))
        self.style.configure('Prompt.TLabel', font=('Inter', 12, 'bold'), foreground='#336699')
        self.style.configure('Info.TLabel', font=('Inter', 10, 'italic'), foreground='#555555')
        
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

        # 1. Panel de Información de Tablas (Nuevo)
        schema_frame = ttk.LabelFrame(input_frame, text="ESQUEMA DE LA BASE DE DATOS", padding="10")
        schema_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        self.schema_text = tk.StringVar()
        self.schema_label = ttk.Label(schema_frame, textvariable=self.schema_text, 
                                     justify=tk.LEFT, wraplength=350, style='Info.TLabel')
        self.schema_label.pack(fill='x')
        self._update_schema_display()


        # 2. Área de Entrada de Query
        ttk.Label(input_frame, text="Escribe tu Consulta SQL aquí:", font=('Inter', 11, 'bold')).grid(row=1, column=0, sticky="w", pady=(0, 5))
        
        self.query_input = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, height=10, font=('Consolas', 10))
        self.query_input.grid(row=2, column=0, sticky="nsew", pady=(0, 10))
        
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

    def _update_schema_display(self):
        """Genera y muestra el texto del esquema de la base de datos."""
        schema_info = ""
        for name, data in self.tables.items():
            schema_info += f"Tabla: {name.upper()}\n"
            schema_info += f"  - Descripción: {data['description']}\n"
        self.schema_text.set(schema_info.strip())

    def _load_tables_to_db(self):
        """Carga las tablas ejecutando scripts SQL (desde archivo o fallback) en la base de datos SQLite."""
        try:
            for table_name, data in self.tables.items():
                sql_script = data['content'] # Usamos el contenido interno por defecto
                file_path = data['file_path']
                
                # Intenta leer el archivo SQL real
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        sql_script = f.read()
                    print(f"Éxito: Leyendo la configuración SQL desde el archivo: {file_path}")
                except FileNotFoundError:
                    # Si no encuentra el archivo real, usa el contenido interno (fallback)
                    # No mostramos el warning aquí para no interrumpir la experiencia si es intencional
                    pass 
                except Exception as e:
                    messagebox.showwarning("Advertencia de Archivo", f"Error al leer {file_path}. Usando datos internos: {e}")

                # Ejecutar el script SQL (CREATE TABLE + INSERTs)
                self.conn.executescript(sql_script)

            self.conn.commit() # Confirmar todas las transacciones
            print("Tablas cargadas exitosamente ejecutando scripts SQL en la DB en memoria.")
        except Exception as e:
            messagebox.showerror("Error de Inicialización SQL", f"No se pudo ejecutar el script SQL para crear las tablas: {e}")
            sys.exit(1)


    def execute_query(self):
        """Ejecuta la consulta del usuario y muestra el resultado en el Treeview."""
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
                table_name = query.split()[1].strip(';').lower()
                
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
                    return # Salimos después de ejecutar el PRAGMA
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
            # CORREGIDO: Comilla simple de cierre
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
            
            # Comparar el contenido de los DataFrames, excluyendo el argumento 'check_column_order'
            # para compatibilidad con versiones antiguas de Pandas.
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
            self.message_label.config(text=f"ERROR SQL o de validación: {e}", foreground='red') # Cita corregida

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
            messagebox.showinfo("¡Felicidades!", "Has completado todos los ejercicios. La aplicación se cerrará.")

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