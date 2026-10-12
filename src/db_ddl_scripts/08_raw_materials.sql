USE coir_business_analytics;
GO

CREATE TABLE dbo.raw_materials (
    raw_material_id INT IDENTITY(1,1) PRIMARY KEY,
    raw_material_name VARCHAR(150) NOT NULL,
    material_category VARCHAR(100),
    unit_of_measure VARCHAR(50),
    standard_cost DECIMAL(12,2),
    reorder_level DECIMAL(12,3)
);
GO
