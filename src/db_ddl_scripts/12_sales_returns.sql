USE coir_business_analytics;
GO

CREATE TABLE dbo.sales_returns (
    return_id INT IDENTITY(1,1) PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    return_date DATE,
    quantity DECIMAL(12,3),
    return_reason VARCHAR(255),
    return_amount DECIMAL(14,2),
    CONSTRAINT FK_sales_returns_sales_orders
        FOREIGN KEY (order_id) REFERENCES dbo.sales_orders(order_id),
    CONSTRAINT FK_sales_returns_products
        FOREIGN KEY (product_id) REFERENCES dbo.products(product_id)
);
GO
