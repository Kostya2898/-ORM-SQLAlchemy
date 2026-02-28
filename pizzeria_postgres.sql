CREATE DATABASE pizzeria_db;

\c pizzeria_db;

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    order_date DATE,
    total_price DECIMAL
);

CREATE TABLE menu (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    price DECIMAL
);

CREATE TABLE order_items (
    order_id INT REFERENCES orders(id),
    menu_id INT REFERENCES menu(id),
    quantity INT,
    PRIMARY KEY (order_id, menu_id)
);

INSERT INTO menu (name, price) VALUES
('Маргарита', 200),
('Пепероні', 250),
('4 Сири', 300),
('Гавайська', 280);

INSERT INTO orders (order_date, total_price) VALUES
(CURRENT_DATE - INTERVAL '10 days', 500),
(CURRENT_DATE - INTERVAL '20 days', 750),
(CURRENT_DATE - INTERVAL '40 days', 600),
(CURRENT_DATE - INTERVAL '70 days', 900);

INSERT INTO order_items VALUES
(1, 1, 2),
(1, 2, 1),
(2, 2, 3),
(3, 3, 2),
(4, 4, 3);

SELECT COUNT(*) AS orders_last_month
FROM orders
WHERE order_date >= CURRENT_DATE - INTERVAL '1 month';

SELECT m.name, SUM(oi.quantity) AS total_ordered
FROM order_items oi
JOIN menu m ON oi.menu_id = m.id
GROUP BY m.name
ORDER BY total_ordered DESC
LIMIT 1;

SELECT AVG(total_price) AS avg_last_3_months
FROM orders
WHERE order_date >= CURRENT_DATE - INTERVAL '3 months';
