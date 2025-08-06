SELECT * FROM products;

SELECT * 
  FROM products 
 WHERE price > 50000;

SELECT ip.invoice_id,
       i.buyer_user_id,
       ip.product_code,
       ip.quantity
  FROM invoice_products ip
  JOIN invoices i ON ip.invoice_id = i.invoice_id
 WHERE ip.product_code = 'P001';

SELECT product_code,
       SUM(quantity) AS total_quantity
  FROM invoice_products
 GROUP BY product_code;

SELECT *
  FROM invoices
 WHERE buyer_user_id = 3;

SELECT *
  FROM invoices
 ORDER BY total_amount DESC;

SELECT *
  FROM invoices
 WHERE invoice_id = 5
 LIMIT 1;
