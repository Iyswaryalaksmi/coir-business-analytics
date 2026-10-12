USE coir_business_analytics;
GO

CREATE TABLE dbo.sales_order_items (
    sales_item_id INT IDENTITY(1,1) PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity DECIMAL(12,3),
    unit_price DECIMAL(12,2),
    discount DECIMAL(12,2) DEFAULT 0,
    sales_amount DECIMAL(14,2),
    CONSTRAINT FK_sales_order_items_sales_orders
        FOREIGN KEY (order_id) REFERENCES dbo.sales_orders(order_id),
    CONSTRAINT FK_sales_order_items_products
        FOREIGN KEY (product_id) REFERENCES dbo.products(product_id)
);
GO
