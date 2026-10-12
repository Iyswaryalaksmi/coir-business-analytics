USE coir_business_analytics;
GO

CREATE TABLE dbo.purchase_order_items (
    purchase_item_id INT IDENTITY(1,1) PRIMARY KEY,
    purchase_order_id INT NOT NULL,
    raw_material_id INT NOT NULL,
    quantity DECIMAL(12,3),
    unit_price DECIMAL(12,2),
    total_amount DECIMAL(14,2),
    CONSTRAINT FK_purchase_order_items_purchase_orders
        FOREIGN KEY (purchase_order_id) REFERENCES dbo.purchase_orders(purchase_order_id),
    CONSTRAINT FK_purchase_order_items_raw_materials
        FOREIGN KEY (raw_material_id) REFERENCES dbo.raw_materials(raw_material_id)
);
GO
