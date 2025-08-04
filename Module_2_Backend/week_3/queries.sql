SELECT * 
FROM products;

SELECT *
FROM products 
WHERE precio > 50000;

SELECT * 
FROM producto_factura
WHERE codigo_producto = 1;

SELECT 
codigo_producto,
SUM(cantidad) AS total_comprado
FROM producto_factura
GROUP BY codigo_producto;

SELECT *	
FROM facturas 
WHERE correo_comprador = 'kevinv@gmail.com';

SELECT * 
FROM facturas 
ORDER BY monto_total DESC;

SELECT *
FROM facturas 
WHERE numero_factura = 1; 