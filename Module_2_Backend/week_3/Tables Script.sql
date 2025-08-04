CREATE TABLE productos (
    codigo TEXT PRIMARY KEY,
    nombre TEXT NOT NULL,
    precio REAL NOT NULL CHECK(precio >= 0),
    fecha_ingreso DATE,
    marca TEXT
);

CREATE TABLE carrito_compras (
    id_carrito INTEGER PRIMARY KEY AUTOINCREMENT,
    email_usuario TEXT NOT NULL
);

CREATE TABLE carrito_productos (
    id_carrito TEXT,
    codigo_producto TEXT,
    cantidad INTEGER NOT NULL CHECK(cantidad > 0),
    PRIMARY KEY (id_carrito, codigo_producto),
    FOREIGN KEY (id_carrito) REFERENCES carrito_compras(id_carrito),
    FOREIGN KEY (codigo_producto) REFERENCES productos(codigo)
);

CREATE TABLE facturas (
    numero_factura INTEGER PRIMARY KEY AUTOINCREMENT,
    id_carrito INTEGER,
    fecha_compra DATETIME DEFAULT CURRENT_TIMESTAMP,
    correo_comprador TEXT NOT NULL,
    monto_total REAL DEFAULT 0 CHECK(monto_total >= 0),
    FOREIGN KEY (id_carrito) REFERENCES carrito_compras(id_carrito)
);

CREATE TABLE producto_factura (
    codigo_producto TEXT,
    numero_factura INTEGER,
    cantidad INTEGER NOT NULL CHECK(cantidad > 0),
    PRIMARY KEY (codigo_producto, numero_factura),
    FOREIGN KEY (codigo_producto) REFERENCES productos(codigo),
    FOREIGN KEY (numero_factura) REFERENCES facturas(numero_factura)
);