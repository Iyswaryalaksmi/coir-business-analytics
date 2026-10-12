USE coir_business_analytics;
GO

CREATE TABLE dbo.customer_segments (
    segment_id INT IDENTITY(1,1) PRIMARY KEY,
    segment_name VARCHAR(100),
    description VARCHAR(255)
);
GO
