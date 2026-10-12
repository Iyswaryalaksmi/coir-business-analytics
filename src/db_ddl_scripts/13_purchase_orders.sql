USE coir_business_analytics;
GO

CREATE TABLE dbo.purchase_orders (
    purchase_order_id INT IDENTITY(1,1) PRIMARY KEY,
    purchase_date DATE NOT NULL,
    supplier_id INT NOT NULL,
    date_id INT,
    status VARCHAR(50),
    total_amount DECIMAL(14,2),
    CONSTRAINT FK_purchase_orders_suppliers
        FOREIGN KEY (supplier_id) REFERENCES dbo.suppliers(supplier_id),
    CONSTRAINT FK_purchase_orders_dim_date
        FOREIGN KEY (date_id) REFERENCES dbo.dim_date(date_id)
);
GO
