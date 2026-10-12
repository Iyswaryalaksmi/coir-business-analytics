USE coir_business_analytics;
GO

CREATE TABLE dbo.production_orders (
    production_order_id INT IDENTITY(1,1) PRIMARY KEY,
    production_date DATE NOT NULL,
    product_id INT NOT NULL,
    planned_quantity DECIMAL(12,3),
    actual_quantity DECIMAL(12,3),
    status VARCHAR(50),
    CONSTRAINT FK_production_orders_products
        FOREIGN KEY (product_id) REFERENCES dbo.products(product_id)
);
GO
