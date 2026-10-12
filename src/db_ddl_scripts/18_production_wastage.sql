USE coir_business_analytics;
GO

CREATE TABLE dbo.production_wastage (
    wastage_id INT IDENTITY(1,1) PRIMARY KEY,
    production_order_id INT NOT NULL,
    raw_material_id INT NOT NULL,
    wastage_quantity DECIMAL(12,3),
    wastage_reason VARCHAR(255),
    wastage_date DATE,
    CONSTRAINT FK_production_wastage_production_orders
        FOREIGN KEY (production_order_id) REFERENCES dbo.production_orders(production_order_id),
    CONSTRAINT FK_production_wastage_raw_materials
        FOREIGN KEY (raw_material_id) REFERENCES dbo.raw_materials(raw_material_id)
);
GO
