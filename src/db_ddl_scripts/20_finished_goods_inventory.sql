USE coir_business_analytics;
GO

CREATE TABLE dbo.finished_goods_inventory (
    finished_inventory_id INT IDENTITY(1,1) PRIMARY KEY,
    product_id INT NOT NULL,
    date_id INT NOT NULL,
    opening_quantity DECIMAL(12,3),
    production_quantity DECIMAL(12,3),
    sales_quantity DECIMAL(12,3),
    return_quantity DECIMAL(12,3),
    closing_quantity DECIMAL(12,3),
    CONSTRAINT FK_finished_goods_inventory_products
        FOREIGN KEY (product_id) REFERENCES dbo.products(product_id),
    CONSTRAINT FK_finished_goods_inventory_dim_date
        FOREIGN KEY (date_id) REFERENCES dbo.dim_date(date_id)
);
GO
