USE coir_business_analytics;
GO

CREATE TABLE dbo.production_materials (
    production_material_id INT IDENTITY(1,1) PRIMARY KEY,
    production_order_id INT NOT NULL,
    raw_material_id INT NOT NULL,
    planned_quantity DECIMAL(12,3),
    actual_quantity DECIMAL(12,3),
    CONSTRAINT FK_production_materials_production_orders
        FOREIGN KEY (production_order_id) REFERENCES dbo.production_orders(production_order_id),
    CONSTRAINT FK_production_materials_raw_materials
        FOREIGN KEY (raw_material_id) REFERENCES dbo.raw_materials(raw_material_id)
);
GO
