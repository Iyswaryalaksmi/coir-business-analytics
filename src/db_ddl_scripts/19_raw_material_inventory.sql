USE coir_business_analytics;
GO

CREATE TABLE dbo.raw_material_inventory (
    raw_inventory_id INT IDENTITY(1,1) PRIMARY KEY,
    raw_material_id INT NOT NULL,
    date_id INT NOT NULL,
    opening_quantity DECIMAL(12,3),
    purchased_quantity DECIMAL(12,3),
    consumed_quantity DECIMAL(12,3),
    closing_quantity DECIMAL(12,3),
    CONSTRAINT FK_raw_material_inventory_raw_materials
        FOREIGN KEY (raw_material_id) REFERENCES dbo.raw_materials(raw_material_id),
    CONSTRAINT FK_raw_material_inventory_dim_date
        FOREIGN KEY (date_id) REFERENCES dbo.dim_date(date_id)
);
GO
