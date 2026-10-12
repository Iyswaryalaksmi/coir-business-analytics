USE coir_business_analytics;
GO

CREATE TABLE dbo.sales_orders (
    order_id INT IDENTITY(1,1) PRIMARY KEY,
    order_date DATE NOT NULL,
    customer_id INT NOT NULL,
    location_id INT,
    total_amount DECIMAL(14,2),
    order_status VARCHAR(50),
    CONSTRAINT FK_sales_orders_customers
        FOREIGN KEY (customer_id) REFERENCES dbo.customers(customer_id),
    CONSTRAINT FK_sales_orders_locations
        FOREIGN KEY (location_id) REFERENCES dbo.locations(location_id)
);
GO
