USE coir_business_analytics;
GO

CREATE TABLE dbo.suppliers (
    supplier_id INT IDENTITY(1,1) PRIMARY KEY,
    supplier_name VARCHAR(150) NOT NULL,
    location_id INT,
    supplier_type VARCHAR(100),
    contact_information VARCHAR(255),
    CONSTRAINT FK_suppliers_locations
        FOREIGN KEY (location_id) REFERENCES dbo.locations(location_id)
);
GO
