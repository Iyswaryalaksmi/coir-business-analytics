USE coir_business_analytics;
GO

CREATE TABLE dbo.payments (
    payment_id INT IDENTITY(1,1) PRIMARY KEY,
    order_id INT NOT NULL,
    payment_date DATE,
    payment_method VARCHAR(50),
    amount DECIMAL(14,2),
    payment_status VARCHAR(50),
    CONSTRAINT FK_payments_sales_orders
        FOREIGN KEY (order_id) REFERENCES dbo.sales_orders(order_id)
);
GO
