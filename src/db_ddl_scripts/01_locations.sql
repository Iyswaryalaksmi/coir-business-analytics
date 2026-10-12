USE coir_business_analytics;
GO

CREATE TABLE dbo.locations (
    location_id INT IDENTITY(1,1) PRIMARY KEY,
    city VARCHAR(100),
    district VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    region VARCHAR(100)
);
GO
