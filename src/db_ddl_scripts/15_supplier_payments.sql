USE coir_business_analytics;
GO

CREATE TABLE dbo.supplier_payments (
    supplier_payment_id INT IDENTITY(1,1) PRIMARY KEY,
    purchase_order_id INT NOT NULL,
    supplier_id INT NOT NULL,
    payment_date DATE,
    payment_method VARCHAR(50),
    amount DECIMAL(14,2),
    payment_status VARCHAR(50),
    CONSTRAINT FK_supplier_payments_purchase_orders
        FOREIGN KEY (purchase_order_id) REFERENCES dbo.purchase_orders(purchase_order_id),
    CONSTRAINT FK_supplier_payments_suppliers
        FOREIGN KEY (supplier_id) REFERENCES dbo.suppliers(supplier_id)
);
GO
